from langchain_groq import ChatGroq
from utils.apierror import APIError
import json


class AnalysisAnswer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            groq_api_key=api_key,
            temperature=0.7
        )

    def score_answer(self, question: str, answer: str, job_context: str = "") -> dict:
        """Score answer out of 5 with feedback"""
        try:
            prompt = f"""You are an expert interview coach scoring a candidate's answer.

Job Context: {job_context}
Question: {question}
Answer: {answer}

Evaluate the answer and respond ONLY with valid JSON (no other text) in this format:
{{
    "score": (0-5 integer),
    "feedback": "Brief feedback on the answer"
}}

Scoring guide:
5 = Excellent answer, directly addresses question, shows strong understanding
4 = Good answer, mostly correct, minor gaps
3 = Adequate answer, covers basics but lacks depth
2 = Weak answer, missing key points
1 = Poor answer, mostly irrelevant
0 = No answer or completely off-topic"""
            
            response = self.llm.invoke(prompt)
            
            # Parse JSON response
            try:
                result = json.loads(response.content.strip())
                score = min(5, max(0, int(result.get("score", 0))))  # Clamp 0-5
                feedback = result.get("feedback", "No feedback provided")
                return {"score": score, "feedback": feedback}
            except json.JSONDecodeError:
                # Fallback if LLM doesn't return valid JSON
                return {"score": 3, "feedback": response.content.strip()}
                
        except Exception as e:
            raise APIError(
                status_code=500,
                message=str(e),
                error_code="ANSWER_SCORING_FAILED"
            )

    def batch_analyze_and_score(self, questions: list, answers: list, job_context: str = "") -> dict:
        """Analyze and score all 2 answers, return total out of 10"""
        try:
            if len(questions) != len(answers):
                raise APIError(
                    status_code=400,
                    message="Number of questions and answers must match",
                    error_code="MISMATCHED_QA"
                )
            
            results = []
            total_score = 0
            
            for question, answer in zip(questions, answers):
                scored = self.score_answer(question, answer, job_context)
                results.append({
                    "question": question,
                    "answer": answer,
                    "score": scored["score"],
                    "feedback": scored["feedback"]
                })
                total_score += scored["score"]
            
            return {
                "question_answers": results,
                "total_score": total_score,  # Out of 50
                "average_score": round(total_score / len(questions), 2),
                "percentage": round((total_score / 50) * 100, 2)
            }
        except APIError:
            raise
        except Exception as e:
            raise APIError(
                status_code=500,
                message=str(e),
                error_code="BATCH_ANALYSIS_FAILED"
            )

            
            