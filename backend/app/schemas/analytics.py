"""Analytics Pydantic schemas.

Request/response models for analytics API endpoints.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class RevenueMetrics(BaseModel):
    """Revenue analytics response model."""
    total: float = Field(..., description="Total revenue in the period")
    daily_breakdown: List[Dict[str, Any]] = Field(
        default=[], description="Daily revenue breakdown"
    )
    by_payment_method: List[Dict[str, Any]] = Field(
        default=[], description="Revenue breakdown by payment method"
    )
    period_days: int = Field(..., description="Analysis period in days")


class OccupancyMetrics(BaseModel):
    """Room occupancy analytics response model."""
    total_rooms: int = Field(..., description="Total number of rooms")
    occupied: int = Field(..., description="Currently occupied rooms")
    available: int = Field(..., description="Available rooms")
    occupancy_rate: float = Field(
        ..., description="Occupancy percentage rate", ge=0, le=100
    )
    by_room_type: List[Dict[str, Any]] = Field(
        default=[], description="Occupancy by room type"
    )
    recent_bookings: int = Field(
        ..., description="Number of bookings in the period"
    )
    period_days: int = Field(..., description="Analysis period in days")


class ProductStat(BaseModel):
    """Single product statistics."""
    id: int
    name: str
    name_ar: Optional[str] = None
    type: str
    price: float
    is_active: bool
    booking_count: int
    revenue: float


class PopularProducts(BaseModel):
    """Popular products response model."""
    products: List[ProductStat] = Field(default=[])
    period_days: int
    total_count: int


class DashboardSummary(BaseModel):
    """Comprehensive dashboard summary."""
    today_revenue: float = Field(..., description="Revenue today")
    month_revenue: float = Field(..., description="Revenue this month")
    active_bookings: int = Field(..., description="Number of active bookings")
    total_customers: int = Field(..., description="Total customer count")
    occupancy_rate: float = Field(..., description="Current occupancy rate %")
    occupied_rooms: int
    available_rooms: int
    last_updated: str = Field(..., description="ISO timestamp of last update")


class TimeRangeQuery(BaseModel):
    """Query parameters for time-range analytics."""
    days: int = Field(default=30, ge=1, le=365, description="Days to analyze")
    start_date: Optional[str] = Field(None, description="Start date (ISO format)")
    end_date: Optional[str] = Field(None, description="End date (ISO format)")
