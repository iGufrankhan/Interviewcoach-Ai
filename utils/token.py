import os
from datetime import datetime, timedelta, timezone
from typing import Any
import logging

from jose import JWTError, ExpiredSignatureError, jwt

from utils.apierror import APIError

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", "3600"))


def create_access_token(
    data: dict[str, Any] | None = None,
    expires_delta: int | None = None,
    user_id: str | None = None,
) -> str:
    if not SECRET_KEY:
        raise APIError(
            status_code=500,
            message="JWT secret is not configured",
            error_code="JWT_SECRET_MISSING",
        )

    to_encode: dict[str, Any] = {}
    if data:
        to_encode.update(data)
    if user_id is not None:
        to_encode["user_id"] = user_id
        logger.info(f"🔑 Creating token for user_id: {user_id}")
        logger.info(f"   Using SECRET_KEY: {SECRET_KEY}")
        logger.info(f"   Using ALGORITHM: {ALGORITHM}")

    if "user_id" not in to_encode:
        raise APIError(
            status_code=400,
            message="user_id is required to create token",
            error_code="USER_ID_REQUIRED",
        )

    expire_seconds = expires_delta if expires_delta is not None else ACCESS_TOKEN_EXPIRE_SECONDS
    expire = datetime.now(timezone.utc) + timedelta(seconds=expire_seconds)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"✅ Token created successfully. First 30 chars: {token[:30]}")
    return token


def verify_access_token(token: str) -> str:
    """
    Verify JWT access token and extract user_id
    
    Args:
        token: JWT token string
        
    Returns:
        user_id from the token
        
    Raises:
        APIError: If token is invalid or expired
    """
    logger.info(f"🔐 Verifying token: {token[:30]}...")
    logger.info(f"   SECRET_KEY being used: {SECRET_KEY}")
    logger.info(f"   ALGORITHM: {ALGORITHM}")
    
    if not SECRET_KEY:
        logger.error("❌ JWT secret key not configured!")
        raise APIError(
            status_code=500,
            message="JWT secret is not configured",
            error_code="JWT_SECRET_MISSING",
        )
    
    try:
        logger.info(f"   Attempting to decode token...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"   Token decoded successfully")
        logger.debug(f"   Payload: {payload}")
        
        user_id: str = payload.get("user_id")
        logger.info(f"   Extracted user_id: {user_id}")
        
        if user_id is None:
            logger.error("❌ user_id not found in token payload")
            raise APIError(
                status_code=401,
                message="Invalid token: user_id not found",
                error_code="INVALID_TOKEN",
            )
        
        logger.info(f"✅ Token verification successful. User ID: {user_id}")
        return user_id
        
    except ExpiredSignatureError as e:
        logger.error(f"❌ Token has expired: {str(e)}")
        raise APIError(
            status_code=401,
            message="Token has expired",
            error_code="TOKEN_EXPIRED",
        )
    except JWTError as e:
        logger.error(f"❌ JWT verification failed: {str(e)}")
        raise APIError(
            status_code=401,
            message=f"Invalid token: {str(e)}",
            error_code="INVALID_TOKEN",
        )

