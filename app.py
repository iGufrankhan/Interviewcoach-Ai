from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
import Dbconfig.config 
from ResumeService.api.uploadresume import router as resume_router
from ResumeService.api.getresumedata import router as update_router
from ResumeService.api.deleteresume import router as delete_router
from AuthService.api.register_api import router as register_router
from AuthService.api.login_api import router as login_router
from AuthService.api.resetpassword_api import api_router as resetpassword_router
from JobMaching.api.analyse import router as analyse_router
from interviewService.api.question_gen import router as question_gen_router
from chat_agent.api.chatBot import router as chat_router  # ADD THIS LINE

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,
)

# Register routers
app.include_router(register_router)
app.include_router(login_router)
app.include_router(resetpassword_router)
app.include_router(resume_router, prefix="/resume")
app.include_router(update_router, prefix="/resume")
app.include_router(delete_router, prefix="/resume")
app.include_router(analyse_router, prefix="/jobmatching")
app.include_router(question_gen_router, prefix="/interviewservice")
app.include_router(chat_router) 

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter


# ============ Health Check & Utility Routes ============

@app.get("/")
async def root():
    """Root endpoint - API is running"""
    return {
        "status": "success",
        "message": "Interview Coach AI API is running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Interview Coach AI Backend"
    }


@app.get("/api/status")
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
                "upload": "/resume/upload",
                "get": "/resume/get",
                "delete": "/resume/delete"
            },
            "job_matching": {
                "analyze": "/jobmatching/analyse"
            },
            "interview": {
                "question_gen": "/interviewservice/generate-questions"
            }
        }
    }


