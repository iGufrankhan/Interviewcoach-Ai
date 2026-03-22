from passlib.context import CryptContext

from Models.userReg.user import User
from utils.apierror import APIError
from utils.apiresponse import success_response
from utils.token import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def login_user(email: str, password: str):
    """Login with email and password."""
    user = User.objects(email=email).first()

    if not user or not pwd_context.verify(password, user.password_hash):
        raise APIError(
            status_code=401,
            message="Invalid credentials",
            error_code="INVALID_CREDENTIALS"
        )

    if not user.is_email_verified:
        raise APIError(
            status_code=403,
            message="Email not verified",
            error_code="EMAIL_NOT_VERIFIED"
        )

    # Create token with email as user_id (matching auth_middleware expectations)
    access_token = create_access_token(user_id=str(user.email))
    return success_response(
        message="User logged in successfully",
        data={
            "user": {
                "id": str(user.id),
                "username": user.username,
                "fullname": user.fullname,
                "email": user.email,
            },
            "access_token": access_token,
            "token_type": "bearer",
        },
        status_code=200
    )