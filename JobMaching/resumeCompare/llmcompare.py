import re
from utils.apierror import APIError
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

class jobDescriptionAnalyzer:
    
    def __init__(self, api_key: str, resume_data: dict, job_description: str):
        self.resume_data = resume_data
        self.job_description = job_description
        self.llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            groq_api_key=api_key,
            temperature=0
        )

        self.prompt_template = """You are a professional recruiter. Analyze the candidate's resume against the job description and provide a comprehensive assessment.

RESUME:
{resume_data}

JOB DESCRIPTION:
{job_description}

ANALYSIS TASK:
1. Extract MUST-HAVE requirements from job description (critical requirements)
2. Extract NICE-TO-HAVE requirements (preferred but not critical)
3. Compare resume against these requirements
4. Assess eligibility and provide actionable feedback

SCORING (0-100):
- 90-100: Excellent fit (has almost all must-haves)
- 70-89: Good fit (has most must-haves, some nice-to-haves)
- 50-69: Moderate fit (has key must-haves, missing some)
- 30-49: Poor fit (missing several must-haves)
- 0-29: Very poor fit (major gaps in must-haves)

RETURN FORMAT (EXACTLY):
Score: [0-100]
Eligible: [YES/PARTIAL/NO]
Strengths: [2-3 bullet points of what resume has that matches job]
Weaknesses: [2-3 bullet points of key missing skills/experience]
Suggestions: [2-3 actionable recommendations to improve candidacy]"""
    
    def analyze(self):
        self.prompt = PromptTemplate(
            input_variables=["resume_data", "job_description"],
            template=self.prompt_template
        )
        
        final_prompt = self.prompt.format(resume_data=self.resume_data, job_description=self.job_description)
        response = self.llm.invoke(final_prompt)
        content = response.content.strip()
        
        # Parse Score
        score_match = re.search(r"Score:\s*(\d{1,3})", content)
        if score_match:
            score = int(score_match.group(1))
            score = max(0, min(score, 100))
        else:
            raise ValueError("Could not extract score from response.")
        
        # Parse Eligible
        eligible_match = re.search(r"Eligible:\s*(YES|PARTIAL|NO)", content, re.IGNORECASE)
        eligible = eligible_match.group(1).upper() if eligible_match else "UNKNOWN"
        
        # Parse Strengths
        strengths_match = re.search(r"Strengths:\s*(.*?)(?=Weaknesses:|$)", content, re.DOTALL)
        strengths = strengths_match.group(1).strip() if strengths_match else "Not specified"
        
        # Parse Weaknesses
        weaknesses_match = re.search(r"Weaknesses:\s*(.*?)(?=Suggestions:|$)", content, re.DOTALL)
        weaknesses = weaknesses_match.group(1).strip() if weaknesses_match else "Not specified"
        
        # Parse Suggestions
        suggestions_match = re.search(r"Suggestions:\s*(.*?)$", content, re.DOTALL)
        suggestions = suggestions_match.group(1).strip() if suggestions_match else "Not specified"
        
        return {
            "score": score,
            "eligible": eligible,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggestions": suggestions
        }
    
    