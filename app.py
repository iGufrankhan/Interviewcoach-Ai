from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
import Dbconfig.config 
from ResumeService.api.uploadresume import router as resume_router
from ResumeService.api.getresumedata import router as update_router
from ResumeService.api.deleteresume import router as delete_router


from AuthService.api.register_api import router as register_router
from AuthService.api.login_api import router as login_router


app = FastAPI()

app.include_router(register_router)
app.include_router(login_router)

app.include_router(resume_router, prefix="/resume")
app.include_router(update_router, prefix="/resume")
app.include_router(delete_router, prefix="/resume")

app.include_router(resume_router, prefix="/resume")
app.include_router(update_router, prefix="/resume")
app.include_router(delete_router, prefix="/resume")


