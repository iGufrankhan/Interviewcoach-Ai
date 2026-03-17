import os
from fastapi import APIRouter
from JobMaching.analyser.resumeanalise import JobMatchingService
from utils.apierror import APIError

router = APIRouter(
    prefix="/api",
    tags=["Resume Analysis"]
)

@router.post("/analyseresume")
async def analyse_resume(resume_id: str, description: str = None, job_url: str = None):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise APIError(status_code=500, message="GROQ_API_KEY environment variable is not set", error_code="MISSING_API_KEY")
    
    if not resume_id:
        raise APIError(status_code=400, message="resume_id is required", error_code="MISSING_RESUME_ID")
    
    # Validate that at least one input is provided
    if not job_url and not description:
        raise APIError(status_code=400, message="Provide either job_url or description", error_code="MISSING_INPUT")
    
    # If both provided, prioritize URL
    if job_url and description:
        description = None
    
    try:
        resume_service = JobMatchingService(api_key, resume_id, description, job_url)
        analysis_result = resume_service.analyze()
        return {"status": "success", "data": analysis_result}
    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(status_code=400, message=str(e), error_code="ANALYSIS_FAILED")
    
    