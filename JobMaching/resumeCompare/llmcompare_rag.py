"""
RAG-based comparison of resume and job description using LLM analysis
"""

import re
from utils.apierror import APIError
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from JobMaching.Rag.prepare_data.rag_data import RagData


class RagLlmCompare:
    """
    RAG-based comparison of resume and job description
    - Uses ChatGroq for LLM analysis
    - Supports both LLM-only and Hybrid RAG modes
    - Handles errors gracefully with detailed logging
    """
    
    def __init__(self, api_key: str, resume_data: dict, job_description: str):
        """
        Initialize RAG LLM comparator
        
        Args:
            api_key: Groq API key
            resume_data: Resume data dictionary
            job_description: Job description text
        """
        self.api_key = api_key
        self.resume_data = resume_data
        self.job_description = job_description
        self.llm = ChatGroq(model="openai/gpt-oss-120b", api_key=self.api_key)
    
    def _format_docs(self, docs):
        """Format retrieved documents into string for LLM"""
        return "\n\n".join([doc.page_content for doc in docs])
    
    def compare(self) -> dict:
        """
        Compare resume against job description using RAG + LLM
        
        Returns:
            Analysis results with score, strengths, weaknesses, suggestions
        """
        try:
            # Prepare RAG data - stores only resume in FAISS
            rag_data = RagData(
                job_description=self.job_description,
                resume_data=self.resume_data
            )
            retriever = rag_data.prepare_for_rag()
            
            # Define prompt template with job description and retrieved resume context
            prompt = PromptTemplate.from_template(
                """You are an expert career coach AI helping job seekers understand resume-job fit.
                
                CRITICAL INSTRUCTION: First, determine if the "Full Job Description" is a genuine job posting. If it consists of random gibberish (e.g. "suyduGVGWE", random characters) or makes no sense, you MUST immediately return a SCORE of 0, ELIGIBLE of NO, and state that the input is invalid gibberish in the suggestions. Do NOT hallucinate a match!
                
                Retrieved Resume Sections:
                {context}
                
                Full Job Description:
                {job_description}
                
                Analyze how well the resume matches the job and provide structured feedback.
                
                RETURN FORMAT (EACH ON OWN LINE):
                SCORE: <Replace with integer 0-100>
                ELIGIBLE: <Replace with YES, PARTIAL, or NO>
                EXPERIENCE_FIT: <Replace with integer 0-100>
                SKILLS_MATCH: <Replace with integer 0-100>
                STRENGTHS: <Replace with 1 to 5 actual strengths, separated by pipe | character>
                MISSING_SKILLS: <Replace with 1 to 5 actual missing skills, separated by pipe | character>
                SUGGESTIONS:
                1. <Replace with first actionable suggestion>
                2. <Replace with second actionable suggestion>
                (and so on...)
                """
            )
            
            
            rag_chain = (
                {
                    "context": retriever | self._format_docs,
                    "job_description": RunnablePassthrough()
                }
                | prompt
                | self.llm
            )
            
           
            result = rag_chain.invoke(self.job_description)
            
           
            analysis = self._parse_response(result.content)
            return analysis
            
        except Exception as e:
            raise APIError(
                status_code=500,
                message=f"RAG-LLM comparison failed: {str(e)}",
                error_code="RAG_LLM_COMPARISON_FAILED"
            )
    
    def _parse_response(self, response_text: str) -> dict:
        """
        Parse LLM response into structured format
        
        Args:
            response_text: Raw LLM response
            
        Returns:
            Parsed analysis dictionary
        """
        result = {
            "overallScore": 0,
            "eligible": "NO",
            "experienceFit": 0,
            "skillsMatch": 0,
            "strengths": [],
            "missingSkills": [],
            "suggestions": []
        }
        
        try:
            # Extract score
            score_match = re.search(r"SCORE:\s*(\d+)", response_text, re.IGNORECASE)
            if score_match:
                result["overallScore"] = int(score_match.group(1))
            
            # Extract eligible status
            eligible_match = re.search(r"ELIGIBLE:\s*(YES|PARTIAL|NO)", response_text, re.IGNORECASE)
            if eligible_match:
                result["eligible"] = eligible_match.group(1).upper()
            
            # Extract experience fit
            exp_match = re.search(r"EXPERIENCE_FIT:\s*(\d+)", response_text, re.IGNORECASE)
            if exp_match:
                result["experienceFit"] = int(exp_match.group(1))
            
            # Extract skills match
            skills_match = re.search(r"SKILLS_MATCH:\s*(\d+)", response_text, re.IGNORECASE)
            if skills_match:
                result["skillsMatch"] = int(skills_match.group(1))
            
            # Extract strengths - pipe separated
            strengths_match = re.search(r"STRENGTHS:\s*([^\n]+)", response_text, re.IGNORECASE)
            if strengths_match:
                strengths_text = strengths_match.group(1).strip()
                result["strengths"] = [s.strip() for s in strengths_text.split("|") if s.strip()][:5]
            
            # Extract missing skills - pipe separated
            missing_match = re.search(r"MISSING_SKILLS:\s*([^\n]+)", response_text, re.IGNORECASE)
            if missing_match:
                missing_text = missing_match.group(1).strip()
                result["missingSkills"] = [s.strip() for s in missing_text.split("|") if s.strip()][:5]
            
            # Extract suggestions - numbered list
            suggestions_match = re.search(r"SUGGESTIONS:\s*(.*?)$", response_text, re.IGNORECASE | re.DOTALL)
            if suggestions_match:
                suggestions_text = suggestions_match.group(1).strip()
                # Find all numbered items
                numbered = re.findall(r'^\d+[\.\)]\s+(.+?)$', suggestions_text, re.MULTILINE)
                result["suggestions"] = [s.strip() for s in numbered if s.strip()][:5]
            
            return result
            
        except Exception as e:
            return result
        
        
        
        
        
        
        