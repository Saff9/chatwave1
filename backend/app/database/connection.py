from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging
import time
import os

logger = logging.getLogger(__name__)

def create_db_engine():
    """Create database engine with retry logic and proper URL handling"""
    max_retries = 5
    retry_delay = 2
    
    # Ensure we're using the correct PostgreSQL URL format
    database_url = settings.DATABASE_URL
    
    # Replace postgres:// with postgresql:// if needed
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        logger.info("Updated database URL to use postgresql:// format")
    
    logger.info(f"Attempting to connect to database: {database_url[:50]}...")  # Log first 50 chars
    
    for attempt in range(max_retries):
        try:
            # Create engine with proper connection settings for Render
            engine = create_engine(
                database_url,
                pool_pre_ping=True,
                pool_recycle=300,
                echo=settings.DEBUG,
                # Add connection timeout and retry settings
                connect_args={
                    "connect_timeout": 30,
                    "options": "-c statement_timeout=30000",
                    "sslmode": "require"  # Add SSL requirement for Render
                }
            )
            
            # Test connection
            with engine.connect() as connection:
                logger.info("Database connection successful!")
                return engine
        except Exception as e:
            logger.error(f"Database connection failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                logger.error("Max retries reached. Could not connect to database.")
                raise e
    
    # If all attempts fail, raise an exception
    raise Exception("Could not connect to database after multiple attempts")

# Create engine with retry logic
engine = create_db_engine()

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """Test database connection"""
    try:
        with engine.connect() as connection:
            logger.info("Database connection test successful!")
            return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
