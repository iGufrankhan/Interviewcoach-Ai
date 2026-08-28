import httpx
import asyncio
import os
import json
from groq import Groq
import logging
from Models.resumeservice.resume_models import Resume_data
from utils.apierror import APIError

logger = logging.getLogger(__name__)

class AgenticSearchService:
    def __init__(self):
        self.groq_api_key = os.environ.get("GROQ_API_KEY")
        self.adzuna_app_id = os.environ.get("ADZUNA_APP_ID")
        self.adzuna_app_key = os.environ.get("ADZUNA_APP_KEY")
        
        if not self.groq_api_key or not self.adzuna_app_id or not self.adzuna_app_key:
            raise APIError(
                error_code="MISSING_API_KEY",
                message="API keys not configured.",
                internal_message="Missing Groq or Adzuna API keys."
            )
            
        self.client = Groq(api_key=self.groq_api_key)

    async def _fetch_resume_text(self, user) -> str:
        resumes = await Resume_data.async_find(user=user)
        if not resumes:
            raise APIError(
                error_code="NO_RESUME",
                message="Please upload a resume first.",
                status_code=400
            )
        
        user_resume = sorted(resumes, key=lambda x: x.created_at, reverse=True)[0]
        
        skills = ", ".join(user_resume.skills) if user_resume.skills else "None"
        experience = ", ".join(user_resume.experience) if user_resume.experience else "None"
        education = ", ".join(user_resume.education) if user_resume.education else "None"
        projects = ", ".join(user_resume.projects) if user_resume.projects else "None"
        
        return f"Skills: {skills}\nExperience: {experience}\nEducation: {education}\nProjects: {projects}"

    async def _analyze_single_job(self, resume_text: str, job: dict) -> dict:
        prompt = f"""
        You are an expert technical recruiter AI.
        Compare this RESUME to this JOB DESCRIPTION. 
        You MUST output valid JSON exactly in this format: {{"match_score": <integer between 0 and 100>, "missing_skills": ["skill1", "skill2"]}}
        
        RESUME: 
        {resume_text[:2000]}
        
        JOB DESCRIPTION: 
        {job.get('description', '')}
        """
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a JSON-only API. You must return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                model="openai/gpt-oss-120b", 
                response_format={"type": "json_object"}
            )
            analysis = json.loads(response.choices[0].message.content)
            
            job['match_score'] = analysis.get('match_score', 0)
            job['missing_skills'] = analysis.get('missing_skills', [])
            return job
        except Exception as e:
            logger.error(f"Groq error during job analysis: {e}")
            job['match_score'] = 0
            job['missing_skills'] = []
            return job

    async def search_and_match(self, target_role: str, user) -> list:
        resume_text = await self._fetch_resume_text(user)
        
        api_url = f"https://api.adzuna.com/v1/api/jobs/us/search/1"
        querystring = {
            "app_id": self.adzuna_app_id,
            "app_key": self.adzuna_app_key,
            "what": target_role,
            "results_per_page": 4, 
        }

        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(api_url, params=querystring)
            response.raise_for_status()
            data = response.json()
            raw_jobs = data.get('results', [])
            
            tasks = [self._analyze_single_job(resume_text, job) for job in raw_jobs]
            analyzed_jobs = await asyncio.gather(*tasks)
            
            analyzed_jobs.sort(key=lambda x: x['match_score'], reverse=True)

            formatted_jobs = [{
                "job_title": job.get('title'),
                "company_name": job.get('company', {}).get('display_name'),
                "job_description": job.get('description'),
                "apply_url": job.get('redirect_url'),
                "match_score": job.get('match_score'),
                "missing_skills": job.get('missing_skills')
            } for job in analyzed_jobs]
            
            return formatted_jobs
