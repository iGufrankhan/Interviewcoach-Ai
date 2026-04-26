<h1 align="center">🔌 Backend API Documentation</h1>

<div align="center">
  <p>Complete reference for the Interview Coach AI REST API.</p>
  <b>Base URL:</b> <code>http://localhost:8000</code> &nbsp;|&nbsp; <b>Version:</b> <code>1.1.0</code>
</div>

---

## 📑 Table of Contents
<details>
<summary>Click to expand</summary>

1. [🔐 Authentication APIs](#-authentication-apis)
2. [📄 Resume APIs](#-resume-apis)
3. [🎯 Interview APIs](#-interview-apis)
4. [💬 Chat APIs](#-chat-apis)
5. [💼 Job Matching APIs](#-job-matching-apis)
6. [⚠️ Error Handling & Response Format](#-error-handling--response-format)
7. [⚙️ Environment Variables & Notes](#-environment-variables--notes)
</details>

---

## 🔐 Authentication APIs
*All protected endpoints require the `Authorization: Bearer <jwt_token>` header.*

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/send-otp` | Send an OTP for registration. |
| `POST` | `/api/auth/register` | Register a new user using the OTP. |
| `POST` | `/api/login/` | Login and receive a JWT access token. |
| `POST` | `/api/auth/request-password-reset` | Send an OTP to reset password. |
| `POST` | `/api/auth/reset-password` | Set a new password using the OTP. |

<details>
<summary><b>View Example Payloads</b></summary>

**Login Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```
**Login Response (200):**
```json
{
  "status": "success",
  "data": {
    "accessToken": "jwt_token_here",
    "email": "user@example.com",
    "username": "johndoe"
  }
}
```
</details>

---

## 📄 Resume APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/resume/upload` | Upload a new resume (PDF, DOCX, TXT). |
| `GET`  | `/resume/get` | Retrieve all parsed resumes for the user. |
| `DELETE`| `/resume/delete/{resume_id}` | Delete a specific resume. |

---

## 🎯 Interview APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/question_gen/generate` | Generate 10 role-specific questions based on a JD. |
| `POST` | `/api/interview/start` | Start an active interview session. |
| `POST` | `/api/interview/submit-answer`| Submit an answer (text or audio). |
| `POST` | `/api/interview/transcribe-audio`| Convert Base64 audio into text via Google Speech. |
| `POST` | `/api/interview/submit` | End the interview and get the final score and feedback. |
| `GET`  | `/api/interview/sessions` | Get all past interviews. |
| `GET`  | `/api/interview/session/{id}` | Get detailed feedback for a specific interview. |

<details>
<summary><b>Audio Transcription Rules</b></summary>

* **Formats:** WAV (recommended), MP3, WebM.
* **Requirements:** 16kHz sample rate, 5-60 seconds max duration.
* **Payload:** `{ "audio_data": "base64_encoded_audio_string" }`
</details>

---

## 💬 Chat APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat/create-session` | Initialize a new Chat Coach session. |
| `POST` | `/api/chat/send-message` | Send a message to the AI coach. |
| `POST` | `/api/chat/chat` | Quick chat with resume context. |
| `GET`  | `/api/chat/sessions` | Retrieve all past chat sessions. |
| `GET`  | `/api/chat/history/{id}` | Retrieve chat history for a session. |

---

## 💼 Job Matching APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/jobmatching/analyse` | Score a resume against a job description and get an action plan. |

<details>
<summary><b>View Response Payload</b></summary>

```json
{
  "status": "success",
  "data": {
    "match_score": 85,
    "missing_skills": ["Docker", "Kubernetes"],
    "matching_skills": ["Python", "Django", "REST APIs"],
    "recommendations": ["Consider learning Docker"],
    "analysis": "Your profile is a good match..."
  }
}
```
</details>

---

## ⚠️ Error Handling & Response Format

**Standard Success Response:**
```json
{
  "status": "success",
  "message": "Operation completed successfully",
  "data": { }
}
```

**Standard Error Response:**
```json
{
  "status": "error",
  "message": "Human-readable error message",
  "error_code": "ERROR_CODE_NAME"
}
```

### Common Error Codes
* `MISSING_API_KEY` (400) - API key not configured.
* `INVALID_TOKEN` (401) - JWT token invalid or expired.
* `AUDIO_NOT_RECOGNIZED` (400) - Could not understand audio.
* `INVALID_INPUT` (400) - Validation error in payload.

---

## ⚙️ Environment Variables & Notes

Required `.env` file variables for the Backend:
```env
GROQ_API_KEY=your_groq_api_key
JWT_SECRET_KEY=your_jwt_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_SECONDS=3600
MONGODB_URI=your_mongodb_connection_string
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```
* **GROQ API:** Get a free key from [console.groq.com](https://console.groq.com)
* **CORS:** Ensure your frontend URL is added to the CORS configuration in `app.py`.

---
<div align="center">
  <i>For testing, use Swagger UI at <a href="http://localhost:8000/docs">http://localhost:8000/docs</a></i>
</div>
