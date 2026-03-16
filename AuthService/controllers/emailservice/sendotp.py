from fastapi_mail import FastMail, MessageSchema
from AuthService.controllers.emailservice.emailTranspoter import CreateTransporter
from Models.userReg.otp import OTP
from AuthService.utils.helper.otpgenerate import generate_otp
from utils.apierror import APIError


async def send_otp_email(email: str, purpose: str = "registration"):
    otp_info = generate_otp()
    otp_code = otp_info["otp"]
    expires_at = otp_info["expires_at"]

    OTP.objects(email=email, purpose=purpose).delete()

    otp_entry = OTP(
        email=email,
        otp=otp_code,
        purpose=purpose,
        expires_at=expires_at
    )
    otp_entry.save()

    message = MessageSchema(
        subject="Your OTP Code",
        recipients=[email],
        body=f"Your OTP code is {otp_code}. It will expire in 5 minutes.",
        subtype="plain",
    )

    fm = FastMail(CreateTransporter)
    try:
        await fm.send_message(message)
        return {"status": "success", "message": "OTP sent successfully"}
    except Exception as e:
        raise APIError(
            status_code=500,
            message=f"Failed to send OTP email: {str(e)}",
            error_code="OTP_EMAIL_SEND_FAILED"
        )
    
    
    
    
 
    
    
    
    

    