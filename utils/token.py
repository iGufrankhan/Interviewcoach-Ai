import os
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, ExpiredSignatureError, jwt

from utils.apierror import APIError

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

    if "user_id" not in to_encode:
        raise APIError(
            status_code=400,
            message="user_id is required to create token",
            error_code="USER_ID_REQUIRED",
        )

    expire_seconds = expires_delta if expires_delta is not None else ACCESS_TOKEN_EXPIRE_SECONDS
    expire = datetime.now(timezone.utc) + timedelta(seconds=expire_seconds)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str) -> str:
    if not SECRET_KEY:
        raise APIError(
            status_code=500,
            message="JWT secret is not configured",
            error_code="JWT_SECRET_MISSING",
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise APIError(
                status_code=401,
                message="Invalid token: user_id missing",
                error_code="INVALID_TOKEN",
            )
        return str(user_id)

    except ExpiredSignatureError:
        raise APIError(
            status_code=401,
            message="Token has expired",
            error_code="TOKEN_EXPIRED",
        )

    except JWTError:
        raise APIError(
            status_code=401,
            message="Invalid token",
            error_code="INVALID_TOKEN",
        )
