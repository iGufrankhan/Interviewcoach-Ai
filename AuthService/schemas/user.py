"""
User authentication and response schemas.

Defines Pydantic models for user registration, login, and API responses
with validation rules for password strength and email format.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
from utils.validators import PasswordValidator

class UserLoginRequest(BaseModel):
    """User login request schema."""
    
    email: EmailStr = Field(..., description="The user's email address")
    password: str = Field(..., min_length=8, description="The user's password")

    @validator("password")
    def validate_password(cls, v: str) -> str:
        """Validate password meets strength requirements."""
        return PasswordValidator.validate_strength(v)


class UserResponse(BaseModel):
    """User profile response schema."""
    
    id: str = Field(..., description="Unique user identifier")
    email: EmailStr = Field(..., description="User email address")
    fullname: Optional[str] = Field(None, description="User's full name")
    created_at: str = Field(..., description="Account creation timestamp (ISO format)")


class userRegistrationRequest(BaseModel):
    """User registration request schema."""
    
    email: EmailStr = Field(..., description="The user's email address")
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=72, 
        description="The user's password (8-72 characters)"
    )
    fullname: Optional[str] = Field(
        default=None, 
        description="The user's full name (optional)"
    )
    registration_token: str = Field(..., description="Token received from OTP verification")

    @validator("password")
    def validate_password_strength(cls, v: str) -> str:
        """
        Validate password meets strength requirements.
        
        Requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one digit
        """
        return PasswordValidator.validate_strength(v)


class userafterRegistrationResponse(BaseModel):
    """Response after successful user registration."""
    
    id: str = Field(..., description="Unique user identifier")
    email: EmailStr = Field(..., description="User email address")
    fullname: Optional[str] = Field(None, description="User's full name")
    username: Optional[str] = Field(None, description="User's username")
