from sqlalchemy import ForeignKey, Integer, String, Numeric, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
import enum

class SentimentLabel(str, enum.Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class Review(Base):
    __tablename__ = "reviews"
    
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id", ondelete="CASCADE"), unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5
    comment: Mapped[str] = mapped_column(String)
    sentiment_score: Mapped[Numeric] = mapped_column(Numeric(3, 2))  # -1 to 1
    sentiment_label: Mapped[SentimentLabel] = mapped_column(default=SentimentLabel.NEUTRAL)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (
        Index('ix_reviews_user_id', 'user_id'),
        Index('ix_reviews_product_id', 'product_id'),
        Index('ix_reviews_rating', 'rating'),
    )
