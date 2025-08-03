from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models import AgentType, MessageRole


class ChatMessage(BaseModel):
    content: str
    role: MessageRole
    agent_type: Optional[AgentType] = None
    created_at: Optional[datetime] = None


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    message: str
    agent_type: AgentType
    conversation_id: int
    message_id: int


class ConversationCreate(BaseModel):
    title: Optional[str] = None


class ConversationResponse(BaseModel):
    id: int
    title: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] = None  # Make this optional
    message_count: int

    class Config:
        from_attributes = True


class ConversationDetail(BaseModel):
    id: int
    title: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] = None  # Make this optional
    messages: List[ChatMessage]

    class Config:
        from_attributes = True