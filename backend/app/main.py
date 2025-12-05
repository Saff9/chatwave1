from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.database.connection import engine, SessionLocal, test_connection
from app.models import models
from app.routers import auth, users, rooms, messages
from app.core import socket_handler
from app.core.config import settings
import uvicorn
import logging

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

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose authorization header for client-side access
    expose_headers=["Access-Control-Allow-Origin"]
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])

# Mount socket.io handler
app.mount("/socket.io", socket_handler.socket_app)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup with error handling"""
    try:
        # Test database connection first
        if test_connection():
            # Create all tables
            models.Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully!")
        else:
            logger.error("Failed to connect to database during startup")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        # Don't crash the app if database isn't ready - it might be a temporary issue
        # The app can still start and handle requests
        logger.info("Continuing startup despite database connection issues...")

@app.get("/")
async def root():
    return {"message": "ChatWave API is running!"}

@app.get("/health")
async def health_check():
    try:
        # Test database connection
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return {"status": "healthy", "service": "chatwave-api", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "service": "chatwave-api", "database": "disconnected", "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
