from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class User(BaseModel):
    username: str
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    password: str

class Message(BaseModel):
    sender: str
    content: str
    timestamp: datetime = datetime.now()
    room: Optional[str] = "general"

class ChatRoom(BaseModel):
    name: str
    participants: List[str] = []
    messages: List[Message] = []

# In-memory storage
users: Dict[str, User] = {}
chat_rooms: Dict[str, ChatRoom] = {"general": ChatRoom(name="general")}
active_connections: Dict[str, Dict[str, any]] = {}
