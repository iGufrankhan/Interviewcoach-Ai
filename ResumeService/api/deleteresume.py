from fastapi import APIRouter, Request
from utils.apiresponse import success_response,error_response
from Models.resumeservice.resume_models import Resume_data



router=APIRouter(
    tags=["Resume Delete"]
)


@router.delete("/delete-resume/{resume_id}")
async def delete_resume(resume_id:str, request: Request):
    from bson import ObjectId
    user = request.state.user
    try:
        # Convert resume_id string to ObjectId
        try:
            resume_oid = ObjectId(resume_id)
        except:
            return error_response(
                message="Invalid resume ID format",
                error_code="INVALID_RESUME_ID",
                status_code=400
            )
        
        resume = await Resume_data.async_find_one(id=resume_oid)
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
        
        await Resume_data.async_delete(id=resume_oid)
        return success_response(
            message="Resume deleted successfully",
            data={"resume_id": str(resume_id)},
            status_code=200
        )
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="DELETE_ERROR",
            status_code=500
        )