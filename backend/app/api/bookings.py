from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.auth import oauth2_scheme
from typing import Optional
import uuid

router = APIRouter(prefix="/api/bookings", tags=["bookings"])

# Mock booking storage
bookings_db = {}

@router.post("/")
async def create_booking(
    booking_data: dict,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """Create new booking"""
    
    # Check idempotency
    if idempotency_key and idempotency_key in bookings_db:
        raise HTTPException(status_code=409, detail="Duplicate request")
    
    booking_id = len(bookings_db) + 1
    booking = {
        "id": booking_id,
        "status": "pending",
        "total_price": 1500.0,
        **booking_data
    }
    
    bookings_db[booking_id] = booking
    if idempotency_key:
        bookings_db[idempotency_key] = booking
    
    return booking

@router.get("/{booking_id}")
async def get_booking(
    booking_id: int,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """Get booking by ID"""
    if booking_id not in bookings_db:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    return bookings_db[booking_id]

@router.get("/")
async def get_user_bookings(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """Get user bookings"""
    return list(bookings_db.values())
