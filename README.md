# Interview Coach AI

Interview Coach AI is a full-stack interview preparation workspace with a FastAPI backend and a Next.js frontend. The backend handles authentication, resume ingestion, parsing, analysis, interview question generation, and chat flows. The frontend provides the landing page, auth screens, dashboards, and product routes.

## What It Does

- Upload resumes in PDF, DOCX, or TXT format.
- Extract structured resume data with a Groq-powered LLM.
- Store and retrieve resume records per authenticated user.
- Generate interview questions and interview flow content.
- Provide chat-based interview coaching.
- Serve a modern Next.js marketing and application UI.

## Repository Layout

```text
app.py                     FastAPI application entrypoint and router wiring
AuthService/               Authentication and account management backend
JobMaching/                Job matching backend routes and analysis logic
ResumeService/             Resume upload, parsing, preprocessing, and storage
chat_agent/                Chat assistant backend routes
interviewService/          Interview question and interview flow backend routes
Frontend/                  Next.js 16 frontend application
utils/                     Shared response, error, config, and token helpers
Dbconfig/                  Database initialization and status helpers
middlewares/               Auth and rate-limit middleware
requirements.txt           Python dependencies for the backend
```

## Backend Overview

The backend entrypoint is [app.py](app.py). It loads environment variables, initializes MongoDB on startup, enables CORS, and registers routers for auth, resume services, job matching, chat, and interview flows.

The resume pipeline is split across several modules:

- [ResumeService/api/uploadresume.py](ResumeService/api/uploadresume.py) handles authenticated resume uploads.
- [ResumeService/services/resumeservice.py](ResumeService/services/resumeservice.py) saves the file, extracts text, preprocesses it, runs LLM analysis, and persists structured results.
- [ResumeService/loaders/resume_loaders.py](ResumeService/loaders/resume_loaders.py) loads PDF, DOCX, and TXT files.
- [ResumeService/preprocessing/preprocessing.py](ResumeService/preprocessing/preprocessing.py) cleans extracted text.
- [ResumeService/analyzer/analysis.py](ResumeService/analyzer/analysis.py) parses resume content into structured JSON.
- [ResumeService/api/getresumedata.py](ResumeService/api/getresumedata.py) returns the authenticated user’s saved resumes.
- [ResumeService/api/deleteresume.py](ResumeService/api/deleteresume.py) deletes a resume after ownership checks.

The shared config in [utils/constant.py](utils/constant.py) shows the main environment values the app expects:

- `DATABASE_URL`
- `DATABASE_NAME`
- `ACCESS_TOKEN_KEY`
- `REFRESH_TOKEN_KEY`
- `GROQ_API_KEY`
- `HF_TOKEN`
- `GMAIL_USER`
- `GMAIL_APP_PASSWORD`
- `CORS_ORIGINS`
- `MAX_FILE_UPLOAD_SIZE`

## Frontend Overview

The frontend lives in [Frontend/package.json](Frontend/package.json) and uses Next.js 16, React 19, Tailwind CSS 4, and TypeScript. The app folder includes the landing page plus route groups for auth, dashboard, resume, job matching, interview prep, and chat.

Important frontend files:

- [Frontend/app/landing-page.tsx](Frontend/app/landing-page.tsx) is the marketing landing page.
- [Frontend/app/page.tsx](Frontend/app/page.tsx) is the main entry page for the app.
- [Frontend/app/layout.tsx](Frontend/app/layout.tsx) provides shared layout structure.
- [Frontend/app/globals.css](Frontend/app/globals.css) contains global styles.

The landing page redirects authenticated users to `/dashboard` and otherwise presents the product overview, feature cards, workflow steps, and calls to action.

## Setup

### Prerequisites

- Python 3.8 or newer
- Node.js 18+ for the frontend
- MongoDB running locally or in Atlas
- Groq API key
- Hugging Face token if you use the embedding or RAG features

### Backend

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```

The backend starts on `http://localhost:8000` by default.

### Frontend

```bash
cd Frontend
npm install
npm run dev
```

The frontend runs on the Next.js default port, usually `http://localhost:3000`.

## Environment Variables

Create a `.env` file in the workspace root for the backend. The code reads these values directly:

```env
DATABASE_URL=mongodb://localhost:27017/interviewcoach
DATABASE_NAME=interviewcoach
ACCESS_TOKEN_KEY=your_access_token_secret
REFRESH_TOKEN_KEY=your_refresh_token_secret
GROQ_API_KEY=your_groq_api_key
HF_TOKEN=your_hugging_face_token
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
MAX_FILE_UPLOAD_SIZE=10485760
```

## Main API Routes

The exact route surface depends on the mounted routers in [app.py](app.py), but the resume endpoints currently exposed include:

- `POST /api/resume/upload-resume`
- `GET /api/resume/user-resumes`
- `GET /api/resume/resume/{resume_id}`
- `DELETE /api/resume/delete-resume/{resume_id}`

Other routers are mounted for authentication, job matching, chat, and interview flows.

## Notes

- The backend uses middleware for authentication and rate limiting.
- Resume uploads are validated for file type, size, and non-empty content.
- The resume analyzer expects clean text and returns structured JSON with name, skills, experience, education, and projects.
- The frontend is already wired for authenticated redirects and a landing-page-first experience.
