from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
import json


class RoomCreate(BaseModel):
    room_number: str = Field(..., min_length=1, max_length=50)
    room_type: str = Field(..., description="standard, deluxe, suite, villa")
    status: str = Field(
        default="available", description="available, occupied, maintenance"
    )
    price_per_night: float = Field(..., gt=0)
    capacity: int = Field(..., ge=1, le=20)
    description_en: Optional[str] = None
    description_ar: Optional[str] = None
    amenities: Optional[Dict[str, Any]] = None
    is_active: bool = False

    class Config:
        schema_extra = {
            "example": {
                "room_number": "101",
                "room_type": "standard",
                "status": "available",
                "price_per_night": 150.0,
                "capacity": 2,
                "description_en": "Comfortable standard room",
                "description_ar": "غرفة قياسية مريحة",
                "is_active": True,
            }
        }


class RoomUpdate(BaseModel):
    room_number: Optional[str] = Field(None, min_length=1, max_length=50)
    room_type: Optional[str] = None
    status: Optional[str] = None
    price_per_night: Optional[float] = Field(None, gt=0)
    capacity: Optional[int] = Field(None, ge=1, le=20)
    description_en: Optional[str] = None
    description_ar: Optional[str] = None
    amenities: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


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
