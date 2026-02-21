from sqlalchemy import String, Numeric, Boolean, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Package(Base):
    __tablename__ = "packages"
    
    name: Mapped[str] = mapped_column(String, nullable=False)
    name_ar: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String)
    discount_pct: Mapped[Numeric] = mapped_column(Numeric(5, 2), default=0)
    tags: Mapped[dict] = mapped_column(JSON, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class PackageItem(Base):
    __tablename__ = "package_items"
    
    package_id: Mapped[int] = mapped_column(ForeignKey("packages.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True)
