from pydantic import BaseModel, EmailStr, Field


class UserLoginRequest(BaseModel):
    email: EmailStr = Field(..., description="The user's email address")
    password: str = Field(..., description="The user's password")


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    fullname: str | None = None
    created_at: str


class userRegistrationRequest(BaseModel):
    email: EmailStr = Field(..., description="The user's email address")
    password: str = Field(..., min_length=8, max_length=72, description="The user's password (8-72 characters)")
    fullname: str | None = Field(default=None, description="The user's full name (optional)")
    registration_token: str = Field(..., description="Token received from OTP verification")


class userafterRegistrationResponse(BaseModel):
    id: str
    email: EmailStr
    fullname: str | None = None
    username: str | None = None