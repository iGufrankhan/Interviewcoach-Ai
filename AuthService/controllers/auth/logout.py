


from Models.userReg.user import User
from utils.apiresponse import error_response, success_response
from lib.helper.SetCookies import clear_cookies
from utils.token import verify_refresh_token


async def logout_user(refresh_token: str):
    """Logout user by invalidating their tokens."""
    if refresh_token:
        try:
            payload = verify_refresh_token(refresh_token)
            user_id = payload.get("user_id")
            if user_id:
                user= User.objects(id=user_id).first()
                if user and user.RefreshToken == refresh_token:
                     user.RefreshToken = None
                     user.save()
                return success_response(
                    message="User logged out successfully",
                    status_code=200
                )
              
        except Exception as e:
            return error_response(
                message="Invalid refresh token",
                status_code=401,
                error_code="INVALID_REFRESH_TOKEN"
            )
   
        
   
    
    
    
    return success_response(
        message="User logged out successfully",
        status_code=200
    )