from utils.apierror import APIError
from JobMaching.loader.job_descpLoad import JobDescriptionLoader
from Models.resumeservice.resume_models import Resume_data



class CompareService:
    
    def __init__(self, api_key: str, resume_id: str, description: str):
        self.api_key = api_key
        self.resume_id = resume_id
        self.description = description
        self.job_loader = JobDescriptionLoader()
    
    def get_data(self):
        if not self.description:
            raise APIError(status_code=400, message="Job description is required", error_code="MISSING_DESCRIPTION")
        
       
        try:
            resume_doc = Resume_data.objects(id=self.resume_id).first()
            if resume_doc is None:
                raise APIError(status_code=400, message=f"Resume not found for ID: {self.resume_id}", error_code="RESUME_NOT_FOUND")
            
            resume_data = {
                "name": resume_doc.name,
                "skills": resume_doc.skills,
                "experience": resume_doc.experience,
                "education": resume_doc.education,
                "projects": resume_doc.projects
            }
        except Exception as e:
            raise APIError(status_code=400, message=f"Failed to load resume data: {str(e)}", error_code="RESUME_LOADING_FAILED")
        
        job_data = self.job_loader.load_job_description(self.description)
        
        if job_data is None:
            raise APIError(status_code=400, message="Failed to load job description data", error_code="JOB_DESCRIPTION_LOADING_FAILED")
        
        return resume_data, job_data
        
        
        
        
       
    
     