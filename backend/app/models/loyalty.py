from sqlalchemy import ForeignKey, Integer, String, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
import enum

class LoyaltyTier(str, enum.Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    VIP = "vip"

class LoyaltyTransactionType(str, enum.Enum):
    EARN = "earn"
    REDEEM = "redeem"
    EXPIRE = "expire"
    BONUS = "bonus"

class LoyaltyAccount(Base):
    __tablename__ = "loyalty_accounts"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    points_balance: Mapped[int] = mapped_column(Integer, default=0)
    tier: Mapped[LoyaltyTier] = mapped_column(default=LoyaltyTier.BRONZE)
    lifetime_points: Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (
        Index('ix_loyalty_accounts_user_id', 'user_id'),
        Index('ix_loyalty_accounts_tier', 'tier'),
    )

class LoyaltyTransaction(Base):
    __tablename__ = "loyalty_transactions"
    
    account_id: Mapped[int] = mapped_column(ForeignKey("loyalty_accounts.id", ondelete="CASCADE"), nullable=False)
    points: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[LoyaltyTransactionType] = mapped_column(nullable=False)
    reference_booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id", ondelete="SET NULL"))
    note: Mapped[str] = mapped_column(String)

    __table_args__ = (
        Index('ix_loyalty_transactions_account_id', 'account_id'),
        Index('ix_loyalty_transactions_type', 'type'),
    )
