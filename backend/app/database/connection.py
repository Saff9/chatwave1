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
    
    # Ensure we're using the correct PostgreSQL URL format
    if database_url.startswith("postgresql://"):
        # Convert to postgres:// format which SQLAlchemy expects
        database_url = database_url.replace("postgresql://", "postgres://", 1)
        logger.info("Updated database URL to use postgres:// format")
    
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
    # Fallback - create a dummy engine and session maker if connection fails
    from sqlalchemy import create_engine
    engine = create_engine("sqlite:///:memory:")  # In-memory SQLite as fallback
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
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
