print("STEP 0: file start")

from dotenv import load_dotenv
load_dotenv()
print("STEP 1: dotenv loaded")

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
print("STEP 2: fastapi imports done")

from middlewares.auth_middleware import AuthMiddleware
print("AuthMiddleware OK")

from middlewares.rate_limit import RateLimitMiddleware
print("RateLimitMiddleware OK")

from utils.apierror import APIError
from utils.error_codes import ErrorCode
from utils.constant import CORS_ORIGINS
print("Utils OK")

from datetime import datetime
import logging, os, sys
print("Basic libs OK")

import Dbconfig.config
print("DB config import OK")

# ===== ROUTERS =====
try:
    from ResumeService.api.uploadresume import router as resume_router
    print("resume_router OK")
except Exception as e:
    print("resume_router ERROR:", e)
    resume_router = None

try:
    from ResumeService.api.getresumedata import router as update_router
    print("update_router OK")
except Exception as e:
    print("update_router ERROR:", e)
    update_router = None

try:
    from ResumeService.api.deleteresume import router as delete_router
    print("delete_router OK")
except Exception as e:
    print("delete_router ERROR:", e)
    delete_router = None

try:
    from AuthService.api.register_api import router as register_router
    print("register_router OK")
except Exception as e:
    print("register_router ERROR:", e)
    register_router = None

try:
    from AuthService.api.login_api import router as login_router
    print("login_router OK")
except Exception as e:
    print("login_router ERROR:", e)
    login_router = None

try:
    from AuthService.api.logout import api_router as logout_router
    print("logout_router OK")
except Exception as e:
    print("logout_router ERROR:", e)
    logout_router = None

try:
    from AuthService.api.resetpassword_api import api_router as resetpassword_router
    print("resetpassword_router OK")
except Exception as e:
    print("resetpassword_router ERROR:", e)
    resetpassword_router = None

try:
    from AuthService.api.refreshtoken import router as refresh_token_router
    print("refresh_token_router OK")
except Exception as e:
    print("refresh_token_router ERROR:", e)
    refresh_token_router = None

try:
    from JobMaching.api.analyse import router as analyse_router
    print("analyse_router OK")
except Exception as e:
    print("analyse_router ERROR:", e)
    analyse_router = None

try:
    from interviewService.api.question_gen import router as question_gen_router
    print("question_gen_router OK")
except Exception as e:
    print("question_gen_router ERROR:", e)
    question_gen_router = None

try:
    from chat_agent.api.chatBot import router as chat_router
    print("chat_router OK")
except Exception as e:
    print("chat_router ERROR:", e)
    chat_router = None

try:
    from interviewService.api.interview_flow import router as interview_flow_router
    print("interview_flow_router OK")
except Exception as e:
    print("interview_flow_router ERROR:", e)
    interview_flow_router = None


# ===== LIFESPAN =====
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("STEP 3: lifespan start")
    try:
        await Dbconfig.config.init_db()
        print("DB CONNECTED")
    except Exception as e:
        print("DB ERROR:", e)
    yield


print("STEP 4: creating app")

app = FastAPI(
    title="Interview Coach AI",
    description="AI-powered interview preparation platform with AI coaching",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

print("STEP 5: adding middleware")

app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_credentials=True, allow_methods=["GET", "POST", "PUT", "DELETE"], allow_headers=["Content-Type", "Authorization"], max_age=3600)

try:
    app.add_middleware(RateLimitMiddleware)
    print("RateLimitMiddleware added")
except Exception as e:
    print("RateLimitMiddleware ERROR:", e)

try:
    app.add_middleware(AuthMiddleware)
    print("AuthMiddleware added")
except Exception as e:
    print("AuthMiddleware ERROR:", e)


@app.get("/health")
async def health():
    try:
        db_status = Dbconfig.config.get_db_status()
        return {"status": "ok", "db": db_status}
    except Exception as e:
        return {"error": str(e)}


print("STEP 6: adding routers")

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

print("STEP 7: app ready")