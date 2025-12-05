from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class MessageBase(BaseModel):
    room_id: UUID
    content: Optional[str] = Field(None, max_length=5000)
    message_type: str = Field(default="text", pattern=r"^(text|image|voice|file)$")
    reply_to: Optional[UUID] = None

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    content: str = Field(..., max_length=5000)

class MessageReactionCreate(BaseModel):
    message_id: UUID
    reaction: str = Field(..., max_length=10)  # emoji

class MessageReactionResponse(BaseModel):
    id: UUID
    message_id: UUID
    user_id: UUID
    reaction: str
    created_at: datetime

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    id: UUID
    sender_id: UUID
    sender_username: str
    sender_avatar: Optional[str] = None
    room_id: UUID
    content: Optional[str]
    media_url: Optional[str] = None
    message_type: str
    reply_to: Optional[UUID] = None
    is_edited: bool
    is_deleted: bool
    expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    reactions: List[MessageReactionResponse] = []

    class Config:
        from_attributes = True

class MessageWithReplies(MessageResponse):
    replies: List['MessageResponse'] = []

class PaginatedMessages(BaseModel):
    messages: List[MessageResponse]
    total: int
    page: int
    page_size: int
    has_more: bool
