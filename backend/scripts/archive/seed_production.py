#!/usr/bin/env python3
"""
Phase 5 Step 1: Production Database Seeding
Populates database with realistic data for testing and demo
"""

import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import AsyncSessionLocal, engine
from app.models import Base, Room, Product, User
from sqlalchemy import select, func, text
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pre-hashed password for all test users: "password123"
HASHED_PASSWORD = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaOBzLm"

async def seed_database():
    """Seed database with production-ready data"""
    
    print("🌱 Starting database seeding...")
    
    # Ensure tables exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as db:
        try:
            # Check existing data
            room_count = await db.scalar(select(func.count()).select_from(Room))
            
            if room_count >= 6:
                print(f"✅ Database already has {room_count} rooms. Skipping seed.")
                return
            
            print(f"📊 Current rooms: {room_count}. Adding more data...")
            
            # ==================== ROOMS ====================
            rooms_data = [
                {
                    "room_number": "101",
                    "room_type": "standard",
                    "capacity": 2,
                    "price_per_night": 100.0,
                    "description_en": "Comfortable standard room with garden view",
                    "description_ar": "غرفة قياسية مريحة مع إطلالة على الحديقة",
                    "amenities": '{"wifi": true, "ac": true, "tv": true, "minibar": false}',
                    "rating": 4.2,
                    "review_count": 15
                },
                {
                    "room_number": "102",
                    "room_type": "standard",
                    "capacity": 2,
                    "price_per_night": 100.0,
                    "description_en": "Cozy standard room with modern amenities",
                    "description_ar": "غرفة قياسية مريحة مع وسائل راحة حديثة",
                    "amenities": '{"wifi": true, "ac": true, "tv": true, "minibar": false}',
                    "rating": 4.3,
                    "review_count": 12
                },
                {
                    "room_number": "201",
                    "room_type": "deluxe",
                    "capacity": 3,
                    "price_per_night": 150.0,
                    "description_en": "Spacious deluxe room with sea view and balcony",
                    "description_ar": "غرفة ديلوكس واسعة مع إطلالة على البحر وشرفة",
                    "amenities": '{"wifi": true, "ac": true, "tv": true, "minibar": true, "balcony": true}',
                    "rating": 4.6,
                    "review_count": 28
                },
                {
                    "room_number": "202",
                    "room_type": "deluxe",
                    "capacity": 3,
                    "price_per_night": 150.0,
                    "description_en": "Premium deluxe room with ocean view",
                    "description_ar": "غرفة ديلوكس مميزة مع إطلالة على المحيط",
                    "amenities": '{"wifi": true, "ac": true, "tv": true, "minibar": true, "balcony": true}',
                    "rating": 4.7,
                    "review_count": 22
                },
                {
                    "room_number": "301",
                    "room_type": "suite",
                    "capacity": 4,
                    "price_per_night": 250.0,
                    "description_en": "Luxury suite with panoramic sea view and jacuzzi",
                    "description_ar": "جناح فاخر مع إطلالة بانورامية على البحر وجاكوزي",
                    "amenities": '{"wifi": true, "ac": true, "tv": true, "minibar": true, "balcony": true, "jacuzzi": true}',
                    "rating": 4.9,
                    "review_count": 35
                },
                {
                    "room_number": "302",
                    "room_type": "suite",
                    "capacity": 4,
                    "price_per_night": 250.0,
                    "description_en": "Presidential suite with private terrace",
                    "description_ar": "الجناح الرئاسي مع تراس خاص",
                    "amenities": '{"wifi": true, "ac": true, "tv": true, "minibar": true, "balcony": true, "jacuzzi": true, "kitchen": true}',
                    "rating": 5.0,
                    "review_count": 18
                },
            ]
            
            for room_data in rooms_data:
                result = await db.execute(
                    select(Room).where(Room.room_number == room_data["room_number"])
                )
                if not result.scalar_one_or_none():
                    room = Room(**room_data)
                    db.add(room)
            
            # ==================== PRODUCTS ====================
            products_data = [
                {
                    "name": "VIP Beach Access",
                    "name_ar": "دخول الشاطئ VIP",
                    "slug": "vip-beach-access",
                    "type": "beach",
                    "base_price": 150.0,
                    "capacity": 2,
                    "description": "Exclusive VIP beach access with private cabana, waiter service, and premium amenities",
                    "description_ar": "دخول حصري لشاطئ VIP مع كابانا خاصة وخدمة نادل ووسائل راحة مميزة"
                },
                {
                    "name": "Standard Beach Access",
                    "name_ar": "دخول الشاطئ القياسي",
                    "slug": "standard-beach-access",
                    "type": "beach",
                    "base_price": 50.0,
                    "capacity": 2,
                    "description": "Standard beach access with sunbed and umbrella",
                    "description_ar": "دخول قياسي للشاطئ مع كرسي استلقاء ومظلة"
                },
                {
                    "name": "Banana Boat Ride",
                    "name_ar": "ركوب قارب الموز",
                    "slug": "banana-boat",
                    "type": "water_activity",
                    "base_price": 35.0,
                    "capacity": 6,
                    "description": "15-minute thrilling banana boat ride",
                    "description_ar": "رحلة مثيرة لمدة 15 دقيقة على قارب الموز",
                    "duration_minutes": 15,
                    "max_weight_kg": 120
                },
                {
                    "name": "Parasailing Adventure",
                    "name_ar": "مغامرة الطيران الشراعي",
                    "slug": "parasailing",
                    "type": "water_activity",
                    "base_price": 85.0,
                    "capacity": 1,
                    "description": "Soar above the Red Sea with breathtaking views",
                    "description_ar": "حلق فوق البحر الأحمر مع مناظر خلابة",
                    "duration_minutes": 20,
                    "max_weight_kg": 100
                },
                {
                    "name": "Jet Ski Rental",
                    "name_ar": "تأجير جت سكي",
                    "slug": "jet-ski",
                    "type": "water_activity",
                    "base_price": 60.0,
                    "capacity": 2,
                    "description": "30-minute jet ski rental with safety equipment",
                    "description_ar": "تأجير جت سكي لمدة 30 دقيقة مع معدات السلامة",
                    "duration_minutes": 30,
                    "max_weight_kg": 180
                },
                {
                    "name": "Snorkeling Trip",
                    "name_ar": "رحلة غطس",
                    "slug": "snorkeling",
                    "type": "water_activity",
                    "base_price": 45.0,
                    "capacity": 10,
                    "description": "2-hour guided snorkeling trip with equipment",
                    "description_ar": "رحلة غطس مصحوبة بمرشد لمدة ساعتين مع المعدات",
                    "duration_minutes": 120
                },
            ]
            
            for product_data in products_data:
                result = await db.execute(
                    select(Product).where(Product.slug == product_data["slug"])
                )
                if not result.scalar_one_or_none():
                    product = Product(**product_data)
                    db.add(product)
            
            # ==================== USERS ====================
            users_data = [
                {
                    "email": "admin@alkhayma.com",
                    "full_name": "System Administrator",
                    "hashed_password": HASHED_PASSWORD,
                    "role": "admin",
                    "is_active": True
                },
                {
                    "email": "staff@alkhayma.com",
                    "full_name": "Resort Staff",
                    "hashed_password": HASHED_PASSWORD,
                    "role": "staff",
                    "is_active": True
                },
                {
                    "email": "guest@test.com",
                    "full_name": "Test Guest",
                    "hashed_password": HASHED_PASSWORD,
                    "role": "guest",
                    "is_active": True
                },
            ]
            
            for user_data in users_data:
                result = await db.execute(
                    select(User).where(User.email == user_data["email"])
                )
                if not result.scalar_one_or_none():
                    user = User(**user_data)
                    db.add(user)
            
            await db.commit()
            
            # ==================== SUMMARY ====================
            final_rooms = await db.scalar(select(func.count()).select_from(Room))
            final_products = await db.scalar(select(func.count()).select_from(Product))
            final_users = await db.scalar(select(func.count()).select_from(User))
            
            print("\n✅ DATABASE SEEDING COMPLETED!")
            print("=" * 60)
            print(f"📊 Final Counts:")
            print(f"   Rooms:    {final_rooms}")
            print(f"   Products: {final_products}")
            print(f"   Users:    {final_users}")
            print("=" * 60)
            print(f"\n👤 Test Accounts (password: password123):")
            print(f"   Admin:  admin@alkhayma.com")
            print(f"   Staff:  staff@alkhayma.com")
            print(f"   Guest:  guest@test.com")
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            await db.rollback()
            raise

if __name__ == "__main__":
    asyncio.run(seed_database())
