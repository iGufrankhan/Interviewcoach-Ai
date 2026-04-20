from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middlewares.auth_middleware import AuthMiddleware
import Dbconfig.config

from ResumeService.api.uploadresume import router as resume_router
from ResumeService.api.getresumedata import router as update_router
from ResumeService.api.deleteresume import router as delete_router
from AuthService.api.register_api import router as register_router
from AuthService.api.login_api import router as login_router
from AuthService.api.logout import api_router as logout_router
from AuthService.api.resetpassword_api import api_router as resetpassword_router
from AuthService.api.refreshtoken import router as refresh_token_router
from JobMaching.api.analyse import router as analyse_router
from interviewService.api.question_gen import router as question_gen_router
from chat_agent.api.chatBot import router as chat_router  
from interviewService.api.interview_flow import router as interview_flow_router
from routes.utility import router as utility_router

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

# Add JWT authentication middleware
app.add_middleware(AuthMiddleware)

# Register routers
app.include_router(utility_router)
app.include_router(register_router)
app.include_router(login_router)
app.include_router(refresh_token_router)
app.include_router(resetpassword_router)
app.include_router(logout_router)
app.include_router(resume_router, prefix="/api/resume")
app.include_router(update_router, prefix="/api/resume")
app.include_router(delete_router, prefix="/api/resume")
app.include_router(analyse_router, prefix="/api/jobmatching")
app.include_router(question_gen_router, prefix="/api/interviewservice")
app.include_router(chat_router)
app.include_router(interview_flow_router)

