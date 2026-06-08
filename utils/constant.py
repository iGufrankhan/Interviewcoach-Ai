
"""
Centralized configuration constants loaded from environment variables.
All environment variables are loaded here and imported by other modules.
"""
import os

# ========== JWT/Authentication ==========
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_KEY = os.getenv("ACCESS_TOKEN_KEY")
REFRESH_TOKEN_KEY = os.getenv("REFRESH_TOKEN_KEY")
ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", "3600"))
REFRESH_TOKEN_EXPIRE_SECONDS = int(os.getenv("REFRESH_TOKEN_EXPIRE_SECONDS", "604800"))

# ========== Database ==========
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017/interviewcoach")
DATABASE_NAME = os.getenv("DATABASE_NAME", "interviewcoach")

# ========== Email Service (Gmail) ==========
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

# ========== External APIs ==========
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ========== Server Configuration ==========
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# ========== File Upload Configuration ==========
MAX_FILE_UPLOAD_SIZE = int(os.getenv("MAX_FILE_UPLOAD_SIZE", "10485760"))  # 10MB default

# ========== CORS Configuration ==========
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS", 
    "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001,https://interviewcoach-ai-frontend-sb7x.vercel.app"
).split(",")


RAG_CHUNK_SIZE = int(os.getenv("RAG_CHUNK_SIZE", "500"))
RAG_CHUNK_OVERLAP = int(os.getenv("RAG_CHUNK_OVERLAP", "100"))
RAG_RETRIEVER_K = int(os.getenv("RAG_RETRIEVER_K", "5"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
HF_TOKEN = os.getenv("HF_TOKEN")
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour expiration (in seconds)   





