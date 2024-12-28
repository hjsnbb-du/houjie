from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas
from .database import get_db
import os
from dotenv import load_dotenv

load_dotenv()

# Configure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configure JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your-secure-secret-key-here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
BASE_DOMAIN = os.getenv("BASE_DOMAIN", "notebook.cv")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_user(username: str, password: str, db: AsyncSession) -> Optional[models.User]:
    query = select(models.User).where(models.User.username == username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    query = select(models.User).where(models.User.username == token_data.username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    return user

def validate_username(username: str) -> bool:
    """Validate username format for subdomain compatibility."""
    import re
    # Only allow lowercase letters, numbers, and hyphens
    # Must start and end with alphanumeric
    # This ensures usernames are valid subdomains
    return bool(re.match(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$", username))

def get_subdomain_from_host(host: str) -> Optional[str]:
    """Extract username from subdomain."""
    if not host or "." not in host:
        return None
    subdomain = host.split(".")[0]
    if validate_username(subdomain):
        return subdomain
    return None
