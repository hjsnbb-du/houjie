"""Chat models for the OpenAI Chat Application."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

@dataclass
class Message:
    """Represents a single message in a conversation."""
    content: str
    role: str  # 'user' or 'assistant'
    timestamp: datetime = field(default_factory=datetime.now)
    id: UUID = field(default_factory=uuid4)

@dataclass
class Conversation:
    """Represents a chat conversation."""
    title: str
    messages: List[Message] = field(default_factory=list)
    model: str = "gpt-3.5-turbo"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    id: UUID = field(default_factory=uuid4)

    def add_message(self, content: str, role: str) -> Message:
        """Add a new message to the conversation."""
        message = Message(content=content, role=role)
        self.messages.append(message)
        self.updated_at = datetime.now()
        return message

    @property
    def last_message(self) -> Optional[Message]:
        """Get the last message in the conversation."""
        return self.messages[-1] if self.messages else None

    @property
    def preview(self) -> str:
        """Get a preview of the last message."""
        if not self.last_message:
            return "No messages yet"
        return (self.last_message.content[:50] + "..."
                if len(self.last_message.content) > 50
                else self.last_message.content)
