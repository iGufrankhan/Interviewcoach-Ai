from pydantic import BaseModel

class CreateSessionRequest(BaseModel):
    title: str = "New Chat"


class SendMessageRequest(BaseModel):
    session_id: str
    message: str
    
    