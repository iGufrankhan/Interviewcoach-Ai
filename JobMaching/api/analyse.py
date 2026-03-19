import os
from fastapi import APIRouter
from JobMaching.analyser.resumeanalise import JobMatchingService
from utils.apierror import APIError

router = APIRouter(
    prefix="/api",
    tags=["Resume Analysis"]
)

@router.post("/analyseresume")
async def analyse_resume(resume_id: str, description: str):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise APIError(status_code=500, message="GROQ_API_KEY environment variable is not set", error_code="MISSING_API_KEY")
    
    if not resume_id:
        raise APIError(status_code=400, message="resume_id is required", error_code="MISSING_RESUME_ID")
    
    if not description:
        raise APIError(
            status_code=400, 
            message="description is required. Provide the job description text.",
            error_code="MISSING_DESCRIPTION"
        )
    
    try:
        resume_service = JobMatchingService(api_key, resume_id, description)
        analysis_result = resume_service.analyze()
        return {"status": "success", "data": analysis_result}
    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(
            status_code=400, 
            message=str(e) + " (Use 'description' parameter to paste job description directly for better results)",
            error_code="ANALYSIS_FAILED"
        )
    
    