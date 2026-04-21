import os
from fastapi import APIRouter, UploadFile, File, Request
from utils.apierror import APIError
from utils.apiresponse import success_response
from utils.error_codes import ErrorCode
from ResumeService.services.resumeservice import ResumeService
from ResumeService.utils.file_validators import validate_file_extension

router = APIRouter(
    tags=["Resume Upload"]
)

if not os.getenv("GROQ_API_KEY"):
    raise APIError(
        error_code=ErrorCode.MISSING_API_KEY,
        internal_message="GROQ_API_KEY environment variable not set"
    )

groq_api_key = os.getenv("GROQ_API_KEY")


@router.post("/upload-resume")
async def upload_resume(request: Request, file: UploadFile = File(...)):
    """Upload and process resume for authenticated user - Requires authentication"""
    
    # Use authenticated user's email
    user = request.state.user
    actual_user_email = user.email
    
    # Validate file extension
    if not validate_file_extension(file.filename):
        raise APIError(
            error_code=ErrorCode.INVALID_FILE_TYPE,
            message="Invalid file type. Allowed types are: PDF, DOCX, or TXT"
        )
    
    try:
        # Initialize ResumeService with authenticated user's email
        resume_service = ResumeService(
            upload_dir="uploads",
            groq_api_key=groq_api_key,
            user_id=actual_user_email
        )
        
        # Process resume (extracts data)
        processed_data = resume_service.process_resume(file)
        
        return success_response(
            message="Resume uploaded and saved successfully",
            data=processed_data,
            status_code=201
        )
    
    except APIError:
        raise
    except Exception as e:
        raise APIError(
            error_code=ErrorCode.RESUME_PROCESSING_FAILED,
            internal_message=str(e)
        )
        