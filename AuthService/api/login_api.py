from fastapi import APIRouter
from utils.apiresponse import success_response, error_response
from utils.apierror import APIError
from AuthService.schemas.user import UserLoginRequest
from AuthService.authservice.registerloginService import LoginUser


router = APIRouter(
    prefix="/api/login",
    tags=["Login"]
)


@router.post("/")
async def login_user(login_request: UserLoginRequest):
    try:
        result = await LoginUser(login_request.email, login_request.password)
        return success_response(
            message="User logged in successfully",
            data=result,
            status_code=200
        )
    except APIError as e:
        detail = e.detail if isinstance(e.detail, dict) else {}
        return error_response(
            message=detail.get("error", "Login failed"),
            error_code=detail.get("error_code", "LOGIN_ERROR"),
            status_code=e.status_code
        )
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="LOGIN_ERROR",
            status_code=500
        )