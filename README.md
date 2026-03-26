# Interview Coach AI

An intelligent FastAPI-based application that helps candidates prepare for interviews by analyzing job descriptions, matching resumes, generating interview questions, and providing personalized feedback.

---

## 📋 Features

### 1. **Resume Analysis & Job Matching**
- Analyze how well your resume matches a job description
- Get a detailed match score (0-100) with eligibility assessment
- Receive actionable strengths, weaknesses, and improvement suggestions
- Framework: MUST-HAVE vs NICE-TO-HAVE requirement matching

### 2. **Interview Question Generation**
- Generate 10 targeted interview questions based on job description
- Questions prioritize job requirements over general topics
- Leverages both job description and resume data for relevance
- Helps candidates prepare for role-specific scenarios

### 3. **Smart Chat Assistant**
- Memory-aware AI chatbot for career guidance and interview preparation
- Maintains conversation history across sessions (persistent storage)
- Leverages Groq's Llama 3.1 for fast, intelligent responses
- Real-time chat widget with typing indicators
- Floating widget interface on dashboard for easy access

### 4. **Comprehensive Candidate Profiling**
- Store and manage candidate resumes
- Track skills, experience, education, and projects
- Support for multiple resume versions per user

---

## 🏗️ Architecture

```
├── AuthService/                    # User authentication & registration
│   ├── api/
│   │   ├── login_api.py
│   │   ├── register_api.py
│   │   └── resetpassword_api.py
│   ├── authservice/
│   ├── controllers/
│   │   └── emailservice/           # Email verification & OTP
│   ├── schemas/
│   └── utils/

├── JobMaching/                     # Resume-Job Matching
│   ├── api/
│   │   └── analyse.py             # POST /api/analyseresume
│   ├── analyser/
│   │   └── resumeanalise.py       # Matching logic
│   ├── loader/
│   │   └── job_descpLoad.py       # Job description processing
│   └── resumeCompare/
│       ├── llmcompare.py          # LLM-based comparison
│       └── llmcompare_rag.py      # RAG-based comparison

├── interviewService/              # Interview Question Generation
│   ├── api/
│   │   └── question_gen.py        # POST /question_gen/generate
│   ├── QuestionGenService/
│   │   └── Questiongen.py         # Question generation logic
│   └── loader/
│       └── get_data.py            # Data loading

├── chat_agent/                    # AI Chat Assistant
│   ├── api/
│   │   └── chatBot.py            # POST /api/chat/* endpoints
│   ├── chatBotService/
│   │   └── chatBotservice.py     # ChatBotService with memory
│   └── schema/
│       └── chatBot.py            # Chat request/response models

├── ResumeService/                 # Resume Management
│   ├── api/
│   │   ├── uploadresume.py
│   │   ├── getresumedata.py
│   │   └── deleteresume.py
│   ├── analyzer/
│   ├── preprocessing/
│   ├── services/
│   └── utils/

├── Models/                        # Database Models
│   ├── userReg/
│   │   ├── user.py               # User model
│   │   └── otp.py                # OTP model
│   ├── resumeservice/
│   │   ├── resume_models.py
│   │   └── resumeschema.py
│   └── chat_bot/
│       └── chat_bot.py           # ChatSession & ChatMessage models

├── middlewares/                  # Custom middleware
│   └── auth_middleware.py

├── Dbconfig/                     # Database configuration
│   └── config.py

├── utils/                        # Utility functions
│   ├── apierror.py              # Custom error handling
│   ├── apiresponse.py           # Response formatting
│   └── token.py                 # JWT token utilities

├── Frontend/                     # Next.js React Frontend
│   ├── app/
│   │   ├── chatbot/
│   │   │   ├── ChatWidget.tsx   # Chat widget component
│   │   │   └── chatWidget.module.css
│   │   ├── dashboard/
│   │   └── ...
│   ├── lib/
│   │   ├── chat/
│   │   │   └── chatApi.ts       # Chat API client
│   │   └── ...
│   └── ...

├── app.py                        # Main FastAPI application
└── requirements.txt              # Project dependencies
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- MongoDB (must be running)
- GROQ API Key (for LLM capabilities)

### 1. Clone & Navigate
```bash
cd "InterviewCoach AI"
```

### 2. Create Virtual Environment
```bash
python -m venv project_2
source project_2/Scripts/activate  # Windows
# or
source project_2/bin/activate      # macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
MONGODB_URI=mongodb://localhost:27017/interviewcoach
JWT_SECRET=your_secret_key_here
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### 5. Start MongoDB
```bash
# Windows
mongod

# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

### 6. Run Application
```bash
python app.py
# or
uvicorn app:app --reload
```

The API will be available at: `http://localhost:8000`

### 7. Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📡 API Endpoints

### Authentication & User Management
```
POST   /auth/register           # Register new user
POST   /auth/login              # Login user
POST   /auth/reset-password     # Reset password
POST   /auth/verify-otp         # Verify OTP
```

### Resume Management
```
POST   /resume/upload           # Upload resume
GET    /resume/get/{resume_id}  # Get resume data
DELETE /resume/delete/{id}      # Delete resume
```

### Chat Agent (AI Assistant)
```
POST   /api/chat/create-session    # Create new chat session
POST   /api/chat/send-message      # Send message and get AI response
GET    /api/chat/sessions          # Get all user chat sessions
GET    /api/chat/session/{id}      # Get chat history for session
```

**Chat Features:**
- ✅ Memory-aware conversation history
- ✅ Persistent storage in MongoDB
- ✅ Auto-loads previous sessions on login
- ✅ Real-time floating widget on dashboard
- ✅ Powered by Groq's Llama 3.1 8B Instant

**Create Session Example:**
```bash
POST /api/chat/create-session
Authorization: Bearer {jwt_token}
```
Response:
```json
{
  "status": "success",
  "data": {
    "session_id": "65a1b2c3d4e5f6g7h8i9"
  }
}
```

**Send Message Example:**
```bash
POST /api/chat/send-message
Authorization: Bearer {jwt_token}

{
  "session_id": "65a1b2c3d4e5f6g7h8i9",
  "message": "My name is Gufran Khan. What skills should I focus on?"
}
```
Response:
```json
{
  "status": "success",
  "data": {
    "response": "Hi Gufran! Based on current market trends, I'd recommend focusing on..."
  }
}
```

### Resume-Job Matching (Job Matching Service)
```
POST   /api/analyseresume
```

**Request Body:**
```json
{
  "resume_id": "user_resume_id",
  "description": "Job description text (copy from job posting)"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "score": 65,
    "eligible": "PARTIAL",
    "strengths": "• Python and MongoDB experience matches job requirements\n• Project management experience",
    "weaknesses": "• Limited cloud platform experience (AWS, Azure required)\n• No microservices architecture background",
    "suggestions": "• Take AWS certification courses\n• Build projects using microservices\n• Gain hands-on cloud deployment experience"
  }
}
```

---

### Interview Question Generation
```
POST   /question_gen/generate
```

**Request Body:**
```json
{
  "resume_id": "user_resume_id",
  "description": "Job description text"
}
```

**Response:**
```json
{
  "questions": [
    "1. Can you describe your experience with Python and how it relates to this role?",
    "2. Tell us about a project where you used MongoDB...",
    "... (8 more questions)"
  ]
}
```

---

## 📊 Workflow Example

### Step 1: Register & Login
```bash
POST /auth/register
POST /auth/login
- Get JWT token for authentication
```

### Step 2: Upload Resume
```bash
POST /resume/upload
- Upload your resume (PDF/DOCX)
- System extracts: skills, experience, education, projects
```

### Step 3: Analyze Job Match
```bash
POST /api/analyseresume
{
  "resume_id": "65a1b2c3d4e5f6g7h8i9",
  "description": "Senior Backend Developer...
  
  Responsibilities:
  - Design scalable microservices
  - Work with AWS/Azure
  - Lead technical discussions
  
  Requirements:
  - 5+ years backend development
  - Kubernetes, Docker
  - System design experience"
}

Response: Score 72, PARTIAL eligible
```

### Step 4: Generate Interview Questions
```bash
POST /question_gen/generate
{
  "resume_id": "65a1b2c3d4e5f6g7h8i9",
  "description": "Senior Backend Developer..."
}

Response: 10 targeted interview questions
```

### Step 5: Practice with AI Assistant
```bash
1. Create Chat Session
   POST /api/chat/create-session
   Response: { "session_id": "..." }

2. Send Practice Questions
   POST /api/chat/send-message
   {
     "session_id": "...",
     "message": "Can you ask me one of those interview questions?"
   }

3. Get Feedback
   - AI asks questions and provides feedback
   - Conversation history is saved for future reference
   - Logout/login preserves your chat history
```

---

## 🧠 AI/LLM Features

### LLM Provider: Groq (Llama 3.1 8B Instant)

#### Resume Matching Logic
- **Framework**: MUST-HAVE vs NICE-TO-HAVE requirements
- **Scoring**: 0-100 based on actual job requirements
- **Output**: Score, Eligibility (YES/PARTIAL/NO), Strengths, Weaknesses, Suggestions

#### Question Generation Logic
- **Approach**: Job description prioritization with resume context
- **Output**: 10 unique, role-specific interview questions
- **Quality**: Targets technical depth and practical scenarios

#### Chat Assistant Features
- **Memory Type**: Persistent conversation history with MongoDB storage
- **Conversation Aware**: Remembers user information across sessions
- **Session Management**: Auto-loads previous sessions on login
- **Architecture**: LangChain RunnableWithMessageHistory with MongoDB backend
- **Response Time**: Sub-second responses via Groq API
- **Use Cases**:
  - Career guidance and skill recommendations
  - Mock interview practice
  - Interview question explanations
  - Resume improvement suggestions
  - Behavioral question preparation

---

## 🔐 Security Features

1. **JWT Authentication**
   - Secure token-based user authentication
   - Token expiration & refresh mechanisms

2. **Password Management**
   - Secure password hashing
   - OTP-based password reset
   - Email verification

3. **Custom Middleware**
   - Authentication middleware for protected routes
   - Error handling middleware

4. **Error Handling**
   - Custom APIError class for consistent error responses
   - Proper HTTP status codes
   - Descriptive error messages

---

## 📦 Dependencies

Core dependencies:
```
fastapi==0.104.1
uvicorn==0.24.0
mongoengine==0.23.1
python-dotenv==1.0.0
langchain==0.1.0
langchain-groq==0.1.0
pydantic==2.0.0
pydantic-settings==2.0.0
```

See `requirements.txt` for complete list.

---

## 🛠️ Development Guide

### Adding New Features

1. **Create API Route** (in `api/` folder)
2. **Create Service Logic** (in respective service folder)
3. **Update Models** (if needed in `Models/`)
4. **Add Tests** (recommended)
5. **Update Documentation** (README, docstrings)

### Code Structure Best Practices
- Keep API layer thin (validation only)
- Move business logic to service layer
- Use models for database operations
- Centralize error handling

---

## 🐛 Troubleshooting

### MongoDB Connection Error
```
Solution: Ensure MongoDB is running
Windows: mongod
macOS: brew services start mongodb-community
```

### GROQ API Key Error
```
Check: GROQ_API_KEY is set in .env file
Test: Make a test API call to verify key validity
```

### Import Errors
```
Solution: pip install -r requirements.txt
Verify: Python path includes project directory
```

---

## 📝 API Response Formats

### Success Response
```json
{
  "status": "success",
  "data": {
    // endpoint-specific data
  }
}
```

### Error Response
```json
{
  "detail": {
    "error": "Error description",
    "error_code": "ERROR_CODE"
  }
}
```

---

## 🚦 HTTP Status Codes

- `200 OK` - Successful request
- `400 Bad Request` - Invalid input/validation error
- `401 Unauthorized` - Authentication failed
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## � Chat Assistant (AI Helper)

### Features
- **Memory Aware**: Remembers user information and conversation history
- **Persistent Storage**: All conversations stored in MongoDB
- **Session Management**: 
  - Create new chat sessions
  - Auto-load previous sessions on login
  - Retrieve full conversation history
- **Real-time Responses**: Powered by Groq's Llama 3.1 8B Instant model
- **Floating Widget**: Accessible from dashboard via floating button

### Technical Architecture
- **Backend**: FastAPI + LangChain with MongoEngine models
- **Memory**: RunnableWithMessageHistory for conversation context
- **Storage**: MongoDB collections (chat_sessions, chat_messages)
- **Frontend**: React component with real-time UI updates
- **Authentication**: JWT-protected endpoints

### How It Works
1. User opens chat widget on dashboard
2. System loads most recent chat session (if exists)
3. Previous conversation history is displayed
4. User can continue conversation with full context awareness
5. All messages saved to MongoDB automatically
6. Even after logout/login, conversation history persists

### Database Models

**ChatSession**
```python
{
  _id: ObjectId,
  user_id: String,        # Email
  email: String,
  title: String,          # "Chat Session"
  created_at: DateTime,
  updated_at: DateTime
}
```

**ChatMessage**
```python
{
  _id: ObjectId,
  session_id: String,     # Reference to ChatSession
  role: String,           # "user" or "assistant"
  content: String,        # Message content
  timestamp: DateTime
}
```

---

## �📈 Performance Tips

1. **Resume Upload**: Keep files < 5MB for faster processing
2. **Job Description**: 500-2000 characters optimal length
3. **Batch Requests**: Limit concurrent API calls to 5-10/second
4. **Chat Sessions**: Limit conversation length to ~100 messages per session
5. **Caching**: Consider caching frequently matched job descriptions
6. **Database**: Ensure MongoDB indexes on session_id and user_id for fast queries

---

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and test
3. Commit with clear messages
4. Push to branch
5. Create Pull Request

---

## 📞 Support

For issues or questions:
1. Check documentation above
2. Review error messages and codes
3. Check MongoDB connection
4. Verify API keys
5. Check logs: `uvicorn app:app --log-level debug`

---

## 📄 License

This project is proprietary. All rights reserved.

---

## 🎯 Roadmap

- [x] Resume analysis & job matching
- [x] Interview question generation
- [x] User authentication
- [x] Resume management
- [x] Email verification & OTP
- [x] AI Chat Assistant with memory
- [ ] Support for multiple resume versions per user
- [ ] Resume parsing improvements (PDF, DOCX formatting)
- [ ] Interview mock sessions with real-time feedback
- [ ] Performance metrics and analytics dashboard
- [ ] Integration with LinkedIn job postings
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Interview video recording and analysis
- [ ] Advanced resume templates
- [ ] Salary negotiation guidance

---

## 🔄 Version History

### v1.1.0 (Current)
- ✅ AI Chat Assistant with memory awareness
- ✅ Persistent conversation history (MongoDB)
- ✅ Auto-load previous sessions on login
- ✅ Floating chat widget on dashboard
- ✅ Real-time responses via Groq Llama 3.1

### v1.0.0
- ✅ Resume analysis & job matching
- ✅ Interview question generation
- ✅ User authentication & JWT
- ✅ Resume management
- ✅ Email verification & OTP

---

**Last Updated**: March 26, 2026

**Maintainer**: Interview Coach AI Team
