from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from Models.chat_bot.chat_bot import ChatSession, ChatMessage
from datetime import datetime


class ChatBotService:
    
    def __init__(self, api_key: str, user_email: str):
        self.api_key = api_key
        self.user_email = user_email
        self.store = {}
        
        self.llm = ChatGroq(
            groq_api_key=api_key,
            model="llama-3.1-8b-instant"
        )
        
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
        
        # Get session history
        session_history = self.get_session_history(session_id)
        
        # Build prompt
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are Interview Coach AI. Help with resumes, interviews, and career advice."),
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




















