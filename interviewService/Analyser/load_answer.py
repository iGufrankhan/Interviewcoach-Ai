from interviewService.anwerService import AnswerService

class load_answer:
    

    
    def load_answers_from_audio(self):
        answer_service = AnswerService()
        answer = answer_service.get_answer_from_audio()
        return answer
    
    def load_answers_from_text(self,text :str):
        answer_service = AnswerService()
        answer = answer_service.get_answer_from_text(text)
        return answer
    
    def store_answer(self, answer: str):
        answer_service = AnswerService()
        answer_service.store_answer(answer)
        
    
    
        