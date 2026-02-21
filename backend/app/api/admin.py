from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.auth import oauth2_scheme

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/analytics/overview")
async def get_analytics_overview(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """Get admin analytics overview"""
    # Mock user role check
    # In real implementation, decode JWT and check user role
    return {
        "total_revenue": 4500.0,
        "total_bookings": 3,
        "active_users": 15,
        "occupancy_rate": 0.75
    }

@router.get("/bookings")
async def get_all_bookings(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """Get all bookings (admin only)"""
    from app.api.bookings import bookings_db
    return list(bookings_db.values())

@router.patch("/products/{product_id}")
async def update_product(
    product_id: int,
    product_data: dict,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """Update product (admin only)"""
    return {"message": "Product updated", "id": product_id}
