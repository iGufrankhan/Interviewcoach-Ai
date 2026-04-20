import os
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, ExpiredSignatureError, jwt

from utils.apierror import APIError
from utils.constant import (
    ACCESS_TOKEN_KEY,
    REFRESH_TOKEN_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_SECONDS,
    REFRESH_TOKEN_EXPIRE_SECONDS,
)   




def create_access_token(
    data: dict[str, Any] | None = None,
    expires_delta: int | None = None,
    user_id: str | None = None,
) -> str:
    if not ACCESS_TOKEN_KEY:
        raise APIError(
            status_code=500,
            message="JWT secret is not configured",
            error_code="ACCESS_TOKEN_KEY",
        )

    to_encode: dict[str, Any] = {}
    if data:
        to_encode.update(data)
    if user_id is not None:
        to_encode["user_id"] = user_id

    if "user_id" not in to_encode:
        raise APIError(
            status_code=400,
            message="user_id is required to create token",
            error_code="USER_ID_REQUIRED",
        )

    expire_seconds = expires_delta if expires_delta is not None else ACCESS_TOKEN_EXPIRE_SECONDS
    expire = datetime.now(timezone.utc) + timedelta(seconds=expire_seconds)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, ACCESS_TOKEN_KEY, algorithm=ALGORITHM)
    return token



def create_refresh_token(
    data: dict[str, Any] | None = None,
    expires_delta: int | None = None,
    user_id: str | None = None,
) -> str:
    if not REFRESH_TOKEN_KEY:
        raise APIError(
            status_code=500,
            message="JWT secret is not configured",
            error_code="REFRESH_TOKEN_",
        )

    to_encode: dict[str, Any] = {}
    if data:
        to_encode.update(data)
    if user_id is not None:
        to_encode["user_id"] = user_id

    if "user_id" not in to_encode:
        raise APIError(
            status_code=400,
            message="user_id is required to create token",
            error_code="USER_ID_REQUIRED",
        )

    expire_seconds = expires_delta if expires_delta is not None else REFRESH_TOKEN_EXPIRE_SECONDS
    expire = datetime.now(timezone.utc) + timedelta(seconds=expire_seconds)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, REFRESH_TOKEN_KEY, algorithm=ALGORITHM)
    return token



def verify_access_token(token: str) -> str:
 
    if not ACCESS_TOKEN_KEY:
        raise APIError(
            status_code=500,
            message="JWT secret is not configured",
            error_code="JWT_SECRET_MISSING",
        )
    
    try:
        payload = jwt.decode(token, ACCESS_TOKEN_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        
        if user_id is None:
            raise APIError(
                status_code=401,
                message="Invalid token: user_id not found",
                error_code="INVALID_TOKEN",
            )
        
        return user_id
        
    except ExpiredSignatureError as e:
        raise APIError(
            status_code=401,
            message="Token has expired",
            error_code="TOKEN_EXPIRED",
        )
    except JWTError as e:
        raise APIError(
            status_code=401,
            message=f"Invalid token: {str(e)}",
            error_code="INVALID_TOKEN",
        )


def verify_refresh_token(token:str)->str:
    
    
    if not REFRESH_TOKEN_KEY:
        raise APIError(
            status_code=500,
            message="JWT secret is not configured",
            error_code="JWT_SECRET_MISSING",
        )
        
    
    try:
        payload = jwt.decode(token, REFRESH_TOKEN_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        
        if user_id is None:
            raise APIError(
                status_code=401,
                message="Invalid token: user_id not found",
                error_code="INVALID_TOKEN",
            )   
        
        return user_id
    except JWTError as e:
        raise APIError(
            status_code=401,
            message=f"Invalid token: {str(e)}",
            error_code="INVALID_TOKEN",
        )
    
    
    