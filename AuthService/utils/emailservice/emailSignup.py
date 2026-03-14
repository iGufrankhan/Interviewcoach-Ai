from datetime import datetime
from passlib.context import CryptContext

from AuthService.utils.emailservice.sendotp import send_otp_email
from AuthService.utils.helper.token import create_access_token
from AuthService.utils.helper.generate_username import generate_unique_username
from AuthService.schemas.users import userafterRegistrationResponse,userRegistrationRequest
from utils.apierror import APIError
from utils.apiresponse import success_response
from Models.userReg.user import User
from Models.userReg.otp import OTP

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



async def initializeemailsignup(email: str):
    """Step 1: Send OTP to email."""
    if not email:
        raise APIError(
            status_code=400,
            message="Email is required",
            error_code="EMAIL_REQUIRED"
        )
    user = User.objects(email=email).first()
    if user:
        raise APIError(
            status_code=409,
            message="Email already registered",
            error_code="EMAIL_EXISTS"
        )

    msg = await send_otp_email(email, purpose="registration")
    if msg.get("status") != "success":
        raise APIError(
            status_code=500,
            message=msg.get("message", "Failed to send OTP"),
            error_code="OTP_SEND_FAILED"
        )

    return success_response(message="OTP sent successfully",status_code=200)


async def verifyotp(email: str, otp: str, purpose: str = "registration"):
    """Step 2: Verify OTP and return access token."""
    if not email or not otp:
        raise APIError(
            status_code=400,
            message="Email and OTP are required",
            error_code="EMAIL_OTP_REQUIRED"
        )
    otp_entry = OTP.objects(email=email, purpose=purpose).first()

    if not otp_entry:
        raise APIError(
            status_code=404,
            message="OTP not found",
            error_code="OTP_NOT_FOUND"
        )

    if otp_entry.expires_at < datetime.utcnow():
        otp_entry.delete()
        raise APIError(
            status_code=400,
            message="OTP expired",
            error_code="OTP_EXPIRED"
        )

    if otp_entry.otp != otp:
        raise APIError(
            status_code=400,
            message="Invalid OTP",
            error_code="OTP_INVALID"
        )

    otp_entry.delete()
    
 
    access_token = create_access_token(user_id=f"temp_{email}")
    
    return success_response(
        message="OTP verified successfully",
        data={"access_token": access_token, "token_type": "bearer"},
        status_code=200
    )
    
    
    
    
    



async def complete_registration(token: str, email: str, password: str, name: str | None = None, username: str | None = None):
    """Step 3: Complete registration with username and name."""

    # Check if email already exists
    if not token:
        raise APIError(
            status_code=400,
            message="please provide token",
            error_code="TOKEN_REQUIRED"
        )
        
    existing_user = User.objects(email=email).first()
    if existing_user:
        raise APIError(
            status_code=409,
            message="Email already registered",
            error_code="EMAIL_EXISTS"
        )

    # Generate username if not provided
    if not username:
        username = generate_unique_username(email)

    # Hash password and create user
    password_hash = pwd_context.hash(password[:72]) 
    new_user = User(
        email=email,
        password_hash=password_hash,
        name=name,
        username=username
    )
    new_user.save()

    # Create token for the new registered user
    access_token = create_access_token(user_id=str(new_user.id))
    
    return success_response(
        message="Registration completed successfully",
        data={
             "id": str(new_user.id), 
            "access_token": access_token,
            "token_type": "bearer"
        },
        status_code=200
    )
       

async def login_user(email: str, password: str):
    """Login with email and password."""
    user = User.objects(email=email).first()
    if not user:
        raise APIError(
            status_code=404,
            message="User not found",
            error_code="USER_NOT_FOUND"
        )

    if not pwd_context.verify(password, user.password_hash):
        raise APIError(
            status_code=401,
            message="Invalid credentials",
            error_code="INVALID_CREDENTIALS"
        )

    access_token = create_access_token(user_id=str(user.id))
    return success_response(
        message="User logged in successfully",
        data={
            "user": {"id": str(user.id)},
            "access_token": access_token,
            "token_type": "bearer"
        },
        status_code=200
    )








