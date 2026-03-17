
from utils.apierror import APIError
from JobMaching.resumeCompare.getterdata import CompareService
from JobMaching.resumeCompare.llmcompare import jobDescriptionAnalyzer


class JobMatchingService:
    def __init__(self, api_key: str, resume_id: str, description: str = None, job_url: str = None):
        if not api_key:
            raise APIError(status_code=500, message="GROQ_API_KEY environment variable is not set", error_code="MISSING_API_KEY")
        
        self.api_key = api_key
        self.resume_id = resume_id
        self.description = description
        self.job_url = job_url
    
    def analyze(self):
        compare_service = CompareService(self.api_key, self.resume_id, self.description, self.job_url)
        self.resume_data, self.job_description = compare_service.get_data()
        
        if self.resume_data is None:
            raise APIError(status_code=400, message="Failed to load resume data", error_code="RESUME_LOADING_FAILED")
        if self.job_description is None:
            raise APIError(status_code=400, message="Failed to load job description data", error_code="JOB_DESCRIPTION_LOADING_FAILED")
        
        analyzer = jobDescriptionAnalyzer(self.api_key, self.resume_data, self.job_description)
        return analyzer.analyze()
        

   