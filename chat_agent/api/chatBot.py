from fastapi import APIRouter, Request
from chat_agent.chatBotService.chatBotservice import ChatBotService
from utils.apiresponse import success_response, error_response
import os
from chat_agent.schema.chatBot import CreateSessionRequest, SendMessageRequest

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat Agent"]
)




@router.post("/create-session")
async def create_session(req: CreateSessionRequest, request: Request):
    user = request.state.user
    """Create a new chat session"""
    try:
        api_key = os.getenv("GROQ_API_KEY")
        service = ChatBotService(api_key, user.email)
        
        session_id = service.create_session(req.title)
        
        return success_response(
            message="Chat session created",
            data={"session_id": session_id},
            status_code=201
        )
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="SESSION_CREATE_ERROR",
            status_code=500
        )


@router.post("/send-message")
async def send_message(req: SendMessageRequest, request: Request):
    user = request.state.user
    """Send message and get AI response"""
    try:
        api_key = os.getenv("GROQ_API_KEY")
        service = ChatBotService(api_key, user.email)
        
        # Validate user owns this session
        if not service.validate_session_ownership(req.session_id):
            return error_response(
                message="Unauthorized: Session not found or does not belong to user",
                error_code="UNAUTHORIZED_SESSION",
                status_code=403
            )
        
        response = service.send_message(req.session_id, req.message)
        
        return success_response(
            message="Message processed",
            data={"response": response},
            status_code=200
        )
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="MESSAGE_SEND_ERROR",
            status_code=500
        )


@router.get("/sessions")
async def get_sessions(request: Request):
    """Get all chat sessions for user"""
    user = request.state.user
    try:
        api_key = os.getenv("GROQ_API_KEY")
        service = ChatBotService(api_key, user.email)
        
        sessions = service.get_all_sessions()
        
        return success_response(
            message="Sessions retrieved",
            data=sessions,
            status_code=200
        )
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="SESSIONS_GET_ERROR",
            status_code=500
        )


@router.get("/session/{session_id}")
async def get_session_history(session_id: str, request: Request):
    """Get chat history for a session"""
    user = request.state.user
    try:
        api_key = os.getenv("GROQ_API_KEY")
        service = ChatBotService(api_key, user.email)
        
        # Validate user owns this session
        if not service.validate_session_ownership(session_id):
            return error_response(
                message="Unauthorized: Session not found or does not belong to user",
                error_code="UNAUTHORIZED_SESSION",
                status_code=403
            )
        
        # Get messages directly from MongoDB
        messages = service.get_session_messages(session_id, limit=100)
        
        return success_response(
            message="Chat history retrieved",
            data=messages,
            status_code=200
        )
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="HISTORY_GET_ERROR",
            status_code=500
        )