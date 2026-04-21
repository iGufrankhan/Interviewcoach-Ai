import os
from fastapi import APIRouter, Request
from interviewService.loader.get_data import InterviewDataLoader
from interviewService.QuestionGenService.Questiongen import QuestionGen
from utils.apierror import APIError
from utils.error_codes import ErrorCode
from utils.apiresponse import success_response
from Models.resumeservice.resume_models import Resume_data

router = APIRouter(
    tags=["question_gen"],
    responses={404: {"description": "Not found"}},
)


@router.post("/generate-questions")
async def generate_questions(description: str, resume_id: str, request: Request):
    """Generate interview questions based on job description and resume."""
    user = request.state.user
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise APIError(
            error_code=ErrorCode.MISSING_API_KEY,
            internal_message="GROQ_API_KEY environment variable not set"
        )
    
    if not resume_id:
        raise APIError(error_code=ErrorCode.INVALID_RESUME_ID)
    
    if not description or len(description.strip()) < 50:
        raise APIError(error_code=ErrorCode.INVALID_JOB_DESCRIPTION)
    
    resume = Resume_data.objects(id=resume_id).first()
    if not resume:
        raise APIError(
            error_code=ErrorCode.RESUME_NOT_FOUND,
            message=f"Resume with ID {resume_id} not found"
        )
    
    try:
        data_loader = InterviewDataLoader()
        context = data_loader.extract_job_info(description, api_key=api_key, resume_id=resume_id)
        
        question_gen = QuestionGen(api_key=api_key)
        questions = question_gen.generate_questions(context)
        
        return success_response(
            message="Interview questions generated successfully",
            data={"questions": questions},
            status_code=200
        )
    
    except APIError:
        raise
    except Exception as e:
        raise APIError(
            error_code=ErrorCode.QUESTION_GENERATION_FAILED,
            internal_message=str(e)
        )



