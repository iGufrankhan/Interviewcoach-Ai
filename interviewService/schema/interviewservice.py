"""
Interview service request and response schemas.

Defines Pydantic models for interview operations including starting interviews,
submitting answers, and managing interview sessions.
"""

from typing import Optional
from pydantic import BaseModel, Field, validator
from lib.validators import StringValidator


# ============================================
# INTERVIEW SESSION SCHEMAS
# ============================================

class StartInterviewRequest(BaseModel):
    """Request to start a new interview session."""
    
    job_description: str = Field(
        ..., 
        min_length=10, 
        description="The job description for the interview"
    )
    resume_id: str = Field(..., description="The resume ID to use for the interview")
    job_title: str = Field(
        default="Interview", 
        min_length=1, 
        description="The job title for the interview"
    )

    @validator("job_description", pre=True)
    def validate_job_description_not_empty(cls, v: str) -> str:
        """Validate job description is not empty or whitespace-only."""
        return StringValidator.validate_not_empty(v, "Job description")

    @validator("resume_id", pre=True)
    def validate_resume_id_not_empty(cls, v: str) -> str:
        """Validate resume ID is not empty."""
        return StringValidator.validate_not_empty(v, "Resume ID")

    @validator("job_title", pre=True)
    def validate_job_title_not_empty(cls, v: str) -> str:
        """Validate job title is not empty."""
        return StringValidator.validate_not_empty(v, "Job title")


class SubmitAnswerRequest(BaseModel):
    """Request to submit an answer to an interview question."""
    
    session_id: str = Field(..., description="The session ID for the interview")
    answer: str = Field(..., min_length=1, description="The answer to the interview question")
    use_audio: bool = Field(
        default=False, 
        description="Whether the answer was provided via audio"
    )

    @validator("session_id", pre=True)
    def validate_session_id_not_empty(cls, v: str) -> str:
        """Validate session ID is not empty."""
        return StringValidator.validate_not_empty(v, "Session ID")

    @validator("answer", pre=True)
    def validate_answer_not_empty(cls, v: str) -> str:
        """Validate answer is not empty or whitespace-only."""
        return StringValidator.validate_not_empty(v, "Answer")


class SubmitInterviewRequest(BaseModel):
    """Request to submit and conclude an interview session."""
    
    session_id: str = Field(..., description="The session ID for the interview")

    @validator("session_id", pre=True)
    def validate_session_id_not_empty(cls, v: str) -> str:
        """Validate session ID is not empty."""
        return StringValidator.validate_not_empty(v, "Session ID")
