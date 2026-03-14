from pydantic import BaseModel, EmailStr, Field


class UserSignupRequest(BaseModel):
    email: EmailStr = Field(..., description="The user's email address")
    password: str = Field(..., min_length=8, max_length=72, description="The user's password (minimum 8 characters)")
    name: str | None = Field(default=None, description="The user's full name (optional)")
    username: str | None = Field(default=None, description="The user's username (optional)")
    token: str = Field(..., description="The OTP token sent to the user's email for verification")


class UserLoginRequest(BaseModel):
    email: EmailStr = Field(..., description="The user's email address")
    password: str = Field(..., description="The user's password")


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str | None = None
    created_at: str

    
    