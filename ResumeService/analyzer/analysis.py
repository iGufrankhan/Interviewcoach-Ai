import json
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

MAX_RETRIES = 3

class ResumeAnalyzer:

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

Extract the following information from the resume text below.

Return ONLY valid JSON in this exact format (no extra text):
{{
  "name": "Full Name",
  "skills": ["skill1", "skill2", "skill3"],
  "experience": ["Job Title at Company (Duration) - Description", "..."],
  "education": ["Degree, Institution, Year - Details", "..."],
  "projects": ["Project Name - Full description with tech stack and details", "..."]
}}

Rules:
- Each experience entry should include job title, company, duration, and key responsibilities.
- Each education entry should include degree, institution, year, and relevant coursework if available.
- Each project entry should include project name, tech stack, and a full description of what was built.
- If a section is not found, use an empty list [].
- Return ONLY the JSON object, nothing else.

Resume Text:
{resume_text}
"""
        )

    def analyze(self, text: str) -> dict:
        final_prompt = self.prompt.format(resume_text=text)

        for attempt in range(MAX_RETRIES):
            response = self.llm.invoke(final_prompt)
            content = response.content.strip()
            parsed = self._parse_json_response(content)

            if self._is_valid(parsed):
                return parsed

        raise ValueError(
            "Could not extract complete resume data. Please try again or upload a clearer resume."
        )

    def _parse_json_response(self, text: str) -> dict:
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        return {
            "name": "",
            "skills": [],
            "experience": [],
            "education": [],
            "projects": []
        }

    def _is_valid(self, data: dict) -> bool:
        if not data.get("name"):
            return False
        if not data.get("skills"):
            return False
        if not data.get("experience") and not data.get("education") and not data.get("projects"):
            return False
        return True

