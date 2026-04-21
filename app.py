from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from middlewares.auth_middleware import AuthMiddleware
from utils.apierror import APIError
from utils.error_codes import ErrorCode, HttpStatusCode
import logging
import Dbconfig.config

# Setup logging
logger = logging.getLogger(__name__)

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

app = FastAPI(
    title="Interview Coach AI",
    description="AI-powered interview preparation platform",
    version="1.0.0"
)

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


# ========== Global Exception Handlers ==========

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    """
    Handle APIError exceptions.
    
    - Returns standardized error response
    - Logs internal message if provided
    - Never exposes internal details to client
    """
    # Log internal error details for debugging
    if exc.internal_message:
        logger.error(
            f"API Error: {exc.error_code}",
            extra={
                "error_code": exc.error_code,
                "internal_message": exc.internal_message,
                "status_code": exc.status_code,
                "path": request.url.path
            }
        )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail  # Already formatted by APIError.__init__
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    """
    Handle Pydantic validation errors.
    
    - Extract field names that failed validation
    - Return user-friendly error message
    - Log details for debugging
    """
    errors = exc.errors()
    field_names = [error["loc"][1] if len(error["loc"]) > 1 else "unknown" for error in errors]
    
    logger.warning(
        f"Validation error on {request.url.path}",
        extra={
            "fields": field_names,
            "errors": errors
        }
    )
    
    return JSONResponse(
        status_code=HttpStatusCode.BAD_REQUEST,
        content={
            "success": False,
            "message": f"Validation error in fields: {', '.join(set(field_names))}",
            "error_code": ErrorCode.INVALID_INPUT,
            "data": None
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected exceptions.
    
    - Never expose internal error details
    - Log full traceback for debugging
    - Return generic error message
    """
    logger.error(
        f"Unexpected error on {request.url.path}",
        exc_info=True,
        extra={"path": request.url.path}
    )
    
    return JSONResponse(
        status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "An unexpected error occurred. Please try again later.",
            "error_code": ErrorCode.INTERNAL_SERVER_ERROR,
            "data": None
        }
    )


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

