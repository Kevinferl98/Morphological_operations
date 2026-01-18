class AppError(Exception):
    status_code = 500

    def __init__(self, message=None):
        super().__init__(message)
        self.message = message or "Internal server error"

class ValidationError(AppError):
    status_code = 422
    def __init__(self, message="Validation error"):
        super().__init__(message)

class BadRequestError(AppError):
    status_code = 400
    def __init__(self, message="Bad request"):
        super().__init__(message)

class NotFoundError(AppError):
    status_code = 404
    def __init__(self, message="Resource not found"):
        super().__init__(message)