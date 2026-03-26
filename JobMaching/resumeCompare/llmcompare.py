import re
from utils.apierror import APIError
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

class jobDescriptionAnalyzer:
    
    def __init__(self, api_key: str, resume_data: dict, job_description: str):
        self.resume_data = resume_data
        self.job_description = job_description
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=api_key,
            temperature=0
        )

        self.prompt_template = """You are a professional recruiter. Analyze the candidate's resume against the job description and provide a comprehensive assessment.

RESUME:
{resume_data}

JOB DESCRIPTION:
{job_description}

ANALYSIS TASK:
1. Extract MUST-HAVE requirements from job description
2. Compare resume against requirements
3. Provide actionable feedback

SCORING (0-100):
- 90-100: Excellent fit
- 70-89: Good fit
- 50-69: Moderate fit
- 30-49: Poor fit
- 0-29: Very poor fit

RETURN FORMAT (EACH ON ITS OWN LINE):
Score: [0-100]
Eligible: [YES/PARTIAL/NO]
Strengths: [strength 1] | [strength 2] | [strength 3] | [strength 4] | [strength 5]
Weaknesses: [weakness 1] | [weakness 2] | [weakness 3] | [weakness 4] | [weakness 5]
Suggestions:
1. [First specific actionable suggestion for improvement]
2. [Second specific actionable suggestion for improvement]
3. [Third specific actionable suggestion for improvement]
4. [Fourth specific actionable suggestion for improvement]
5. [Fifth specific actionable suggestion for improvement]"""
    
    def analyze(self):
        self.prompt = PromptTemplate(
            input_variables=["resume_data", "job_description"],
            template=self.prompt_template
        )
        
        final_prompt = self.prompt.format(resume_data=self.resume_data, job_description=self.job_description)
        response = self.llm.invoke(final_prompt)
        content = response.content.strip()
        
        score_match = re.search(r"Score:\s*(\d{1,3})", content)
        if score_match:
            score = int(score_match.group(1))
            score = max(0, min(score, 100))
        else:
            raise ValueError("Could not extract score from response.")
        
        eligible_match = re.search(r"Eligible:\s*(YES|PARTIAL|NO)", content, re.IGNORECASE)
        eligible = eligible_match.group(1).upper() if eligible_match else "UNKNOWN"
        
        # Extract strengths - pipe separated
        strengths_match = re.search(r"Strengths:\s*([^\n]+)", content)
        strengths = self._parse_pipe_separated(strengths_match.group(1)) if strengths_match else []
        
        # Extract weaknesses - pipe separated
        weaknesses_match = re.search(r"Weaknesses:\s*([^\n]+)", content)
        missing_skills = self._parse_pipe_separated(weaknesses_match.group(1)) if weaknesses_match else []
        
        # Extract suggestions - numbered list
        suggestions_match = re.search(r"Suggestions:\s*(.*?)(?:^[A-Z]|\Z)", content, re.MULTILINE | re.DOTALL)
        suggestions = self._parse_numbered_suggestions(suggestions_match.group(1)) if suggestions_match else []
        
        experience_fit = max(0, min(100, int(score * 1.1)))
        skills_match = score
        
        return {
            "overallScore": score,
            "experienceFit": experience_fit,
            "skillsMatch": skills_match,
            "eligible": eligible,
            "strengths": strengths,
            "missingSkills": missing_skills,
            "suggestions": suggestions
        }
    
    def _parse_pipe_separated(self, text: str) -> list:
        """Parse pipe-separated items and return as list (max 5 items)"""
        if not text or text.strip() == "":
            return []
        
        # Split by pipe
        items = text.split('|')
        
        cleaned_items = []
        for item in items:
            cleaned = item.strip()
            if cleaned and len(cleaned) > 3:
                cleaned_items.append(cleaned)
        
        return cleaned_items[:5]
    
    def _parse_numbered_suggestions(self, text: str) -> list:
        """Parse numbered suggestions (1., 2., etc.) and return as list (max 5 items)"""
        if not text or text.strip() == "":
            return []
        
        # Find all numbered items like "1. suggestion text" or "1) suggestion text"
        pattern = r'^\d+[\.\)]\s+(.+?)$'
        matches = re.findall(pattern, text, re.MULTILINE)
        
        cleaned_items = []
        for match in matches:
            cleaned = match.strip()
            if cleaned and len(cleaned) > 5:
                cleaned_items.append(cleaned)
        
        return cleaned_items[:5]