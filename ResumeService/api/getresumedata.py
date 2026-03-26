from fastapi import APIRouter, Depends
from utils.apiresponse import success_response,error_response
from Models.resumeservice.resume_models import Resume_data
from Models.userReg.user import User
from middlewares.auth_middleware import verify_jwt

router=APIRouter(
    prefix="/api",
    tags=["Get Resume Data"]
)


@router.get("/user-resumes")
async def get_user_resumes(user=Depends(verify_jwt)):
    """Get all resumes for the authenticated user"""
    try:
        # Use authenticated user's email
        actual_user_email = user.email
        
        # Find user by email
        user_obj = User.objects(email=actual_user_email).first()
        if not user_obj:
            return success_response(
                message="No resumes found for this user",
                data=[],
                status_code=200
            )
        
        # Query by user reference
        resumes = Resume_data.objects(user=user_obj)
        
        if not resumes:
            return success_response(
                message="No resumes found for this user",
                data=[],
                status_code=200
            )
        
        resumes_list = []
        for resume in resumes:
            resume_dict = resume.to_mongo()
            resume_dict["resume_id"] = str(resume_dict.pop("_id"))
            # Convert user ObjectId to string
            if "user" in resume_dict:
                resume_dict["user_id"] = str(resume_dict["user"])
                resume_dict.pop("user")
            resume_dict["email"] = user_obj.email
            if "created_at" in resume_dict:
                resume_dict["created_at"] = resume_dict["created_at"].isoformat()
            resumes_list.append(resume_dict)
        
        return success_response(
            message="Resumes found",
            data=resumes_list,
            status_code=200
        )
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="GET_USER_RESUMES_ERROR",
            status_code=500
        )

@router.get("/resume/{resume_id}")
async def get_resume(resume_id:str, user=Depends(verify_jwt)):
    try:
        resume=Resume_data.objects(id=resume_id).first()
        if not resume:
            return error_response(
                message="Resume Not Found",
                error_code="RESUME_NOT_FOUND",
                status_code=404
            )
        resume_dict = resume.to_mongo()
        resume_dict["id"] = str(resume_dict.pop("_id"))
        # Convert user ObjectId to string
        if "user" in resume_dict:
            resume_dict["user_id"] = str(resume_dict["user"])
            resume_dict.pop("user")
        resume_dict["email"] = resume.user.email
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