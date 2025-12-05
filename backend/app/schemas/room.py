from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from .user import UserResponse

class RoomBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., pattern=r"^(private|group)$")  # 'private', 'group'
    max_members: Optional[int] = Field(25, ge=2, le=500)

class RoomCreate(RoomBase):
    pass

class RoomUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    max_members: Optional[int] = Field(None, ge=2, le=500)

class RoomMemberResponse(BaseModel):
    id: UUID
    user_id: UUID
    username: str
    avatar_url: Optional[str]
    role: str
    joined_at: datetime

    class Config:
        from_attributes = True

class RoomResponse(BaseModel):
    id: UUID
    name: str
    type: str
    max_members: int
    avatar_url: Optional[str] = None
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    members: List[RoomMemberResponse] = []
    last_message: Optional[str] = None
    last_message_time: Optional[datetime] = None

    class Config:
        from_attributes = True

class RoomMemberAdd(BaseModel):
    user_id: UUID
    role: Optional[str] = "member"  # 'admin', 'moderator', 'member'
