import asyncio
from app.core.database import engine, Base

# Import all models to register them with Base
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.package import Package, PackageItem
from app.models.user import User
from app.models.booking import Booking, BookingItem
from app.models.payment import Payment
from app.models.review import Review
from app.models.loyalty import LoyaltyAccount, LoyaltyTransaction
from app.models.audit import AuditLog
from app.models.blog import BlogPost

async def create_all_tables():
    """Create all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ All tables created successfully:")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")

if __name__ == "__main__":
    asyncio.run(create_all_tables())
