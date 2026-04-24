from fastapi import APIRouter, Request, Query
from utils.apiresponse import success_response,error_response
from utils.apierror import APIError
from Models.resumeservice.resume_models import Resume_data
from Models.userReg.user import User

router=APIRouter(
    tags=["Get Resume Data"]
)


@router.get("/user-resumes")
async def get_user_resumes(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page (1-100)")
):
    """Get paginated resumes for authenticated user"""
    try:
        # Use authenticated user's email
        user = request.state.user
        actual_user_email = user.email
        
        user_obj = await User.async_find_one(email=actual_user_email)
        if not user_obj:
            raise APIError(status_code=404, message="User not found", error_code="USER_NOT_FOUND")
        
        total = await Resume_data.async_count(user=user_obj)
        
        if total == 0:
            return success_response(
                message="No resumes found for this user",
                data={
                    "resumes": [],
                    "pagination": {
                        "page": page,
                        "limit": limit,
                        "total": 0,
                        "total_pages": 0
                    }
                },
                status_code=200
            )
        
        skip = (page - 1) * limit
        resumes = await Resume_data.async_find(skip=skip, limit=limit, user=user_obj)
        
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
            data={
                "resumes": resumes_list,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "total_pages": (total + limit - 1) // limit
                }
            },
            status_code=200
        )
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="GET_USER_RESUMES_ERROR",
            status_code=500
        )

@router.get("/resume/{resume_id}")
async def get_resume(resume_id:str, request: Request):
    user = request.state.user
    try:
        resume = await Resume_data.async_find_one(id=resume_id)
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