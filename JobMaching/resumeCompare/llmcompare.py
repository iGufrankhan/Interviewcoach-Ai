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

        self.prompt_template = """You are an AI assistant. I provide you data of my resume like my name, skills, experience, projects, education.
       I will provide you with a job description and you will compare it with my resume data and give me a score out of 100 based on how well my resume matches the job description.
       
       Resume Data:
       {resume_data}
       
       Job Description:
       {job_description}
       
       The score should be based on the following criteria:
       1. Skills Match (40 points): How many of the required skills in the job description are present in the resume.
       2. Experience Match (30 points): How well the candidate's experience aligns with the job requirements, including relevant job titles, companies, and durations.
       3. Education Match (20 points): How well the candidate's educational background matches the job requirements, including degrees, institutions, and graduation years.
       4. Project Match (10 points): How well the candidate's projects align with the job description, including relevance and complexity.
       
       Return the response in this format:
       Score: [number between 0 and 100]
       Explanation: [brief explanation of the score in 2-3 sentences, highlighting key strengths and weaknesses]"""
    
    def analyze(self):
        self.prompt = PromptTemplate(
            input_variables=["resume_data", "job_description"],
            template=self.prompt_template
        )
        
        final_prompt = self.prompt.format(resume_data=self.resume_data, job_description=self.job_description)
        response = self.llm.invoke(final_prompt)
        content = response.content.strip()
        
        score_match = re.search(r"Score:\s*(\d{1,3})", content)
        explanation_match = re.search(r"Explanation:\s*(.*)", content, re.DOTALL)

        if score_match:
            score = int(score_match.group(1))
            # Set minimum score of 10
            score = max(score, 10)
        else:
            raise ValueError("Could not extract a valid score from the response.")

        explanation = explanation_match.group(1).strip() if explanation_match else "No explanation provided."

        return {"score": score, "explanation": explanation}
    
    