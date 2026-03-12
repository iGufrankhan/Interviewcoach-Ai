from fastapi import APIRouter
from utils.apiresponse import success_response,error_response
from Models.resumeservice.resume_models import Resume_data



router=APIRouter(
    prefix="/api",
    tags=["Resume Delete"]
)


@router.delete("/resume/{resume_id}")
async def delete_resume(resume_id:str):
    try:
        resume=Resume_data.objects(id=resume_id).first()
        if not resume:
            return error_response(
                message="Resume Not Found",
                error_code=" NOT_FOUND",
                status_code=404
            )
        resume.delete()
        return success_response(
            message="Resume deleted successfully",
            data={"id": str(resume_id)},
            status_code=200
        )
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="DELETE_ERROR",
            status_code=500
        )