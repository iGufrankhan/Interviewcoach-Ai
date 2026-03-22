from Models.resumeservice.resume_models import Resume_data
from Models.resumeservice.resumeschema import create_resume_schema
from Models.userReg.user import User
from utils.apierror import APIError
import logging

logger = logging.getLogger(__name__)

def save_resume(resume_data, user_id):
    """Saves the structured resume data to the database."""
    try:
        logger.info(f"💾 Saving resume for user: {user_id}")
        logger.info(f"   Resume data keys: {resume_data.keys() if isinstance(resume_data, dict) else 'N/A'}")
        
        # user_id is now the email (from JWT token)
        user = User.objects(email=user_id).first()
        
        if not user:
            logger.error(f"❌ User not found: {user_id}")
            raise APIError(
                status_code=404,
                message="User not found",
                error_code="USER_NOT_FOUND"
            )
        
        logger.info(f"✅ User found: {user.email}")
        logger.info(f"   Creating Resume_data object...")
        
        resume_doc = Resume_data(
            user=user,
            name=resume_data.get("name", ""),
            skills=_ensure_list(resume_data.get("skills")),
            experience=_ensure_list(resume_data.get("experience")),
            education=_ensure_list(resume_data.get("education")),
            projects=_ensure_list(resume_data.get("projects")),
        )
        logger.info(f"   Resume object created, saving to database...")
        resume_doc.save()
        logger.info(f"✅ Resume saved successfully with ID: {resume_doc.id}")
        return create_resume_schema(resume_doc)
    
    except APIError:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to save resume: {str(e)}", exc_info=True)
        raise APIError(
            status_code=500,
            message=f"Failed to save resume: {str(e)}",
            error_code="SAVE_ERROR"
        )


def get_resume_by_id(resume_id):
    """Fetch resume by ID"""
    try:
        resume = Resume_data.objects(id=resume_id).first()
        if not resume:
            raise APIError(
                status_code=404,
                message="Resume not found",
                error_code="RESUME_NOT_FOUND"
            )
        return create_resume_schema(resume)
    except APIError:
        raise
    except Exception as e:
        raise APIError(
            status_code=500,
            message="Failed to fetch resume",
            error_code="FETCH_ERROR"
        )


def get_user_resumes(user_id):
    """Fetch all resumes for a user"""
    try:
        # user_id is now the email (from JWT token)
        user = User.objects(email=user_id).first()
        if not user:
            raise APIError(
                status_code=404,
                message="User not found",
                error_code="USER_NOT_FOUND"
            )
        
        resumes = Resume_data.objects(user=user)
        return [create_resume_schema(r) for r in resumes]
    except APIError:
        raise
    except Exception as e:
        raise APIError(
            status_code=500,
            message="Failed to fetch user resumes",
            error_code="FETCH_ERROR"
        )


def _ensure_list(value):
    """Convert value to list"""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]