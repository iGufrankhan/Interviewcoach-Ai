<h1 align="center">🎯 Interview Coach AI</h1>

<div align="center">
  <p>An intelligent, FastAPI-based application that helps candidates prepare for interviews by analyzing job descriptions, matching resumes, generating targeted interview questions, and providing personalized feedback.</p>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white)](https://www.python.org)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
  [![MongoDB](https://img.shields.io/badge/MongoDB-Enabled-47A248.svg?logo=mongodb&logoColor=white)](https://www.mongodb.com)
  [![Groq](https://img.shields.io/badge/LLM-Groq_Llama_3.1-f55036.svg)](https://groq.com)
  [![LangChain](https://img.shields.io/badge/LangChain-Integration-00A6D6.svg)](https://langchain.com)
  [![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7.svg?logo=render&logoColor=white)](https://interviewcoach-ai-backend.onrender.com)
</div>

<br />

> **🚀 Live Backend API:** [Access Live API](https://interviewcoach-ai-backend.onrender.com)

---

## ✨ Key Features

### 📄 1. Resume Analysis & Job Matching
* **Deep Match Analysis:** Compares your resume against job descriptions to provide a detailed match score (0-100).
* **Smart Evaluation:** Evaluates eligibility based on *MUST-HAVE* vs *NICE-TO-HAVE* requirements.
* **Actionable Feedback:** Receive clear strengths, weaknesses, and improvement suggestions to boost your chances.

### ❓ 2. Interview Question Generation
* **Targeted Questions:** Generates 10 role-specific interview questions based heavily on the job description.
* **Context-Aware:** Leverages your resume data to ask highly relevant, personalized questions rather than generic ones.

### 🤖 3. Smart Chat Assistant
* **Memory-Aware Chat:** Maintains conversation history across sessions using persistent storage.
* **Real-time AI:** Powered by Groq's Llama 3.1 for lightning-fast, intelligent coaching and guidance.
* **Seamless UI Integration:** Ready to power real-time chat widgets with typing indicators and floating interfaces.

### 👤 4. Candidate Profiling
* **Resume Vault:** Securely store and manage multiple resume versions.
* **Skill Tracking:** Automatically track extracted skills, experience, education, and projects.

---

## 🧠 AI & LLM Capabilities

<details>
<summary><b>💬 Chat Assistant Features</b> (Click to expand)</summary>

* **Memory Type:** Persistent conversation history with MongoDB storage.
* **Session Management:** Auto-loads previous sessions on login.
* **Architecture:** LangChain `RunnableWithMessageHistory` paired with a MongoDB backend.
* **Response Time:** Sub-second responses powered by Groq API.
* **Use Cases:** Mock interviews, behavioral prep, skill recommendations, and resume tweaks.
</details>

<details>
<summary><b>🔍 Embeddings & RAG (Retrieval-Augmented Generation)</b> (Click to expand)</summary>

* **Hugging Face Embeddings:** Uses `all-MiniLM-L6-v2` (384-dimensional vectors) for accurate semantic matching.
* **Vector Search (FAISS):** Fast semantic search across resume chunks (500-character chunks with 100-character overlap) to prevent LLM hallucination.
* **RAG Workflow:** 
  1. Uploaded resume is parsed into chunks.
  2. Vectors are stored in a FAISS index and cached.
  3. Job description is semantically compared against chunks.
  4. Top 5 matching sections are retrieved and passed to the LLM for precise scoring and feedback.
</details>

---

## 🏗️ System Architecture

```text
├── AuthService/                    # User authentication & registration
│   ├── api/                        # Login, Register, Password Reset routes
│   ├── controllers/                # Email verification & OTP services
│   └── schemas/                    # Pydantic validation schemas
├── JobMatching/                    # Resume-Job Matching (Score & Feedback)
│   ├── analyser/                   # Core matching logic
│   └── resumeCompare/              # LLM and RAG-based comparison engines
├── interviewService/               # Interview Question Generation
├── chat_agent/                     # AI Chat Assistant (LangChain + Groq)
├── ResumeService/                  # Resume Management (Upload, Parse, Delete)
├── Models/                         # MongoEngine Database Models (User, Resume, Chat)
├── middlewares/                    # Custom Auth & Rate-limiting middlewares
├── Dbconfig/                       # MongoDB configuration
├── Frontend/                       # Next.js React Frontend (If included in repo)
├── app.py                          # Main FastAPI application entrypoint
└── requirements.txt                # Python dependencies
```

---

## 🚀 Installation & Setup

### Prerequisites
* **Python 3.8+**
* **MongoDB** (running locally or via Atlas)
* **GROQ API Key** (for fast LLM capabilities)
* **Hugging Face Token** (for Embeddings)

### 1. Clone & Navigate
```bash
git clone https://github.com/yourusername/Interviewcoach-Ai.git
cd "InterviewCoach AI"
```

### 2. Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
MONGODB_URI=mongodb://localhost:27017/interviewcoach
JWT_SECRET=your_secret_key_here
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```
> *Get your free `HF_TOKEN` from [Hugging Face Settings](https://huggingface.co/settings/tokens).*

### 5. Start MongoDB
Ensure MongoDB is running on your system (`mongod`, `brew services start mongodb-community`, or `sudo systemctl start mongod`).

### 6. Run the Application
```bash
uvicorn app:app --reload
```
API runs at: `http://localhost:8000`

### 7. View API Docs
Navigate to **[http://localhost:8000/docs](http://localhost:8000/docs)** for the Swagger UI.

---

## 📡 API Reference

### 🔐 Authentication
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Login and receive JWT token |
| `POST` | `/auth/reset-password` | Reset account password |
| `POST` | `/auth/verify-otp` | Verify email OTP |

### 📄 Resumes
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/resume/upload` | Upload resume (PDF/DOCX) |
| `GET` | `/api/resume/get/{id}` | Get parsed resume data |
| `DELETE` | `/api/resume/delete/{id}` | Delete a resume |

### 🤖 Job Matching & AI
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/jobmatching/analyseresume` | Score resume against job description |
| `POST` | `/api/interviewservice/generate` | Generate 10 role-specific questions |

### 💬 Chat Agent
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/chat/create-session` | Start a new AI chat session |
| `POST` | `/api/chat/send-message` | Send message & get AI response |
| `GET` | `/api/chat/sessions` | List all chat sessions |
| `GET` | `/api/chat/session/{id}` | Get full chat history |

---

## 📊 Typical Workflow

1. **Auth:** `POST /auth/login` to get a JWT token.
2. **Upload:** `POST /api/resume/upload` to store your resume and extract skills.
3. **Match:** `POST /api/jobmatching/analyseresume` with your `resume_id` and a target Job Description to get an eligibility score.
4. **Prepare:** `POST /api/interviewservice/generate` to get highly targeted practice questions.
5. **Practice:** Create a Chat Session (`POST /api/chat/create-session`) and practice answering the questions with the AI Agent (`POST /api/chat/send-message`). 

---

## 🔐 Security

* **JWT Authentication:** Secure, token-based authentication with expiration mechanisms.
* **Password Hashing:** Robust encryption for user credentials.
* **OTP Verification:** Secure email verification for registration and password resets.
* **Middleware Protection:** Custom rate-limiting and authorization layers.

---

## 🎯 Roadmap

- [x] Resume parsing, analysis & job matching
- [x] Context-aware interview question generation
- [x] JWT User authentication & secure resume management
- [x] AI Chat Assistant with MongoDB memory
- [ ] Support for multiple resume versions per user
- [ ] Improved parsing for complex PDF/DOCX layouts
- [ ] Real-time interview mock sessions (Voice/Video)
- [ ] Performance metrics and analytics dashboard
- [ ] Multi-language support

---

<div align="center">
  <b>Built with ❤️ by the Interview Coach AI Team</b><br>
  <i>Last Updated: April 2026</i>
</div>
