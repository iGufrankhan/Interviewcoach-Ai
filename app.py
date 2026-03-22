from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import Dbconfig.config 
from ResumeService.api.uploadresume import router as resume_router
from ResumeService.api.getresumedata import router as update_router
from ResumeService.api.deleteresume import router as delete_router


from AuthService.api.register_api import router as register_router
from AuthService.api.login_api import router as login_router


from JobMaching.api.analyse import router as analyse_router

from interviewService.api.question_gen import router as question_gen_router


app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(register_router)
app.include_router(login_router)

app.include_router(resume_router, prefix="/resume")
app.include_router(update_router, prefix="/resume")
app.include_router(delete_router, prefix="/resume")

app.include_router(analyse_router, prefix="/jobmatching")

app.include_router(question_gen_router, prefix="/interviewservice")


