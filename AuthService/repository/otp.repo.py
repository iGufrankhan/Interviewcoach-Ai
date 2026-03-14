from Models.userReg.otp import OTP
from datetime import datetime, timedelta


async def create_otp_entry(email: str, otp: str, purpose: str = "registration"):
    otp_entry = OTP(email=email, otp=otp, purpose=purpose)
    otp_entry.save()
    return otp_entry
