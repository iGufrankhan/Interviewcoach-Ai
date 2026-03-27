from mongoengine import Document, ReferenceField, ListField, StringField, IntField, FloatField, DateTimeField, DictField
from datetime import datetime
from Models.userReg.user import User


class InterviewSession(Document):
    """Store complete interview session with all Q&A and scores"""
    meta = {'collection': 'interview_sessions'}
    
    user = ReferenceField(User, required=True)
    job_title = StringField(required=True)
    job_description = StringField(required=True)
    resume_id = StringField(required=True)
    
    questions = ListField(StringField())  # All 10 questions
    answers = ListField(StringField())  # All 10 answers (audio or text)
    
    # Scoring: list of dicts with score and feedback for each answer
    question_answers = ListField(DictField(), default=list)  # [{question, answer, score, feedback}, ...]
    
    total_score = FloatField(default=0)  # Out of 10
    status = StringField(default="in_progress", choices=["in_progress", "completed"])  # Track if interview finished
    
    created_at = DateTimeField(default=datetime.now)
    completed_at = DateTimeField()
    
    def add_question_answer(self, question: str, answer: str, score: float = 0, feedback: str = ""):
        """Add a question-answer pair with score and feedback"""
        self.question_answers.append({
            "question": question,
            "answer": answer,
            "score": score,
            "feedback": feedback
        })
        self.save()
    
    def calculate_total_score(self):
        """Calculate total score after all answers are scored"""
        if not self.question_answers:
            return 0
        
        total = sum(item.get("score", 0) for item in self.question_answers)
        self.total_score = total
        self.status = "completed"
        self.completed_at = datetime.now()
        self.save()
        return total
    
    def get_average_score(self):
        """Get average score per question"""
        if not self.question_answers:
            return 0
        return self.total_score / len(self.question_answers)
