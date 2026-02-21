from sqlalchemy import Date, Integer, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.core.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), index=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    total_capacity: Mapped[int] = mapped_column(Integer)
    available: Mapped[int] = mapped_column(Integer)
    booked: Mapped[int] = mapped_column(Integer, default=0)

    product: Mapped["Product"] = relationship("Product")

    __table_args__ = (
        Index("ix_inventory_product_date", "product_id", "date", unique=True),
    )
