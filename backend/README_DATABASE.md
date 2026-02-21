# Resort Platform - Database & Redis Setup

## Files Created

### 1. `/resort-platform/backend/app/core/database.py`
Async SQLAlchemy configuration with:
- AsyncPG engine (pool_size=10, max_overflow=20, pool_pre_ping=True)
- Echo enabled in development, disabled in production
- AsyncSessionLocal factory (expire_on_commit=False, autoflush=False)
- Base declarative class with id, created_at, updated_at
- get_db() FastAPI dependency

### 2. `/resort-platform/backend/app/core/redis.py`
Redis async client with:
- Redis connection from REDIS_URL
- get_redis() FastAPI dependency
- @cache() decorator with configurable expiry and key prefix
- invalidate_pattern() function for cache invalidation

### 3. `/resort-platform/backend/tests/test_database.py`
Database connection test that validates:
- Session creation
- Query execution (SELECT 1)
- Result assertion

## Test Results
✅ test_db_connection PASSED

## Usage Examples

### Database
```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db, Base

# Define model
class Product(Base):
    __tablename__ = "products"
    name: Mapped[str] = mapped_column(String(100))

# Use in endpoint
@app.get("/products")
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    return result.scalars().all()
```

### Redis Cache
```python
from app.core.redis import cache, invalidate_pattern

@cache(expire=300, key_prefix="products")
async def get_expensive_data(product_id: int):
    # This result will be cached for 5 minutes
    return await fetch_from_db(product_id)

# Invalidate cache
await invalidate_pattern("products:*")
```

## Environment Variables
```bash
DATABASE_URL=postgresql+asyncpg://postgres:changeme123@localhost:5432/resort_db
REDIS_URL=redis://localhost:6379
ENVIRONMENT=development  # or production
```

## Dependencies
- sqlalchemy==2.0.25
- asyncpg==0.29.0
- redis==5.0.1
- alembic==1.13.1
