from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ChatWave API"
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database - FIX: Use postgresql:// instead of postgres://
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/chatwave")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # External Services
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    CLOUDINARY_URL: Optional[str] = os.getenv("CLOUDINARY_URL")
    MAIL_USERNAME: Optional[str] = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: Optional[str] = os.getenv("MAIL_PASSWORD")
    
    # CORS
   ALLOWED_ORIGINS: List[str] = [
    "http://localhost:3000",  # for local development
    "https://chatwave-seven.vercel.app",  # your Vercel domain
    "https://chatwave-seven-git-main-saffan-s-projects.vercel.app",  # if you have this
    # Add your specific Vercel URL
]
    
    # Debug
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Media settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "image/gif", "audio/mpeg", "audio/wav"]
    
    # Rate limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 3600  # 1 hour

    class Config:
        env_file = ".env"

settings = Settings()
