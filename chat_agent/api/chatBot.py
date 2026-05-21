from fastapi import APIRouter, Request, Query
from slowapi import Limiter
from slowapi.util import get_remote_address
from chat_agent.chatBotService.chatBotservice import ChatBotService
from utils.apiresponse import success_response, error_response
from utils.apierror import APIError
from utils.constant import GROQ_API_KEY
from chat_agent.schema.chatBot import CreateSessionRequest, SendMessageRequest, GetMessagesRequest

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat Agent"]
)




@router.post("/create-session")
async def create_session(req: CreateSessionRequest, request: Request):
    """Create a new chat session"""
    user = request.state.user
    try:
        api_key = GROQ_API_KEY
        if not api_key:
            return error_response(
                message="GROQ_API_KEY is not configured",
                error_code="MISSING_API_KEY",
                status_code=500
            )
        
        service = ChatBotService(api_key, user.email)
        session_id = await service.create_session(req.title)
        
        return success_response(
            message="Chat session created",
            data={"session_id": session_id},
            status_code=201
        )
    except APIError as e:
        return error_response(
            message=e.detail.get("error", "Failed to create session"),
            error_code=e.detail.get("error_code", "SESSION_CREATE_ERROR"),
            status_code=e.status_code
        )
    except Exception as e:
        return error_response(
            message="Failed to create session",
            error_code="SESSION_CREATE_ERROR",
            status_code=500
        )


@limiter.limit("10/minute")
@router.post("/send-message")
async def send_message(req: SendMessageRequest, request: Request):
    """Send message and get AI response - Rate limited to 10/minute"""
    user = request.state.user
    try:
        api_key = GROQ_API_KEY
        if not api_key:
            return error_response(
                message="GROQ_API_KEY is not configured",
                error_code="MISSING_API_KEY",
                status_code=500
            )
        
        service = ChatBotService(api_key, user.email)
        
        # Validate user owns this session
        if not await service.validate_session_ownership(req.session_id):
            return error_response(
                message="Unauthorized: Session not found or does not belong to user",
                error_code="UNAUTHORIZED_SESSION",
                status_code=403
            )
        
        response = await service.send_message(req.session_id, req.message)
        
        return success_response(
            message="Message processed",
            data={"response": response},
            status_code=200
        )
    except APIError as e:
        return error_response(
            message=e.detail.get("error", "Failed to send message"),
            error_code=e.detail.get("error_code", "MESSAGE_SEND_ERROR"),
            status_code=e.status_code
        )
    except Exception as e:
        return error_response(
            message="Failed to send message",
            error_code="MESSAGE_SEND_ERROR",
            status_code=500
        )


@router.get("/sessions")
async def get_sessions(
    request: Request,
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    limit: int = Query(10, ge=1, le=100, description="Items per page (1-100)")
):
    """Get chat sessions for user with pagination
    
    Args:
        page: Page number (1-indexed)
        limit: Items per page (max 100 to prevent large queries)
    
    Returns:
        {
            "sessions": [...],
            "pagination": {
                "page": 1,
                "limit": 10,
                "total": 1000,
                "total_pages": 100
            }
        }
    """
    user = request.state.user
    try:
        api_key = GROQ_API_KEY
        if not api_key:
            return error_response(
                message="GROQ_API_KEY is not configured",
                error_code="MISSING_API_KEY",
                status_code=500
            )
        
        service = ChatBotService(api_key, user.email)
    
        # Get total count for pagination metadata
        total = await service.get_sessions_count()
        
        # Calculate skip for database query
        skip = (page - 1) * limit
        
        # Get paginated sessions
        sessions = await service.get_all_sessions(skip=skip, limit=limit)
        
        return success_response(
            message="Sessions retrieved",
            data={
                "sessions": sessions,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "total_pages": (total + limit - 1) // limit
                }
            }
        )
    except Exception as e:
        return error_response(
            message="Failed to retrieve sessions",
            error_code="SESSIONS_GET_ERROR",
            status_code=500
        )


@router.get("/session/{session_id}")
async def get_session_history(
    session_id: str,
    request: Request,
    limit: int = Query(100, ge=1, le=500, description="Max messages to return (1-500)"),
    skip: int = Query(0, ge=0, description="Messages to skip for pagination")
):
    """Get chat history for a session with pagination
    
    Args:
        session_id: Chat session ID
        limit: Number of messages to return (1-500, default 100)
        skip: Number of messages to skip (default 0)
    """
    user = request.state.user
    try:
        api_key = GROQ_API_KEY
        if not api_key:
            return error_response(
                message="GROQ_API_KEY is not configured",
                error_code="MISSING_API_KEY",
                status_code=500
            )
        
        service = ChatBotService(api_key, user.email)
        
        # Validate user owns this session
        if not await service.validate_session_ownership(session_id):
            return error_response(
                message="Unauthorized: Session not found or does not belong to user",
                error_code="UNAUTHORIZED_SESSION",
                status_code=403
            )
        
        # Get messages with pagination
        messages = await service.get_session_messages(session_id, limit=limit, skip=skip)
        
        return success_response(
            message="Chat history retrieved",
            data={
                "messages": messages,
                "limit": limit,
                "skip": skip
            },
            status_code=200
        )
    except Exception as e:
        return error_response(
            message="Failed to retrieve chat history",
            error_code="HISTORY_GET_ERROR",
            status_code=500
        )


@router.get("/session/{session_id}/stats")
async def get_session_stats(session_id: str, request: Request):
    """Get statistics for a chat session"""
    user = request.state.user
    try:
        api_key = GROQ_API_KEY
        if not api_key:
            return error_response(
                message="GROQ_API_KEY is not configured",
                error_code="MISSING_API_KEY",
                status_code=500
            )
        
        service = ChatBotService(api_key, user.email)
        
        # Validate user owns this session
        if not await service.validate_session_ownership(session_id):
            return error_response(
                message="Unauthorized: Session not found or does not belong to user",
                error_code="UNAUTHORIZED_SESSION",
                status_code=403
            )
        
        stats = await service.get_session_stats(session_id)
        
        return success_response(
            message="Session statistics retrieved",
            data=stats,
            status_code=200
        )
    except Exception as e:
        return error_response(
            message="Failed to retrieve session statistics",
            error_code="STATS_GET_ERROR",
            status_code=500
        )


@router.delete("/session/{session_id}")
async def delete_session(session_id: str, request: Request):
    """Delete a chat session and all its messages"""
    user = request.state.user
    try:
        api_key = GROQ_API_KEY
        if not api_key:
            return error_response(
                message="GROQ_API_KEY is not configured",
                error_code="MISSING_API_KEY",
                status_code=500
            )
        
        service = ChatBotService(api_key, user.email)
        
        # Validate user owns this session
        if not await service.validate_session_ownership(session_id):
            return error_response(
                message="Unauthorized: Session not found or does not belong to user",
                error_code="UNAUTHORIZED_SESSION",
                status_code=403
            )
        
        await service.delete_session(session_id)
        
        return success_response(
            message="Session deleted successfully",
            status_code=200
        )
    except Exception as e:
        return error_response(
            message="Failed to delete session",
            error_code="SESSION_DELETE_ERROR",
            status_code=500
        )
