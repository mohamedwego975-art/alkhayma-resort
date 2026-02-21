from sqlalchemy import String, Numeric, Integer, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Package(Base):
    __tablename__ = "packages"

    name: Mapped[str] = mapped_column(String(200))
    name_ar: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    description_ar: Mapped[str | None] = mapped_column(String, nullable=True)
    discount_percent: Mapped[float] = mapped_column(Numeric(5, 2))
    is_active: Mapped[bool] = mapped_column(default=True)

    items: Mapped[list["PackageItem"]] = relationship("PackageItem", back_populates="package", cascade="all, delete-orphan")


class PackageItem(Base):
    __tablename__ = "package_items"

    package_id: Mapped[int] = mapped_column(ForeignKey("packages.id", ondelete="CASCADE"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), index=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    package: Mapped["Package"] = relationship("Package", back_populates="items")
    product: Mapped["Product"] = relationship("Product")

    __table_args__ = (
        Index("ix_package_items_package_product", "package_id", "product_id"),
    )
