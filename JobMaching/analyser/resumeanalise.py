
"""
Job Matching Service with Hybrid RAG support
"""

from utils.apierror import APIError
from JobMaching.loader.getterdata import CompareService
from JobMaching.resumeCompare.llmcompare import jobDescriptionAnalyzer
from JobMaching.resumeCompare.llmcompare_rag import RagLlmCompare


class JobMatchingService:
    """
    Job matching service supporting both LLM-only and Hybrid RAG modes
    """
    
    def __init__(self, api_key: str, resume_id: str, description: str, use_rag: bool = True):
        """
        Initialize job matching service
        
        Args:
            api_key: Groq API key
            resume_id: Resume ID to analyze
            description: Job description
            use_rag: Use hybrid RAG system (True) or LLM-only (False)
        """
        if not api_key:
            raise APIError(status_code=500, message="GROQ_API_KEY environment variable is not set", error_code="MISSING_API_KEY")
        
        self.api_key = api_key
        self.resume_id = resume_id
        self.description = description
        self.use_rag = use_rag
    
    def analyze(self):
        """
        Perform resume-job matching analysis
        
        Returns:
            Analysis results with score, eligibility, insights
        """
        try:
            compare_service = CompareService(self.api_key, self.resume_id, self.description)
            self.resume_data, self.job_description = compare_service.get_data()
            
            if self.resume_data is None:
                raise APIError(status_code=400, message="Failed to load resume data", error_code="RESUME_LOADING_FAILED")
            if self.job_description is None:
                raise APIError(status_code=400, message="Failed to load job description data", error_code="JOB_DESCRIPTION_LOADING_FAILED")
            
           
            if self.use_rag:
                return self._hybrid_analysis()
            else:
                return self._llm_only_analysis()
                
        except APIError:
            raise
        except Exception as e:
            raise APIError(
                status_code=500,
                message=f"Analysis failed: {str(e)}",
                error_code="ANALYSIS_FAILED"
            )
    
    def _llm_only_analysis(self):
        """
        Traditional LLM-only analysis
        
        Returns:
            LLM analysis results
        """
        analyzer = jobDescriptionAnalyzer(self.api_key, self.resume_data, self.job_description)
        result = analyzer.analyze()
        result["analysisMethod"] = "llm_only"
        return result
    
    def _hybrid_analysis(self):
        """
        Hybrid RAG analysis combining retriever + LLM
        
        Returns:
            Hybrid analysis results
        """
        try:
            rag_analyzer = RagLlmCompare(
                api_key=self.api_key,
                resume_data=self.resume_data,
                job_description=self.job_description
            )
            result = rag_analyzer.compare()
            result["analysisMethod"] = "hybrid_rag"
            return result
            
        except Exception as e:
            # Fallback to LLM-only if RAG fails
            return self._llm_only_analysis()
        

   