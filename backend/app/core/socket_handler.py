import socketio
import asyncio
from typing import Dict, List
from app.core.config import settings
from app.core.security import verify_token
from app.database.connection import get_db
from app.crud import users, rooms
import logging

logger = logging.getLogger(__name__)

# Initialize Socket.IO server
sio = socketio.AsyncServer(
    cors_allowed_origins=settings.ALLOWED_ORIGINS,
    async_mode='asgi',
    logger=True,
    engineio_logger=True
)

# Store connected users and their rooms
connected_users: Dict[str, Dict] = {}
user_rooms: Dict[str, List[str]] = {}

@sio.event
async def connect(sid, environ, auth):
    """Handle user connection"""
    try:
        # Extract token from query parameters or headers
        token = None
        if 'HTTP_AUTHORIZATION' in environ:
            token = environ['HTTP_AUTHORIZATION'].replace('Bearer ', '')
        elif 'token' in environ.get('QUERY_STRING', ''):
            # Extract from query string if needed
            pass
        
        if not token:
            await sio.disconnect(sid)
            return
        
        # Verify token
        token_data = verify_token(token)
        if not token_data:
            await sio.disconnect(sid)
            return
        
        # Store user connection
        connected_users[sid] = {
            'user_id': str(token_data.user_id),
            'username': token_data.username,
            'sid': sid
        }
        
        # Add to user_rooms tracking
        if sid not in user_rooms:
            user_rooms[sid] = []
        
        logger.info(f"User {token_data.username} connected with SID: {sid}")
        
        # Notify other users about online status
        await sio.emit('user_connected', {
            'user_id': str(token_data.user_id),
            'username': token_data.username
        })
        
    except Exception as e:
        logger.error(f"Connection error: {e}")
        await sio.disconnect(sid)

@sio.event
async def disconnect(sid):
    """Handle user disconnection"""
    if sid in connected_users:
        user_data = connected_users[sid]
        username = user_data['username']
        user_id = user_data['user_id']
        
        # Remove from all rooms
        for room in user_rooms.get(sid, []):
            await sio.leave_room(sid, room)
        
        # Clean up tracking
        if sid in user_rooms:
            del user_rooms[sid]
        if sid in connected_users:
            del connected_users[sid]
        
        logger.info(f"User {username} disconnected with SID: {sid}")
        
        # Notify other users about offline status
        await sio.emit('user_disconnected', {
            'user_id': user_id,
            'username': username
        })

@sio.event
async def join_room(sid, data):
    """Handle joining a room"""
    try:
        room_id = data.get('room_id')
        if not room_id:
            return
        
        # Add user to room
        await sio.enter_room(sid, room_id)
        
        if sid not in user_rooms:
            user_rooms[sid] = []
        if room_id not in user_rooms[sid]:
            user_rooms[sid].append(room_id)
        
        logger.info(f"User {sid} joined room {room_id}")
        
        # Notify room about new user
        await sio.emit('user_joined', {
            'room_id': room_id,
            'user_id': connected_users[sid]['user_id'],
            'username': connected_users[sid]['username']
        }, room=room_id)
        
    except Exception as e:
        logger.error(f"Error joining room: {e}")

@sio.event
async def leave_room(sid, data):
    """Handle leaving a room"""
    try:
        room_id = data.get('room_id')
        if not room_id:
            return
        
        # Remove user from room
        await sio.leave_room(sid, room_id)
        
        if sid in user_rooms and room_id in user_rooms[sid]:
            user_rooms[sid].remove(room_id)
        
        logger.info(f"User {sid} left room {room_id}")
        
        # Notify room about user leaving
        await sio.emit('user_left', {
            'room_id': room_id,
            'user_id': connected_users[sid]['user_id'],
            'username': connected_users[sid]['username']
        }, room=room_id)
        
    except Exception as e:
        logger.error(f"Error leaving room: {e}")

@sio.event
async def send_message(sid, data):
    """Handle sending a message"""
    try:
        room_id = data.get('room_id')
        message_data = {
            'sender_id': connected_users[sid]['user_id'],
            'sender_username': connected_users[sid]['username'],
            'content': data.get('content'),
            'message_type': data.get('message_type', 'text'),
            'timestamp': data.get('timestamp', str(datetime.utcnow())),
            'message_id': data.get('message_id')
        }
        
        logger.info(f"Sending message to room {room_id}: {message_data}")
        
        # Broadcast message to room
        await sio.emit('receive_message', message_data, room=room_id)
        
    except Exception as e:
        logger.error(f"Error sending message: {e}")

@sio.event
async def typing_start(sid, data):
    """Handle typing start event"""
    try:
        room_id = data.get('room_id')
        username = connected_users[sid]['username']
        
        await sio.emit('typing_start', {
            'username': username
        }, room=room_id)
        
    except Exception as e:
        logger.error(f"Error in typing_start: {e}")

@sio.event
async def typing_stop(sid, data):
    """Handle typing stop event"""
    try:
        room_id = data.get('room_id')
        username = connected_users[sid]['username']
        
        await sio.emit('typing_stop', {
            'username': username
        }, room=room_id)
        
    except Exception as e:
        logger.error(f"Error in typing_stop: {e}")

# Create ASGI app
socket_app = socketio.ASGIApp(sio, socketio_path='/socket.io')
