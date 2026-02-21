from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

router = APIRouter(prefix="/api/payments", tags=["payments"])

@router.post("/webhooks/payment")
async def payment_webhook(webhook_data: dict, db: AsyncSession = Depends(get_db)):
    """Handle payment webhook"""
    from app.api.bookings import bookings_db
    
    booking_id = webhook_data.get("booking_id")
    if booking_id and booking_id in bookings_db:
        bookings_db[booking_id]["status"] = "confirmed"
        return {"message": "Payment processed"}
    
    return {"message": "Booking not found"}

@router.post("/process")
async def process_payment(payment_data: dict, db: AsyncSession = Depends(get_db)):
    """Process payment"""
    return {"status": "success", "transaction_id": "txn_123456"}
