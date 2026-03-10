from fastapi import HTTPException


class APIError(HTTPException):

    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: str = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "error": message,
                "error_code": error_code
            }
        )