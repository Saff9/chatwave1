from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional, List
from datetime import datetime
from app.models.models import Room, RoomMember, User, Message
from app.schemas.room import RoomCreate, RoomUpdate
from uuid import UUID
import uuid

def get_user_rooms(db: Session, user_id: str) -> List[Room]:
    """Get all rooms for a user"""
    return db.query(Room).join(
        RoomMember, Room.id == RoomMember.room_id
    ).filter(
        RoomMember.user_id == UUID(user_id)
    ).all()

def get_room(db: Session, room_id: str) -> Optional[Room]:
    """Get room by ID"""
    return db.query(Room).filter(Room.id == UUID(room_id)).first()

def create_room(db: Session, room_data: RoomCreate, creator_id: str) -> Room:
    """Create a new room"""
    db_room = Room(
        name=room_data.name,
        type=room_data.type,
        max_members=room_data.max_members,
        created_by=UUID(creator_id)
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    
    # Add creator as member
    add_member_to_room(db, str(db_room.id), creator_id, "admin")
    return db_room

def update_room(db: Session, room_id: str, room_update: RoomUpdate) -> Room:
    """Update room"""
    db_room = db.query(Room).filter(Room.id == UUID(room_id)).first()
    if not db_room:
        return None
    
    update_data = room_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_room, field, value)
    
    db.commit()
    db.refresh(db_room)
    return db_room

def delete_room(db: Session, room_id: str) -> bool:
    """Delete room"""
    db_room = db.query(Room).filter(Room.id == UUID(room_id)).first()
    if db_room:
        db.delete(db_room)
        db.commit()
        return True
    return False

def is_user_room_member(db: Session, room_id: str, user_id: str) -> bool:
    """Check if user is a member of the room"""
    member = db.query(RoomMember).filter(
        and_(
            RoomMember.room_id == UUID(room_id),
            RoomMember.user_id == UUID(user_id)
        )
    ).first()
    return member is not None

def add_member_to_room(db: Session, room_id: str, user_id: str, role: str = "member") -> bool:
    """Add member to room"""
    # Check if already a member
    existing_member = db.query(RoomMember).filter(
        and_(
            RoomMember.room_id == UUID(room_id),
            RoomMember.user_id == UUID(user_id)
        )
    ).first()
    
    if existing_member:
        # Update role if already a member
        existing_member.role = role
        db.commit()
        return True
    
    # Add new member
    member = RoomMember(
        room_id=UUID(room_id),
        user_id=UUID(user_id),
        role=role
    )
    db.add(member)
    db.commit()
    return True

def remove_member_from_room(db: Session, room_id: str, user_id: str) -> bool:
    """Remove member from room"""
    member = db.query(RoomMember).filter(
        and_(
            RoomMember.room_id == UUID(room_id),
            RoomMember.user_id == UUID(user_id)
        )
    ).first()
    
    if member:
        db.delete(member)
        db.commit()
        return True
    return False

def get_room_members(db: Session, room_id: str) -> List[User]:
    """Get all members of a room"""
    return db.query(User).join(
        RoomMember, User.id == RoomMember.user_id
    ).filter(
        RoomMember.room_id == UUID(room_id)
    ).all()

def get_room_last_message(db: Session, room_id: str) -> Optional[Message]:
    """Get the last message in a room"""
    return db.query(Message).filter(
        Message.room_id == UUID(room_id)
    ).order_by(Message.created_at.desc()).first()
