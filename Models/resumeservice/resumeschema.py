def create_resume_schema(resume_data):
    return {
        "id": str(resume_data.id),
        "name": resume_data.name,
        "skills": resume_data.skills,
        "experience": resume_data.experience,
        "education": resume_data.education,
        "projects": resume_data.projects,
        "created_at": str(resume_data.created_at)
    }

