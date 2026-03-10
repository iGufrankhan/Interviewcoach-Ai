from fastapi.responses import JSONResponse


def success_response(
    message: str = "Success",
    data=None,
    status_code: int = 200
):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data
        }
    )


def error_response(
    message: str = "Error",
    error_code: str = None,
    status_code: int = 400
):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "error_code": error_code
        }
    )