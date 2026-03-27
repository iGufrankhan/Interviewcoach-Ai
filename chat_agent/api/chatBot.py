from fastapi import APIRouter, Depends
from chat_agent.chatBotService.chatBotservice import ChatBotService
from middlewares.auth_middleware import verify_jwt
from utils.apiresponse import success_response, error_response
import os
from chat_agent.schema.chatBot import CreateSessionRequest, SendMessageRequest

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat Agent"]
)




@router.post("/create-session")
async def create_session(request: CreateSessionRequest, user=Depends(verify_jwt)):
    """Create a new chat session"""
    try:
        api_key = os.getenv("GROQ_API_KEY")
        service = ChatBotService(api_key, user.email)
        
        session_id = service.create_session(request.title)
        
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
async def send_message(request: SendMessageRequest, user=Depends(verify_jwt)):
    """Send message and get AI response"""
    try:
        api_key = os.getenv("GROQ_API_KEY")
        service = ChatBotService(api_key, user.email)
        
        # Validate user owns this session
        if not service.validate_session_ownership(request.session_id):
            return error_response(
                message="Unauthorized: Session not found or does not belong to user",
                error_code="UNAUTHORIZED_SESSION",
                status_code=403
            )
        
        response = service.send_message(request.session_id, request.message)
        
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
async def get_sessions(user=Depends(verify_jwt)):
    """Get all chat sessions for user"""
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
async def get_session_history(session_id: str, user=Depends(verify_jwt)):
    """Get chat history for a session"""
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
        
        history = service.get_session_history(session_id)
        messages = [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in history.messages
        ]
        
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