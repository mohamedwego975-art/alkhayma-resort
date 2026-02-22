#!/usr/bin/env python3
"""Initialize database with sample data"""

import sys
import asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import engine, AsyncSessionLocal
from app.models import Base, Room, Product, User
from passlib.context import CryptContext
from sqlalchemy import select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def init_db():
    print("🔧 Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as db:
        try:
            # Check if data exists
            result = await db.execute(select(Room))
            if result.scalars().first():
                print("✅ Database already has data")
                return
            
            print("📝 Adding sample data...")
            
            # Add Rooms
            rooms = [
                Room(
                    room_number="101",
                    room_type="Standard",
                    capacity=2,
                    price_per_night=100.0,
                    description_en="Comfortable standard room with sea view",
                    description_ar="غرفة قياسية مريحة مع إطلالة على البحر",
                    amenities={"wifi": True, "ac": True, "tv": True, "minibar": True},
                    is_available=True
                ),
                Room(
                    room_number="102",
                    room_type="Deluxe",
                    capacity=3,
                    price_per_night=150.0,
                    description_en="Spacious deluxe room with balcony",
                    description_ar="غرفة ديلوكس واسعة مع شرفة",
                    amenities={"wifi": True, "ac": True, "tv": True, "minibar": True, "balcony": True},
                    is_available=True
                ),
                Room(
                    room_number="201",
                    room_type="Suite",
                    capacity=4,
                    price_per_night=250.0,
                    description_en="Luxury suite with ocean view",
                    description_ar="جناح فاخر مع إطلالة على المحيط",
                    amenities={"wifi": True, "ac": True, "tv": True, "minibar": True, "balcony": True, "jacuzzi": True},
                    is_available=True
                ),
                Room(
                    room_number="202",
                    room_type="Standard",
                    capacity=2,
                    price_per_night=100.0,
                    description_en="Cozy standard room",
                    description_ar="غرفة قياسية مريحة",
                    amenities={"wifi": True, "ac": True, "tv": True},
                    is_available=True
                ),
                Room(
                    room_number="301",
                    room_type="Deluxe",
                    capacity=3,
                    price_per_night=150.0,
                    description_en="Premium deluxe room",
                    description_ar="غرفة ديلوكس مميزة",
                    amenities={"wifi": True, "ac": True, "tv": True, "minibar": True},
                    is_available=True
                ),
                Room(
                    room_number="302",
                    room_type="Suite",
                    capacity=4,
                    price_per_night=250.0,
                    description_en="Presidential suite",
                    description_ar="الجناح الرئاسي",
                    amenities={"wifi": True, "ac": True, "tv": True, "minibar": True, "balcony": True, "jacuzzi": True, "kitchen": True},
                    is_available=True
                ),
            ]
            
            for room in rooms:
                db.add(room)
            
            # Add Products
            products = [
                Product(
                    name="VIP Beach Access",
                    name_ar="دخول الشاطئ VIP",
                    type="service",
                    base_price=150.0,
                    capacity=2,
                    description="Exclusive VIP beach access with cabana",
                    is_available=True
                ),
                Product(
                    name="Standard Beach Access",
                    name_ar="دخول الشاطئ القياسي",
                    type="service",
                    base_price=50.0,
                    capacity=2,
                    description="Standard beach access",
                    is_available=True
                ),
                Product(
                    name="Banana Boat",
                    name_ar="قارب الموز",
                    type="activity",
                    base_price=35.0,
                    capacity=4,
                    description="15 minutes of fun on banana boat",
                    is_available=True
                ),
                Product(
                    name="Parasailing",
                    name_ar="الطيران الشراعي",
                    type="activity",
                    base_price=85.0,
                    capacity=1,
                    description="Fly above the sea",
                    is_available=True
                ),
            ]
            
            for product in products:
                db.add(product)
            
            # Add Admin User
            admin = User(
                email="admin@alkhayma.com",
                full_name="Admin User",
                hashed_password=pwd_context.hash("admin123"),
                role="admin",
                is_active=True
            )
            db.add(admin)
            
            # Add Test User
            user = User(
                email="user@test.com",
                full_name="Test User",
                hashed_password=pwd_context.hash("user123"),
                role="guest",
                is_active=True
            )
            db.add(user)
            
            await db.commit()
            
            # Print summary
            result_rooms = await db.execute(select(Room))
            result_products = await db.execute(select(Product))
            result_users = await db.execute(select(User))
            
            print(f"\n✅ Database initialized successfully!")
            print(f"📊 Summary:")
            print(f"   Rooms: {len(result_rooms.scalars().all())}")
            print(f"   Products: {len(result_products.scalars().all())}")
            print(f"   Users: {len(result_users.scalars().all())}")
            print(f"\n👤 Test Accounts:")
            print(f"   Admin: admin@alkhayma.com / admin123")
            print(f"   User: user@test.com / user123")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            await db.rollback()
            raise

if __name__ == "__main__":
    asyncio.run(init_db())
