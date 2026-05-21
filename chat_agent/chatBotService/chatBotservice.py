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
from datetime import datetime, timedelta
from utils.apierror import APIError
from typing import List, Dict, Optional


class ChatBotService:
    
    def __init__(self, api_key: str, user_email: str):
        self.api_key = api_key
        self.user_email = user_email
        self.store = {}  # In-memory session cache
        self.resume_cache = None  # Resume data cache
        self.resume_cache_time = None  # Cache timestamp
        self.cache_ttl = 300  # Cache for 5 minutes
        
        self.llm = ChatGroq(
            groq_api_key=api_key,
            model="llama-3.1-8b-instant"
        )
    
    async def get_user_resume(self) -> dict:
        """Fetch user's resume data from MongoDB with caching (5 min TTL)"""
        # Check cache
        if self.resume_cache is not None and self.resume_cache_time is not None:
            time_elapsed = (datetime.now() - self.resume_cache_time).total_seconds()
            if time_elapsed < self.cache_ttl:
                return self.resume_cache
        
        try:
            user = await User.async_find_one(email=self.user_email)
            if not user:
                self.resume_cache = {}
                self.resume_cache_time = datetime.now()
                return {}
            
            resume = await Resume_data.async_find_one(user=user)
            if not resume:
                self.resume_cache = {}
                self.resume_cache_time = datetime.now()
                return {}
            
            resume_data = {
                "name": resume.name or "Not provided",
                "skills": resume.skills or [],
                "experience": resume.experience or [],
                "education": resume.education or [],
                "projects": resume.projects or []
            }
            
            # Cache the result
            self.resume_cache = resume_data
            self.resume_cache_time = datetime.now()
            
            return resume_data
        except Exception as e:
            return {}
        
    async def validate_session_ownership(self, session_id: str) -> bool:
        """Verify user owns this session"""
        try:
            session = await ChatSession.async_find_one(id=session_id)
            if not session:
                return False
            return session.email == self.user_email
        except Exception as e:
            return False
    
    async def search_messages(self, keywords: List[str], session_id: Optional[str] = None, limit: int = 5) -> List[Dict]:
        """Search messages in MongoDB by keywords"""
        try:
            query = {}
            if session_id:
                query["session_id"] = session_id
            else:
                query["email"] = self.user_email
            
            messages = await ChatMessage.async_find(limit=limit, **query)
            
            return [
                {
                    "id": str(msg.id),
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat(),
                    "session_id": str(msg.session_id)
                }
                for msg in messages
            ]
        except Exception as e:
            return []
    
    async def get_relevant_context(self, session_id: str, message: str, limit: int = 3) -> str:
        """Retrieve relevant conversation context from MongoDB based on recent messages"""
        try:
            messages = await ChatMessage.async_find(session_id=session_id, limit=limit * 2)
            
            context_lines = []
            for msg in reversed(messages):
                role_label = "User" if msg.role == 'user' else "Assistant"
                context_lines.append(f"{role_label}: {msg.content}")
            
            return "\n".join(context_lines) if context_lines else ""
        except Exception as e:
            return ""
    
    async def get_session_stats(self, session_id: str) -> Dict:
        """Get conversation statistics for a session"""
        try:
            messages = await ChatMessage.async_find(session_id=session_id)
            user_messages = [m for m in messages if m.role == 'user']
            ai_messages = [m for m in messages if m.role == 'assistant']
            
            session = await ChatSession.async_find_one(id=session_id)
            
            return {
                "total_messages": len(messages),
                "user_messages": len(user_messages),
                "ai_messages": len(ai_messages),
                "created_at": session.created_at.isoformat() if session else None,
                "updated_at": session.updated_at.isoformat() if session else None,
                "session_duration": self._calculate_duration(session) if session else None
            }
        except Exception as e:
            return {}
    
    def _calculate_duration(self, session) -> str:
        """Calculate session duration"""
        duration = session.updated_at - session.created_at
        hours = duration.total_seconds() / 3600
        minutes = (duration.total_seconds() % 3600) / 60
        return f"{int(hours)}h {int(minutes)}m"
    
    async def create_session(self, title: str = "New Chat"):
        """Create a new chat session"""
        try:
            new_session = ChatSession(   
                user_id=self.user_email,
                email=self.user_email,
                title=title
            )
            await new_session.async_save()
            return str(new_session.id)
        except Exception as e:
            raise APIError(status_code=500, message="Failed to create session", error_code="SESSION_CREATE_ERROR")
   
    async def get_session_history(self, session: str) -> BaseChatMessageHistory:
        """Get or create session history, loading from MongoDB if exists"""
        if session not in self.store:
            # Create new history object
            history = ChatMessageHistory()
            
            # Load existing messages from MongoDB
            messages = await ChatMessage.async_find(session_id=session, limit=1000)
            for msg in messages:
                if msg.role == 'user':
                    history.add_user_message(msg.content)
                elif msg.role == 'assistant':
                    history.add_ai_message(msg.content)
            
            # Cache in memory
            self.store[session] = history
        
        return self.store[session]
    
    async def send_message(self, session_id: str, message: str):
        # Validate session ownership
        if not await self.validate_session_ownership(session_id):
            raise APIError(status_code=403, message="Unauthorized access to session", error_code="UNAUTHORIZED")
        
        # Save user message to MongoDB
        msg = ChatMessage(
            session_id=session_id,
            role='user',
            content=message
        )
        await msg.async_save()
        
        # Pre-load session history from MongoDB (populates self.store cache)
        await self.get_session_history(session_id)
        
        # Create sync getter that returns from cache
        def get_session_history_sync(session_id: str):
            if session_id not in self.store:
                self.store[session_id] = ChatMessageHistory()
            return self.store[session_id]
        
        # Get cached session history
        session_history = get_session_history_sync(session_id)
        session_history.add_user_message(message)
        
        # Fetch user's resume data (uses cache with TTL)
        resume = await self.get_user_resume()
        
        # Format resume data for context
        resume_context = self._format_resume_context(resume)
        
        # Get relevant conversation context from MongoDB
        conversation_context = await self.get_relevant_context(session_id, message, limit=3)
        context_prompt = f"\n\nRecent Conversation Context:\n{conversation_context}" if conversation_context else ""
        
        # Build prompt with resume context and conversation history
        system_prompt = f"""You are Interview Coach AI. Help with resumes, interviews, and career advice.

User's Profile Information:
{resume_context}{context_prompt}

Use this information to provide personalized advice tailored to the user's background, skills, and experience.
Ensure responses are consistent with previous conversation context."""
        
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
            get_session_history_sync,
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
        await ai_msg.async_save()
        
        # Append AI message to cache
        session_history.add_ai_message(response)
        
        # Update session's updated_at timestamp
        try:
            session = await ChatSession.async_find_one(id=session_id)
            if session:
                session.updated_at = datetime.now()
                await session.async_save()
        except Exception as e:
            pass
        
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
    
    async def get_all_sessions(self, skip: int = 0, limit: int = 10) -> list:
        """Get paginated chat sessions for user"""
        try:
            sessions = await ChatSession.async_find(skip=skip, limit=limit, email=self.user_email)
            message_counts = {}
            for s in sessions:
                msgs = await ChatMessage.async_find(session_id=str(s.id))
                message_counts[str(s.id)] = len(msgs)
            
            return [
                {
                    "_id": str(s.id),
                    "title": s.title,
                    "email": s.email,
                    "created_at": s.created_at.isoformat(),
                    "updated_at": s.updated_at.isoformat(),
                    "message_count": message_counts.get(str(s.id), 0)
                }
                for s in sessions
            ]
        except Exception as e:
            return []
    
    async def get_sessions_count(self) -> int:
        """Get total count of sessions for user"""
        try:
            return await ChatSession.async_count(email=self.user_email)
        except Exception as e:
            return 0
    
    async def get_session_messages(self, session_id: str, limit: int = 50, skip: int = 0) -> List[Dict]:
        """Retrieve paginated messages from a session"""
        if not await self.validate_session_ownership(session_id):
            raise APIError(status_code=403, message="Unauthorized access to session", error_code="UNAUTHORIZED")
        
        try:
            messages = await ChatMessage.async_find(session_id=session_id, skip=skip, limit=limit)
            return [
                {
                    "id": str(msg.id),
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in messages
            ]
        except Exception as e:
            return []
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete a session and all its messages"""
        if not await self.validate_session_ownership(session_id):
            raise APIError(status_code=403, message="Unauthorized access to session", error_code="UNAUTHORIZED")
        
        try:
            await ChatMessage.async_delete(session_id=session_id)
            await ChatSession.async_delete(id=session_id)
            
            # Clear from cache
            if session_id in self.store:
                del self.store[session_id]
            
            return True
        except Exception as e:
            return False
