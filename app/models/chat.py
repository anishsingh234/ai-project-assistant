from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None  # if None, new conversation starts

class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    created_at: datetime

class ChatResponse(BaseModel):
    conversation_id: str
    reply: str