import os
import logging
from fastapi import APIRouter, UploadFile, File, Depends
from utils.apierror import APIError
from utils.apiresponse import success_response, error_response
from ResumeService.services.resumeservice import ResumeService
from ResumeService.utils.file_validators import validate_file_extension
from ResumeService.repository.resume_datasave import get_user_resumes
from middlewares.auth_middleware import verify_jwt

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Resume Upload"]
)

if not os.getenv("GROQ_API_KEY"):
    raise APIError(
        status_code=500, 
        message="GROQ_API_KEY environment variable not set", 
        error_code="MISSING_API_KEY"
    )

groq_api_key = os.getenv("GROQ_API_KEY")


@router.post("/upload-resume/{user_id}")
async def upload_resume(user_id: str, file: UploadFile = File(...), user=Depends(verify_jwt)):
    """Upload and process resume for a user - Requires authentication"""
    
    # Use authenticated user's email, not URL parameter (security measure)
    actual_user_id = user.email
    logger.info(f"📤 Resume upload started")
    logger.info(f"   Authenticated user email: {actual_user_id}")
    logger.info(f"   URL parameter user_id: {user_id}")
    logger.info(f"   File name: {file.filename}")
    logger.info(f"   File size: {file.size if file.size else 'unknown'} bytes")
    logger.info(f"   Content type: {file.content_type}")
    
    # Validate file extension
    if not validate_file_extension(file.filename):
        logger.warning(f"❌ Invalid file type: {file.filename}")
        return error_response(
            message="Invalid file type. Allowed types are: pdf, docx, txt",
            error_code="INVALID_FILE_TYPE",
            status_code=400
        )
    
    logger.info("✅ File extension validated")
     
    try:
        # Initialize ResumeService with authenticated user's email
        logger.info("🔧 Initializing ResumeService...")
        resume_service = ResumeService(
            upload_dir="uploads",
            groq_api_key=groq_api_key,
            user_id=actual_user_id
        )
        logger.info("✅ ResumeService initialized")
        
        # Process resume (extracts data)
        logger.info("⚙️  Processing resume...")
        processed_data = resume_service.process_resume(file)
        logger.info(f"✅ Resume processed and saved successfully")
        logger.debug(f"   Processed data keys: {processed_data.keys() if isinstance(processed_data, dict) else 'N/A'}")
        
        return success_response(
            message="Resume uploaded and saved successfully",
            data=processed_data,
            status_code=201
        )
    
    except APIError as e:
        logger.error(f"❌ APIError during resume upload: {e.detail}")
        error_code = e.detail.get("error_code", "API_ERROR") if isinstance(e.detail, dict) else "API_ERROR"
        error_msg = e.detail.get("error", str(e.detail)) if isinstance(e.detail, dict) else str(e.detail)
        return error_response(
            message=error_msg,
            error_code=error_code,
            status_code=e.status_code
        )
    except Exception as e:
        logger.error(f"❌ Unexpected error during resume upload: {str(e)}", exc_info=True)
        return error_response(
            message=str(e),
            error_code="PROCESSING_ERROR",
            status_code=500
        )
