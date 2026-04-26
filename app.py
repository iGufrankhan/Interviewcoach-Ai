from dotenv import load_dotenv
load_dotenv()
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from datetime import datetime, timezone
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from middlewares.auth_middleware import AuthMiddleware
from middlewares.rate_limit import RateLimitMiddleware

from utils.apierror import APIError
from utils.error_codes import ErrorCode
from utils.constant import CORS_ORIGINS

from datetime import datetime
import logging, os, sys

import Dbconfig.config

# ===== ROUTERS =====
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


# ===== LIFESPAN =====
@asynccontextmanager
async def lifespan(app: FastAPI):
    await Dbconfig.config.init_db()
    yield


app = FastAPI(
    title="Interview Coach AI",
    description="AI-powered interview preparation platform with AI coaching",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600
)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuthMiddleware)

START_TIME = datetime.now(timezone.utc)

@app.get("/")
def home():
    uptime_seconds = int((datetime.now(timezone.utc) - START_TIME).total_seconds())

    return {
        "service": app.title,
        "version": app.version,
        "status": "running",
        "environment": "production",
        "uptime_seconds": uptime_seconds,
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "openapi": "/openapi.json"
        },
        "features": [
            "Authentication",
            "Resume Analysis",
            "Job Matching",
            "Interview Q&A",
            "Chat Assistant"
        ],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/health")
async def health():
    now = datetime.now(timezone.utc)
    uptime = int((now - START_TIME).total_seconds())

    try:
        db_status = Dbconfig.config.get_db_status()
        db_connected = db_status.get("is_connected", False)
    except Exception as e:
        db_status = {"error": str(e)}
        db_connected = False

    return {
        "status": "healthy" if db_connected else "degraded",
        "service": app.title,
        "version": app.version,
        "uptime_seconds": uptime,
        "timestamp": now.isoformat(),
        "checks": {
            "api": "ok",
            "database": {
                "status": "connected" if db_connected else "disconnected",
                "details": db_status
            }
        }
    }


# ===== ROUTES =====
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