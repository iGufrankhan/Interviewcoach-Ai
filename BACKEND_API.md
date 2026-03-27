# Interview Coach AI - Backend API Documentation

## Base URL
```
http://localhost:8000
```

---

## Table of Contents
1. [Authentication APIs](#authentication-apis)
2. [Resume APIs](#resume-apis)
3. [Interview APIs](#interview-apis)
4. [Chat APIs](#chat-apis)
5. [Job Matching APIs](#job-matching-apis)
6. [Error Handling](#error-handling)
7. [Response Format](#response-format)

---

## Authentication APIs

### 1. Send OTP for Registration
**Endpoint:** `POST /api/auth/send-otp`

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "OTP sent to email",
  "data": {
    "email": "user@example.com"
  }
}
```

---

### 2. Register User
**Endpoint:** `POST /api/auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "otp": "123456",
  "password": "securePassword123",
  "fullname": "John Doe",
  "username": "johndoe"
}
```

**Response (201):**
```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "user_id": "user_object_id",
    "email": "user@example.com",
    "username": "johndoe"
  }
}
```

---

### 3. Login
**Endpoint:** `POST /api/login/`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "accessToken": "jwt_token_here",
    "email": "user@example.com",
    "username": "johndoe"
  }
}
```

---

### 4. Request Password Reset
**Endpoint:** `POST /api/auth/request-password-reset`

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Password reset OTP sent to email"
}
```

---

### 5. Reset Password
**Endpoint:** `POST /api/auth/reset-password`

**Request Body:**
```json
{
  "email": "user@example.com",
  "otp": "123456",
  "new_password": "newPassword123"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Password reset successfully"
}
```

---

## Resume APIs

### 1. Upload Resume
**Endpoint:** `POST /resume/upload`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: multipart/form-data
```

**Request Form Data:**
- `file`: Resume file (PDF, DOCX, TXT)

**Response (201):**
```json
{
  "status": "success",
  "message": "Resume uploaded successfully",
  "data": {
    "resume_id": "resume_object_id",
    "filename": "resume.pdf",
    "upload_date": "2026-03-27T10:30:00Z"
  }
}
```

---

### 2. Get User Resumes
**Endpoint:** `GET /resume/get`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Resumes retrieved",
  "data": [
    {
      "resume_id": "resume_object_id",
      "filename": "resume.pdf",
      "content": "extracted resume text...",
      "upload_date": "2026-03-27T10:30:00Z"
    }
  ]
}
```

---

### 3. Delete Resume
**Endpoint:** `DELETE /resume/delete/{resume_id}`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Resume deleted successfully"
}
```

---

## Interview APIs

### 1. Start Interview
**Endpoint:** `POST /api/interview/start`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "job_title": "Senior Software Engineer",
  "job_description": "We are looking for a senior engineer with 5+ years of experience...",
  "resume_id": "resume_object_id"
}
```

**Response (201):**
```json
{
  "status": "success",
  "message": "Interview started",
  "data": {
    "session_id": "session_object_id",
    "questions": [
      "Tell us about your experience with Python?",
      "How do you handle debugging complex issues?"
    ],
    "total_questions": 2
  }
}
```

---

### 2. Submit Answer
**Endpoint:** `POST /api/interview/submit-answer`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "session_id": "session_object_id",
  "answer": "I have 7 years of Python experience...",
  "use_audio": false
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Answer 1 saved",
  "data": {
    "question_number": 1,
    "total_questions": 2,
    "remaining": 1
  }
}
```

---

### 3. Transcribe Audio
**Endpoint:** `POST /api/interview/transcribe-audio`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "audio_data": "base64_encoded_audio_string"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Audio transcribed successfully",
  "data": {
    "transcribed_text": "I have 7 years of experience with..."
  }
}
```

**Error Response (400):**
```json
{
  "status": "error",
  "message": "Could not understand audio. Please speak clearly and try again.",
  "error_code": "AUDIO_NOT_RECOGNIZED"
}
```

---

### 4. Submit Interview
**Endpoint:** `POST /api/interview/submit`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "session_id": "session_object_id"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Interview analyzed and scored",
  "data": {
    "session_id": "session_object_id",
    "total_score": 8,
    "score_out_of_10": 8,
    "percentage": 80.0,
    "average_per_question": 4.0,
    "question_answers": [
      {
        "question": "Tell us about your experience with Python?",
        "answer": "I have 7 years of Python experience...",
        "score": 4,
        "feedback": "Good technical knowledge demonstrated..."
      },
      {
        "question": "How do you handle debugging complex issues?",
        "answer": "I use systematic debugging approaches...",
        "score": 4,
        "feedback": "Strong problem-solving approach..."
      }
    ]
  }
}
```

---

### 5. Get Interview Session
**Endpoint:** `GET /api/interview/session/{session_id}`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Interview session retrieved",
  "data": {
    "session_id": "session_object_id",
    "job_title": "Senior Software Engineer",
    "status": "completed",
    "questions_count": 2,
    "answers_count": 2,
    "total_score": 8,
    "created_at": "2026-03-27T10:30:00Z",
    "completed_at": "2026-03-27T10:45:00Z",
    "question_answers": []
  }
}
```

---

### 6. Get All User Interviews
**Endpoint:** `GET /api/interview/sessions`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Interviews retrieved",
  "data": [
    {
      "session_id": "session_object_id",
      "job_title": "Senior Software Engineer",
      "status": "completed",
      "total_score": 8,
      "created_at": "2026-03-27T10:30:00Z",
      "completed_at": "2026-03-27T10:45:00Z"
    }
  ]
}
```

---

## Chat APIs

### 1. Send Message (with Resume Context)
**Endpoint:** `POST /api/chat/chat`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "What are some tips for cracking interviews?",
  "resume_id": "resume_object_id"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Message processed",
  "data": {
    "response": "Based on your resume, here are some tailored tips...",
    "session_id": "chat_session_id"
  }
}
```

---

### 2. Get Chat History
**Endpoint:** `GET /api/chat/history/{session_id}`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Chat history retrieved",
  "data": [
    {
      "user_message": "What are some tips for cracking interviews?",
      "bot_response": "Based on your resume, here are some tailored tips...",
      "timestamp": "2026-03-27T10:30:00Z"
    }
  ]
}
```

---

## Job Matching APIs

### 1. Analyze Job Description
**Endpoint:** `POST /jobmatching/analyse`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "resume_id": "resume_object_id",
  "job_description": "We are looking for a senior engineer with 5+ years of experience in Python, Django, and cloud deployment..."
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Job analysis completed",
  "data": {
    "match_score": 85,
    "missing_skills": ["Docker", "Kubernetes"],
    "matching_skills": ["Python", "Django", "REST APIs"],
    "recommendations": [
      "Consider learning Docker for containerization",
      "Kubernetes experience would be a plus"
    ],
    "analysis": "Your profile is a good match for this position..."
  }
}
```

---

## Error Handling

### Standard Error Response Format
```json
{
  "status": "error",
  "message": "Human-readable error message",
  "error_code": "ERROR_CODE_NAME"
}
```

### Common Status Codes

| Status Code | Meaning |
|------------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (missing/invalid token) |
| 403 | Forbidden (not allowed) |
| 404 | Not Found |
| 422 | Unprocessable Entity (validation failed) |
| 503 | Service Unavailable |
| 500 | Internal Server Error |

### Common Error Codes

| Error Code | Meaning | HTTP Status |
|-----------|---------|-------------|
| MISSING_API_KEY | API key not configured | 400 |
| SESSION_NOT_FOUND | Interview session not found | 404 |
| UNAUTHORIZED | User not authorized | 403 |
| INVALID_TOKEN | JWT token invalid or expired | 401 |
| AUDIO_NOT_RECOGNIZED | Could not understand audio | 400 |
| SPEECH_SERVICE_ERROR | Speech recognition service unavailable | 503 |
| INVALID_AUDIO_FORMAT | Audio format not supported | 400 |
| TRANSCRIPTION_FAILED | Audio transcription failed | 500 |
| USER_NOT_FOUND | User does not exist | 404 |
| INVALID_CREDENTIALS | Email or password incorrect | 401 |

---

## Response Format

### Success Response
```json
{
  "status": "success",
  "message": "Operation completed successfully",
  "data": {
    // Response data here
  }
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Error description",
  "error_code": "ERROR_CODE",
  "details": {}
}
```

---

## Authentication

All protected endpoints require JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

The token is obtained from the login endpoint and should be stored in `localStorage` or cookies.

---

## Rate Limiting

Currently not enforced, but recommended rate limits per endpoint:
- Authentication endpoints: 5 requests per minute
- Interview endpoints: 10 requests per session
- Chat endpoint: 30 requests per minute
- Resume endpoints: 10 requests per minute

---

## Audio Transcription

### Supported Formats
- WAV (recommended)
- MP3 (converted to WAV)
- WebM (converted to WAV)

### Requirements
- Audio sample rate: 16000 Hz (recommended)
- Duration: 5 seconds - 60 seconds
- File size: Max 5MB

### Transcription Process
1. Browser records audio using MediaRecorder API
2. Audio is converted to Base64
3. Sent to `/api/interview/transcribe-audio` endpoint
4. Backend transcribes using Google Speech-to-Text API
5. Transcribed text returned to frontend
6. User can edit or submit the transcribed text

---

## Interview Scoring

### Scoring Breakdown
- Total questions: 2
- Points per question: 5
- Total points: 10

### Performance Levels
- **80-100%** (8-10 points): Excellent
- **60-79%** (6-7 points): Good
- **40-59%** (4-5 points): Average
- **Below 40%** (0-3 points): Needs Improvement

### Evaluation Criteria
- Technical accuracy
- Communication clarity
- Problem-solving approach
- Relevance to job description
- Experience demonstration

---

## Environment Variables

Required in `.env` file:
```
GROQ_API_KEY=your_groq_api_key
JWT_SECRET_KEY=your_jwt_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_SECONDS=3600
MONGODB_URI=your_mongodb_connection_string
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

---

## Testing

### Using cURL

**Login:**
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

**Start Interview:**
```bash
curl -X POST http://localhost:8000/api/interview/start \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{"job_title":"Engineer","job_description":"desc","resume_id":"id"}'
```

**Submit Answer:**
```bash
curl -X POST http://localhost:8000/api/interview/submit-answer \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{"session_id":"id","answer":"My answer","use_audio":false}'
```

---

## Troubleshooting

### Audio Transcription Issues
1. **"Invalid audio format"** - Ensure audio is WAV format
2. **"Could not understand audio"** - Speak louder and clearer
3. **"Speech service unavailable"** - Check internet connection
4. **Timeout** - Try shorter audio clips (< 60 seconds)

### Authentication Issues
1. **"Invalid token"** - Token may have expired, login again
2. **"Unauthorized"** - User doesn't have permission
3. **Token not sent** - Ensure Authorization header is present

### Resume Upload Issues
1. **File too large** - Max size is 5MB
2. **Unsupported format** - Only PDF, DOCX, TXT allowed
3. **Upload failed** - Check internet connection

---

## Support

For issues or questions:
- Email: support@interviewcoach.ai
- Documentation: /docs (Swagger UI)
- Health check: GET /health

---

## Version
**API Version:** 1.0.0  
**Last Updated:** March 27, 2026
