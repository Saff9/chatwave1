from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text  # Add this import
from app.database.connection import engine, SessionLocal, test_connection, Base
from app.models import models
from app.routers import auth, users, rooms, messages
from app.core import socket_handler
from app.core.config import settings
import uvicorn
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ChatWave API",
    description="A modern messaging platform API",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

# CORS middleware - Updated configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
    # Expose authorization header for client-side access
    expose_headers=["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials", "Authorization"]
)

# Include routers - Make sure auth router is included
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])

# Mount socket.io handler
app.mount("/socket.io", socket_handler.socket_app)

# Dependency
def get_db():
    if SessionLocal:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        yield None

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup with error handling"""
    if engine:
        try:
            # Test database connection first
            if test_connection():
                # Create all tables
                Base.metadata.create_all(bind=engine)
                logger.info("Database tables created successfully!")
            else:
                logger.error("Failed to connect to database during startup")
        except Exception as e:
            logger.error(f"Error during startup: {e}")
            logger.info("Continuing startup despite database connection issues...")
    else:
        logger.warning("No database engine available - running in limited mode")

@app.get("/")
async def root():
    return {"message": "ChatWave API is running!"}

@app.get("/health")
async def health_check():
    if engine:
        try:
            # Test database connection with proper SQLAlchemy text() wrapper
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                row = result.fetchone()
                if row:
                    return {"status": "healthy", "service": "chatwave-api", "database": "connected"}
                else:
                    return {"status": "unhealthy", "service": "chatwave-api", "database": "connection_failed"}
        except Exception as e:
            return {"status": "unhealthy", "service": "chatwave-api", "database": "disconnected", "error": str(e)}
    else:
        return {"status": "limited", "service": "chatwave-api", "database": "not configured"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
