from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from middlewares.auth_middleware import AuthMiddleware
from middlewares.rate_limit import RateLimitMiddleware

from utils.constant import CORS_ORIGINS

import Dbconfig.config


# ===== ROUTERS (simple try/catch) =====
try:
    from ResumeService.api.uploadresume import router as resume_router
except:
    resume_router = None

try:
    from ResumeService.api.getresumedata import router as update_router
except:
    update_router = None

try:
    from ResumeService.api.deleteresume import router as delete_router
except:
    delete_router = None

try:
    from AuthService.api.register_api import router as register_router
except:
    register_router = None

try:
    from AuthService.api.login_api import router as login_router
except:
    login_router = None

try:
    from AuthService.api.logout import api_router as logout_router
except:
    logout_router = None

try:
    from AuthService.api.resetpassword_api import api_router as resetpassword_router
except:
    resetpassword_router = None

try:
    from AuthService.api.refreshtoken import router as refresh_token_router
except:
    refresh_token_router = None

try:
    from JobMaching.api.analyse import router as analyse_router
except:
    analyse_router = None

try:
    from interviewService.api.question_gen import router as question_gen_router
except:
    question_gen_router = None

try:
    from chat_agent.api.chatBot import router as chat_router
except:
    chat_router = None

try:
    from interviewService.api.interview_flow import router as interview_flow_router
except:
    interview_flow_router = None


# ===== LIFESPAN =====
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await Dbconfig.config.init_db()
    except:
        pass
    yield


app = FastAPI(
    title="Interview Coach AI",
    description="AI-powered interview preparation platform",
    version="1.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"]
)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuthMiddleware)


START_TIME = datetime.now(timezone.utc)

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
if register_router: app.include_router(register_router)
if login_router: app.include_router(login_router)
if refresh_token_router: app.include_router(refresh_token_router)
if resetpassword_router: app.include_router(resetpassword_router)
if logout_router: app.include_router(logout_router)

if resume_router: app.include_router(resume_router, prefix="/api/resume")
if update_router: app.include_router(update_router, prefix="/api/resume")
if delete_router: app.include_router(delete_router, prefix="/api/resume")

if analyse_router: app.include_router(analyse_router, prefix="/api/jobmatching")
if question_gen_router: app.include_router(question_gen_router, prefix="/api/interviewservice")

if chat_router: app.include_router(chat_router)
if interview_flow_router: app.include_router(interview_flow_router)