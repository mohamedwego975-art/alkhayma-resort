from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import select
from app.core.config import settings
from app.api.endpoints import auth, bookings, rooms, products, notifications
from app.api import analytics
from app.services import email_service, whatsapp_service

app = FastAPI(
    title="الخيمة Beach Resort API",
    description="Resort booking and management system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "code": "INTERNAL_ERROR", "details": {}}
    )

@app.get("/api/health")
async def health_check():
    """Health check endpoint that verifies DB and Redis connections."""
    db_status = "ok"
    redis_status = "ok"
    
    try:
        # Check DB connection
        from app.core.database import engine
        async with engine.connect() as conn:
            await conn.execute(select(1))
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    try:
        # Check Redis connection
        from app.core.redis import redis_client
        await redis_client.ping()
    except Exception as e:
        redis_status = f"error: {str(e)}"
    
    overall_status = "ok" if db_status == "ok" and redis_status == "ok" else "degraded"
    
    return {
        "status": overall_status,
        "db": db_status,
        "redis": redis_status
    }

@app.get("/")
async def root():
    return {"message": "الخيمة Beach Resort API", "version": "1.0.0"}

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    await email_service.initialize()
    await whatsapp_service.initialize()

app.include_router(auth.router, prefix="/api")
app.include_router(bookings.router, prefix="/api")
app.include_router(rooms.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(notifications.router, prefix="/api")
app.include_router(analytics.router)
