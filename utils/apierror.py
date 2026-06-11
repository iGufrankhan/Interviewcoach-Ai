from fastapi import HTTPException
from utils.error_codes import ErrorCode, ERROR_CODE_TO_STATUS, ERROR_MESSAGES


class APIError(HTTPException):
    def __init__(
        self,
        error_code: str,
        message: str = None,
        status_code: int = None,
        internal_message: str = None
    ):
        # Auto-determine status code from error code if not provided
        if status_code is None:
            status_code = ERROR_CODE_TO_STATUS.get(error_code, 500)
        
        # Use provided message or default user-friendly message
        if message is None:
            message = ERROR_MESSAGES.get(error_code, "An error occurred. Please try again.")
        
        self.error_code = error_code
        self.message = message
        self.internal_message = internal_message
        
        super().__init__(
            status_code=status_code,
            detail={
                "success": False,
                "message": message,
                "error_code": error_code
            }
        )