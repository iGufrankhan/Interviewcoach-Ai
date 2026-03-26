from pydantic import BaseModel, EmailStr, Field


class OTPRequest(BaseModel):
    email: EmailStr = Field(..., description="The user's email address to receive OTP")


class OTPVerificationRequest(BaseModel):
    email: EmailStr = Field(..., description="The user's email address associated with OTP")
    otp: str = Field(..., min_length=4, max_length=10, description="The OTP code")


class ResendOTPRequest(BaseModel):
    email: EmailStr = Field(..., description="The user's email address to resend OTP")


class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(..., description="The user's email address to receive password reset OTP")


class PasswordResetOTPRequest(BaseModel):
    """Schema for requesting password reset OTP"""
    email: EmailStr = Field(..., description="The user's email address to receive password reset OTP")


class PasswordResetVerificationRequest(BaseModel):
    """Schema for verifying password reset OTP"""
    email: EmailStr = Field(..., description="The user's email address associated with password reset")
    otp: str = Field(..., min_length=6, max_length=6, description="The OTP code (6 digits)")
    new_password: str = Field(..., min_length=8, description="The new password for the user")


class PasswordResetOTPVerifyRequest(BaseModel):
    """Schema for verifying password reset OTP only"""
    email: EmailStr = Field(..., description="The user's email address")
    otp: str = Field(..., min_length=6, max_length=6, description="The OTP code (6 digits)")



class PasswordResetCompleteRequest(BaseModel):
    email: EmailStr = Field(..., description="The user's email address associated with password reset")
    new_password: str = Field(..., min_length=8, description="The new password for the user")
    reset_token: str = Field(..., description="The short-lived token obtained after OTP verification for password reset")


class PasswordResetFinalRequest(BaseModel):
    """Schema for resetting password after OTP verification"""
    email: EmailStr = Field(..., description="The user's email address")
    new_password: str = Field(..., min_length=8, description="The new password for the user")

