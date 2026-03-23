import os
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from JobMaching.analyser.resumeanalise import JobMatchingService
from utils.apierror import APIError
from middlewares.auth_middleware import verify_jwt

router = APIRouter(
    prefix="/api",
    tags=["Resume Analysis"]
)

class AnalyseResumeRequest(BaseModel):
    resume_id: str
    description: str

@router.post("/analyseresume")
async def analyse_resume(request: AnalyseResumeRequest, user=Depends(verify_jwt)):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise APIError(status_code=500, message="GROQ_API_KEY environment variable is not set", error_code="MISSING_API_KEY")
    
    if not request.resume_id:
        raise APIError(status_code=400, message="resume_id is required", error_code="MISSING_RESUME_ID")
    
    if not request.description:
        raise APIError(
            status_code=400, 
            message="description is required. Provide the job description text.",
            error_code="MISSING_DESCRIPTION"
        )
    
    try:
        resume_service = JobMatchingService(api_key, request.resume_id, request.description)
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
    