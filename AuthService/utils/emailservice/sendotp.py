import os
import random
from datetime import datetime, timedelta
from .emailTranspoter import CreateTransporter
from Models.userReg.otp.model import OTP
from utils.helper.otpgenerate import generate_otp
from utils.apiresponse import success_response, error_response
from utils.apierror import APIError


async def send_otp_email(email: str,purpose: str = "registration"):
    
    otp_info = generate_otp()
    otp_code = otp_info["otp"]
    expires_at = otp_info["expires_at"]
    
     # delete existing OTP for the email and purpose
    OTP.objects(email=email, purpose=purpose).delete()
    
    # store new OTP in the database
    otp_entry = OTP(email=email, otp=otp_code, purpose=purpose, expires_at=expires_at)
    otp_entry.save()
    
    message = MessageSchema(
        subject="Your OTP Code",
        recipients=[email],
        body=f"Your OTP code is {otp_code}. It will expire in 5 minutes.",
        subtype="plain"
    )
    fm = FastMail(CreateTransporter)
    try:
        await fm.send_message(message)
        return success_response("OTP sent successfully")
    except Exception as e:
        raise APIError("Failed to send OTP email", str(e))
    
    
    
    
 
    
    
    
    

    