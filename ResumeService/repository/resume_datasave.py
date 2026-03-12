from Models.resumeservice.resume_models import Resume_data
from Models.resumeservice.resumeschema import create_resume_schema

def save_resume(resume_data):
    resume_doc = Resume_data(
        name=resume_data.get("name", ""),
        skills=resume_data.get("skills", []),
        experience=_ensure_list(resume_data.get("experience")),
        education=_ensure_list(resume_data.get("education")),
        projects=_ensure_list(resume_data.get("projects")),
    )
    resume_doc.save()
    return create_resume_schema(resume_doc)

def _ensure_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]