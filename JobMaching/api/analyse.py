from fastapi import APIRouter, Request
from pydantic import BaseModel, Field, validator
from JobMaching.analyser.resumeanalise import JobMatchingService
from utils.apierror import APIError
from utils.error_codes import ErrorCode
from utils.apiresponse import success_response
from utils.constant import GROQ_API_KEY
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Resume Analysis"]
)


class AnalyseResumeRequest(BaseModel):
    """Resume analysis request model"""
    resume_id: str = Field(..., min_length=1, description="Resume ID to analyze")
    description: str = Field(..., min_length=50, description="Job description text (min 50 characters)")
    use_rag: bool = Field(
        default=True, 
        description="Use Hybrid RAG system (True) or LLM-only (False)"
    )
    
    @validator("resume_id")
    def validate_resume_id(cls, v):
        if not v or not v.strip():
            raise ValueError("Resume ID cannot be empty")
        return v.strip()
    
    @validator("description")
    def validate_description(cls, v):
        if len(v.strip()) < 50:
            raise ValueError("Job description must be at least 50 characters")
        return v


@router.post("/analyseresume")
async def analyse_resume(request: Request, req_body: AnalyseResumeRequest):

    user = request.state.user
    
    api_key = GROQ_API_KEY
    if not api_key:
        logger.error("GROQ_API_KEY not configured")
        raise APIError(
            error_code=ErrorCode.MISSING_API_KEY,
            internal_message="GROQ_API_KEY environment variable is not set"
        )
    
    try:
        resume_service = JobMatchingService(
            api_key=api_key, 
            resume_id=req_body.resume_id, 
            description=req_body.description,
            use_rag=req_body.use_rag
        )
        analysis_result = resume_service.analyze()
        
        return success_response(
            message="Resume analysis completed successfully",
            data=analysis_result,
            status_code=200
        )
        
    except APIError:
        
        raise
    except ValueError as e:
        logger.warning(f"Validation error during analysis: {str(e)}")
        raise APIError(
            error_code=ErrorCode.INVALID_JOB_DESCRIPTION,
            internal_message=str(e)
        )
    except Exception as e:
        logger.error(f"Analysis failed for resume {req_body.resume_id}", exc_info=True)
        raise APIError(
            error_code=ErrorCode.ANALYSIS_FAILED,
            internal_message=str(e)
        )