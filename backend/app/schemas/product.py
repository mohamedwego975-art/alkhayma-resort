from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):
    name: str
    name_ar: Optional[str] = None
    description: Optional[str] = None
    description_ar: Optional[str] = None
    type: str
    base_price: float = Field(ge=0)
    capacity: int = Field(ge=1, default=1)
    is_active: bool = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    name_ar: Optional[str] = None
    description: Optional[str] = None
    description_ar: Optional[str] = None
    type: Optional[str] = None
    base_price: Optional[float] = Field(None, ge=0)
    capacity: Optional[int] = Field(None, ge=1)
    is_active: Optional[bool] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    name_ar: Optional[str] = None
    description: Optional[str] = None
    description_ar: Optional[str] = None
    type: str
    base_price: float
    capacity: int
    is_active: bool
    images: Optional[dict] = None
    amenities: Optional[dict] = None
    tags: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True
