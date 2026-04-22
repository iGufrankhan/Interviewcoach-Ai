"""
OTP and password reset schemas.

Defines Pydantic models for OTP verification, password reset, and related operations
with validation for numeric OTP codes and password strength.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
from lib.validators import OTPValidator, PasswordValidator, StringValidator


class OTPRequest(BaseModel):
    """Request to send OTP to email."""
    
    email: EmailStr = Field(..., description="The user's email address to receive OTP")


class OTPVerificationRequest(BaseModel):
    """Request to verify OTP code."""
    
    email: EmailStr = Field(..., description="The user's email address associated with OTP")
    otp: str = Field(..., min_length=4, max_length=10, description="The OTP code")

    @validator("otp", pre=True)
    def validate_otp_not_empty(cls, v: str) -> str:
        """Validate OTP is not empty before processing."""
        return StringValidator.validate_not_empty(v, "OTP")

    @validator("otp")
    def validate_otp_numeric(cls, v: str) -> str:
        """Validate OTP contains only numeric characters."""
        return OTPValidator.validate_numeric(v)


class ResendOTPRequest(BaseModel):
    """Request to resend OTP."""
    
    email: EmailStr = Field(..., description="The user's email address to resend OTP")


class PasswordResetRequest(BaseModel):
    """Request password reset OTP."""
    
    email: EmailStr = Field(..., description="The user's email address to receive password reset OTP")


class PasswordResetOTPRequest(BaseModel):
    """Request password reset OTP."""
    
    email: EmailStr = Field(..., description="The user's email address to receive password reset OTP")


class PasswordResetVerificationRequest(BaseModel):
    """Verify password reset OTP and set new password."""
    
    email: EmailStr = Field(..., description="The user's email address associated with password reset")
    otp: str = Field(..., min_length=6, max_length=6, description="The OTP code (6 digits)")
    new_password: str = Field(..., min_length=8, description="The new password for the user")

    @validator("otp", pre=True)
    def validate_otp_not_empty(cls, v: str) -> str:
        """Validate OTP is not empty."""
        return StringValidator.validate_not_empty(v, "OTP")

    @validator("otp")
    def validate_otp_numeric(cls, v: str) -> str:
        """Validate OTP contains only numeric characters."""
        return OTPValidator.validate_numeric(v)

    @validator("new_password", pre=True)
    def validate_password_not_empty(cls, v: str) -> str:
        """Validate password is not empty."""
        return StringValidator.validate_not_empty(v, "Password")

    @validator("new_password")
    def validate_password_strength(cls, v: str) -> str:
        """Validate password meets strength requirements."""
        return PasswordValidator.validate_strength(v)


class PasswordResetOTPVerifyRequest(BaseModel):
    """Verify password reset OTP only."""
    
    email: EmailStr = Field(..., description="The user's email address")
    otp: str = Field(..., min_length=6, max_length=6, description="The OTP code (6 digits)")

    @validator("otp", pre=True)
    def validate_otp_not_empty(cls, v: str) -> str:
        """Validate OTP is not empty."""
        return StringValidator.validate_not_empty(v, "OTP")

    @validator("otp")
    def validate_otp_numeric(cls, v: str) -> str:
        """Validate OTP contains only numeric characters."""
        return OTPValidator.validate_numeric(v)


class PasswordResetCompleteRequest(BaseModel):
    """Complete password reset with verified token."""
    
    email: EmailStr = Field(..., description="The user's email address associated with password reset")
    new_password: str = Field(..., min_length=8, description="The new password for the user")
    reset_token: str = Field(
        ..., 
        description="The short-lived token obtained after OTP verification for password reset"
    )

    @validator("new_password", pre=True)
    def validate_password_not_empty(cls, v: str) -> str:
        """Validate password is not empty."""
        return StringValidator.validate_not_empty(v, "Password")

    @validator("reset_token", pre=True)
    def validate_token_not_empty(cls, v: str) -> str:
        """Validate reset token is not empty."""
        return StringValidator.validate_not_empty(v, "Reset token")

    @validator("new_password")
    def validate_password_strength(cls, v: str) -> str:
        """Validate password meets strength requirements."""
        return PasswordValidator.validate_strength(v)


class PasswordResetFinalRequest(BaseModel):
    """Reset password after OTP verification."""
    
    email: EmailStr = Field(..., description="The user's email address")
    new_password: str = Field(..., min_length=8, description="The new password for the user")

    @validator("new_password", pre=True)
    def validate_password_not_empty(cls, v: str) -> str:
        """Validate password is not empty."""
        return StringValidator.validate_not_empty(v, "Password")

    @validator("new_password")
    def validate_password_strength(cls, v: str) -> str:
        """Validate password meets strength requirements."""
        return PasswordValidator.validate_strength(v)

