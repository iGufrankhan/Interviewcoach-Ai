from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import logging
from utils.apierror import APIError
from Models.userReg.user import User
from utils.token import verify_access_token

logger = logging.getLogger(__name__)


def _extract_bearer_token(auth_header: str | None) -> str | None:
    """Extract Bearer token from Authorization header"""
    if not auth_header:
        return None
    if auth_header.startswith("Bearer "):
        return auth_header.replace("Bearer ", "", 1).strip()
    return None


class AuthMiddleware(BaseHTTPMiddleware):
    """
    FastAPI ASGI middleware for JWT authentication.
    
    - Extracts token from cookies or Authorization header
    - Validates token and attaches user to request.state
    - Skips authentication for public routes
    """
    
    # Routes that don't require authentication
    PUBLIC_ROUTES = {
        "/",
        "/health",
        "/api/status",
        "/docs",
        "/openapi.json",
        "/redoc",
    }
    
    async def dispatch(self, request: Request, call_next):
        # Skip auth for public routes
        if request.url.path in self.PUBLIC_ROUTES:
            return await call_next(request)
        

        auth_endpoints = {"/api/login", "/api/auth", "/login"}
        if any(request.url.path.startswith(endpoint) for endpoint in auth_endpoints):
            return await call_next(request)
        
        # Extract token from cookies or Authorization header
        token = request.cookies.get("accessToken") or _extract_bearer_token(
            request.headers.get("Authorization")
        )
        
        if not token:
            logger.warning(f"Missing token for {request.url.path}")
            return JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized request", "error_code": "UNAUTHORIZED"},
            )
        
        try:
            user_id = verify_access_token(token)
            user = await User.async_find_one(email=user_id)
            if not user:
                logger.warning(f"User not found for token: {user_id}")
                return JSONResponse(
                    status_code=401,
                    content={
                        "detail": "Invalid access token - user not found",
                        "error_code": "INVALID_TOKEN",
                    },
                )
            
            # Attach user to request state
            request.state.user = user
            
        except APIError as e:
            logger.error(f"Token verification failed: {e.message}")
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.message, "error_code": e.error_code},
            )
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or expired token", "error_code": "INVALID_TOKEN"},
            )
        
        return await call_next(request)