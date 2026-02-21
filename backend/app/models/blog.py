from sqlalchemy import ForeignKey, String, Text, Boolean, DateTime, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class BlogPost(Base):
    __tablename__ = "blog_posts"
    
    title: Mapped[str] = mapped_column(String, nullable=False)
    title_ar: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_ar: Mapped[str] = mapped_column(Text, nullable=False)
    meta_description: Mapped[str] = mapped_column(String)
    featured_image: Mapped[str] = mapped_column(String)
    tags: Mapped[dict] = mapped_column(JSON, default=dict)
    linked_products: Mapped[dict] = mapped_column(JSON, default=dict)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    published_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))

    __table_args__ = (
        Index('ix_blog_posts_slug', 'slug'),
        Index('ix_blog_posts_is_published', 'is_published'),
        Index('ix_blog_posts_published_at', 'published_at'),
    )
