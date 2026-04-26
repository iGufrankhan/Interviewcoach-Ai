<h1 align="center">🔗 Backend-Frontend Integration Guide</h1>

<div align="center">
  <p>Complete guide on how the Interview Coach AI Next.js Frontend communicates with the FastAPI Backend.</p>
</div>

---

## 📑 Table of Contents
<details>
<summary>Click to expand</summary>

1. [🏗️ Architecture Overview](#-architecture-overview)
2. [⚙️ Setup & Configuration](#-setup--configuration)
3. [📡 Frontend API Utilities](#-frontend-api-utilities)
4. [🌊 Data Flow Examples](#-data-flow-examples)
5. [🔐 Authentication Flow](#-authentication-flow)
6. [⚠️ CORS & Security](#-cors--security)
7. [🐛 Debugging & Troubleshooting](#-debugging--troubleshooting)
8. [🚀 Deployment](#-deployment)
</details>

---

## 🏗️ Architecture Overview

```text
Frontend (Next.js/React)
         ↓
API Layer (lib/api.ts) — TypeScript Safe
         ↓
Backend (FastAPI) @ http://localhost:8000
         ↓
Database (MongoDB) & External APIs (Groq, HuggingFace)
```

---

## ⚙️ Setup & Configuration

### Backend
1. Create a `.env` file containing `GROQ_API_KEY` and `MONGODB_URL`.
2. Start the FastAPI server:
   ```bash
   uvicorn app:app --reload --port 8000
   ```

### Frontend
1. Navigate to the `Frontend/` folder and install dependencies (`npm install`).
2. Create `Frontend/.env.local` and add the backend URL:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```
3. Start the Next.js dev server:
   ```bash
   npm run dev
   ```

---

## 📡 Frontend API Utilities

All backend interactions should go through `Frontend/lib/api.ts` which handles token injection, error handling, and type safety automatically.

```typescript
// Example usage in React components
import { fetchUserResumes, generateInterviewQuestions, uploadResume } from '@/lib/api';

// Fetching
const resumes = await fetchUserResumes(userId);
const questions = await generateInterviewQuestions(description, resumeId);

// Mutations
const result = await uploadResume(userId, file);
```

---

## 🌊 Data Flow Examples

### 1. Interview Question Generation
1. User enters Job Description + selects a Resume.
2. Frontend calls `generateInterviewQuestions()`.
3. Backend receives request, validates JWT, fetches resume from MongoDB, and calls Groq LLM.
4. Groq generates 10 tailored questions.
5. Frontend stores questions in `localStorage` and navigates to the practice room.

### 2. Resume Upload
1. User selects a PDF/DOCX file.
2. Frontend calls `uploadResume()`.
3. Backend validates file, extracts text, parses skills via AI, and stores in MongoDB.
4. Backend returns the parsed resume object.
5. Frontend updates the UI to show the newly uploaded resume.

---

## 🔐 Authentication Flow

1. **Login:** Send credentials to `POST /login`.
2. **Store:** Save `access_token` and `user_id` in `localStorage` (or secure cookies).
3. **Use:** Append the token to the Authorization header in all requests: `Authorization: Bearer {token}`.
4. **Validation:** Backend validates the JWT signature on every protected route and returns `401 Unauthorized` if expired or invalid.

---

## ⚠️ CORS & Security

By default, the backend allows requests from `http://localhost:3000` and `http://127.0.0.1:3000`. 
To add production domains, update `app.py`:
```python
allow_origins=[
    "http://localhost:3000",
    "https://your-production-domain.com",
]
```

---

## 🐛 Debugging & Troubleshooting

### Common Issues
* **CORS Error (Access Blocked):** Ensure your frontend URL exactly matches the strings in `allow_origins` in `app.py`.
* **401 Unauthorized:** Your token is expired or missing. Ensure `lib/api.ts` is injecting `Bearer {token}` correctly.
* **404 Not Found:** Ensure `NEXT_PUBLIC_API_URL` points to `http://localhost:8000` (without trailing slashes).

### Enable Frontend Debugging
```env
# In .env.local
NEXT_PUBLIC_DEBUG=true
```

---

## 🚀 Deployment

### Backend
Use `gunicorn` for production deployment instead of `uvicorn`:
```bash
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Frontend
Update `.env.production.local` with the production API URL:
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```
Then build and start:
```bash
npm run build
npm run start
```
