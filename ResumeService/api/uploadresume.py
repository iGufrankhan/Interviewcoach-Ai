from fastapi import APIRouter, UploadFile, File, Request
from utils.apierror import APIError
from utils.apiresponse import success_response
from utils.error_codes import ErrorCode
from utils.constant import GROQ_API_KEY, MAX_FILE_UPLOAD_SIZE
from ResumeService.services.resumeservice import ResumeService
from ResumeService.utils.file_validators import validate_file_extension
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Resume Upload"]
)

if not GROQ_API_KEY:
    raise APIError(
        error_code=ErrorCode.MISSING_API_KEY,
        internal_message="GROQ_API_KEY environment variable not set"
    )

groq_api_key = GROQ_API_KEY


@router.post("/upload-resume")
async def upload_resume(request: Request, file: UploadFile = File(...)):
    """Upload and process resume for authenticated user - Requires authentication"""
    
    # Use authenticated user's email
    user = request.state.user
    actual_user_email = user.email
    
    # Validate file size
    if file.size is None:
        logger.warning(f"File size is None for upload by {actual_user_email}")
    elif file.size > MAX_FILE_UPLOAD_SIZE:
        logger.warning(
            f"File upload rejected: size {file.size} bytes exceeds limit {MAX_FILE_UPLOAD_SIZE}",
            extra={"user": actual_user_email, "filename": file.filename}
        )
        raise APIError(
            error_code=ErrorCode.INVALID_INPUT,
            message=f"File size exceeds maximum allowed size ({MAX_FILE_UPLOAD_SIZE / (1024*1024):.1f}MB)",
            internal_message=f"Upload rejected: {file.filename} is {file.size} bytes"
        )
    
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
        