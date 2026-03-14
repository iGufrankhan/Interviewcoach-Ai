from pydantic import BaseModel, EmailStr, Field



class userRegistrationRequest(BaseModel):
    email: EmailStr = Field(..., description="The user's email address")
    password: str = Field(..., min_length=8, max_length=72, description="The user's password (8-72 characters)")
    name: str | None = Field(default=None, description="The user's full name (optional)")
    username: str | None = Field(default=None, description="The user's username (optional)")
    
class userafterRegistrationResponse(BaseModel):
    id: str
    email: EmailStr
    name: str | None = None
    username: str | None = None
