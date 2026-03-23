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
        strengths_text = strengths_match.group(1).strip() if strengths_match else "Not specified"
        strengths = self._parse_bullet_points(strengths_text)
        
        # Parse Weaknesses (Missing Skills)
        weaknesses_match = re.search(r"Weaknesses:\s*(.*?)(?=Suggestions:|$)", content, re.DOTALL)
        weaknesses_text = weaknesses_match.group(1).strip() if weaknesses_match else "Not specified"
        missing_skills = self._parse_bullet_points(weaknesses_text)
        
        # Parse Suggestions
        suggestions_match = re.search(r"Suggestions:\s*(.*?)$", content, re.DOTALL)
        suggestions_text = suggestions_match.group(1).strip() if suggestions_match else "Not specified"
        suggestions = self._parse_bullet_points(suggestions_text)
        
        # Calculate component scores (percentages of overall score)
        experience_fit = max(0, min(100, int(score * 1.1)))  # Slightly weighted
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
    
    def _parse_bullet_points(self, text: str) -> list:
        """Parse bullet points from text and return as list (max 5 items)"""
        if not text or text == "Not specified":
            return []
        
        # Split by common bullet point markers and newlines
        points = re.split(r'[\n•\-*]', text)
        
        # Clean up: remove empty strings and items that are just numbers
        cleaned_points = []
        for p in points:
            cleaned = p.strip()
            # Skip empty strings and items that are just numbers (like "1.", "2.", etc.)
            if cleaned and not re.match(r'^\d+\.?$', cleaned):
                cleaned_points.append(cleaned)
        
        # Limit to 5 items maximum
        return cleaned_points[:5] if cleaned_points else []