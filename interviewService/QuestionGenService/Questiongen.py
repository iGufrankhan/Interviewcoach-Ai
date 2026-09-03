from langchain_groq import ChatGroq
from utils.apierror import APIError

from langchain_core.prompts import PromptTemplate



class QuestionGen:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def generate_questions(self, context):
        
        try:
            
            prompt="""You are an interview coach generating interview questions for a specific job application.

**CRITICAL INSTRUCTIONS:**
1. Look for the section marked "==================== JOB INFORMATION ===================="
2. Extract: role, required skills, experience level, responsibilities, qualifications
3. Generate 10 UNIQUE questions based ONLY on this job description
4. Use the CANDIDATE RESUME section only to:
   - Create follow-up questions if resume shows skill mismatches
   - Ask about relevant experience from the candidate's background
   - Bridge gaps between job requirements and candidate's resume

**Question Guidelines:**
- Each question MUST be directly relevant to the job posting
- Questions should assess:
  * Technical competency for the role
  * Experience with required tools/technologies
  * Relevant past work examples
  * Ability to handle job responsibilities
- Format: numbered list (1. Question here, 2. Question here, ... 10. Question here)
- Only return the 10 numbered questions - no explanations, preamble, or additional text

CONTEXT:
{context}
            """ 
            llm = ChatGroq(
                groq_api_key=self.api_key,
                model_name="openai/gpt-oss-120b",
                temperature=0.7,
                max_tokens=2048
            )
            
            prompt_template = PromptTemplate(
                input_variables=["context"],
                template=prompt
            )
            final_prompt = prompt_template.format(context=context)
            response = llm.invoke(final_prompt)
            
            import re
            lines = response.content.strip().split("\n")
            questions = []
            for line in lines:
                line = line.strip()
                # Match 1., 1), - , *, or **1.** followed by text
                match = re.search(r'^\s*(?:(?:\*\*)?\d+[\.\)](?:\*\*)?|-|\*)\s*(.*)', line)
                if match:
                    question = match.group(1).strip()
                    if question:
                        questions.append(question)
            
            # Fallback if no questions matched the format but we have text
            if not questions and lines:
                questions = [l.strip() for l in lines if len(l.strip()) > 15][:10]
                
            return questions[:10]
        except Exception as e:
            raise APIError(status_code=500, message=str(e), error_code="QUESTION_GENERATION_FAILED")
        
            
            
            
            
           