"""
Prometheus metrics endpoint for monitoring
"""
from fastapi import APIRouter
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time
import psutil
import asyncio
from app.core.database import AsyncSessionLocal
from sqlalchemy import text

router = APIRouter()

# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_CONNECTIONS = Gauge('database_connections_active', 'Active database connections')
MEMORY_USAGE = Gauge('memory_usage_bytes', 'Memory usage in bytes')
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percentage')

@router.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    
    # Update system metrics
    MEMORY_USAGE.set(psutil.virtual_memory().used)
    CPU_USAGE.set(psutil.cpu_percent())
    
    # Update database metrics
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT count(*) FROM pg_stat_activity WHERE state = 'active'"))
            active_connections = result.scalar() or 0
            ACTIVE_CONNECTIONS.set(active_connections)
    except Exception:
        pass
    
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Middleware to track requests
async def track_request_metrics(request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    REQUEST_DURATION.observe(duration)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    return response
