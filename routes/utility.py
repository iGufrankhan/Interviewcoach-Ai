from fastapi import APIRouter

router = APIRouter(tags=["Utility"])


@router.get("/")
async def root():
    """Root endpoint - API is running"""
    return {
        "status": "success",
        "message": "Interview Coach AI API is running",
        "version": "1.0.0"
    }


@router.get("/health")
async def health_check():
    """Health check endpoint - includes database connection status"""
    from Dbconfig.config import is_database_connected
    
    db_status = is_database_connected()
    return {
        "status": "healthy" if db_status else "degraded",
        "service": "Interview Coach AI Backend",
        "database": "connected" if db_status else "disconnected"
    }


@router.get("/api/health/db")
async def database_health_check():
    """Detailed database health check endpoint"""
    from Dbconfig.config import get_connection_status
    
    status = get_connection_status()
    return {
        "database": status["connected"],
        "connection_status": "connected" if status["connected"] else "disconnected",
        "error": status["error"],
        "retry_attempts": status["retry_count"],
        "last_attempt": status["last_attempt"]
    }


@router.post("/api/health/db/reconnect")
async def database_reconnect():
    """Manually retry database connection"""
    from Dbconfig.config import retry_connection, get_connection_status
    
    success = retry_connection()
    status = get_connection_status()
    
    return {
        "reconnect_attempt": "success" if success else "failed",
        "connection_status": "connected" if status["connected"] else "disconnected",
        "error": status["error"],
        "retry_attempts": status["retry_count"]
    }


@router.get("/api/status")
async def api_status():
    """API status and available services"""
    return {
        "status": "operational",
        "services": {
            "authentication": {
                "register": "/api/auth/send-otp",
                "login": "/api/login/",
                "password_reset": "/api/auth/request-password-reset"
            },
            "resume": {
                "upload": "/api/resume/upload-resume",
                "get": "/api/resume/user-resumes",
                "delete": "/api/resume/delete-resume/{id}"
            },
            "job_matching": {
                "analyze": "/api/jobmatching/analyseresume"
            },
            "interview": {
                "question_gen": "/api/interviewservice/generate-questions",
                "start": "/api/interview/start",
                "submit-answer": "/api/interview/submit-answer",
                "submit": "/api/interview/submit"
            },
            "chat": {
                "create_session": "/api/chat/create-session",
                "send_message": "/api/chat/send-message"
            }
        }
    }
