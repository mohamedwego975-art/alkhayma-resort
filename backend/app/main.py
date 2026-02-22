from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

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
