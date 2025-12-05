from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, UUID, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.sql import func
import uuid
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_online = Column(Boolean, default=False)
    last_seen = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Room(Base):
    __tablename__ = "rooms"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)  # 'private', 'group'
    max_members = Column(Integer, default=25)
    avatar_url = Column(String(500), nullable=True)
    created_by = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class RoomMember(Base):
    __tablename__ = "room_members"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_id = Column(PostgresUUID(as_uuid=True), ForeignKey("rooms.id"), nullable=False)
    user_id = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    role = Column(String(20), default="member")  # 'admin', 'moderator', 'member'
    joined_at = Column(DateTime, server_default=func.now())
    left_at = Column(DateTime, nullable=True)

class Message(Base):
    __tablename__ = "messages"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    room_id = Column(PostgresUUID(as_uuid=True), ForeignKey("rooms.id"), nullable=False)
    content = Column(Text, nullable=True)
    media_url = Column(String(500), nullable=True)
    message_type = Column(String(20), default="text")  # 'text', 'image', 'voice', 'file'
    reply_to = Column(PostgresUUID(as_uuid=True), ForeignKey("messages.id"), nullable=True)
    is_edited = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=True)  # For 24-hour media
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class MessageReaction(Base):
    __tablename__ = "message_reactions"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(PostgresUUID(as_uuid=True), ForeignKey("messages.id"), nullable=False)
    user_id = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    reaction = Column(String(10), nullable=False)  # emoji
    created_at = Column(DateTime, server_default=func.now())

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    session_token = Column(String(255), unique=True, nullable=False)
    refresh_token = Column(String(255), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    is_active = Column(Boolean, default=True)

class AIRequestLog(Base):
    __tablename__ = "ai_request_logs"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    request_type = Column(String(50), nullable=False)  # 'translation', 'summary', 'quick_reply'
    request_data = Column(Text, nullable=False)
    response_data = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
