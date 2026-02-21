from sqlalchemy import String, Numeric, Integer, Boolean, Enum as SQLEnum, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
import enum
from app.core.database import Base


class ProductType(str, enum.Enum):
    room = "room"
    beach = "beach"
    restaurant = "restaurant"
    cafe = "cafe"
    water_activity = "water_activity"
    event = "event"


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(200))
    name_ar: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    type: Mapped[ProductType] = mapped_column(SQLEnum(ProductType, name="product_type"), index=True)
    base_price: Mapped[float] = mapped_column(Numeric(10, 2))
    capacity: Mapped[int] = mapped_column(Integer)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    description_ar: Mapped[str | None] = mapped_column(String, nullable=True)
    images: Mapped[dict] = mapped_column(JSONB, default=dict)
    amenities: Mapped[dict] = mapped_column(JSONB, default=dict)
    tags: Mapped[dict] = mapped_column(JSONB, default=dict)
    min_age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_weight_kg: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    time_slots: Mapped[dict] = mapped_column(JSONB, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (
        Index("ix_products_type_active", "type", "is_active"),
    )
