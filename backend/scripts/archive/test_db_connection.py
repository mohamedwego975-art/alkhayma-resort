import asyncio
from sqlalchemy import text
from app.core.database import AsyncSessionLocal

async def test_db_connection():
    """Test database connection"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        value = result.scalar()
        assert value == 1
        print("✅ Database connection test passed")

if __name__ == "__main__":
    asyncio.run(test_db_connection())
