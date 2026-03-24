from datetime import datetime
from passlib.context import CryptContext
import logging

from AuthService.controllers.emailservice.sendotp import send_otp_email
from utils.token import create_access_token, verify_access_token
from AuthService.utils.helper.generate_username import generate_unique_username
from utils.apierror import APIError
from utils.apiresponse import success_response, error_response
from Models.userReg.user import User
from Models.userReg.otp import OTP

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def initializeemailsignup(email: str):
    """Step 1: Send OTP to email or notify if user already exists."""
    user = User.objects(email=email).first()

    # Check if user already exists
    if user:
        return error_response(
            message="Setup failed. Please try again.",
            status_code=200,
            data={"user_exists": True}
        )

    msg = await send_otp_email(email, purpose="registration")
    if msg.get("status") != "success":
        raise APIError(
            status_code=500,
            message=msg.get("message", "Failed to send OTP"),
            error_code="OTP_SEND_FAILED"
        )

    return success_response(
        message="OTP has been sent",
        status_code=200,
        data={"user_exists": False}
    )


async def verifyotp(email: str, otp: str):
    """Step 2: Verify OTP and return short-lived registration token."""
    otp_entry = OTP.objects(
        email=email,
        purpose="registration"
    ).order_by("-created_at").first()

    if not otp_entry:
        raise APIError(
            status_code=400,
            message="Invalid or expired OTP",
            error_code="OTP_INVALID_OR_EXPIRED"
        )

    if otp_entry.expires_at < datetime.utcnow():
        otp_entry.delete()
        raise APIError(
            status_code=400,
            message="Invalid or expired OTP",
            error_code="OTP_INVALID_OR_EXPIRED"
        )

    if otp_entry.otp != otp:
        raise APIError(
            status_code=400,
            message="Invalid or expired OTP",
            error_code="OTP_INVALID_OR_EXPIRED"
        )

    otp_entry.delete()
   

    registration_token = create_access_token(user_id=f"reg:{email}")
    return success_response(
        message="OTP verified successfully",
        data={"registration_token": registration_token, "token_type": "bearer"},
        status_code=200
    )


async def resend_otp(email: str):
    """Resend OTP to email if user is still in registration flow."""
    user = User.objects(email=email).first()

    # Do not reveal whether email exists.
    if user:
        return success_response(
            message="OTP resent successfully",
            status_code=200
        )

    msg = await send_otp_email(email, purpose="registration")
    if msg.get("status") != "success":
        raise APIError(
            status_code=500,
            message=msg.get("message", "Failed to send OTP"),
            error_code="OTP_SEND_FAILED"
        )

    return success_response(
        message="otp resent successfully",
        status_code=200
    )


async def complete_registration(email: str, password: str, fullname: str, registration_token: str):
    """Step 3: Complete registration only with verified registration token."""
    
    try:
        token_user_id = verify_access_token(registration_token)
      
    except Exception as e:
        raise APIError(
            status_code=401,
            message="Invalid registration token",
            error_code="INVALID_REGISTRATION_TOKEN"
        )

    if not token_user_id or not token_user_id.startswith("reg:"):
        raise APIError(
            status_code=401,
            message="Invalid registration token",
            error_code="INVALID_REGISTRATION_TOKEN"
        )

    token_email = token_user_id.replace("reg:", "", 1)
    
    if token_email.lower() != email.lower():
        raise APIError(
            status_code=401,
            message="Registration token does not match email",
            error_code="REGISTRATION_TOKEN_EMAIL_MISMATCH"
        )

    existing_user = User.objects(email=email).first()
    if existing_user:
        raise APIError(
            status_code=409,
            message="Setup failed. Please try again.",
            error_code="EMAIL_EXISTS"
        )

    username = generate_unique_username(email)
    password_hash = pwd_context.hash(password[:72])

    new_user = User(
        email=email,
        password_hash=password_hash,
        fullname=fullname,
        username=username,
        is_email_verified=True
    )
    new_user.save()
  
    # Generate access token for the newly registered user
    access_token = create_access_token(user_id=str(new_user.email))
 
    return success_response(
        message="Registration completed successfully",
        data={
            "access_token": access_token,
            "user_id": str(new_user.id),
            "user": {
                "id": str(new_user.id),
                "email": new_user.email,
                "username": new_user.username,
                "fullname": new_user.fullname
            }
        },
        status_code=200
    )











