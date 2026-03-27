from pydantic import BaseModel
# Request/Response Models
class StartInterviewRequest(BaseModel):
    job_description: str
    resume_id: str
    job_title: str = "Interview"


class SubmitAnswerRequest(BaseModel):
    session_id: str
    answer: str
    use_audio: bool = False


class SubmitInterviewRequest(BaseModel):
    session_id: str
