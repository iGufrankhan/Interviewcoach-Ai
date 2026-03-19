import os
from fastapi import APIRouter, UploadFile, File
from utils.apierror import APIError
from utils.apiresponse import success_response, error_response
from ResumeService.services.resumeservice import ResumeService
from ResumeService.utils.file_validators import validate_file_extension
from ResumeService.repository.resume_datasave import save_resume

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
async def upload_resume(user_id: str, file: UploadFile = File(...)):
    """Upload and process resume for a user"""
    
    # Validate file extension
    if not validate_file_extension(file.filename):
        return error_response(
            message="Invalid file type. Allowed types are: pdf, docx, txt",
            error_code="INVALID_FILE_TYPE",
            status_code=400
        )
    
     
    try:
        # Initialize ResumeService with user_id
        resume_service = ResumeService(
            upload_dir="uploads",
            groq_api_key=groq_api_key,
            user_id=user_id
        )
        
        # Process resume (extracts data)
        processed_data = resume_service.process_resume(file)
        
        # Save to database
        resume_result = save_resume(processed_data, user_id)
        
        return success_response(
            message="Resume uploaded and saved successfully",
            data=resume_result,
            status_code=201
        )
    
    except APIError as e:
        return error_response(
            message=e.detail,
            error_code=e.error_code,
            status_code=e.status_code
        )
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="PROCESSING_ERROR",
            status_code=500
        )


