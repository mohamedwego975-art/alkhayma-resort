from pydantic import BaseModel
from decimal import Decimal
from typing import List, Dict, Any, Optional
from datetime import datetime


class ProductResponse(BaseModel):
    id: int
    name: str
    name_ar: str
    slug: str
    type: str
    base_price: Decimal
    capacity: int
    description: Optional[str] = None
    description_ar: Optional[str] = None
    images: Dict = {}
    amenities: Dict = {}
    tags: Dict = {}
    min_age: Optional[int] = None
    max_weight_kg: Optional[int] = None
    duration_minutes: Optional[int] = None
    is_active: bool
    sort_order: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProductDetailResponse(ProductResponse):
    inventory_status: str  # "available" or "soldout"
    average_rating: Optional[float] = None
    review_count: int = 0


class PackageResponse(BaseModel):
    id: int
    name: str
    name_ar: str
    slug: str
    description: Optional[str] = None
    description_ar: Optional[str] = None
    discount_percent: Decimal
    is_active: bool
    
    class Config:
        from_attributes = True


class HomeResponse(BaseModel):
    featured_rooms: List[ProductResponse]
    packages: List[PackageResponse]
    activities_teaser: List[ProductResponse]


class PaginatedProductsResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    page: int
    limit: int
    pages: int


class PriceBreakdownResponse(BaseModel):
    base_price: Decimal
    final_price: Decimal
    nightly_rate: Decimal
    discounts: List[Dict[str, Any]]
    multipliers: List[Dict[str, Any]]
    total_savings: Decimal
    currency: str = "USD"
    
    class Config:
        from_attributes = True
