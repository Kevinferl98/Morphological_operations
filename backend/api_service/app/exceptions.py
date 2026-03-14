from fastapi import HTTPException

class AppError(HTTPException):
    def __init__(self, message="Internal server error", status_code=500):
        super().__init__(status_code=status_code, detail=message)

class ValidationError(AppError):
    def __init__(self, message="Validation error"):
        super().__init__(message, status_code=422)

class BadRequestError(AppError):
    def __init__(self, message="Bad request"):
        super().__init__(message, status_code=400)

class NotFoundError(AppError):
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)