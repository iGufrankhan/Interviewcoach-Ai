from fastapi import Request
import logging
from utils.apierror import APIError
from Models.userReg.user import User
from utils.token import verify_access_token

logger = logging.getLogger(__name__)


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
        logger.error("❌ No token found in request")
        raise APIError(
            status_code=401,
            message="Unauthorized request",
            error_code="UNAUTHORIZED",
        )

    logger.info(f"🔐 Verifying JWT token: {token[:20]}...")
    
    user_id = verify_access_token(token)
    if not user_id:
        logger.error("❌ Token verification returned empty user_id")
        raise APIError(
            status_code=401,
            message="Invalid access token",
            error_code="INVALID_TOKEN",
        )

    logger.info(f"✅ Token verified. User email: {user_id}")

    # user_id contains the email since we store email in the token
    user = User.objects(email=user_id).first()
    if not user:
        logger.error(f"❌ User not found in database for email: {user_id}")
        raise APIError(
            status_code=401,
            message="Invalid access token - user not found",
            error_code="INVALID_TOKEN",
        )

    logger.info(f"✅ User found: {user.email}")
    request.state.user = user
    return user