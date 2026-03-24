from fastapi import APIRouter, Depends
from utils.apiresponse import success_response,error_response
from Models.resumeservice.resume_models import Resume_data
from middlewares.auth_middleware import verify_jwt



router=APIRouter(
    prefix="/api",
    tags=["Resume Delete"]
)


@router.delete("/delete-resume/{resume_id}")
async def delete_resume(resume_id:str, user=Depends(verify_jwt)):
    try:
        resume=Resume_data.objects(id=resume_id).first()
        if not resume:
            return error_response(
                message="Resume Not Found",
                error_code="NOT_FOUND",
                status_code=404
            )
        
        # Verify the resume belongs to the authenticated user
        if str(resume.user.id) != str(user.id):
            return error_response(
                message="Unauthorized - Resume does not belong to you",
                error_code="UNAUTHORIZED",
                status_code=403
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