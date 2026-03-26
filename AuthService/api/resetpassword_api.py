from fastapi import APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from utils.apiresponse import error_response
from utils.apierror import APIError
from AuthService.schemas.otp import ResendOTPRequest, PasswordResetOTPRequest, PasswordResetVerificationRequest, PasswordResetFinalRequest, PasswordResetOTPVerifyRequest
from AuthService.authservice.resetPasswordService import (
    request_password_reset,
    verify_password_reset_otp,
    resend_password_reset_otp,
    reset_password
)



api_router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


limiter = Limiter(key_func=get_remote_address)

@limiter.limit("5/minute")
@api_router.post("/request-forgot-password")
async def request_forgot_password_endpoint(request: Request, body: PasswordResetOTPRequest):
    try:
        result = await request_password_reset(body.email)
        return result
    except APIError as e:
        detail = e.detail if isinstance(e.detail, dict) else {}
        return error_response(
            message=detail.get("error", "Failed to initiate password reset"),
            error_code=detail.get("error_code", "PASSWORD_RESET_ERROR"),
            status_code=e.status_code
        )
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="PASSWORD_RESET_ERROR",
            status_code=500
        )
        
        
@limiter.limit("5/minute")
@api_router.post("/verify-forgot-password-otp")
async def verify_forgot_password_otp_endpoint(request: Request, body: PasswordResetOTPVerifyRequest):
    try:
        result = await verify_password_reset_otp(body.email, body.otp)
        return result
    except APIError as e:
        detail = e.detail if isinstance(e.detail, dict) else {}
        return error_response(
            message=detail.get("error", "OTP verification failed"),
            error_code=detail.get("error_code", "OTP_VERIFICATION_ERROR"),
            status_code=e.status_code
        )
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="OTP_VERIFICATION_ERROR",
            status_code=500
        )
        
@limiter.limit("5/minute")
@api_router.post("/resend-forgot-password-otp")
async def resend_forgot_password_otp_endpoint(request: Request, body: PasswordResetOTPRequest):
    try:
        result = await resend_password_reset_otp(body.email)
        return result
    except APIError as e:
        detail = e.detail if isinstance(e.detail, dict) else {}
        return error_response(
            message=detail.get("error", "Failed to resend OTP"),
            error_code=detail.get("error_code", "OTP_RESEND_ERROR"),
            status_code=e.status_code
        )
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="OTP_RESEND_ERROR",
            status_code=500
        )
        
        
@limiter.limit("5/minute")
@api_router.post("/reset-forgot-password")
async def reset_forgot_password_endpoint(request: Request, body: PasswordResetFinalRequest):
    try:
        result = await reset_password(body.email, body.new_password)
        return result
    except APIError as e:
        detail = e.detail if isinstance(e.detail, dict) else {}
        return error_response(
            message=detail.get("error", "Password reset failed"),
            error_code=detail.get("error_code", "PASSWORD_RESET_FAILED"),
            status_code=e.status_code
        )
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="PASSWORD_RESET_FAILED",
            status_code=500
        )




