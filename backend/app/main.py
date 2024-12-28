from fastapi import FastAPI, Depends, HTTPException, Header, Request, status
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import markdown
import uuid
from datetime import timedelta
from typing import Optional, List
from . import models, schemas, database, auth
from sqlalchemy.future import select
from sqlalchemy import and_, desc

app = FastAPI()

# Configure CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://markdown-note-app-9wvo9hb0.devinapps.com",
        "*.notebook.cv",
        "https://*.notebook.cv",
        "http://*.notebook.cv"
    ],  # Frontend development, production, and subdomain servers
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.on_event("startup")
async def startup_event():
    await database.init_db()

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/api/register", response_model=schemas.User)
async def register_user(
    user: schemas.UserCreate,
    db: AsyncSession = Depends(database.get_db)
):
    # Validate username format
    if not auth.validate_username(user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username format. Username must contain only lowercase letters, numbers, and hyphens, and must start and end with an alphanumeric character."
        )
    
    # Check if username already exists
    query = select(models.User).where(models.User.username == user.username)
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create new user
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@app.post("/api/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(database.get_db)
):
    user = await auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/me", response_model=schemas.User)
async def read_users_me(
    current_user: models.User = Depends(auth.get_current_user)
):
    return current_user

@app.get("/api/blog/{username}/notes", response_model=List[schemas.Note])
async def get_user_public_notes(
    username: str,
    request: Request,
    x_username: Annotated[str | None, Header(alias="X-Username")] = None,
    db: AsyncSession = Depends(database.get_db)
):
    # Verify username matches subdomain if accessed via subdomain
    if x_username and x_username != username:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    # Get user
    user_query = select(models.User).where(models.User.username == username)
    result = await db.execute(user_query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    # Get public notes for the user
    query = select(models.Note).where(
        and_(
            models.Note.user_id == user.id,
            models.Note.is_public == True
        )
    ).order_by(desc(models.Note.created_at))
    
    result = await db.execute(query)
    notes = result.scalars().all()
    
    return notes

@app.post("/api/notes", response_model=schemas.Note)
async def create_note(
    note: schemas.NoteCreate,
    request: Request,
    current_user: Optional[models.User] = Depends(auth.get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    share_id = str(uuid.uuid4())
    
    # Create note with user_id if authenticated
    note_data = note.model_dump()
    if current_user:
        note_data["user_id"] = current_user.id
    
    db_note = models.Note(**note_data, share_id=share_id)
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    
    # Generate share URL with subdomain if user is authenticated
    if current_user:
        db_note.share_url = f"https://{current_user.username}.{auth.BASE_DOMAIN}/s/{share_id}"
    
    return db_note

@app.get("/api/notes/{share_id}", response_model=schemas.Note)
async def get_note(
    share_id: str,
    request: Request,
    x_username: Annotated[str | None, Header(alias="X-Username")] = None,
    db: AsyncSession = Depends(database.get_db)
):
    query = select(models.Note).where(models.Note.share_id == share_id)
    result = await db.execute(query)
    note = result.scalar_one_or_none()
    
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # If accessed via subdomain, verify the note belongs to that user
    if x_username:
        user_query = select(models.User).where(models.User.username == x_username)
        result = await db.execute(user_query)
        user = result.scalar_one_or_none()
        
        if not user or (note.user_id != user.id and not note.is_public):
            raise HTTPException(status_code=404, detail="Note not found")
    
    return note

@app.get("/api/notes/{share_id}/html")
async def get_note_html(
    share_id: str,
    request: Request,
    x_username: Annotated[str | None, Header(alias="X-Username")] = None,
    db: AsyncSession = Depends(database.get_db)
):
    query = select(models.Note).where(models.Note.share_id == share_id)
    result = await db.execute(query)
    note = result.scalar_one_or_none()
    
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # If accessed via subdomain, verify the note belongs to that user
    if x_username:
        user_query = select(models.User).where(models.User.username == x_username)
        result = await db.execute(user_query)
        user = result.scalar_one_or_none()
        
        if not user or (note.user_id != user.id and not note.is_public):
            raise HTTPException(status_code=404, detail="Note not found")
    
    html_content = markdown.markdown(
        note.content,
        extensions=['fenced_code', 'tables']
    )
    return {"html": html_content}
