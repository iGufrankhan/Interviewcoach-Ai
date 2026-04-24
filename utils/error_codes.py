"""
Standardized error codes for the application.
Used for structured error responses and frontend error handling.
Includes granular error codes for precise error handling and client feedback.
"""

class ErrorCode:
    """Standardized error codes for all application errors"""
    
    # ===== Authentication Errors (401, 400) =====
    UNAUTHORIZED = "UNAUTHORIZED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INVALID_TOKEN = "INVALID_TOKEN"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    TOKEN_INVALID_SIGNATURE = "TOKEN_INVALID_SIGNATURE"
    EMAIL_NOT_VERIFIED = "EMAIL_NOT_VERIFIED"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"
    USERNAME_ALREADY_EXISTS = "USERNAME_ALREADY_EXISTS"
    INVALID_OTP = "INVALID_OTP"
    OTP_EXPIRED = "OTP_EXPIRED"
    OTP_MAX_ATTEMPTS = "OTP_MAX_ATTEMPTS"
    PASSWORD_WEAK = "PASSWORD_WEAK"
    ACCOUNT_LOCKED = "ACCOUNT_LOCKED"
    ACCOUNT_SUSPENDED = "ACCOUNT_SUSPENDED"
    
    # ===== Validation Errors (400) =====
    INVALID_INPUT = "INVALID_INPUT"
    MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
    INVALID_EMAIL = "INVALID_EMAIL"
    INVALID_PASSWORD = "INVALID_PASSWORD"
    PASSWORD_MISMATCH = "PASSWORD_MISMATCH"
    INVALID_PHONE = "INVALID_PHONE"
    INVALID_DATE_FORMAT = "INVALID_DATE_FORMAT"
    INVALID_FILE_TYPE = "INVALID_FILE_TYPE"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    FILE_EMPTY = "FILE_EMPTY"
    INVALID_RESUME_ID = "INVALID_RESUME_ID"
    INVALID_JOB_DESCRIPTION = "INVALID_JOB_DESCRIPTION"
    JOB_DESCRIPTION_TOO_SHORT = "JOB_DESCRIPTION_TOO_SHORT"
    INVALID_JSON = "INVALID_JSON"
    INVALID_QUERY_PARAMS = "INVALID_QUERY_PARAMS"
    
    # ===== Resource Not Found (404) =====
    NOT_FOUND = "NOT_FOUND"
    RESUME_NOT_FOUND = "RESUME_NOT_FOUND"
    USER_RESUME_NOT_FOUND = "USER_RESUME_NOT_FOUND"
    CHAT_SESSION_NOT_FOUND = "CHAT_SESSION_NOT_FOUND"
    INTERVIEW_SESSION_NOT_FOUND = "INTERVIEW_SESSION_NOT_FOUND"
    USER_NOT_FOUND_BY_ID = "USER_NOT_FOUND_BY_ID"
    ENDPOINT_NOT_FOUND = "ENDPOINT_NOT_FOUND"
    
    # ===== Permission/Authorization Errors (403) =====
    FORBIDDEN = "FORBIDDEN"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"
    RESOURCE_OWNER_ONLY = "RESOURCE_OWNER_ONLY"
    ADMIN_REQUIRED = "ADMIN_REQUIRED"
    
    # ===== Resource Conflict (409) =====
    RESOURCE_ALREADY_EXISTS = "RESOURCE_ALREADY_EXISTS"
    DUPLICATE_ENTRY = "DUPLICATE_ENTRY"
    RESOURCE_IN_USE = "RESOURCE_IN_USE"
    
    # ===== Rate Limiting (429) =====
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS"
    TOO_MANY_LOGIN_ATTEMPTS = "TOO_MANY_LOGIN_ATTEMPTS"
    TOO_MANY_OTP_REQUESTS = "TOO_MANY_OTP_REQUESTS"
    
    # ===== Processing/Business Logic Errors (400-422) =====
    PROCESSING_ERROR = "PROCESSING_ERROR"
    RESUME_PROCESSING_FAILED = "RESUME_PROCESSING_FAILED"
    RESUME_PARSING_FAILED = "RESUME_PARSING_FAILED"
    TEXT_EXTRACTION_FAILED = "TEXT_EXTRACTION_FAILED"
    ANALYSIS_FAILED = "ANALYSIS_FAILED"
    QUESTION_GENERATION_FAILED = "QUESTION_GENERATION_FAILED"
    CHAT_FAILED = "CHAT_FAILED"
    TRANSCRIPTION_FAILED = "TRANSCRIPTION_FAILED"
    AUDIO_NOT_RECOGNIZED = "AUDIO_NOT_RECOGNIZED"
    INVALID_AUDIO_FORMAT = "INVALID_AUDIO_FORMAT"
    AUDIO_TOO_LONG = "AUDIO_TOO_LONG"
    AUDIO_TOO_SHORT = "AUDIO_TOO_SHORT"
    EMPTY_AUDIO = "EMPTY_AUDIO"
    MATCHING_FAILED = "MATCHING_FAILED"
    EMBEDDING_FAILED = "EMBEDDING_FAILED"
    
    # ===== Configuration/Setup Errors (500) =====
    MISSING_API_KEY = "MISSING_API_KEY"
    MISSING_CONFIGURATION = "MISSING_CONFIGURATION"
    INVALID_CONFIGURATION = "INVALID_CONFIGURATION"
    ENVIRONMENT_NOT_SET = "ENVIRONMENT_NOT_SET"
    
    # ===== External Service Errors (502-503) =====
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    GROQ_API_ERROR = "GROQ_API_ERROR"
    HUGGINGFACE_API_ERROR = "HUGGINGFACE_API_ERROR"
    SPEECH_SERVICE_ERROR = "SPEECH_SERVICE_ERROR"
    EMAIL_SERVICE_ERROR = "EMAIL_SERVICE_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    TIMEOUT = "TIMEOUT"
    
    # ===== Database Errors (500) =====
    DATABASE_ERROR = "DATABASE_ERROR"
    DATABASE_CONNECTION_FAILED = "DATABASE_CONNECTION_FAILED"
    QUERY_FAILED = "QUERY_FAILED"
    DOCUMENT_NOT_FOUND = "DOCUMENT_NOT_FOUND"
    TRANSACTION_FAILED = "TRANSACTION_FAILED"
    
    # ===== Server Errors (500) =====
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"
    SERVER_INITIALIZATION_FAILED = "SERVER_INITIALIZATION_FAILED"


class HttpStatusCode:
    """HTTP status codes"""
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504


# Mapping of error codes to HTTP status codes
ERROR_CODE_TO_STATUS = {
    # Authentication (401)
    ErrorCode.UNAUTHORIZED: HttpStatusCode.UNAUTHORIZED,
    ErrorCode.INVALID_CREDENTIALS: HttpStatusCode.UNAUTHORIZED,
    ErrorCode.INVALID_TOKEN: HttpStatusCode.UNAUTHORIZED,
    ErrorCode.TOKEN_EXPIRED: HttpStatusCode.UNAUTHORIZED,
    ErrorCode.TOKEN_INVALID_SIGNATURE: HttpStatusCode.UNAUTHORIZED,
    ErrorCode.EMAIL_NOT_VERIFIED: HttpStatusCode.UNAUTHORIZED,
    ErrorCode.ACCOUNT_LOCKED: HttpStatusCode.UNAUTHORIZED,
    ErrorCode.ACCOUNT_SUSPENDED: HttpStatusCode.UNAUTHORIZED,
    ErrorCode.OTP_MAX_ATTEMPTS: HttpStatusCode.UNAUTHORIZED,
    
    # Not found (404)
    ErrorCode.NOT_FOUND: HttpStatusCode.NOT_FOUND,
    ErrorCode.RESUME_NOT_FOUND: HttpStatusCode.NOT_FOUND,
    ErrorCode.USER_NOT_FOUND: HttpStatusCode.NOT_FOUND,
    ErrorCode.USER_NOT_FOUND_BY_ID: HttpStatusCode.NOT_FOUND,
    ErrorCode.USER_RESUME_NOT_FOUND: HttpStatusCode.NOT_FOUND,
    ErrorCode.CHAT_SESSION_NOT_FOUND: HttpStatusCode.NOT_FOUND,
    ErrorCode.INTERVIEW_SESSION_NOT_FOUND: HttpStatusCode.NOT_FOUND,
    ErrorCode.ENDPOINT_NOT_FOUND: HttpStatusCode.NOT_FOUND,
    
    # Forbidden (403)
    ErrorCode.FORBIDDEN: HttpStatusCode.FORBIDDEN,
    ErrorCode.INSUFFICIENT_PERMISSIONS: HttpStatusCode.FORBIDDEN,
    ErrorCode.RESOURCE_OWNER_ONLY: HttpStatusCode.FORBIDDEN,
    ErrorCode.ADMIN_REQUIRED: HttpStatusCode.FORBIDDEN,
    
    # Conflict (409)
    ErrorCode.EMAIL_ALREADY_EXISTS: HttpStatusCode.CONFLICT,
    ErrorCode.USERNAME_ALREADY_EXISTS: HttpStatusCode.CONFLICT,
    ErrorCode.RESOURCE_ALREADY_EXISTS: HttpStatusCode.CONFLICT,
    ErrorCode.DUPLICATE_ENTRY: HttpStatusCode.CONFLICT,
    ErrorCode.RESOURCE_IN_USE: HttpStatusCode.CONFLICT,
    
    # Too many requests (429)
    ErrorCode.RATE_LIMIT_EXCEEDED: HttpStatusCode.TOO_MANY_REQUESTS,
    ErrorCode.TOO_MANY_REQUESTS: HttpStatusCode.TOO_MANY_REQUESTS,
    ErrorCode.TOO_MANY_LOGIN_ATTEMPTS: HttpStatusCode.TOO_MANY_REQUESTS,
    ErrorCode.TOO_MANY_OTP_REQUESTS: HttpStatusCode.TOO_MANY_REQUESTS,
    
    # Validation & Bad requests (400)
    ErrorCode.INVALID_INPUT: HttpStatusCode.BAD_REQUEST,
    ErrorCode.MISSING_REQUIRED_FIELD: HttpStatusCode.BAD_REQUEST,
    ErrorCode.INVALID_EMAIL: HttpStatusCode.BAD_REQUEST,
    ErrorCode.INVALID_PASSWORD: HttpStatusCode.BAD_REQUEST,
    ErrorCode.PASSWORD_WEAK: HttpStatusCode.BAD_REQUEST,
    ErrorCode.PASSWORD_MISMATCH: HttpStatusCode.BAD_REQUEST,
    ErrorCode.INVALID_PHONE: HttpStatusCode.BAD_REQUEST,
    ErrorCode.INVALID_DATE_FORMAT: HttpStatusCode.BAD_REQUEST,
    ErrorCode.INVALID_FILE_TYPE: HttpStatusCode.BAD_REQUEST,
    ErrorCode.FILE_TOO_LARGE: HttpStatusCode.BAD_REQUEST,
    ErrorCode.FILE_EMPTY: HttpStatusCode.BAD_REQUEST,
    ErrorCode.INVALID_RESUME_ID: HttpStatusCode.BAD_REQUEST,
    ErrorCode.INVALID_JOB_DESCRIPTION: HttpStatusCode.BAD_REQUEST,
    ErrorCode.JOB_DESCRIPTION_TOO_SHORT: HttpStatusCode.BAD_REQUEST,
    ErrorCode.INVALID_JSON: HttpStatusCode.BAD_REQUEST,
    ErrorCode.INVALID_QUERY_PARAMS: HttpStatusCode.BAD_REQUEST,
    ErrorCode.INVALID_OTP: HttpStatusCode.BAD_REQUEST,
    ErrorCode.OTP_EXPIRED: HttpStatusCode.BAD_REQUEST,
    ErrorCode.INVALID_AUDIO_FORMAT: HttpStatusCode.BAD_REQUEST,
    ErrorCode.EMPTY_AUDIO: HttpStatusCode.BAD_REQUEST,
    
    # Processing errors (422 or 400)
    ErrorCode.PROCESSING_ERROR: HttpStatusCode.UNPROCESSABLE_ENTITY,
    ErrorCode.RESUME_PROCESSING_FAILED: HttpStatusCode.UNPROCESSABLE_ENTITY,
    ErrorCode.RESUME_PARSING_FAILED: HttpStatusCode.UNPROCESSABLE_ENTITY,
    ErrorCode.TEXT_EXTRACTION_FAILED: HttpStatusCode.UNPROCESSABLE_ENTITY,
    ErrorCode.ANALYSIS_FAILED: HttpStatusCode.UNPROCESSABLE_ENTITY,
    ErrorCode.QUESTION_GENERATION_FAILED: HttpStatusCode.UNPROCESSABLE_ENTITY,
    ErrorCode.CHAT_FAILED: HttpStatusCode.UNPROCESSABLE_ENTITY,
    ErrorCode.TRANSCRIPTION_FAILED: HttpStatusCode.UNPROCESSABLE_ENTITY,
    ErrorCode.AUDIO_NOT_RECOGNIZED: HttpStatusCode.BAD_REQUEST,
    ErrorCode.AUDIO_TOO_LONG: HttpStatusCode.BAD_REQUEST,
    ErrorCode.AUDIO_TOO_SHORT: HttpStatusCode.BAD_REQUEST,
    ErrorCode.MATCHING_FAILED: HttpStatusCode.UNPROCESSABLE_ENTITY,
    ErrorCode.EMBEDDING_FAILED: HttpStatusCode.UNPROCESSABLE_ENTITY,
    
    # External service errors (502-503)
    ErrorCode.EXTERNAL_SERVICE_ERROR: HttpStatusCode.SERVICE_UNAVAILABLE,
    ErrorCode.GROQ_API_ERROR: HttpStatusCode.SERVICE_UNAVAILABLE,
    ErrorCode.HUGGINGFACE_API_ERROR: HttpStatusCode.SERVICE_UNAVAILABLE,
    ErrorCode.SPEECH_SERVICE_ERROR: HttpStatusCode.SERVICE_UNAVAILABLE,
    ErrorCode.EMAIL_SERVICE_ERROR: HttpStatusCode.SERVICE_UNAVAILABLE,
    ErrorCode.SERVICE_UNAVAILABLE: HttpStatusCode.SERVICE_UNAVAILABLE,
    ErrorCode.TIMEOUT: HttpStatusCode.GATEWAY_TIMEOUT,
    
    # Database errors (500)
    ErrorCode.DATABASE_ERROR: HttpStatusCode.INTERNAL_SERVER_ERROR,
    ErrorCode.DATABASE_CONNECTION_FAILED: HttpStatusCode.INTERNAL_SERVER_ERROR,
    ErrorCode.QUERY_FAILED: HttpStatusCode.INTERNAL_SERVER_ERROR,
    ErrorCode.TRANSACTION_FAILED: HttpStatusCode.INTERNAL_SERVER_ERROR,
    
    # Configuration errors (500)
    ErrorCode.MISSING_API_KEY: HttpStatusCode.INTERNAL_SERVER_ERROR,
    ErrorCode.MISSING_CONFIGURATION: HttpStatusCode.INTERNAL_SERVER_ERROR,
    ErrorCode.INVALID_CONFIGURATION: HttpStatusCode.INTERNAL_SERVER_ERROR,
    ErrorCode.ENVIRONMENT_NOT_SET: HttpStatusCode.INTERNAL_SERVER_ERROR,
    ErrorCode.SERVER_INITIALIZATION_FAILED: HttpStatusCode.INTERNAL_SERVER_ERROR,
    
    # Server errors (500)
    ErrorCode.INTERNAL_SERVER_ERROR: HttpStatusCode.INTERNAL_SERVER_ERROR,
    ErrorCode.UNEXPECTED_ERROR: HttpStatusCode.INTERNAL_SERVER_ERROR,
}


# User-friendly error messages (hide implementation details)
# These are shown to users; internal messages go to logs only
ERROR_MESSAGES = {
    # Authentication
    ErrorCode.UNAUTHORIZED: "You are not authorized to access this resource.",
    ErrorCode.INVALID_CREDENTIALS: "Invalid email or password. Please try again.",
    ErrorCode.INVALID_TOKEN: "Your session has expired. Please log in again.",
    ErrorCode.TOKEN_EXPIRED: "Your session has expired. Please log in again.",
    ErrorCode.TOKEN_INVALID_SIGNATURE: "Invalid session token. Please log in again.",
    ErrorCode.EMAIL_NOT_VERIFIED: "Please verify your email before logging in.",
    ErrorCode.USER_NOT_FOUND: "User not found.",
    ErrorCode.EMAIL_ALREADY_EXISTS: "An account with this email already exists.",
    ErrorCode.USERNAME_ALREADY_EXISTS: "This username is already taken.",
    ErrorCode.INVALID_OTP: "Invalid OTP. Please try again.",
    ErrorCode.OTP_EXPIRED: "OTP has expired. Please request a new one.",
    ErrorCode.OTP_MAX_ATTEMPTS: "Too many OTP attempts. Please request a new OTP.",
    ErrorCode.PASSWORD_WEAK: "Password is too weak. Use at least 8 characters with uppercase, lowercase, and numbers.",
    ErrorCode.ACCOUNT_LOCKED: "Your account has been locked. Please contact support.",
    ErrorCode.ACCOUNT_SUSPENDED: "Your account has been suspended. Please contact support.",
    
    # Validation
    ErrorCode.INVALID_INPUT: "Invalid input provided. Please check your data.",
    ErrorCode.MISSING_REQUIRED_FIELD: "Required field is missing.",
    ErrorCode.INVALID_EMAIL: "Please enter a valid email address.",
    ErrorCode.INVALID_PASSWORD: "Password does not meet requirements.",
    ErrorCode.PASSWORD_MISMATCH: "Passwords do not match.",
    ErrorCode.INVALID_PHONE: "Please enter a valid phone number.",
    ErrorCode.INVALID_DATE_FORMAT: "Invalid date format. Please use YYYY-MM-DD.",
    ErrorCode.INVALID_FILE_TYPE: "Invalid file type. Please upload a PDF, DOCX, or TXT file.",
    ErrorCode.FILE_TOO_LARGE: "File size exceeds the maximum limit of 5MB.",
    ErrorCode.FILE_EMPTY: "File is empty. Please upload a file with content.",
    ErrorCode.INVALID_RESUME_ID: "Invalid resume ID.",
    ErrorCode.INVALID_JOB_DESCRIPTION: "Please provide a valid job description (minimum 50 characters).",
    ErrorCode.JOB_DESCRIPTION_TOO_SHORT: "Job description must be at least 50 characters.",
    ErrorCode.INVALID_JSON: "Invalid JSON format.",
    ErrorCode.INVALID_QUERY_PARAMS: "Invalid query parameters.",
    
    # Not found
    ErrorCode.NOT_FOUND: "Resource not found.",
    ErrorCode.RESUME_NOT_FOUND: "Resume not found.",
    ErrorCode.USER_NOT_FOUND_BY_ID: "User not found.",
    ErrorCode.USER_RESUME_NOT_FOUND: "Resume not found for this user.",
    ErrorCode.CHAT_SESSION_NOT_FOUND: "Chat session not found.",
    ErrorCode.INTERVIEW_SESSION_NOT_FOUND: "Interview session not found.",
    ErrorCode.ENDPOINT_NOT_FOUND: "Endpoint not found.",
    
    # Permission
    ErrorCode.FORBIDDEN: "You do not have permission to access this resource.",
    ErrorCode.INSUFFICIENT_PERMISSIONS: "You do not have permission to perform this action.",
    ErrorCode.RESOURCE_OWNER_ONLY: "You can only access your own resources.",
    ErrorCode.ADMIN_REQUIRED: "Administrator access required.",
    
    # Conflict
    ErrorCode.RESOURCE_ALREADY_EXISTS: "This resource already exists.",
    ErrorCode.DUPLICATE_ENTRY: "This entry already exists.",
    ErrorCode.RESOURCE_IN_USE: "This resource is currently in use.",
    
    # Rate limiting
    ErrorCode.RATE_LIMIT_EXCEEDED: "Too many requests. Please try again in a few moments.",
    ErrorCode.TOO_MANY_REQUESTS: "Too many requests. Please slow down and try again.",
    ErrorCode.TOO_MANY_LOGIN_ATTEMPTS: "Too many login attempts. Please try again later.",
    ErrorCode.TOO_MANY_OTP_REQUESTS: "Too many OTP requests. Please try again later.",
    
    # Processing
    ErrorCode.PROCESSING_ERROR: "Unable to process your request. Please try again.",
    ErrorCode.RESUME_PROCESSING_FAILED: "Failed to process resume. Please try uploading again.",
    ErrorCode.RESUME_PARSING_FAILED: "Unable to parse resume content. Please check the file format.",
    ErrorCode.TEXT_EXTRACTION_FAILED: "Failed to extract text from file.",
    ErrorCode.ANALYSIS_FAILED: "Analysis failed. Please try again.",
    ErrorCode.QUESTION_GENERATION_FAILED: "Failed to generate questions. Please try again.",
    ErrorCode.CHAT_FAILED: "Chat service failed. Please try again.",
    ErrorCode.TRANSCRIPTION_FAILED: "Failed to transcribe audio. Please try again or use text input.",
    ErrorCode.AUDIO_NOT_RECOGNIZED: "Could not understand audio. Please speak clearly and try again.",
    ErrorCode.INVALID_AUDIO_FORMAT: "Invalid audio format. Ensure audio is in WAV format.",
    ErrorCode.AUDIO_TOO_LONG: "Audio is too long. Please record less than 60 seconds.",
    ErrorCode.AUDIO_TOO_SHORT: "Audio is too short. Please record at least 3 seconds.",
    ErrorCode.EMPTY_AUDIO: "Please record some audio before submitting.",
    ErrorCode.MATCHING_FAILED: "Resume matching failed. Please try again.",
    ErrorCode.EMBEDDING_FAILED: "Failed to create embeddings. Please try again.",
    
    # External services
    ErrorCode.EXTERNAL_SERVICE_ERROR: "External service is unavailable. Please try again later.",
    ErrorCode.GROQ_API_ERROR: "AI service is temporarily unavailable. Please try again.",
    ErrorCode.HUGGINGFACE_API_ERROR: "Embedding service is temporarily unavailable. Please try again.",
    ErrorCode.SPEECH_SERVICE_ERROR: "Speech recognition service is temporarily unavailable. Please try again or use text.",
    ErrorCode.EMAIL_SERVICE_ERROR: "Email service is temporarily unavailable. Please try again later.",
    ErrorCode.SERVICE_UNAVAILABLE: "Service is temporarily unavailable. Please try again later.",
    ErrorCode.TIMEOUT: "Request timeout. Please try again.",
    
    # Database
    ErrorCode.DATABASE_ERROR: "Database error. Please try again.",
    ErrorCode.DATABASE_CONNECTION_FAILED: "Unable to connect to database. Please try again.",
    ErrorCode.QUERY_FAILED: "Database query failed. Please try again.",
    ErrorCode.TRANSACTION_FAILED: "Transaction failed. Please try again.",
    
    # Configuration
    ErrorCode.MISSING_API_KEY: "System configuration error. Please contact administrator.",
    ErrorCode.MISSING_CONFIGURATION: "System is not properly configured. Please contact administrator.",
    ErrorCode.INVALID_CONFIGURATION: "System configuration is invalid. Please contact administrator.",
    ErrorCode.ENVIRONMENT_NOT_SET: "System environment not set. Please contact administrator.",
    
    # Server
    ErrorCode.INTERNAL_SERVER_ERROR: "An unexpected error occurred. Please try again later.",
    ErrorCode.UNEXPECTED_ERROR: "An unexpected error occurred. Our team has been notified.",
    ErrorCode.SERVER_INITIALIZATION_FAILED: "Server failed to start. Please contact administrator.",
}
