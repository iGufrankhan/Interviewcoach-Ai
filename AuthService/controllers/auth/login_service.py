from passlib.context import CryptContext

from Models.userReg.user import User
from utils.apierror import APIError
from utils.apiresponse import success_response
from utils.token import create_access_token,create_refresh_token, verify_access_token,verify_refresh_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def login_user(email: str, password: str):
    """Login with email and password."""
    user = await User.async_find_one(email=email)
    
    

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
    access_token = create_access_token(user_id=email)
    refresh_token = create_refresh_token(user_id=email)
    
    user.RefreshToken = refresh_token
    await user.async_save()
    
    
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
            "refresh_token": refresh_token,
            "token_type": "bearer",
        },
        status_code=200
    )
    
    
    
async def Refreshtoken(refresh_token: str):
    
    if(not refresh_token):
        raise APIError(
            status_code=401,
            message="Refresh token is required",
            error_code="REFRESH_TOKEN_REQUIRED")
        
        
    try:
        payload = verify_access_token(refresh_token)
        user_email = payload.get("user_id")  # This is the email
        
        user = await User.async_find_one(email=user_email)
        if not user or user.RefreshToken != refresh_token:
            raise APIError(
                status_code=401,
                message="Invalid refresh token",
                error_code="INVALID_REFRESH_TOKEN"
            )
            
        # Generate new access token with email
        new_access_token = create_access_token(user_id=user_email)
        user.RefreshToken = refresh_token
        await user.async_save()
        return success_response(
            message="Access token refreshed successfully",
            data={
                "access_token": new_access_token,
                "token_type": "bearer"
            },
            status_code=200
        )
        
    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(
            status_code=401,
            message=f"Token verification failed: {str(e)}",
            error_code="TOKEN_VERIFICATION_FAILED"
        )
        
    
    