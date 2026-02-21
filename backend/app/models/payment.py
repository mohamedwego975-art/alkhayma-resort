from sqlalchemy import ForeignKey, String, Numeric, DateTime, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
import enum

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentGateway(str, enum.Enum):
    PAYMOB = "paymob"
    STRIPE = "stripe"

class Payment(Base):
    __tablename__ = "payments"
    
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    gateway: Mapped[PaymentGateway] = mapped_column(nullable=False)
    gateway_payment_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    amount: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String, default="USD")
    status: Mapped[PaymentStatus] = mapped_column(default=PaymentStatus.PENDING)
    gateway_response: Mapped[dict] = mapped_column(JSON, default=dict)
    paid_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        Index('ix_payments_booking_id', 'booking_id'),
        Index('ix_payments_gateway_payment_id', 'gateway_payment_id'),
        Index('ix_payments_status', 'status'),
    )
