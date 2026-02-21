#!/usr/bin/env python3
"""Add more sample data"""

import sys
import asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import AsyncSessionLocal
from app.models import Room, Product, User
from passlib.context import CryptContext
from sqlalchemy import select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def add_data():
    async with AsyncSessionLocal() as db:
        try:
            print("📝 Adding more data...")
            
            # Add more rooms
            new_rooms = [
                Room(
                    room_number="102",
                    room_type="deluxe",
                    capacity=3,
                    price_per_night=150.0,
                    description_en="Spacious deluxe room with balcony",
                    description_ar="غرفة ديلوكس واسعة مع شرفة",
                    amenities='{"wifi": true, "ac": true, "tv": true, "minibar": true, "balcony": true}',
                    is_active=True,
                    rating=4.5,
                    review_count=12
                ),
                Room(
                    room_number="202",
                    room_type="standard",
                    capacity=2,
                    price_per_night=100.0,
                    description_en="Cozy standard room",
                    description_ar="غرفة قياسية مريحة",
                    amenities='{"wifi": true, "ac": true, "tv": true}',
                    is_active=True,
                    rating=4.2,
                    review_count=8
                ),
                Room(
                    room_number="301",
                    room_type="suite",
                    capacity=4,
                    price_per_night=300.0,
                    description_en="Presidential suite with ocean view",
                    description_ar="الجناح الرئاسي مع إطلالة على المحيط",
                    amenities='{"wifi": true, "ac": true, "tv": true, "minibar": true, "balcony": true, "jacuzzi": true, "kitchen": true}',
                    is_active=True,
                    rating=4.9,
                    review_count=25
                ),
            ]
            
            for room in new_rooms:
                # Check if exists
                result = await db.execute(select(Room).where(Room.room_number == room.room_number))
                if not result.scalar_one_or_none():
                    db.add(room)
            
            # Add Products
            products = [
                Product(
                    name="VIP Beach Access",
                    name_ar="دخول الشاطئ VIP",
                    slug="vip-beach-access",
                    type="beach",
                    base_price=150.0,
                    capacity=2,
                    description="Exclusive VIP beach access with cabana"
                ),
                Product(
                    name="Standard Beach Access",
                    name_ar="دخول الشاطئ القياسي",
                    slug="standard-beach-access",
                    type="beach",
                    base_price=50.0,
                    capacity=2,
                    description="Standard beach access"
                ),
                Product(
                    name="Banana Boat",
                    name_ar="قارب الموز",
                    slug="banana-boat",
                    type="water_activity",
                    base_price=35.0,
                    capacity=4,
                    description="15 minutes of fun on banana boat"
                ),
                Product(
                    name="Parasailing",
                    name_ar="الطيران الشراعي",
                    slug="parasailing",
                    type="water_activity",
                    base_price=85.0,
                    capacity=1,
                    description="Fly above the sea"
                ),
            ]
            
            for product in products:
                result = await db.execute(select(Product).where(Product.name == product.name))
                if not result.scalar_one_or_none():
                    db.add(product)
            
            # Add Users
            users = [
                User(
                    email="admin@alkhayma.com",
                    full_name="Admin User",
                    hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaOBzLm",  # admin123
                    role="admin",
                    is_active=True
                ),
                User(
                    email="user@test.com",
                    full_name="Test User",
                    hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaOBzLm",  # user123
                    role="guest",
                    is_active=True
                ),
            ]
            
            for user in users:
                result = await db.execute(select(User).where(User.email == user.email))
                if not result.scalar_one_or_none():
                    db.add(user)
            
            await db.commit()
            
            # Print summary
            from sqlalchemy import func
            rooms_count = await db.scalar(select(func.count()).select_from(Room))
            products_count = await db.scalar(select(func.count()).select_from(Product))
            users_count = await db.scalar(select(func.count()).select_from(User))
            
            print(f"\n✅ Data added successfully!")
            print(f"📊 Summary:")
            print(f"   Rooms: {rooms_count}")
            print(f"   Products: {products_count}")
            print(f"   Users: {users_count}")
            print(f"\n👤 Test Accounts:")
            print(f"   Admin: admin@alkhayma.com / admin123")
            print(f"   User: user@test.com / user123")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            await db.rollback()
            raise

if __name__ == "__main__":
    asyncio.run(add_data())
