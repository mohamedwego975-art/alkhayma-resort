"""
Security middleware for FastAPI application
Includes rate limiting, CORS protection, and security headers
"""

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
import time
from typing import Callable

# Configure logging
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


class SecurityMiddleware(BaseHTTPMiddleware):
    """Custom security middleware for adding security headers"""

    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()

        # Process request
        response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self' https://api.stripe.com;"
        )
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )

        # Add timing header for monitoring
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        return response


def setup_security_middleware(app: FastAPI, allowed_origins: list = None):
    """
    Setup all security middleware for the application

    Args:
        app: FastAPI application instance
        allowed_origins: List of allowed CORS origins (defaults to localhost variants)
    """

    if allowed_origins is None:
        allowed_origins = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "http://localhost",
            "http://frontend:5173",
            "http://frontend",
        ]

    # Add rate limiter to app
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Add custom security headers middleware (MUST be first for proper ordering)
    app.add_middleware(SecurityMiddleware)

    # CORS middleware with restricted settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Process-Time"],
        max_age=600,  # 10 minutes cache for preflight requests
    )

    # Trusted host middleware (prevent host header attacks)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "localhost",
            "127.0.0.1",
            "backend",
            "frontend",
            "*.localhost",
            "*",
        ],
    )

    logger.info("Security middleware configured successfully")


# Rate limit decorators for different endpoints
def auth_limit():
    """Rate limit for authentication endpoints (stricter)"""
    return limiter.limit("5/minute")


def api_limit():
    """Rate limit for general API endpoints"""
    return limiter.limit("100/minute")


def booking_limit():
    """Rate limit for booking endpoints (prevent abuse)"""
    return limiter.limit("10/minute")


def search_limit():
    """Rate limit for search endpoints"""
    return limiter.limit("30/minute")
