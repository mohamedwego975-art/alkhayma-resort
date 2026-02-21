from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
import json


class RoomResponse(BaseModel):
    id: int
    room_number: str
    room_type: str
    status: str
    price_per_night: float
    capacity: int
    description_en: Optional[str] = None
    description_ar: Optional[str] = None
    amenities: Optional[Dict[str, Any]] = None
    is_active: bool
    rating: float = 4.0
    review_count: int = 0
    created_at: datetime

    @validator("amenities", pre=True)
    def parse_amenities(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except:
                return {}
        return v

    class Config:
        from_attributes = True


class RoomAvailabilityQuery(BaseModel):
    check_in: str
    check_out: str
    room_type: Optional[str] = None
    guests: int = Field(ge=1, default=1)
