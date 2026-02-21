from fastapi import HTTPException, status
from typing import Any

class AppException(HTTPException):
    def __init__(self, status_code: int, error: str, code: str, details: Any = None):
        super().__init__(status_code=status_code, detail={
            "error": error,
            "code": code,
            "details": details or {}
        })

class NotFoundException(AppException):
    def __init__(self, resource: str, id: Any):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error=f"{resource} not found",
            code="NOT_FOUND",
            details={"resource": resource, "id": id}
        )

class AlreadyExistsException(AppException):
    def __init__(self, resource: str, field: str, value: Any):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error=f"{resource} already exists",
            code="ALREADY_EXISTS",
            details={"resource": resource, "field": field, "value": value}
        )

class ValidationException(AppException):
    def __init__(self, message: str, details: Any = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error=message,
            code="VALIDATION_ERROR",
            details=details
        )

class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error=message,
            code="UNAUTHORIZED",
            details={}
        )

class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error=message,
            code="FORBIDDEN",
            details={}
        )
