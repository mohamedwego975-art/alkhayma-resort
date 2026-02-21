from sqlalchemy import String, Integer, Numeric, ForeignKey, Date, Enum as SQLEnum, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import date
from decimal import Decimal
import enum
from app.core.database import Base


class BookingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"


class Booking(Base):
    __tablename__ = "bookings"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    idempotency_key: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    status: Mapped[BookingStatus] = mapped_column(SQLEnum(BookingStatus, name="booking_status"), default=BookingStatus.pending, index=True)
    
    check_in: Mapped[date] = mapped_column(Date, index=True)
    check_out: Mapped[date] = mapped_column(Date)
    
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    pricing_breakdown: Mapped[dict] = mapped_column(JSONB, default=dict)
    
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    user: Mapped["User"] = relationship("User")
    items: Mapped[list["BookingItem"]] = relationship("BookingItem", back_populates="booking", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_bookings_user_status", "user_id", "status"),
        Index("ix_bookings_check_in_out", "check_in", "check_out"),
    )


class BookingItem(Base):
    __tablename__ = "booking_items"

    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id", ondelete="CASCADE"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), index=True)
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    
    booking: Mapped["Booking"] = relationship("Booking", back_populates="items")
    product: Mapped["Product"] = relationship("Product")

    __table_args__ = (
        Index("ix_booking_items_booking_product", "booking_id", "product_id"),
    )
