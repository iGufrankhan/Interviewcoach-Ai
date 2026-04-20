import os
import time
import logging
from dotenv import load_dotenv
from mongoengine import connect, ConnectionError as MongoConnectionError
from pymongo.errors import ServerSelectionTimeoutError

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB connection URI from environment variables
uri = os.getenv("DATABASE_URL")
db_name = os.getenv("DATABASE_NAME", "interviewcoach")

# Connection state tracking
_db_connection_status = {
    "connected": False,
    "error": None,
    "last_attempt": None,
    "retry_count": 0
}


def _connect_with_retry(max_retries: int = 3, base_delay: float = 1.0) -> bool:
    """
    Attempt to connect to MongoDB with exponential backoff retry logic.
    
    Args:
        max_retries: Maximum number of connection attempts
        base_delay: Initial delay between retries in seconds
        
    Returns:
        bool: True if connection successful, False otherwise
    """
    if not uri:
        logger.error("DATABASE_URL environment variable not set")
        _db_connection_status["error"] = "DATABASE_URL not configured"
        return False
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting MongoDB connection (attempt {attempt + 1}/{max_retries})...")
            connect(
                db=db_name,
                host=uri,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                retryWrites=True
            )
            logger.info("✓ Successfully connected to MongoDB via MongoEngine!")
            _db_connection_status["connected"] = True
            _db_connection_status["error"] = None
            _db_connection_status["retry_count"] = attempt
            return True
            
        except (MongoConnectionError, ServerSelectionTimeoutError) as e:
            _db_connection_status["error"] = str(e)
            _db_connection_status["last_attempt"] = time.time()
            
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)  # Exponential backoff
                logger.warning(
                    f"MongoDB connection failed (attempt {attempt + 1}/{max_retries}). "
                    f"Retrying in {delay}s... Error: {e}"
                )
                time.sleep(delay)
            else:
                logger.error(
                    f"Failed to connect to MongoDB after {max_retries} attempts. "
                    f"Error: {e}. App will continue but database operations will fail."
                )
                return False
                
        except Exception as e:
            logger.error(f"Unexpected error during MongoDB connection: {e}")
            _db_connection_status["error"] = str(e)
            return False
    
    return False


def is_database_connected() -> bool:
    """Check if database is currently connected"""
    return _db_connection_status["connected"]


def get_connection_status() -> dict:
    """Get detailed database connection status"""
    return {
        "connected": _db_connection_status["connected"],
        "error": _db_connection_status["error"],
        "last_attempt": _db_connection_status["last_attempt"],
        "retry_count": _db_connection_status["retry_count"]
    }


def retry_connection() -> bool:
    """
    Retry database connection at runtime.
    Useful if DB was temporarily down during startup.
    
    Returns:
        bool: True if connection successful
    """
    logger.info("Attempting runtime database reconnection...")
    return _connect_with_retry(max_retries=2, base_delay=0.5)


# Attempt initial connection without blocking app startup
_connect_with_retry(max_retries=3, base_delay=1.0)

