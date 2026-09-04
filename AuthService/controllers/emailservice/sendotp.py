from Models.userReg.otp import OTP
from AuthService.utils.helper.otpgenerate import generate_otp
from utils.apierror import APIError
from AuthService.controllers.emailservice.emailTranspoter import CreateTransporter
from fastapi_mail import MessageSchema, FastMail, MessageType
import logging

logger = logging.getLogger(__name__)

async def send_otp_email(email: str, purpose: str = "registration"):
    otp_info = generate_otp()
    otp_code = otp_info["otp"]
    expires_at = otp_info["expires_at"]

    existing_otps = await OTP.async_find(email=email, purpose=purpose)
    for otp_obj in existing_otps:
        await OTP.async_delete(id=otp_obj.id)

    otp_entry = OTP(
        email=email,
        otp=otp_code,
        purpose=purpose,
        expires_at=expires_at
    )
    await otp_entry.async_save()

    try:
        logger.info(f" Attempting to send OTP to {email} via Gmail SMTP...")
        
        message = MessageSchema(
            subject="Your OTP Code for Interview Coach AI",
            recipients=[email],
            body=f"Your OTP code is: {otp_code}\n\nThis code will expire in 5 minutes.\n\nIf you didn't request this, please ignore this email.",
            subtype=MessageType.plain
        )
        
        fm = FastMail(CreateTransporter)
        await fm.send_message(message)
        
        logger.info(f" OTP sent successfully to {email}")
        return {"status": "success", "message": "OTP sent successfully"}
    except Exception as e:
        logger.error(f" Failed to send OTP email to {email}: {str(e)}")
        raise APIError(
            status_code=500,
            message=f"Failed to send OTP email: {str(e)}",
            error_code="OTP_EMAIL_SEND_FAILED"
        )
    
    
    
    
 
    
    
    
    

    