from fastapi import APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from utils.apiresponse import error_response
from utils.apierror import APIError
from AuthService.schemas.user import UserLoginRequest
from AuthService.authservice.registerloginService import LoginUser

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    prefix="/api/login",
    tags=["Login"]
)


@limiter.limit("5/minute")
@router.post("/")
async def login_user(request: Request, login_request: UserLoginRequest):
    try:
        result = await LoginUser(login_request.email, login_request.password)
        return result
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