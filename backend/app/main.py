"""
Al-Khayma Beach Resort API
Professional FastAPI application with comprehensive security, logging, and error handling
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from sqlalchemy import select
import logging

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.core.error_handlers import setup_error_handlers, AppException
from app.core.security_middleware import setup_security_middleware
from app.api.endpoints import auth, bookings, content, rooms, products, notifications
from app.api import analytics
from app.services import email_service, whatsapp_service

# Setup logging
logger = setup_logging(
    app_name="alkhayma",
    log_level=settings.LOG_LEVEL if hasattr(settings, 'LOG_LEVEL') else "INFO",
    enable_json=settings.ENVIRONMENT == "production" if hasattr(settings, 'ENVIRONMENT') else False
)

# Initialize FastAPI app
app = FastAPI(
    title="الخيمة Beach Resort API",
    description="""
    Resort booking and management system API
    
    ## Features
    - 🔐 Secure authentication and authorization
    - 📅 Room and beach booking management
    - 💳 Payment integration (Paymob, Stripe)
    - 🔔 Real-time notifications
    - 📊 Analytics and reporting
    - 🛡️ Rate limiting and security
    
    ## Authentication
    Most endpoints require Bearer token authentication. 
    Use `/api/auth/login` to obtain a token.
    """,
    version="1.0.0",
    docs_url=None,  # Custom docs endpoint
    redoc_url=None,  # Custom redoc endpoint
    openapi_url="/api/openapi.json",
    contact={
        "name": "Al-Khayma Support",
        "email": "support@alkhayma-resort.com",
        "url": "https://alkhayma-resort.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Setup security middleware
setup_security_middleware(app, settings.cors_origins)

# Setup error handlers
setup_error_handlers(app)

@app.get("/api/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint that verifies DB and Redis connections
    
    Returns:
        Status of all system components
    """
    db_status = "ok"
    redis_status = "ok"
    
    try:
        from app.core.database import engine
        async with engine.connect() as conn:
            await conn.execute(select(1))
    except Exception as e:
        db_status = f"error: {str(e)}"
        logger.error(f"Health check - DB error: {e}")
    
    try:
        from app.core.redis import redis_client
        await redis_client.ping()
    except Exception as e:
        redis_status = f"error: {str(e)}"
        logger.error(f"Health check - Redis error: {e}")
    
    overall_status = "ok" if db_status == "ok" and redis_status == "ok" else "degraded"
    
    if overall_status != "ok":
        logger.warning(f"Health check failed: status={overall_status}, db={db_status}, redis={redis_status}")
    
    return {
        "status": overall_status,
        "db": db_status,
        "redis": redis_status,
        "version": "1.0.0",
        "environment": getattr(settings, 'ENVIRONMENT', 'development')
    }

# Root endpoint
@app.get("/", tags=["General"])
async def root():
    """API root endpoint"""
    return {
        "name": "الخيمة Beach Resort API",
        "version": "1.0.0",
        "documentation": "/api/docs",
        "health": "/api/health"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("🚀 Starting up Al-Khayma Beach Resort API")
    
    try:
        await email_service.initialize()
        logger.info("✅ Email service initialized")
    except Exception as e:
        logger.error(f"❌ Email service initialization failed: {e}")
    
    try:
        await whatsapp_service.initialize()
        logger.info("✅ WhatsApp service initialized")
    except Exception as e:
        logger.error(f"❌ WhatsApp service initialization failed: {e}")
    
    logger.info("✅ Application startup complete")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Shutting down Al-Khayma Beach Resort API")
    
    try:
        from app.core.database import engine
        await engine.dispose()
        logger.info("✅ Database connections closed")
    except Exception as e:
        logger.error(f"❌ Error closing database connections: {e}")
    
    logger.info("✅ Application shutdown complete")

app.include_router(auth.router, prefix="/api")
app.include_router(bookings.router, prefix="/api")
app.include_router(rooms.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(notifications.router, prefix="/api")
app.include_router(content.router, prefix="/api")
app.include_router(analytics.router)
