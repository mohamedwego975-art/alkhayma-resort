from pydantic import BaseModel, Field
from datetime import date
from decimal import Decimal
from typing import List, Optional, Dict, Any


class CreateBookingRequest(BaseModel):
    product_id: int
    check_in: date
    check_out: date
    quantity: int = Field(ge=1)
    addons: List[int] = []
    idempotency_key: str = Field(min_length=1, max_length=255)
    notes: Optional[str] = None


class BookingResponse(BaseModel):
    booking_id: int
    status: str
    check_in: str
    check_out: str
    total_price: str
    pricing_breakdown: Dict[str, Any]
    product: Dict[str, Any]
