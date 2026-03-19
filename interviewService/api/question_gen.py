from fastapi import APIRouter
from interviewService.loader.get_data import InterviewDataLoader
from utils.apierror import APIError
from Models.resumeservice.resume_models import Resume_data

import os
from interviewService.QuestionGenService.Questiongen import QuestionGen

router = APIRouter(
    prefix="/question_gen",
    tags=["question_gen"],
    responses={404: {"description": "Not found"}},
)


@router.post("/generate")
async def generate_questions(description: str, resume_id: str):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise APIError(status_code=400, message="API key is required", error_code="MISSING_API_KEY")
    
    if not resume_id:
        raise APIError(status_code=400, message="Resume ID is required", error_code="MISSING_RESUME_ID")
    
    if not description:
        raise APIError(status_code=400, message="Job description is required", error_code="MISSING_DESCRIPTION")
    
    resume = Resume_data.objects(id=resume_id).first()
    if not resume:
        raise APIError(status_code=404, message=f"Resume with ID {resume_id} not found", error_code="RESUME_NOT_FOUND")
    
    try:
        data_loader = InterviewDataLoader()
        context = data_loader.extract_job_info(description, api_key=api_key, resume_id=resume_id)
        
        question_gen = QuestionGen(api_key=api_key)
        questions = question_gen.generate_questions(context)
        
        return {"questions": questions}
    
    except APIError:
        raise
    except Exception as e:
        raise APIError(status_code=500, message=str(e), error_code="QUESTION_GEN_ERROR")



