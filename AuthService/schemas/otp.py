from pydantic import BaseModel, EmailStr, Field


class OTPRequest(BaseModel):
    email: EmailStr = Field(..., description="The user's email address to receive OTP")


class OTPVerificationRequest(BaseModel):
    email: EmailStr = Field(..., description="The user's email address associated with OTP")
    otp: str = Field(..., min_length=4, max_length=10, description="The OTP code")


