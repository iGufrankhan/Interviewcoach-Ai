from pydantic import BaseModel, Field


class CreateSessionRequest(BaseModel):
    title: str = Field(default="New Chat", min_length=1, max_length=100)


class SendMessageRequest(BaseModel):
    session_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1, max_length=5000)


class GetMessagesRequest(BaseModel):
    session_id: str = Field(..., min_length=1)
    limit: int = Field(default=100, ge=1, le=500)
    skip: int = Field(default=0, ge=0)