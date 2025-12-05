from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.message import MessageCreate, MessageUpdate, MessageResponse, MessageReactionCreate
from app.core.security import verify_token
from app.crud import messages, users, rooms
from app.core.config import settings

router = APIRouter(prefix="/messages", tags=["messages"])

def get_current_user(token: str = Depends(verify_token), db: Session = Depends(get_db)):
    """Get current user from token"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = users.get_user_by_id(db, token.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.get("/{room_id}", response_model=List[MessageResponse])
async def get_room_messages(
    room_id: str,
    skip: int = 0,
    limit: int = 50,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get messages for a room"""
    # Check if user is a member of the room
    if not rooms.is_user_room_member(db, room_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this room"
        )
    
    return messages.get_room_messages(db, room_id, skip=skip, limit=limit)

@router.post("/", response_model=MessageResponse)
async def create_message(
    message: MessageCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new message"""
    # Check if user is a member of the room
    if not rooms.is_user_room_member(db, message.room_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this room"
        )
    
    return messages.create_message(db, message, current_user.id)

@router.put("/{message_id}", response_model=MessageResponse)
async def update_message(
    message_id: str,
    message_update: MessageUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a message"""
    message = messages.get_message(db, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Check if user is the sender of the message
    if str(message.sender_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only edit your own messages"
        )
    
    return messages.update_message(db, message_id, message_update)

@router.delete("/{message_id}")
async def delete_message(
    message_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a message"""
    message = messages.get_message(db, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Check if user is the sender of the message or room admin
    if str(message.sender_id) != str(current_user.id):
        room = rooms.get_room(db, message.room_id)
        if room.created_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Can only delete your own messages or as room admin"
            )
    
    messages.delete_message(db, message_id)
    return {"status": "success", "message": "Message deleted successfully"}

@router.post("/{message_id}/reactions")
async def add_reaction(
    message_id: str,
    reaction_data: MessageReactionCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add reaction to a message"""
    # Check if message exists and user has access
    message = messages.get_message(db, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Check if user is a member of the room
    if not rooms.is_user_room_member(db, message.room_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this room"
        )
    
    messages.add_message_reaction(db, message_id, current_user.id, reaction_data.reaction)
    return {"status": "success", "message": "Reaction added successfully"}

@router.delete("/{message_id}/reactions/{reaction}")
async def remove_reaction(
    message_id: str,
    reaction: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove reaction from a message"""
    messages.remove_message_reaction(db, message_id, current_user.id, reaction)
    return {"status": "success", "message": "Reaction removed successfully"}
