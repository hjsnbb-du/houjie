from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50, pattern=r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    password: constr(min_length=8)

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class NoteBase(BaseModel):
    content: str
    title: Optional[str] = None
    is_public: bool = True

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    share_id: str
    created_at: datetime
    user_id: Optional[int] = None
    share_url: Optional[str] = None

    class Config:
        from_attributes = True
