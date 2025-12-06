from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging
import os

logger = logging.getLogger(__name__)

def create_db_engine():
    """Create database engine with proper Supabase configuration"""
    # Get the database URL from environment
    database_url = settings.DATABASE_URL
    
    # Ensure we're using the correct PostgreSQL URL format for SQLAlchemy
    # The psycopg2 driver is required for PostgreSQL connections
    if database_url.startswith("postgres://"):
        # Replace with psycopg2 driver which is required for PostgreSQL
        database_url = database_url.replace("postgres://", "postgresql+psycopg2://", 1)
        logger.info("Updated database URL to use postgresql+psycopg2:// format")
    elif database_url.startswith("postgresql://"):
        # Replace with psycopg2 driver which is required for PostgreSQL
        database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        logger.info("Updated database URL to use postgresql+psycopg2:// format")
    
    logger.info(f"Connecting to database: {database_url[:50]}...")
    
    try:
        # Create engine with proper settings for Supabase
        engine = create_engine(
            database_url,
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=300,    # Recycle connections every 5 minutes
            pool_size=5,         # Smaller pool size for free tier
            max_overflow=10,     # Allow some overflow
            echo=settings.DEBUG, # Log SQL statements in debug mode
            # Proper connection arguments for Supabase
            connect_args={
                "connect_timeout": 30,  # 30 second connection timeout
                "options": "-c statement_timeout=30000",  # 30 second statement timeout
                "sslmode": "require"    # Require SSL for Supabase
            }
        )
        
        # Test the connection by attempting to connect
        with engine.connect() as connection:
            logger.info("Database connection successful!")
            return engine
            
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        # Don't raise the exception immediately - let the app start and handle gracefully
        return None

# Create engine - this might be None if connection fails
engine = create_db_engine()

if engine:
    # Create session if engine is available
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
else:
    # This is critical - we need to handle the case where engine fails
    logger.error("Failed to create database engine!")
    raise Exception("Database engine creation failed - check your connection string")

def get_db():
    """Dependency for getting database session"""
    if not engine:
        logger.error("No database engine available!")
        yield None
        return
        
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """Test database connection"""
    if not engine:
        logger.error("No database engine available")
        return False
    
    try:
        with engine.connect() as connection:
            # Execute a simple query to test the connection
            result = connection.execute("SELECT 1")
            row = result.fetchone()
            if row:
                logger.info("Database connection test successful!")
                return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
