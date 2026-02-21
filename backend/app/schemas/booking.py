from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

class BookingCreate(BaseModel):
    room_id: int
    check_in: date
    check_out: date
    guests: int = Field(ge=1)
    total_price: float = Field(ge=0)

class BookingResponse(BaseModel):
    id: int
    user_id: int
    room_id: int
    check_in: date
    check_out: date
    guests: int
    total_price: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
