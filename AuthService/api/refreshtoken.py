from fastapi import APIRouter
from utils.apierror import APIError
from utils.apiresponse import error_response
from AuthService.authservice.registerloginService import RefreshToken
from AuthService.schemas.token import RefreshTokenRequest

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/refresh-token")
async def refresh_token(request: RefreshTokenRequest):
    """Refresh access token using a valid refresh token
    
    **Request Body:**
    - `refresh_token` (str, required): Valid refresh token
    
    **Returns:**
    - New access token and refresh token on success
    """
    try:
        result = await RefreshToken(request.refresh_token)
        return result
    except APIError as e:
        detail = e.detail if isinstance(e.detail, dict) else {}
        return error_response(
            message=detail.get("error", "Failed to refresh token"),
            error_code=detail.get("error_code", "TOKEN_REFRESH_ERROR"),
            status_code=e.status_code
        )
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="TOKEN_REFRESH_ERROR",
            status_code=500
        )