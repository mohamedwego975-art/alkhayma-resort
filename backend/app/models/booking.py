from sqlalchemy import ForeignKey, String, Numeric, DateTime, Integer, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
import enum

class BookingStatus(str, enum.Enum):
    PENDING_PAYMENT = "pending_payment"
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class BookingSource(str, enum.Enum):
    WEB = "web"
    WHATSAPP = "whatsapp"
    ADMIN = "admin"

class Booking(Base):
    __tablename__ = "bookings"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[BookingStatus] = mapped_column(default=BookingStatus.PENDING_PAYMENT)
    total_price: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String, default="USD")
    check_in: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    check_out: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    notes: Mapped[str] = mapped_column(String)
    idempotency_key: Mapped[str] = mapped_column(String, unique=True, index=True)
    pricing_breakdown: Mapped[dict] = mapped_column(JSON, default=dict)
    source: Mapped[BookingSource] = mapped_column(default=BookingSource.WEB)

    __table_args__ = (
        Index('ix_bookings_user_id', 'user_id'),
        Index('ix_bookings_status', 'status'),
        Index('ix_bookings_check_in', 'check_in'),
    )

class BookingItem(Base):
    __tablename__ = "booking_items"
    
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit_price: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    addons: Mapped[dict] = mapped_column(JSON, default=dict)

    __table_args__ = (
        Index('ix_booking_items_booking_id', 'booking_id'),
        Index('ix_booking_items_product_id', 'product_id'),
    )
