from fastapi_mail import FastMail, MessageSchema
from AuthService.controllers.emailservice.emailTranspoter import CreateTransporter
from Models.userReg.otp import OTP
from AuthService.utils.helper.otpgenerate import generate_otp
from utils.apierror import APIError
import os
import logging

logger = logging.getLogger(__name__)


async def send_otp_email(email: str, purpose: str = "registration"):
    otp_info = generate_otp()
    otp_code = otp_info["otp"]
    expires_at = otp_info["expires_at"]

    # Debug: Check if email config is loaded
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    
    if not gmail_user or not gmail_password:
        logger.error(f"❌ Email not configured! GMAIL_USER={gmail_user}, GMAIL_PASSWORD={'***' if gmail_password else 'NOT SET'}")
        raise APIError(
            status_code=500,
            message="Email service not configured",
            error_code="EMAIL_CONFIG_MISSING"
        )

    OTP.objects(email=email, purpose=purpose).delete()

    otp_entry = OTP(
        email=email,
        otp=otp_code,
        purpose=purpose,
        expires_at=expires_at
    )
    otp_entry.save()

    message = MessageSchema(
        subject="Your OTP Code for Interview Coach AI",
        recipients=[email],
        body=f"Your OTP code is: {otp_code}\n\nThis code will expire in 5 minutes.\n\nIf you didn't request this, please ignore this email.",
        subtype="plain",
    )

    fm = FastMail(CreateTransporter)
    try:
        logger.info(f"📧 Attempting to send OTP to {email}...")
        await fm.send_message(message)
        logger.info(f"✅ OTP sent successfully to {email}")
        return {"status": "success", "message": "OTP sent successfully"}
    except Exception as e:
        logger.error(f"❌ Failed to send OTP email to {email}: {str(e)}")
        raise APIError(
            status_code=500,
            message=f"Failed to send OTP email: {str(e)}",
            error_code="OTP_EMAIL_SEND_FAILED"
        )
    
    
    
    
 
    
    
    
    

    