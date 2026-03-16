from fastapi import Request
from utils.apierror import APIError
from Models.userReg.user import User
from utils.token import verify_access_token


def _extract_bearer_token(auth_header: str | None) -> str | None:
    if not auth_header:
        return None
    if auth_header.startswith("Bearer "):
        return auth_header.replace("Bearer ", "", 1).strip()
    return None


async def verify_jwt(request: Request):
    token = request.cookies.get("accessToken") or _extract_bearer_token(
        request.headers.get("Authorization")
    )

    if not token:
        raise APIError(
            status_code=401,
            message="Unauthorized request",
            error_code="UNAUTHORIZED",
        )

    user_id = verify_access_token(token)
    if not user_id:
        raise APIError(
            status_code=401,
            message="Invalid access token",
            error_code="INVALID_TOKEN",
        )

    user = User.objects(id=user_id).first()
    if not user:
        raise APIError(
            status_code=401,
            message="Invalid access token",
            error_code="INVALID_TOKEN",
        )

    request.state.user = user
    return user