from fastapi import APIRouter
from utils.apierror import APIError
from utils.apiresponse import error_response
from AuthService.authservice.registerloginService import RefreshToken

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/refresh-token")
async def refresh_token(refresh_token: str):
    try:
        result = await RefreshToken(refresh_token)
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