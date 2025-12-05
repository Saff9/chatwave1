from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.database.connection import engine, SessionLocal
from app.models import models
from app.routers import auth, users, rooms, messages
from app.core import socket_handler
from app.core.config import settings
import uvicorn
import logging

# Create all tables (moved to startup event)
def create_tables():
    try:
        models.Base.metadata.create_all(bind=engine)
        logging.info("Database tables created successfully!")
    except Exception as e:
        logging.error(f"Error creating database tables: {e}")
        raise

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
    """Create database tables on startup"""
    create_tables()

@app.get("/")
async def root():
    return {"message": "ChatWave API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "chatwave-api"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
