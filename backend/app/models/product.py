from sqlalchemy import String, Numeric, Integer, Boolean, Text, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
import enum

class ProductType(str, enum.Enum):
    ROOM = "room"
    BEACH = "beach"
    RESTAURANT = "restaurant"
    CAFE = "cafe"
    WATER_ACTIVITY = "water_activity"
    EVENT = "event"

class Product(Base):
    __tablename__ = "products"
    
    name: Mapped[str] = mapped_column(String, nullable=False)
    name_ar: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    type: Mapped[ProductType] = mapped_column(nullable=False)
    base_price: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, default=1)
    description: Mapped[str] = mapped_column(Text)
    description_ar: Mapped[str] = mapped_column(Text)
    images: Mapped[dict] = mapped_column(JSON, default=dict)
    amenities: Mapped[dict] = mapped_column(JSON, default=dict)
    tags: Mapped[dict] = mapped_column(JSON, default=dict)
    min_age: Mapped[int] = mapped_column(Integer, default=0)
    max_weight_kg: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    time_slots: Mapped[dict] = mapped_column(JSON, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (
        Index('ix_products_type', 'type'),
        Index('ix_products_is_active', 'is_active'),
        Index('ix_products_slug', 'slug'),
    )
