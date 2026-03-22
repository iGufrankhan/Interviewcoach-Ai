# Backend-Frontend Integration Guide

## Overview

This document describes the complete integration between the Interview Coach AI backend (FastAPI) and frontend (Next.js).

## Architecture

```
Frontend (Next.js/React)
         ↓
API Layer (lib/api.ts)
         ↓
Next.js API Routes (optional, for server-side requests)
         ↓
Backend (FastAPI) @ http://localhost:8000
         ↓
Database (MongoDB)
         ↓
External APIs (Groq LLM, Email Services)
```

## Setup

### Backend Setup

1. **Enable CORS** - Already configured in `app.py` with:
   ```python
   CORSMiddleware(
       allow_origins=["http://localhost:3000", "http://localhost:3001"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Environment Variables** - Ensure backend has:
   ```
   GROQ_API_KEY=your_api_key
   MONGODB_URL=your_mongodb_connection
   ```

3. **Run Backend**:
   ```bash
   # Activate virtual environment
   source project_2/Scripts/activate  # Windows
   # or
   source project_2/bin/activate      # Mac/Linux
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run FastAPI server
   uvicorn app:app --reload --port 8000
   ```

### Frontend Setup

1. **Install Dependencies**:
   ```bash
   cd Frontend
   npm install
   ```

2. **Configure Environment** - Update `Frontend/.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Run Frontend**:
   ```bash
   npm run dev
   # Server runs on http://localhost:3000
   ```

## API Endpoints

### Resume Management

#### Get User's Resumes
```
GET /resume/api/user-resumes/{user_id}
Authorization: Bearer {JWT_TOKEN}

Response:
{
  "data": [
    {
      "resume_id": "...",
      "filename": "resume.pdf",
      "created_at": "2024-03-22T...",
      "extracted_data": {
        "name": "...",
        "email": "...",
        "phone": "...",
        "skills": [...],
        "experience": [...],
        "education": [...]
      }
    }
  ],
  "message": "Resumes found"
}
```

#### Get Specific Resume
```
GET /resume/api/resume/{resume_id}
Authorization: Bearer {JWT_TOKEN}

Response:
{
  "data": { ... resume object ... },
  "message": "Resume found"
}
```

#### Upload Resume
```
POST /resume/api/upload-resume/{user_id}
Authorization: Bearer {JWT_TOKEN}
Content-Type: multipart/form-data

Body: file (resume.pdf, resume.docx, or resume.txt)

Response:
{
  "data": { ... resume object ... },
  "message": "Resume uploaded and saved successfully"
}
```

### Interview Service

#### Generate Interview Questions
```
POST /interviewservice/question_gen/generate
Authorization: Bearer {JWT_TOKEN}

Query Parameters:
  - description: string (job description)
  - resume_id: string (resume ID)

Response:
{
  "questions": [
    "Question 1?",
    "Question 2?",
    ...
  ]
}
```

### Job Matching

#### Analyze Job Match
```
POST /jobmatching/api/analyse
Authorization: Bearer {JWT_TOKEN}

Query Parameters:
  - description: string (job description)
  - resume_id: string (resume ID)

Response:
{
  "data": { ... analysis results ... },
  "message": "Analysis complete"
}
```

## Frontend API Utilities

### File: `Frontend/lib/api.ts`

Provides TypeScript-based API utilities for all backend endpoints:

```typescript
// Get user resumes
const resumes = await fetchUserResumes(userId);

// Generate interview questions
const questions = await generateInterviewQuestions(description, resumeId);

// Get specific resume
const resume = await getResume(resumeId);

// Analyze job match
const analysis = await analyzeJobMatch(description, resumeId);

// Upload resume
const result = await uploadResume(userId, file);

// Delete resume
await deleteResume(resumeId);
```

### Features:
- **Automatic token injection** from localStorage
- **Error handling** with meaningful messages
- **Type safety** with TypeScript interfaces
- **Environment-based API URL** (configurable via `.env.local`)

## Data Flow Examples

### 1. Interview Question Generation

```
User enters job description and selects resume
         ↓
Frontend calls generateInterviewQuestions()
         ↓
API calls /interviewservice/question_gen/generate
         ↓
Backend:
  - Validates JWT token
  - Fetches resume from MongoDB
  - Extracts job information
  - Calls Groq LLM API
  - Generates 10 questions
         ↓
Returns questions array
         ↓
Frontend stores in localStorage
         ↓
Navigates to interview-results page
         ↓
User practices answering questions
         ↓
User can export/download results
```

### 2. Resume Upload

```
User selects file from computer
         ↓
Frontend calls uploadResume()
         ↓
API sends FormData to /resume/api/upload-resume/{user_id}
         ↓
Backend:
  - Validates file type (PDF, DOCX, TXT)
  - Extracts text from file
  - Parses resume data (name, skills, experience, etc.)
  - Stores in MongoDB
  - Returns resume object
         ↓
Frontend receives resume data
         ↓
Displays success message
         ↓
New resume appears in list
```

## Authentication Flow

1. **Login** (from auth page):
   ```
   POST /login
   Body: { email, password }
   Response: { access_token, user_id, ... }
   ```

2. **Store Token**:
   ```javascript
   localStorage.setItem('token', response.access_token);
   localStorage.setItem('user_id', response.user_id);
   ```

3. **Use Token** in all API requests:
   ```
   Authorization: Bearer {token}
   ```

4. **Token Validation**:
   - Backend verifies JWT token in every request
   - Extracts user info from token
   - Returns 401 if token invalid

## Error Handling

### Backend Errors
```json
{
  "detail": "Error message",
  "error_code": "ERROR_TYPE",
  "status_code": 400
}
```

### Frontend Handling
```typescript
try {
  const data = await generateInterviewQuestions(desc, resumeId);
} catch (error) {
  // Display error to user
  setError(error.message);
}
```

## CORS Configuration

Backend allows requests from:
- `http://localhost:3000` (development)
- `http://localhost:3001` (alternative)
- `http://127.0.0.1:3000`
- `http://127.0.0.1:3001`

To add production domains, update `app.py`:
```python
allow_origins=[
    "http://localhost:3000",
    "https://yourdomain.com",
]
```

## Security Considerations

1. **JWT Tokens**:
   - Stored in localStorage (consider secure cookies for production)
   - Sent in Authorization header
   - Validated server-side on every request

2. **CORS**:
   - Configured to only allow frontend origins
   - Prevents unauthorized cross-origin requests

3. **File Validation**:
   - Resume uploads validated for file type
   - Size limits enforced server-side

4. **Input Validation**:
   - All query parameters validated
   - Job descriptions and resume IDs validated

5. **Environment Variables**:
   - API keys not exposed to frontend
   - Sensitive config server-side only

## Debugging

### Enable Debug Logging
```javascript
// In .env.local
NEXT_PUBLIC_DEBUG=true
```

### Check Network Requests
1. Open DevTools (F12)
2. Go to Network tab
3. Look for API requests
4. Check Response and Headers

### Backend Logs
```bash
# Terminal where backend is running shows all requests
# Look for [GET], [POST], [DELETE] entries
```

### Common Issues

**Issue: CORS Error**
```
Access to XMLHttpRequest blocked by CORS policy
```
- Ensure backend has CORS middleware enabled
- Check frontend URL is in allowed_origins

**Issue: 401 Unauthorized**
```
{"detail":"Invalid token"}
```
- Ensure JWT token is stored in localStorage
- Token might be expired (re-login required)
- Check Authorization header format: "Bearer {token}"

**Issue: API Not Found (404)**
```
{"detail":"Not Found"}
```
- Check endpoint URL format
- Verify API prefix (/resume, /interviewservice, etc.)
- Check method (GET vs POST)

## Deployment

### Backend Deployment
```bash
# Use production server (not uvicorn)
pip install gunicorn
gunicorn app:app -w 4 -b 0.0.0.0:8000
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Deploy next.js app (Vercel, Netlify, Docker, etc.)
npm run start
```

### Update API URL
```
# .env.production.local
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

## Testing

### Manual Testing Checklist
- [ ] Can upload resume
- [ ] Can view uploaded resumes
- [ ] Can generate interview questions
- [ ] Questions are relevant to job description
- [ ] Can answer and navigate questions
- [ ] Can export/download results
- [ ] Logout and re-login works
- [ ] Token refresh works

### API Testing with curl
```bash
# Generate questions
curl -X POST \
  "http://localhost:8000/interviewservice/question_gen/generate?description=Software%20Engineer&resume_id=123" \
  -H "Authorization: Bearer {your_token}"

# Get user resumes
curl -X GET \
  "http://localhost:8000/resume/api/user-resumes/{user_id}" \
  -H "Authorization: Bearer {your_token}"
```

## Performance Optimization

1. **Frontend**:
   - Caching resume list locally
   - Debouncing API calls
   - Lazy loading components

2. **Backend**:
   - Database indexing on user_id
   - Question generation caching
   - Connection pooling for MongoDB

## Future Enhancements

1. **Real-time Features**:
   - WebSocket for live feedback
   - Real-time collaboration

2. **Advanced Caching**:
   - Redis for session storage
   - CDN for assets

3. **Analytics**:
   - Track usage metrics
   - Performance monitoring

4. **Mobile App**:
   - React Native version
   - Offline support with sync

## Support & Troubleshooting

For issues:
1. Check the error message in console
2. Review debug logs
3. Check network requests (DevTools)
4. Verify environment variables
5. Test backend independently (Postman/curl)
