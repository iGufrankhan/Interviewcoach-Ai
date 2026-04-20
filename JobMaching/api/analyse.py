from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from JobMaching.analyser.resumeanalise import JobMatchingService
from utils.apierror import APIError
import os

router = APIRouter(
    tags=["Resume Analysis"]
)

class AnalyseResumeRequest(BaseModel):
    """Resume analysis request model"""
    resume_id: str = Field(..., description="Resume ID to analyze")
    description: str = Field(..., description="Job description text")
    use_rag: bool = Field(
        default=True, 
        description="Use Hybrid RAG system (True) or LLM-only (False)"
    )

@router.post("/analyseresume")
async def analyse_resume(request: Request, req_body: AnalyseResumeRequest):
    """
    Analyze resume against job description
    
    Protected route - requires JWT authentication (handled by middleware)
    
    Supports two modes:
    - Hybrid RAG (use_rag=True): Combines FAISS semantic search + LLM analysis for better accuracy
    - LLM-only (use_rag=False): Traditional LLM-based comparison
    
    Returns:
    - overallScore: 0-100 match score
    - eligible: YES/PARTIAL/NO
    - For hybrid mode: combines retrieverScore and llmScore
    """
    # User already authenticated by middleware
    user = request.state.user
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise APIError(status_code=500, message="GROQ_API_KEY environment variable is not set", error_code="MISSING_API_KEY")
    
    if not req_body.resume_id:
        raise APIError(status_code=400, message="resume_id is required", error_code="MISSING_RESUME_ID")
    
    if not req_body.description:
        raise APIError(
            status_code=400, 
            message="description is required. Provide the job description text.",
            error_code="MISSING_DESCRIPTION"
        )
    
    try:
        resume_service = JobMatchingService(
            api_key=api_key, 
            resume_id=req_body.resume_id, 
            description=req_body.description,
            use_rag=req_body.use_rag
        )
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

    