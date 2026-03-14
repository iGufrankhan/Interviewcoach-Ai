from pydantic import BaseModel, EmailStr, Field


class OTPRequest(BaseModel):
    email: EmailStr = Field(..., description="The user's email address to receive OTP")


class OTPVerificationRequest(BaseModel):
    email: EmailStr = Field(..., description="The user's email address associated with OTP")
    otp: str = Field(..., min_length=4, max_length=10, description="The OTP code")
    purpose: str = Field(default="registration", description="OTP purpose")
class OTPRequest(BaseModel):
    email: str = Field(..., description="The user's email address to receive the OTP for registration")
    


class OTPVerificationRequest(BaseModel):
    email: str = Field(..., description="The user's email address associated with the OTP")
    otp: str = Field(..., description="The OTP sent to the user's email for verification")
    purpose: str = Field("registration", description="The purpose of the OTP (default is 'registration')")
    
    
    