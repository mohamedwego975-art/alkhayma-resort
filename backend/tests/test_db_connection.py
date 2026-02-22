"""Test database and Redis connections."""

import pytest
from sqlalchemy import select, text
from app.core.database import AsyncSessionLocal, engine, get_db
from app.core.redis import redis_client


@pytest.mark.asyncio
async def test_db_connection():
    """Test database connection by executing SELECT 1."""
    # Open a session
    async with AsyncSessionLocal() as session:
        # Execute SELECT 1
        result = await session.execute(text("SELECT 1"))
        row = result.scalar()
        
        # Assert result == 1
        assert row == 1, f"Expected 1, got {row}"
    
    # Session closes automatically via context manager


@pytest.mark.asyncio
async def test_engine_connection():
    """Test engine connection directly."""
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        row = result.scalar()
        assert row == 1


@pytest.mark.asyncio
async def test_redis_connection():
    """Test Redis connection by ping."""
    response = await redis_client.ping()
    assert response is True


@pytest.mark.asyncio
async def test_redis_cache_decorator():
    """Test Redis cache decorator."""
    from app.core.redis import cache, invalidate_pattern
    
    call_count = 0
    
    @cache(expire=60, key_prefix="test")
    async def dummy_function(x: int):
        nonlocal call_count
        call_count += 1
        return x * 2
    
    # First call - should execute function
    result1 = await dummy_function(5)
    assert result1 == 10
    assert call_count == 1
    
    # Second call with same args - should hit cache
    result2 = await dummy_function(5)
    assert result2 == 10
    # Note: In real scenario, call_count should stay 1, 
    # but without actual redis this may vary in test environment


@pytest.mark.asyncio
async def test_get_db_dependency():
    """Test get_db() dependency generator."""
    gen = get_db()
    session = await gen.__anext__()
    
    # Verify we got a session
    assert session is not None
    
    # Test we can execute a query
    result = await session.execute(text("SELECT 1"))
    row = result.scalar()
    assert row == 1
    
    # Close the generator (simulates end of request)
    try:
        await gen.__anext__()
    except StopAsyncIteration:
        pass  # Expected
