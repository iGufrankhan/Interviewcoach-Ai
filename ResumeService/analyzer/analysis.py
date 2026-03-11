import json
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate


class ResumeAnalyzer:
    """
    Uses an LLM to extract structured information from resume text.
    """

    def __init__(self, api_key: str):
        self.llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            groq_api_key=api_key,
            temperature=0
        )

        self.prompt = PromptTemplate(
            input_variables=["resume_text"],
            template="""
You are an AI resume parser.

Extract the following information from the resume:

1. Name
2. Skills
3. Experience
4. Education
5. Projects

Return ONLY raw text in the following  format:
name: <name>
skills: <comma separated skills>
experience: <experience details>
education: <education details>
projects: <project details>


Resume Text:
{resume_text}
"""
        )




    def analyze(self, text: str) -> dict:
        """
        Analyze resume text using LLM and return structured data.
        """

        final_prompt = self.prompt.format(resume_text=text)

        response = self.llm.invoke(final_prompt)

        content = response.content
        

        content = self.parse_resume_text(content)

        return content
    
    
    def parse_resume_text(self, text: str) -> dict:
        """
        Parse the raw text response from the LLM into structured dictionary.
        """

        result = {}
        lines = text.splitlines()

        for line in lines:

            if ':' not in line:
                continue

            key, value = line.split(':', 1)

            key = key.strip().lower()
            value = value.strip()

            # split skills and projects
            if key == "skills":
                result[key] = [s.strip().lower() for s in value.split(",") if s.strip()]

            else:
                result[key] = value
                
           
        return result
    
