from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from ResumeService.api.uploadresume import router as resume_router

app = FastAPI()

app.include_router(resume_router, prefix="/resume")
