from fastapi import APIRouter
from utils.apiresponse import error_response
from utils.apierror import APIError
from AuthService.schemas.user import userRegistrationRequest as UserSignupRequest
from AuthService.schemas.otp import OTPRequest, OTPVerificationRequest
from AuthService.authservice.registerloginService import (
    SendOTP,
    VerifyOTP,
    CompleteRegistration,
    ResendOTP,
)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/send-otp")
async def send_otp(request: OTPRequest):
    try:
        result = await SendOTP(request.email)
        return result
    except APIError as e:
        detail = e.detail if isinstance(e.detail, dict) else {}
        return error_response(
            message=detail.get("error", "Failed to send OTP"),
            error_code=detail.get("error_code", "OTP_SEND_ERROR"),
            status_code=e.status_code
        )
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="OTP_SEND_ERROR",
            status_code=500
        )


@router.post("/verify-otp")
async def verify_otp(request: OTPVerificationRequest):
    try:
        print(f"📨 Verify OTP request: email={request.email}, otp={request.otp}")
        result = await VerifyOTP(request.email, request.otp)
        print(f"✅ VerifyOTP returned: {result}")
        if isinstance(result, dict):
            print(f"   Data keys: {result.get('data', {}).keys() if result.get('data') else 'NO DATA'}")
            if result.get('data'):
                print(f"   registration_token present: {'registration_token' in result['data']}")
        return result
    except APIError as e:
        detail = e.detail if isinstance(e.detail, dict) else {}
        return error_response(
            message=detail.get("error", "OTP verification failed"),
            error_code=detail.get("error_code", "OTP_VERIFICATION_ERROR"),
            status_code=e.status_code
        )
    except Exception as e:
        print(f"❌ Verify OTP error: {str(e)}")
        return error_response(
            message=str(e),
            error_code="OTP_VERIFICATION_ERROR",
            status_code=500
        )


@router.post("/resend-otp")
async def resend_otp(request: OTPRequest):
    try:
        result = await ResendOTP(request.email)
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


@router.post("/complete-registration")
async def complete_registration(request: UserSignupRequest):
    try:
        print(f"📦 Received complete-registration request:")
        print(f"   Email: {request.email}")
        print(f"   Token: {request.registration_token[:20] if request.registration_token else 'EMPTY'}...")
        print(f"   Token length: {len(request.registration_token) if request.registration_token else 0}")
        
        result = await CompleteRegistration(
            request.email,
            request.password,
            request.fullname,
            request.registration_token,
        )
        return result
    except APIError as e:
        detail = e.detail if isinstance(e.detail, dict) else {}
        return error_response(
            message=detail.get("error", "Registration failed"),
            error_code=detail.get("error_code", "REGISTRATION_ERROR"),
            status_code=e.status_code
        )
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="REGISTRATION_ERROR",
            status_code=500
        )