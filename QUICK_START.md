# Quick Start Guide - Interview Coach AI

## Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- MongoDB running locally or cloud connection
- Groq API key

## Step-by-Step Setup

### 1. Backend Setup & Run

```bash
# Navigate to project root
cd "c:\Users\kakab\OneDrive\Desktop\InterviewCoach AI"

# Activate Python virtual environment
.\project_2\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Set environment variables (create .env file in root)
echo GROQ_API_KEY=your_api_key_here > .env
echo MONGODB_URL=your_mongodb_url >> .env

# Start FastAPI backend
uvicorn app:app --reload --port 8000
```

Backend running on: `http://localhost:8000`

### 2. Frontend Setup & Run

```bash
# Open new terminal/PowerShell

# Navigate to Frontend folder
cd "c:\Users\kakab\OneDrive\Desktop\InterviewCoach AI\Frontend"

# Install dependencies
npm install

# Ensure .env.local exists with:
NEXT_PUBLIC_API_URL=http://localhost:8000

# Start Next.js dev server
npm run dev
```

Frontend running on: `http://localhost:3000`

### 3. Access the Application

1. Open browser: `http://localhost:3000`
2. On homepage, click "Login" or "Get Started"
3. Create account or login with existing credentials
4. Upload a resume
5. Go to Interview Service
6. Select resume + job description
7. Generate questions and practice!

## Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed (replace PID)
taskkill /PID <PID> /F

# Try different port
uvicorn app:app --reload --port 8001
```

### Frontend shows API errors
- Check if backend is running on port 8000
- Verify CORS is enabled in app.py
- Check token in localStorage (DevTools > Application)
- Network tab in DevTools shows actual error

### Resume upload fails
- Check file format (PDF, DOCX, TXT only)
- Ensure GROQ_API_KEY is set
- Check file size (usually max 10MB)

### Questions not generating
- Verify GROQ_API_KEY is valid
- Ensure resume data extracted correctly
- Check backend logs for detailed error

## API Health Check

### Check Backend Status
```bash
curl http://localhost:8000/docs
```
Should show Swagger UI with all endpoints

### Test API Call
```bash
curl -X GET \
  "http://localhost:8000/resume/api/user-resumes/test-user" \
  -H "Authorization: Bearer {your_token}"
```

## Development Tips

### Hot Reload
- **Backend**: Automatically reloads on file changes
- **Frontend**: Automatically reloads on file changes
- No need to restart during development

### Debug Mode
```javascript
// Frontend .env.local
NEXT_PUBLIC_DEBUG=true
```
Then check DevTools console for extra logging

### Database
- View MongoDB: Install MongoDB Compass
- Connect to your MONGODB_URL
- Explore collections in compass

### API Testing
Use Postman or Thunder Client to test endpoints independently

## File Structure Summary

```
InterviewCoach AI/
├── app.py                           # FastAPI entry point
├── requirements.txt                 # Python dependencies
├── .env                             # Backend config (create this)
│
├── AuthService/                     # Authentication
├── ResumeService/                   # Resume upload/management
├── interviewService/                # Interview Q&A generation
├── JobMaching/                      # Job matching analysis
├── Models/                          # Database models
├── middlewares/                     # Auth middleware
├── utils/                           # Shared utilities
│
├── Frontend/
│   ├── app/                         # Next.js routes
│   │   ├── (InterviewService)/      # Interview pages
│   │   ├── (resumeService)/         # Resume management
│   │   ├── (auth)/                  # Login/Register
│   │   ├── (jobmatching)/           # Job analysis
│   │   └── api/                     # API routes
│   ├── lib/
│   │   └── api.ts                   # API utilities
│   ├── .env.local                   # Frontend config (create this)
│   ├── package.json
│   └── tsconfig.json
│
└── BACKEND_FRONTEND_INTEGRATION.md  # Full integration guide
```

## Next Steps

1. ✅ Backend running
2. ✅ Frontend running
3. ✅ Create user account
4. ✅ Upload resume
5. ✅ Generate interview questions
6. 🔄 Customize and extend features
7. 🚀 Deploy to production

## Production Deployment

### Update Configuration
```
# .env (Backend)
GROQ_API_KEY=production_key
MONGODB_URL=production_mongodb_url

# Frontend/.env.production.local
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### Deploy Backend
```bash
# Build Docker image or use hosting service
# Popular options: AWS, Google Cloud, Azure, Heroku, Railway

gunicorn app:app -w 4 -b 0.0.0.0:8000
```

### Deploy Frontend
```bash
# Build for production
npm run build

# Deploy to: Vercel, Netlify, AWS S3 + CloudFront, Docker, etc.
npm run start
```

## Support & Documentation

- **Full Integration Guide**: See `BACKEND_FRONTEND_INTEGRATION.md`
- **Interview Service**: See `Frontend/app/(InterviewService)/README.md`
- **Swagger UI**: Visit `http://localhost:8000/docs`

## Useful Commands

```bash
# Backend
uvicorn app:app --reload              # Run backend with hot reload
uvicorn app:app --port 8001           # Run on different port

# Frontend
npm run dev                            # Development mode
npm run build                          # Production build
npm run start                          # Start production server
npm run lint                           # Run linter

# Database
# MongoDB - connect with Compass or CLI
mongosh  # if installed
```

## Common Environment Variables

```bash
# Backend
GROQ_API_KEY=xxxxxxxxxxxxx
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/dbname
JWT_SECRET=your_jwt_secret
DEBUG=True  # Optional

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_DEBUG=false  # Optional
```

Enjoy building! 🚀
