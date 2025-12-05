from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from datetime import datetime
from app.models.models import User
from app.schemas.user import UserCreate, UserUpdate
from uuid import UUID
import uuid

def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == UUID(user_id)).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get list of users"""
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, username: str, email: str, hashed_password: str) -> User:
    """Create a new user"""
    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_profile(db: Session, user_id: str, user_update: UserUpdate) -> User:
    """Update user profile"""
    db_user = db.query(User).filter(User.id == UUID(user_id)).first()
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_last_seen(db: Session, user_id: str) -> User:
    """Update user's last seen timestamp"""
    db_user = db.query(User).filter(User.id == UUID(user_id)).first()
    if db_user:
        db_user.last_seen = datetime.utcnow()
        db.commit()
        db.refresh(db_user)
    return db_user

def update_user_online_status(db: Session, user_id: str, is_online: bool) -> User:
    """Update user's online status"""
    db_user = db.query(User).filter(User.id == UUID(user_id)).first()
    if db_user:
        db_user.is_online = is_online
        db.commit()
        db.refresh(db_user)
    return db_user
