from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductResponse(BaseModel):
    id: int
    name: str
    name_ar: Optional[str] = None
    description: Optional[str] = None
    description_ar: Optional[str] = None
    type: str
    price: float
    stock: int
    is_active: bool
    images: Optional[list] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    name_ar: Optional[str] = None
    description: Optional[str] = None
    description_ar: Optional[str] = None
    type: str
    price: float = Field(ge=0)
    stock: int = Field(ge=0)
    is_active: bool = True
