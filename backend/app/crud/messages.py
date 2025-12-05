from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from datetime import datetime
from app.models.models import Message, MessageReaction, User
from app.schemas.message import MessageCreate, MessageUpdate
from uuid import UUID
import uuid

def get_message(db: Session, message_id: str) -> Optional[Message]:
    """Get message by ID"""
    return db.query(Message).filter(Message.id == UUID(message_id)).first()

def get_room_messages(db: Session, room_id: str, skip: int = 0, limit: int = 50) -> List[Message]:
    """Get messages for a room"""
    return db.query(Message).filter(
        Message.room_id == UUID(room_id)
    ).order_by(
        Message.created_at.desc()
    ).offset(skip).limit(limit).all()

def create_message(db: Session, message_data: MessageCreate, sender_id: str) -> Message:
    """Create a new message"""
    db_message = Message(
        sender_id=UUID(sender_id),
        room_id=UUID(message_data.room_id),
        content=message_data.content,
        message_type=message_data.message_type,
        reply_to=message_data.reply_to
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def update_message(db: Session, message_id: str, message_update: MessageUpdate) -> Message:
    """Update message"""
    db_message = db.query(Message).filter(Message.id == UUID(message_id)).first()
    if not db_message:
        return None
    
    db_message.content = message_update.content
    db_message.is_edited = True
    db.commit()
    db.refresh(db_message)
    return db_message

def delete_message(db: Session, message_id: str) -> bool:
    """Delete message"""
    db_message = db.query(Message).filter(Message.id == UUID(message_id)).first()
    if db_message:
        db_message.is_deleted = True  # Soft delete
        db.commit()
        return True
    return False

def add_message_reaction(db: Session, message_id: str, user_id: str, reaction: str) -> bool:
    """Add reaction to message"""
    # Check if reaction already exists
    existing_reaction = db.query(MessageReaction).filter(
        and_(
            MessageReaction.message_id == UUID(message_id),
            MessageReaction.user_id == UUID(user_id),
            MessageReaction.reaction == reaction
        )
    ).first()
    
    if existing_reaction:
        return True  # Already exists
    
    reaction_obj = MessageReaction(
        message_id=UUID(message_id),
        user_id=UUID(user_id),
        reaction=reaction
    )
    db.add(reaction_obj)
    db.commit()
    return True

def remove_message_reaction(db: Session, message_id: str, user_id: str, reaction: str) -> bool:
    """Remove reaction from message"""
    reaction_obj = db.query(MessageReaction).filter(
        and_(
            MessageReaction.message_id == UUID(message_id),
            MessageReaction.user_id == UUID(user_id),
            MessageReaction.reaction == reaction
        )
    ).first()
    
    if reaction_obj:
        db.delete(reaction_obj)
        db.commit()
        return True
    return False

def get_message_reactions(db: Session, message_id: str) -> List[MessageReaction]:
    """Get all reactions for a message"""
    return db.query(MessageReaction).filter(
        MessageReaction.message_id == UUID(message_id)
    ).all()
