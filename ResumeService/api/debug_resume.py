from fastapi import APIRouter, Request
from utils.apiresponse import success_response, error_response
from Models.resumeservice.resume_models import Resume_data
from Models.userReg.user import User
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Debug Resume"]
)


@router.get("/debug/resume-status")
async def debug_resume_status(request: Request):
    """Debug endpoint to check resume data and user references
    - Shows authenticated user info
    - Lists all resumes in database
    - Shows user references in each resume
    """
    try:
        # Get authenticated user
        user = request.state.user
        logger.info(f"DEBUG: Authenticated user - email: {user.email}, id: {user.id}")
        
        # Find user by email (same as get endpoint does)
        user_by_email = await User.async_find_one(email=user.email)
        logger.info(f"DEBUG: User.async_find_one(email={user.email}) returned: {user_by_email}")
        if user_by_email:
            logger.info(f"   ID: {user_by_email.id}")
        
        # Get all resumes (no filter)
        all_resumes = await Resume_data.async_find_all()
        logger.info(f"DEBUG: Total resumes in database: {len(all_resumes)}")
        
        resumes_info = []
        for resume in all_resumes:
            resume_dict = {
                "resume_id": str(resume.id),
                "name": resume.name,
                "user_reference": str(resume.user.id) if resume.user else "None",
                "user_email": resume.user.email if resume.user else "None",
                "created_at": str(resume.created_at),
            }
            resumes_info.append(resume_dict)
            logger.info(f"   Resume: {resume_dict}")
        
        # Try to find resumes for this specific user
        resumes_for_user = await Resume_data.async_find_all(user=user)
        logger.info(f"DEBUG: Resume_data.async_find_all(user=request.state.user) returned {len(resumes_for_user)} resumes")
        
        resumes_for_user_by_email = await Resume_data.async_find_all(user=user_by_email)
        logger.info(f"DEBUG: Resume_data.async_find_all(user=user_by_email) returned {len(resumes_for_user_by_email)} resumes")
        
        # Count check
        total_count = await Resume_data.async_count(user=user)
        total_count_by_email = await Resume_data.async_count(user=user_by_email)
        logger.info(f"DEBUG: async_count(user=request.state.user) = {total_count}")
        logger.info(f"DEBUG: async_count(user=user_by_email) = {total_count_by_email}")
        
        return success_response(
            message="Debug info retrieved",
            data={
                "authenticated_user": {
                    "email": user.email,
                    "id": str(user.id),
                },
                "user_by_email_lookup": {
                    "email": user_by_email.email if user_by_email else None,
                    "id": str(user_by_email.id) if user_by_email else None,
                    "found": user_by_email is not None,
                },
                "all_resumes": resumes_info,
                "resumes_for_current_user": len(resumes_for_user),
                "resumes_for_user_by_email": len(resumes_for_user_by_email),
                "count_current_user": total_count,
                "count_user_by_email": total_count_by_email,
                "user_id_match": str(user.id) == str(user_by_email.id) if user_by_email else False,
            },
            status_code=200
        )
        
    except Exception as e:
        logger.error(f"Debug endpoint error: {str(e)}", exc_info=True)
        return error_response(
            message=f"Debug error: {str(e)}",
            error_code="DEBUG_ERROR",
            status_code=500
        )
