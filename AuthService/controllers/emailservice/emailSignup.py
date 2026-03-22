from datetime import datetime
from passlib.context import CryptContext
import logging

from AuthService.controllers.emailservice.sendotp import send_otp_email
from utils.token import create_access_token, verify_access_token
from AuthService.utils.helper.generate_username import generate_unique_username
from utils.apierror import APIError
from utils.apiresponse import success_response
from Models.userReg.user import User
from Models.userReg.otp import OTP

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def initializeemailsignup(email: str):
    """Step 1: Send OTP to email or notify if user already exists."""
    user = User.objects(email=email).first()

    # Check if user already exists
    if user:
        return success_response(
            message="User already exists with this email",
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
    logger.info(f"🔐 Verifying OTP for email: {email}")
    
    otp_entry = OTP.objects(
        email=email,
        purpose="registration"
    ).order_by("-created_at").first()

    if not otp_entry:
        logger.error(f"❌ OTP entry not found for {email}")
        raise APIError(
            status_code=400,
            message="Invalid or expired OTP",
            error_code="OTP_INVALID_OR_EXPIRED"
        )

    if otp_entry.expires_at < datetime.utcnow():
        logger.error(f"❌ OTP expired for {email}")
        otp_entry.delete()
        raise APIError(
            status_code=400,
            message="Invalid or expired OTP",
            error_code="OTP_INVALID_OR_EXPIRED"
        )

    if otp_entry.otp != otp:
        logger.error(f"❌ OTP mismatch for {email}. Got: {otp}, Expected: {otp_entry.otp}")
        raise APIError(
            status_code=400,
            message="Invalid or expired OTP",
            error_code="OTP_INVALID_OR_EXPIRED"
        )

    otp_entry.delete()
    logger.info(f"✅ OTP verified successfully for {email}")

    registration_token = create_access_token(user_id=f"reg:{email}")
    logger.info(f"✅ Registration token created: {registration_token[:30]}...")

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
    logger.info(f"🔐 Attempting complete_registration for email: {email}")
    logger.debug(f"📝 Token received (first 20 chars): {registration_token[:20] if registration_token else 'NONE'}...")
    
    try:
        token_user_id = verify_access_token(registration_token)
        logger.info(f"✅ Token verified successfully. User ID from token: {token_user_id}")
    except Exception as e:
        logger.error(f"❌ Token verification failed: {str(e)}")
        raise APIError(
            status_code=401,
            message="Invalid registration token",
            error_code="INVALID_REGISTRATION_TOKEN"
        )

    if not token_user_id or not token_user_id.startswith("reg:"):
        logger.error(f"❌ Invalid token format. Expected 'reg:' prefix but got: {token_user_id}")
        raise APIError(
            status_code=401,
            message="Invalid registration token",
            error_code="INVALID_REGISTRATION_TOKEN"
        )

    token_email = token_user_id.replace("reg:", "", 1)
    logger.debug(f"📧 Email from token: {token_email}, Email from request: {email}")
    
    if token_email.lower() != email.lower():
        logger.error(f"❌ Email mismatch! Token email: {token_email}, Request email: {email}")
        raise APIError(
            status_code=401,
            message="Registration token does not match email",
            error_code="REGISTRATION_TOKEN_EMAIL_MISMATCH"
        )

    existing_user = User.objects(email=email).first()
    if existing_user:
        logger.warning(f"⚠️  User already exists: {email}")
        raise APIError(
            status_code=409,
            message="Email already registered",
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
    
    logger.info(f"✅ User registered successfully! ID: {new_user.id}, Email: {email}")

    # Generate access token for the newly registered user
    access_token = create_access_token(user_id=str(new_user.email))
    logger.info(f"✅ Access token generated for new user: {email}")

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











