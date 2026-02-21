from sqlalchemy import String, Integer, Numeric, ForeignKey, Enum as SQLEnum, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from decimal import Decimal
import enum
from app.core.database import Base


class PaymentGateway(str, enum.Enum):
    paymob = "paymob"
    stripe = "stripe"


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"
    refunded = "refunded"


class Payment(Base):
    __tablename__ = "payments"

    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id", ondelete="CASCADE"), unique=True, index=True)
    gateway: Mapped[PaymentGateway] = mapped_column(SQLEnum(PaymentGateway, name="payment_gateway"))
    status: Mapped[PaymentStatus] = mapped_column(SQLEnum(PaymentStatus, name="payment_status"), default=PaymentStatus.pending, index=True)
    
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(String(3))
    
    gateway_order_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    gateway_payment_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    
    payment_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    
    booking: Mapped["Booking"] = relationship("Booking")

    __table_args__ = (
        Index("ix_payments_gateway_status", "gateway", "status"),
    )


class PaymentWebhookLog(Base):
    __tablename__ = "payment_webhook_logs"

    gateway: Mapped[PaymentGateway] = mapped_column(SQLEnum(PaymentGateway, name="payment_gateway"), index=True)
    payload: Mapped[dict] = mapped_column(JSONB)
    signature: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_valid: Mapped[bool] = mapped_column(default=False)
    processed: Mapped[bool] = mapped_column(default=False, index=True)
    
    __table_args__ = (
        Index("ix_webhook_logs_gateway_processed", "gateway", "processed"),
    )
