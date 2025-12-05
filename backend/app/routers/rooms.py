from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.room import RoomCreate, RoomUpdate, RoomResponse, RoomMemberAdd
from app.core.security import verify_token
from app.crud import rooms, users
from app.core.config import settings

router = APIRouter(prefix="/rooms", tags=["rooms"])

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

@router.get("/", response_model=List[RoomResponse])
async def get_user_rooms(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all rooms for current user"""
    return rooms.get_user_rooms(db, current_user.id)

@router.post("/", response_model=RoomResponse)
async def create_room(
    room: RoomCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new room"""
    return rooms.create_room(db, room, current_user.id)

@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(room_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get room by ID"""
    room = rooms.get_room(db, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Check if user is a member of the room
    if not rooms.is_user_room_member(db, room_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this room"
        )
    
    return room

@router.put("/{room_id}", response_model=RoomResponse)
async def update_room(
    room_id: str,
    room_update: RoomUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update room"""
    room = rooms.get_room(db, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Check if user is admin of the room
    if room.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only room admin can update room"
        )
    
    return rooms.update_room(db, room_id, room_update)

@router.delete("/{room_id}")
async def delete_room(room_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete room"""
    room = rooms.get_room(db, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Check if user is admin of the room
    if room.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only room admin can delete room"
        )
    
    rooms.delete_room(db, room_id)
    return {"status": "success", "message": "Room deleted successfully"}

@router.post("/{room_id}/members")
async def add_member_to_room(
    room_id: str,
    member_data: RoomMemberAdd,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add member to room"""
    room = rooms.get_room(db, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Check if user is admin of the room
    if room.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only room admin can add members"
        )
    
    rooms.add_member_to_room(db, room_id, member_data.user_id, member_data.role)
    return {"status": "success", "message": "Member added successfully"}

@router.delete("/{room_id}/members/{user_id}")
async def remove_member_from_room(
    room_id: str,
    user_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove member from room"""
    room = rooms.get_room(db, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Check if user is admin of the room or removing themselves
    if room.created_by != current_user.id and str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only room admin or user themselves can remove member"
        )
    
    rooms.remove_member_from_room(db, room_id, user_id)
    return {"status": "success", "message": "Member removed successfully"}
