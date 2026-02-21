from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RoomResponse(BaseModel):
    id: int
    room_number: str
    room_type: str
    status: str
    price_per_night: float
    capacity: int
    description_en: Optional[str] = None
    description_ar: Optional[str] = None
    amenities: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class RoomAvailabilityQuery(BaseModel):
    check_in: str
    check_out: str
    room_type: Optional[str] = None
    guests: int = Field(ge=1, default=1)
