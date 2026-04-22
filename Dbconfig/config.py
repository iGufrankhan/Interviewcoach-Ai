"""
MongoDB database connection management.
"""

import os
import time
import logging
import atexit
import signal
from dotenv import load_dotenv
from mongoengine import connect, disconnect
from pymongo.errors import PyMongoError
from utils.constant import DATABASE_URL, DATABASE_NAME

logger = logging.getLogger(__name__)
load_dotenv()

MAX_RETRIES = 3
RETRY_INTERVAL = 5


class DatabaseConnection:
    """MongoDB connection manager with automatic retry and reconnection logic."""
    
    def __init__(self):
        self.retry_count = 0
        self.is_connected = False
        self.mongo_uri = DATABASE_URL
        self.db_name = DATABASE_NAME
        
        self._register_signal_handlers()
        self._register_exit_handler()
    
    def _register_signal_handlers(self):
        """Register handlers for graceful shutdown."""
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)
    
    def _register_exit_handler(self):
        """Register handler for program exit."""
        atexit.register(self._handle_shutdown)
    
    def _handle_shutdown(self, signum=None, frame=None):
        """Handle application termination gracefully."""
        try:
            logger.info("Closing MongoDB connection...")
            disconnect()
            logger.info("✓ MongoDB connection closed")
        except Exception as e:
            logger.error(f"Error during database disconnection: {e}")
        finally:
            if signum is not None:
                exit(0)
    
    async def connect(self):
        """Connect to MongoDB with retry logic."""
        try:
            if not self.mongo_uri:
                raise ValueError("MongoDB URI is not defined in environment variables")
            
            logger.info(f"Attempting MongoDB connection to {self.mongo_uri.split('@')[-1]}...")
            
            connect(
                db=self.db_name,
                host=self.mongo_uri,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                retryWrites=True,
                maxPoolSize=10,
            )
            
            self.is_connected = True
            self.retry_count = 0
            logger.info("✅ MongoDB connected successfully")
            
        except PyMongoError as e:
            logger.error(f"MongoDB connection error: {e}")
            self.is_connected = False
            await self._handle_connection_error()
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            self.is_connected = False
            await self._handle_connection_error()
    
    async def _handle_connection_error(self):
        """Handle connection errors with retry logic."""
        if self.retry_count < MAX_RETRIES:
            self.retry_count += 1
            logger.warning(
                f"Retrying connection... Attempt {self.retry_count}/{MAX_RETRIES} "
                f"in {RETRY_INTERVAL}s"
            )
            await self._async_sleep(RETRY_INTERVAL)
            await self.connect()
        else:
            logger.error(f"Failed to connect to MongoDB after {MAX_RETRIES} attempts")
    
    @staticmethod
    async def _async_sleep(seconds):
        """Async sleep wrapper."""
        time.sleep(seconds)
    
    def get_connection_status(self) -> dict:
        """Get current connection status."""
        return {
            "is_connected": self.is_connected,
            "retry_count": self.retry_count,
            "mongo_uri": self.mongo_uri.split('@')[-1] if '@' in self.mongo_uri else self.mongo_uri,
            "db_name": self.db_name
        }


db_connection = DatabaseConnection()


async def init_db():
    """Initialize database connection at startup."""
    await db_connection.connect()


def get_db_status() -> dict:
    """Get database connection status."""
    return db_connection.get_connection_status()


def is_database_connected() -> bool:
    """Check if database is connected."""
    return db_connection.is_connected

