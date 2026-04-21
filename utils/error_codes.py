"""
Standardized error codes for the application.
Used for structured error responses and frontend error handling.
"""

class ErrorCode:
    """Standardized error codes"""
    
    # Authentication errors (4xx)
    UNAUTHORIZED = "UNAUTHORIZED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INVALID_TOKEN = "INVALID_TOKEN"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    EMAIL_NOT_VERIFIED = "EMAIL_NOT_VERIFIED"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"
    USERNAME_ALREADY_EXISTS = "USERNAME_ALREADY_EXISTS"
    INVALID_OTP = "INVALID_OTP"
    OTP_EXPIRED = "OTP_EXPIRED"
    
    # Validation errors (4xx)
    INVALID_INPUT = "INVALID_INPUT"
    MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
    INVALID_EMAIL = "INVALID_EMAIL"
    INVALID_PASSWORD = "INVALID_PASSWORD"
    PASSWORD_MISMATCH = "PASSWORD_MISMATCH"
    INVALID_FILE_TYPE = "INVALID_FILE_TYPE"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    INVALID_RESUME_ID = "INVALID_RESUME_ID"
    INVALID_JOB_DESCRIPTION = "INVALID_JOB_DESCRIPTION"
    
    # Resource not found (4xx)
    NOT_FOUND = "NOT_FOUND"
    RESUME_NOT_FOUND = "RESUME_NOT_FOUND"
    USER_RESUME_NOT_FOUND = "USER_RESUME_NOT_FOUND"
    CHAT_SESSION_NOT_FOUND = "CHAT_SESSION_NOT_FOUND"
    
    # Permission errors (4xx)
    FORBIDDEN = "FORBIDDEN"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"
    
    # Rate limit errors (4xx)
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS"
    
    # Processing errors (5xx)
    PROCESSING_ERROR = "PROCESSING_ERROR"
    RESUME_PROCESSING_FAILED = "RESUME_PROCESSING_FAILED"
    ANALYSIS_FAILED = "ANALYSIS_FAILED"
    QUESTION_GENERATION_FAILED = "QUESTION_GENERATION_FAILED"
    CHAT_FAILED = "CHAT_FAILED"
    
    # Server errors (5xx)
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    MISSING_API_KEY = "MISSING_API_KEY"
    MISSING_CONFIGURATION = "MISSING_CONFIGURATION"


class HttpStatusCode:
    """HTTP status codes"""
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


# Mapping of error codes to status codes
ERROR_CODE_TO_STATUS = {
    # Authentication (401)
    ErrorCode.UNAUTHORIZED: HttpStatusCode.UNAUTHORIZED,
    ErrorCode.INVALID_CREDENTIALS: HttpStatusCode.UNAUTHORIZED,
    ErrorCode.INVALID_TOKEN: HttpStatusCode.UNAUTHORIZED,
    ErrorCode.TOKEN_EXPIRED: HttpStatusCode.UNAUTHORIZED,
    ErrorCode.EMAIL_NOT_VERIFIED: HttpStatusCode.UNAUTHORIZED,
    ErrorCode.INVALID_OTP: HttpStatusCode.UNAUTHORIZED,
    ErrorCode.OTP_EXPIRED: HttpStatusCode.UNAUTHORIZED,
    
    # Not found (404)
    ErrorCode.NOT_FOUND: HttpStatusCode.NOT_FOUND,
    ErrorCode.RESUME_NOT_FOUND: HttpStatusCode.NOT_FOUND,
    ErrorCode.USER_NOT_FOUND: HttpStatusCode.NOT_FOUND,
    ErrorCode.USER_RESUME_NOT_FOUND: HttpStatusCode.NOT_FOUND,
    ErrorCode.CHAT_SESSION_NOT_FOUND: HttpStatusCode.NOT_FOUND,
    
    # Forbidden (403)
    ErrorCode.FORBIDDEN: HttpStatusCode.FORBIDDEN,
    ErrorCode.INSUFFICIENT_PERMISSIONS: HttpStatusCode.FORBIDDEN,
    
    # Conflict (409)
    ErrorCode.EMAIL_ALREADY_EXISTS: HttpStatusCode.CONFLICT,
    ErrorCode.USERNAME_ALREADY_EXISTS: HttpStatusCode.CONFLICT,
    
    # Too many requests (429)
    ErrorCode.RATE_LIMIT_EXCEEDED: HttpStatusCode.TOO_MANY_REQUESTS,
    ErrorCode.TOO_MANY_REQUESTS: HttpStatusCode.TOO_MANY_REQUESTS,
    
    # Validation & Bad requests (400)
    ErrorCode.INVALID_INPUT: HttpStatusCode.BAD_REQUEST,
    ErrorCode.MISSING_REQUIRED_FIELD: HttpStatusCode.BAD_REQUEST,
    ErrorCode.INVALID_EMAIL: HttpStatusCode.BAD_REQUEST,
    ErrorCode.INVALID_PASSWORD: HttpStatusCode.BAD_REQUEST,
    ErrorCode.PASSWORD_MISMATCH: HttpStatusCode.BAD_REQUEST,
    ErrorCode.INVALID_FILE_TYPE: HttpStatusCode.BAD_REQUEST,
    ErrorCode.FILE_TOO_LARGE: HttpStatusCode.BAD_REQUEST,
    ErrorCode.INVALID_RESUME_ID: HttpStatusCode.BAD_REQUEST,
    ErrorCode.INVALID_JOB_DESCRIPTION: HttpStatusCode.BAD_REQUEST,
}


# User-friendly error messages (hide implementation details)
ERROR_MESSAGES = {
    ErrorCode.UNAUTHORIZED: "You are not authorized to access this resource.",
    ErrorCode.INVALID_CREDENTIALS: "Invalid email or password.",
    ErrorCode.INVALID_TOKEN: "Your session has expired. Please log in again.",
    ErrorCode.TOKEN_EXPIRED: "Your session has expired. Please log in again.",
    ErrorCode.EMAIL_NOT_VERIFIED: "Please verify your email before logging in.",
    ErrorCode.USER_NOT_FOUND: "User not found.",
    ErrorCode.EMAIL_ALREADY_EXISTS: "An account with this email already exists.",
    ErrorCode.USERNAME_ALREADY_EXISTS: "This username is already taken.",
    ErrorCode.INVALID_OTP: "Invalid OTP. Please try again.",
    ErrorCode.OTP_EXPIRED: "OTP has expired. Please request a new one.",
    
    ErrorCode.INVALID_INPUT: "Invalid input provided.",
    ErrorCode.MISSING_REQUIRED_FIELD: "Required field is missing.",
    ErrorCode.INVALID_EMAIL: "Please enter a valid email address.",
    ErrorCode.INVALID_PASSWORD: "Password does not meet requirements.",
    ErrorCode.PASSWORD_MISMATCH: "Passwords do not match.",
    ErrorCode.INVALID_FILE_TYPE: "Invalid file type. Please upload a PDF, DOCX, or TXT file.",
    ErrorCode.FILE_TOO_LARGE: "File size exceeds the maximum limit of 5MB.",
    ErrorCode.INVALID_RESUME_ID: "Invalid resume ID.",
    ErrorCode.INVALID_JOB_DESCRIPTION: "Please provide a valid job description (minimum 50 characters).",
    
    ErrorCode.NOT_FOUND: "Resource not found.",
    ErrorCode.RESUME_NOT_FOUND: "Resume not found.",
    ErrorCode.USER_RESUME_NOT_FOUND: "Resume not found for this user.",
    ErrorCode.CHAT_SESSION_NOT_FOUND: "Chat session not found.",
    
    ErrorCode.FORBIDDEN: "You do not have permission to access this resource.",
    ErrorCode.INSUFFICIENT_PERMISSIONS: "You do not have permission to perform this action.",
    
    ErrorCode.RATE_LIMIT_EXCEEDED: "Too many requests. Please try again later.",
    ErrorCode.TOO_MANY_REQUESTS: "Too many requests. Please try again later.",
    
    ErrorCode.PROCESSING_ERROR: "An error occurred while processing your request.",
    ErrorCode.RESUME_PROCESSING_FAILED: "Failed to process resume. Please try again.",
    ErrorCode.ANALYSIS_FAILED: "Failed to analyze resume. Please try again.",
    ErrorCode.QUESTION_GENERATION_FAILED: "Failed to generate interview questions. Please try again.",
    ErrorCode.CHAT_FAILED: "Failed to process chat message. Please try again.",
    
    ErrorCode.INTERNAL_SERVER_ERROR: "An unexpected error occurred. Please try again later.",
    ErrorCode.DATABASE_ERROR: "Database error. Please try again later.",
    ErrorCode.EXTERNAL_SERVICE_ERROR: "External service error. Please try again later.",
    ErrorCode.MISSING_API_KEY: "Configuration error. Please contact support.",
    ErrorCode.MISSING_CONFIGURATION: "Configuration error. Please contact support.",
}
