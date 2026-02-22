"""
Database configuration with optimized connection pooling
Professional async SQLAlchemy setup for production use
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, DateTime, func
from app.core.config import settings

# Create async engine with optimized connection pool
# Production-ready settings for high performance
engine = create_async_engine(
    settings.database_url,
    echo=True if settings.environment == "development" else False,
    # Pool configuration
    pool_size=20,              # Base number of connections
    max_overflow=30,           # Extra connections when needed
    pool_pre_ping=True,        # Verify connections before use
    pool_recycle=300,          # Recycle connections after 5 minutes
    pool_timeout=30,           # Wait up to 30s for available connection
    # Performance optimizations
    connect_args={
        "command_timeout": 60,  # Query timeout
        "server_settings": {
            "jit": "off"  # Disable JIT for short queries
        }
    }
)

# Create async session factory with optimized settings
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,    # Don't expire objects after commit
    autoflush=False,          # Manual flush control for better performance
    autocommit=False         # Explicit transaction control
)

# Base declarative class with timestamp fields
class Base(DeclarativeBase):
    """Base model with automatic timestamps"""
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(),
        nullable=True
    )

# Dependency to get database session with automatic cleanup
async def get_db():
    """
    Get database session with automatic cleanup
    
    Usage:
        @app.get("/items/")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Connection pool monitoring
async def get_pool_status():
    """Get database connection pool status for monitoring"""
    return {
        "size": engine.pool.size(),
        "checked_in": engine.pool.checkedin(),
        "checked_out": engine.pool.checkedout(),
        "overflow": engine.pool.overflow()
    }
