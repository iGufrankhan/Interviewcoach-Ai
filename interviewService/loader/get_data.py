
#  get data from resume and job description
from Models.resumeservice.resume_models import Resume_data
from JobMaching.loader.job_descpLoad import JobDescriptionLoader
from utils.apierror import APIError




class InterviewDataLoader:
    
    def extract_job_info(self, job_description: str, api_key: str, resume_id: str) -> str:
        try:
            job_loader = JobDescriptionLoader()
            job_info = job_loader.load_job_description(job_description)
            
            resume_doc = Resume_data.objects(id=resume_id).first()
            if resume_doc is None:
                raise APIError(status_code=400, message=f"Resume not found for ID: {resume_id}", error_code="RESUME_NOT_FOUND")
            
            resume_data = {
                "name": resume_doc.name,    
                "skills": resume_doc.skills,
                "experience": resume_doc.experience,
                "education": resume_doc.education,
                "projects": resume_doc.projects
            }
            
            return join_resume_with_job_info(job_info, resume_data)
        
        except Exception as e:
            raise APIError(status_code=400, message=f"Failed to extract job information: {str(e)}", error_code="JOB_INFO_EXTRACTION_FAILED")
        
        
        
def join_resume_with_job_info(job_info: str, resume_data: dict) -> str:
    """
    Joins job and resume info with clear section markers for LLM clarity
    """
    if not job_info or not job_info.strip():
        raise APIError(
            status_code=400,
            message="Job description is empty",
            error_code="EMPTY_JOB_INFO"
        )
    
    joined_data = f"""==================== JOB INFORMATION ====================
{job_info}

==================== CANDIDATE RESUME ====================
"""
    
    for key, value in resume_data.items():
        if value:
            joined_data += f"{key.upper()}: {value}\n"
    
    joined_data += "\n" + "=" * 60
    return joined_data


            
            
            
        
        
        
            
            
            
            