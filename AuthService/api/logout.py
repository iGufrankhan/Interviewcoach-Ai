from fastapi import APIRouter
from utils.apierror import APIError
from AuthService.authservice.registerloginService import LogoutUser


api_router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

@api_router.post("/logout")
async def logout_endpoint(refresh_token: str):
    try:
        result = await LogoutUser(refresh_token)
        return result
    except APIError as e:
        detail = e.detail if isinstance(e.detail, dict) else {}
        return {
            "status": "error",
            "message": detail.get("error", "Logout failed"),
            "error_code": detail.get("error_code", "LOGOUT_ERROR"),
            "data": None
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "error_code": "LOGOUT_ERROR",
            "data": None
        }
        
    