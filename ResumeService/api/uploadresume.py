import os
from fastapi import APIRouter, UploadFile, File
from utils.apierror import APIError
from utils.apiresponse import success_response, error_response
from ResumeService.services.resumeservice import ResumeService
from ResumeService.utils.file_validators import validate_file_extension

router = APIRouter()

if not os.getenv("GROQ_API_KEY"):
    raise APIError(status_code=500, message="GROQ_API_KEY environment variable not set", error_code="MISSING_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize ResumeService
resume_service = ResumeService(
    upload_dir="uploads",
    groq_api_key=groq_api_key
    
)


@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    # Validate file extension
    if not validate_file_extension(file.filename):
        return error_response(
            message="Invalid file type. Allowed types are: pdf, docx, txt",
            error_code="INVALID_FILE_TYPE",
            status_code=400
        )

    try:
        result = resume_service.process_resume(file)
        return success_response(
            message="Resume processed successfully",
            data=result,
            status_code=200
        )
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="PROCESSING_ERROR",
            status_code=500
        )









