from fastapi import HTTPException, status


class AppException(Exception):
    """Base application exception."""
    
    def __init__(self, message: str, error_code: str, status_code: int = 400):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, "NOT_FOUND", 404)


class ValidationError(AppException):
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR", 400)


class AppointmentConflictError(AppException):
    def __init__(self, message: str = "Time slot unavailable"):
        super().__init__(message, "APPOINTMENT_CONFLICT", 409)


class ProviderUnavailableError(AppException):
    def __init__(self, message: str = "Provider not available"):
        super().__init__(message, "PROVIDER_UNAVAILABLE", 400)


class InvalidTransitionError(AppException):
    def __init__(self, message: str):
        super().__init__(message, "INVALID_TRANSITION", 400)


class UnauthorizedError(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, "UNAUTHORIZED", 401)


class ForbiddenError(AppException):
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, "FORBIDDEN", 403)
