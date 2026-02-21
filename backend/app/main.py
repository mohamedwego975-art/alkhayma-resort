from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.api.auth import router as auth_router, limiter
from app.api.products import router as products_router
from app.api.bookings import router as bookings_router
from app.api.payments import router as payments_router
from app.api.loyalty import router as loyalty_router
from app.api.admin import router as admin_router
# from app.api.metrics import router as metrics_router

app = FastAPI(
    title="الخيمة Beach Resort API",
    description="Resort booking and management system",
    version="1.0.0"
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(bookings_router)
app.include_router(payments_router)
app.include_router(loyalty_router)
app.include_router(admin_router)
# app.include_router(metrics_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "الخيمة Beach Resort API", "version": "1.0.0"}
