"""
Error handling middleware and custom exceptions
Provides centralized error handling with detailed logging
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import Any, Dict, Optional
import logging
import traceback
from datetime import datetime

logger = logging.getLogger(__name__)


class AppException(Exception):
    """Base application exception"""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(AppException):
    """Validation error exception"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
            details=details
        )


class AuthenticationException(AppException):
    """Authentication error exception"""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="AUTHENTICATION_ERROR"
        )


class AuthorizationException(AppException):
    """Authorization error exception"""
    
    def __init__(self, message: str = "Access denied"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="AUTHORIZATION_ERROR"
        )


class NotFoundException(AppException):
    """Resource not found exception"""
    
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            message=f"{resource} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND"
        )


class ConflictException(AppException):
    """Resource conflict exception"""
    
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT"
        )


class RateLimitException(AppException):
    """Rate limit exceeded exception"""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_EXCEEDED"
        )


def setup_error_handlers(app: FastAPI):
    """Setup error handlers for the application"""
    
    @app.exception_handler(AppException)
    async def handle_app_exception(request: Request, exc: AppException):
        """Handle custom application exceptions"""
        logger.warning(
            f"Application exception: {exc.error_code} - {exc.message}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "error_code": exc.error_code,
                "status_code": exc.status_code
            }
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.message,
                "code": exc.error_code,
                "details": exc.details,
                "timestamp": datetime.utcnow().isoformat(),
                "path": request.url.path
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        """Handle request validation errors"""
        errors = []
        for error in exc.errors():
            errors.append({
                "field": ".".join(str(x) for x in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })
        
        logger.warning(
            f"Validation error: {len(errors)} field(s) failed validation",
            extra={
                "path": request.url.path,
                "method": request.method,
                "errors": errors
            }
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "Validation failed",
                "code": "VALIDATION_ERROR",
                "details": {"fields": errors},
                "timestamp": datetime.utcnow().isoformat(),
                "path": request.url.path
            }
        )
    
    @app.exception_handler(SQLAlchemyError)
    async def handle_database_error(request: Request, exc: SQLAlchemyError):
        """Handle database errors"""
        error_message = str(exc)
        
        # Check for specific database errors
        if isinstance(exc, IntegrityError):
            if "unique constraint" in error_message.lower():
                message = "Resource already exists"
                status_code = status.HTTP_409_CONFLICT
                error_code = "DUPLICATE_RESOURCE"
            else:
                message = "Database constraint violation"
                status_code = status.HTTP_400_BAD_REQUEST
                error_code = "CONSTRAINT_VIOLATION"
        else:
            message = "Database error occurred"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            error_code = "DATABASE_ERROR"
        
        logger.error(
            f"Database error: {error_message}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "error_type": type(exc).__name__
            },
            exc_info=True
        )
        
        return JSONResponse(
            status_code=status_code,
            content={
                "error": message,
                "code": error_code,
                "details": {} if status_code >= 500 else {"message": error_message},
                "timestamp": datetime.utcnow().isoformat(),
                "path": request.url.path
            }
        )
    
    @app.exception_handler(Exception)
    async def handle_generic_exception(request: Request, exc: Exception):
        """Handle all unhandled exceptions"""
        logger.error(
            f"Unhandled exception: {str(exc)}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "exception_type": type(exc).__name__
            },
            exc_info=True
        )
        
        # In production, don't expose internal details
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal server error",
                "code": "INTERNAL_ERROR",
                "details": {},
                "timestamp": datetime.utcnow().isoformat(),
                "path": request.url.path
            }
        )


class ErrorResponse:
    """Helper class for creating error responses"""
    
    @staticmethod
    def validation_error(field: str, message: str) -> Dict[str, Any]:
        return {
            "error": "Validation failed",
            "code": "VALIDATION_ERROR",
            "details": {
                "fields": [{"field": field, "message": message}]
            }
        }
    
    @staticmethod
    def not_found(resource: str = "Resource") -> Dict[str, Any]:
        return {
            "error": f"{resource} not found",
            "code": "NOT_FOUND"
        }
    
    @staticmethod
    def unauthorized() -> Dict[str, Any]:
        return {
            "error": "Authentication required",
            "code": "UNAUTHORIZED"
        }
    
    @staticmethod
    def forbidden() -> Dict[str, Any]:
        return {
            "error": "Access denied",
            "code": "FORBIDDEN"
        }
    
    @staticmethod
    def conflict(message: str = "Resource conflict") -> Dict[str, Any]:
        return {
            "error": message,
            "code": "CONFLICT"
        }
    
    @staticmethod
    def rate_limit() -> Dict[str, Any]:
        return {
            "error": "Rate limit exceeded. Please try again later.",
            "code": "RATE_LIMIT_EXCEEDED"
        }
