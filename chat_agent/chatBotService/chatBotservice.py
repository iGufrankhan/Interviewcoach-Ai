from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from Models.chat_bot.chat_bot import ChatSession, ChatMessage
from Models.resumeservice.resume_models import Resume_data
from Models.userReg.user import User
from datetime import datetime
from utils.apierror import APIError


class ChatBotService:
    
    def __init__(self, api_key: str, user_email: str):
        self.api_key = api_key
        self.user_email = user_email
        self.store = {}
        
        self.llm = ChatGroq(
            groq_api_key=api_key,
            model="llama-3.1-8b-instant"
        )
    
    def get_user_resume(self) -> dict:
        """Fetch user's resume data from MongoDB"""
        try:
            user = User.objects(email=self.user_email).first()
            if not user:
                return {}
            
            resume = Resume_data.objects(user=user).first()
            if not resume:
                return {}
            
            return {
                "name": resume.name or "Not provided",
                "skills": resume.skills or [],
                "experience": resume.experience or [],
                "education": resume.education or [],
                "projects": resume.projects or []
            }
        except Exception as e:
            print(f"Error fetching resume: {e}")
            return {}
        
    def validate_session_ownership(self, session_id: str) -> bool:
        """Verify user owns this session"""
        try:
            session = ChatSession.objects(id=session_id).first()
            if not session:
                return False
            return session.email == self.user_email
        except Exception as e:
            print(f"Error validating session: {e}")
            return False
    
    def create_session(self, title: str = "New Chat"):
        new_session = ChatSession(   
            user_id=self.user_email,
            email=self.user_email,
            title=title
        )
        new_session.save()
        return str(new_session.id)
   
    def get_session_history(self, session: str) -> BaseChatMessageHistory:
        """Get or create session history, loading from MongoDB if exists"""
        if session not in self.store:
            # Create new history object
            history = ChatMessageHistory()
            
            # Load existing messages from MongoDB
            messages = ChatMessage.objects(session_id=session).order_by('timestamp')
            for msg in messages:
                if msg.role == 'user':
                    history.add_user_message(msg.content)
                elif msg.role == 'assistant':
                    history.add_ai_message(msg.content)
            
            # Cache in memory
            self.store[session] = history
        
        return self.store[session]
    
    def send_message(self, session_id: str, message: str):
        # Save user message to MongoDB
        msg = ChatMessage(
            session_id=session_id,
            role='user',
            content=message
        )
        msg.save()
        
        # Clear cache to force reload from MongoDB
        if session_id in self.store:
            del self.store[session_id]
        
        # Get fresh session history from MongoDB
        session_history = self.get_session_history(session_id)
        
        # Fetch user's resume data
        resume = self.get_user_resume()
        
        # Format resume data for context
        resume_context = self._format_resume_context(resume)
        
        # Build prompt with resume context
        system_prompt = f"""You are Interview Coach AI. Help with resumes, interviews, and career advice.

User's Profile Information:
{resume_context}

Use this information to provide personalized advice tailored to the user's background, skills, and experience."""
        
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        question_answer_chain = (
            qa_prompt
            | self.llm
            | StrOutputParser()
        )
        
        # Conversational chain with memory
        conversational_chain = RunnableWithMessageHistory(
            question_answer_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        
        # Invoke
        response = conversational_chain.invoke(
            {"input": message},
            config={"configurable": {"session_id": session_id}},
        )
        
        # Save AI response to MongoDB
        ai_msg = ChatMessage(
            session_id=session_id,
            role='assistant',
            content=response
        )
        ai_msg.save()
        
        return response
    
    def _format_resume_context(self, resume: dict) -> str:
        """Format resume data into a readable context string"""
        if not resume:
            return "No resume data available."
        
        lines = []
        
        if resume.get("name"):
            lines.append(f"Name: {resume['name']}")
        
        if resume.get("skills"):
            skills_text = ", ".join(resume["skills"])
            lines.append(f"Skills: {skills_text}")
        
        if resume.get("education"):
            lines.append("Education:")
            for edu in resume["education"]:
                lines.append(f"  - {edu}")
        
        if resume.get("experience"):
            lines.append("Experience:")
            for exp in resume["experience"]:
                lines.append(f"  - {exp}")
        
        if resume.get("projects"):
            lines.append("Projects:")
            for proj in resume["projects"]:
                lines.append(f"  - {proj}")
        
        return "\n".join(lines) if lines else "No resume details available."
    
    def get_all_sessions(self) -> list:
        """Get all chat sessions for user"""
        sessions = ChatSession.objects(email=self.user_email).order_by('-updated_at')
        return [
            {
                "id": str(s.id),
                "title": s.title,
                "created_at": s.created_at.isoformat(),
                "updated_at": s.updated_at.isoformat()
            }
            for s in sessions
        ]




















