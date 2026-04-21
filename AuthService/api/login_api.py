from fastapi import APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from AuthService.schemas.user import UserLoginRequest
from AuthService.authservice.registerloginService import LoginUser
from utils.apierror import APIError
from utils.error_codes import ErrorCode
import logging

logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    prefix="/api/login",
    tags=["Login"]
)


@limiter.limit("5/minute")
@router.post("/")
async def login_user(request: Request, login_request: UserLoginRequest):
    """
    User login endpoint with rate limiting (5 requests/minute).
    
    Args:
        login_request: User credentials (email & password)
    
    Returns:
        Access token, refresh token, and user info on success
    
    Raises:
        APIError with standardized error codes for all failure scenarios
    """
    try:
        result = await LoginUser(login_request.email, login_request.password)
        return result
    except APIError:
        # Re-raise APIError as-is (already has proper error code)
        raise
    except Exception as e:
        # Catch unexpected errors and convert to APIError
        logger.error(f"Login failed for {login_request.email}", exc_info=True)
        raise APIError(
            error_code=ErrorCode.INVALID_CREDENTIALS,
            internal_message=str(e)
        )