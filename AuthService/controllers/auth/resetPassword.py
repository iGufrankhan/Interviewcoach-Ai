


from datetime import datetime, timezone
from passlib.context import CryptContext

from AuthService.controllers.emailservice.sendotp import send_otp_email
from Models.userReg.otp import OTP
from Models.userReg.user import User
from utils.apierror import APIError
from utils.apiresponse import success_response
from utils.token import create_access_token, verify_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def request_password_reset(email: str):
    """Initiate password reset by sending OTP to email."""
    email_lower = email.lower().strip()
    user = User.objects(email__iexact=email_lower).first()

    if not user:
        raise APIError(
            status_code=404,
            message="User not found",
            error_code="USER_NOT_FOUND"
        )
        
    msg = await send_otp_email(email_lower, purpose="password_reset")
    if msg.get("status") != "success":
        raise APIError(
            status_code=500,
            message=msg.get("message", "Failed to send OTP"),
            error_code="OTP_SEND_FAILED"
        )
        
    
    return success_response(
        message="An OTP has been sent for password reset",
        status_code=200
    )
    
    

async def verify_password_reset_otp(email: str, otp: str):
    """Verify OTP for password reset and return a short-lived token."""
    email_lower = email.lower().strip()
    otp_entry = OTP.objects(
        email__iexact=email_lower,
        purpose="password_reset"
    ).order_by("-created_at").first()

    if not otp_entry:
        raise APIError(
            status_code=400,
            message="Invalid or expired OTP",
            error_code="OTP_INVALID_OR_EXPIRED"
        )

    if otp_entry.expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
        otp_entry.delete()
        raise APIError(
            status_code=400,
            message="Invalid or expired OTP",
            error_code="OTP_INVALID_OR_EXPIRED"
        )

    if otp_entry.otp != otp:
        raise APIError(
            status_code=400,
            message="Incorrect OTP",
            error_code="OTP_INCORRECT"
        )
    
    # Get user to fetch user_id
    user = User.objects(email__iexact=email_lower).first()
    if not user:
        raise APIError(
            status_code=404,
            message="User not found",
            error_code="USER_NOT_FOUND"
        )
  
    reset_token = create_access_token(
        user_id=str(user.id)
    )

    # Optionally, you can delete the OTP after successful verification
    otp_entry.delete()

    return success_response(
        message="OTP verified successfully",
        status_code=200,
        data={"reset_token": reset_token}
    )
    
    
async def resend_password_reset_otp(email: str):
    """Resend OTP for password reset."""
    email_lower = email.lower().strip()
    user = User.objects(email__iexact=email_lower).first()

    if not user:
        raise APIError(
            status_code=404,
            message="User not found",
            error_code="USER_NOT_FOUND"
        )
    msg = await send_otp_email(email_lower, purpose="password_reset")
    if msg.get("status") != "success":
        raise APIError(
            status_code=500,
            message=msg.get("message", "Failed to send OTP"),
            error_code="OTP_SEND_FAILED"
        )
    return success_response(
        message="A new OTP has been sent for password reset",
        status_code=200
    )
    
    
async def reset_password(email: str, new_password: str):
    """Reset password using the provided reset token."""
    email_lower = email.lower().strip()
    user = User.objects(email__iexact=email_lower).first()
    
    if not user:
        raise APIError(
            status_code=404,
            message="User not found",
            error_code="USER_NOT_FOUND"
        )
    
    user.password_hash = pwd_context.hash(new_password[:72])
    user.save()
    
    return success_response(
        message="Password has been reset successfully",
        status_code=200
    )