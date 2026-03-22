from fastapi import APIRouter, Depends
from utils.apiresponse import success_response,error_response
from Models.resumeservice.resume_models import Resume_data
from middlewares.auth_middleware import verify_jwt


router=APIRouter(
    prefix="/api",
    tags=["Get Resume Data"]
)


@router.get("/resume/{resume_id}")
async def get_resume(resume_id:str, user=Depends(verify_jwt)):
    try:
        resume=Resume_data.objects(id=resume_id).first()
        if not resume:
            return error_response(
                message="Resume Not Found",
                error_code=" NOT_FOUND",
                status_code=404
            )
        resume_dict = resume.to_mongo()
        resume_dict["id"] = str(resume_dict.pop("_id"))
        if "created_at" in resume_dict:
            resume_dict["created_at"] = resume_dict["created_at"].isoformat()
        return success_response(
            message="Resume found",
            data=resume_dict,
            status_code=200
        )
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="GET_ERROR",
            status_code=500
        )
            
           