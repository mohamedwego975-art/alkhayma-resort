"""
Seed data script for الخيمة Beach Resort
Run this to populate the database with sample rooms, products, and testimonials
"""

import asyncio
import logging
from datetime import datetime, timezone
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.room import Room, RoomType
from app.models.product import Product, ProductType
from app.models.user import User, UserRole

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def seed_rooms():
    """Seed rooms with sample data"""
    async with AsyncSessionLocal() as session:
        # Check if rooms already exist
        result = await session.execute(select(Room))
        if result.scalars().first():
            logger.info("Rooms already seeded, skipping...")
            return
        
        rooms_data = [
            {
                "room_number": "101",
                "room_type": RoomType.DELUXE,
                "description_en": "Spacious deluxe room with stunning Red Sea views, featuring a king-size bed, modern furnishings, and a private balcony.",
                "description_ar": "غرفة ديلوكس فسيحة بإطلالات خلابة على البحر الأحمر، مع سرير كينج حديث وشرفة خاصة.",
                "price_per_night": 120.00,
                "capacity": 2,
                "amenities": "WiFi,TV,AC,Mini Bar,Safe,Sea View",
                "is_active": True
            },
            {
                "room_number": "102",
                "room_type": RoomType.DELUXE,
                "description_en": "Elegant deluxe room with garden views, perfect for couples seeking tranquility and comfort.",
                "description_ar": "غرفة ديلوكس أنيقة بإطلالات على الحديقة، مثالية للأزواج الباحثين عن الهدوء والراحة.",
                "price_per_night": 110.00,
                "capacity": 2,
                "amenities": "WiFi,TV,AC,Mini Bar,Safe,Garden View",
                "is_active": True
            },
            {
                "room_number": "201",
                "room_type": RoomType.SUITE,
                "description_en": "Luxurious suite with separate living area, master bedroom, and panoramic sea views from the private terrace.",
                "description_ar": "جناح فاخر مع منطقة معيشة منفصلة وغرفة نوم رئيسية وإطلالات بانورامية على البحر من التراس الخاص.",
                "price_per_night": 250.00,
                "capacity": 3,
                "amenities": "WiFi,TV,AC,Mini Bar,Safe,Sea View,Jacuzzi,Living Room",
                "is_active": True
            },
            {
                "room_number": "202",
                "room_type": RoomType.SUITE,
                "description_en": "Premium suite featuring two bedrooms, two bathrooms, and a spacious terrace overlooking the pool.",
                "description_ar": "جناح بريميوم يضم غرفتي نوم وحمامين وتراس فسيح يطل على المسبح.",
                "price_per_night": 300.00,
                "capacity": 4,
                "amenities": "WiFi,TV,AC,Mini Bar,Safe,Pool View,2 Bedrooms,2 Bathrooms,Kitchenette",
                "is_active": True
            },
            {
                "room_number": "301",
                "room_type": RoomType.VILLA,
                "description_en": "Family room with connecting rooms, perfect for families with children. Features garden views and kid-friendly amenities.",
                "description_ar": "غرفة عائلية مع غرف متصلة، مثالية للعائلات ذات الأطفال. تضم إطلالات على الحديقة ووسائل راحة مناسبة للأطفال.",
                "price_per_night": 180.00,
                "capacity": 4,
                "amenities": "WiFi,TV,AC,Mini Bar,Safe,Garden View,Connecting Rooms,Kids Amenities",
                "is_active": True
            },
            {
                "room_number": "401",
                "room_type": RoomType.VILLA,
                "description_en": "The ultimate luxury experience. Presidential suite with 3 bedrooms, private pool, butler service, and 360° sea views.",
                "description_ar": "تجربة فاخرة في أقصى درجاتها. الجناح الرئاسي مع 3 غرف نوم ومسبح خاص وخدمة كونسيرج وإطلالات 360° على البحر.",
                "price_per_night": 800.00,
                "capacity": 6,
                "amenities": "WiFi,TV,AC,Mini Bar,Safe,Sea View,Private Pool,Butler Service,3 Bedrooms,Dining Room,Kitchen",
                "is_active": True
            }
        ]
        
        for room_data in rooms_data:
            room = Room(**room_data)
            session.add(room)
        
        await session.commit()
        logger.info(f"Seeded {len(rooms_data)} rooms")

async def seed_products():
    """Seed products (activities, spa, dining add-ons)"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Product))
        if result.scalars().first():
            logger.info("Products already seeded, skipping...")
            return
        
        products_data = [
            {
                "name": "VIP Beach Access",
                "name_ar": "وصول VIP للشاطئ",
                "slug": "vip-beach-access",
                "type": ProductType.BEACH,
                "base_price": 65.00,
                "capacity": 10,
                "description": "Private cabana with premium amenities including dedicated waiter service",
                "description_ar": "كابينة خاصة مع خدمات متميزة وخدمة نادل مخصصة",
                "duration_minutes": 480,
                "max_weight_kg": 120,
                "is_active": True,
                "updated_at": datetime.now(timezone.utc),
            },
            {
                "name": "Romantic Beach Dinner",
                "name_ar": "عشاء رومانسي على الشاطئ",
                "slug": "romantic-beach-dinner",
                "type": ProductType.RESTAURANT,
                "base_price": 150.00,
                "capacity": 2,
                "description": "Private candlelit dinner on the beach with personalized menu",
                "description_ar": "عشاء خاص على الشاطئ مع قائمة شخصية",
                "duration_minutes": 180,
                "max_weight_kg": 120,
                "is_active": True,
                "updated_at": datetime.now(timezone.utc),
            },
            {
                "name": "Couples Spa Package",
                "name_ar": "باقة سبا للأزواج",
                "slug": "couples-spa-package",
                "type": ProductType.WATER_ACTIVITY,
                "base_price": 120.00,
                "capacity": 2,
                "description": "60-minute couples massage with aromatherapy and private suite",
                "description_ar": "تدليك للأزواج 60 دقيقة مع العلاج العطري وغرفة خاصة",
                "duration_minutes": 120,
                "max_weight_kg": 120,
                "is_active": True,
                "updated_at": datetime.now(timezone.utc),
            },
            {
                "name": "Sunset Yacht Cruise",
                "name_ar": "رحلة يخت عند الغروب",
                "slug": "sunset-yacht-cruise",
                "type": ProductType.WATER_ACTIVITY,
                "base_price": 300.00,
                "capacity": 8,
                "description": "2-hour private yacht cruise with champagne and canapés",
                "description_ar": "رحلة يخت خاصة ساعتين مع الشمبانيا والمقبلات",
                "duration_minutes": 120,
                "max_weight_kg": 150,
                "is_active": True,
                "updated_at": datetime.now(timezone.utc),
            },
            {
                "name": "Scuba Diving Experience",
                "name_ar": "تجربة الغوص",
                "slug": "scuba-diving-experience",
                "type": ProductType.WATER_ACTIVITY,
                "base_price": 85.00,
                "capacity": 4,
                "description": "Beginner scuba diving with certified instructor and all equipment",
                "description_ar": "غوص للمبتدئين مع مدرب معتمد وجميع المعدات",
                "duration_minutes": 180,
                "max_weight_kg": 120,
                "is_active": True,
                "updated_at": datetime.now(timezone.utc),
            },
        ]
        for product_data in products_data:
            product = Product(**product_data)
            session.add(product)
        
        await session.commit()
        logger.info(f"Seeded {len(products_data)} products")

async def seed_admin():
    """Create admin user if not exists (for login to admin panel)."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == "admin@alkhayma.com"))
        if result.scalar_one_or_none():
            logger.info("Admin user already exists, skipping.")
            return
        admin = User(
            email="admin@alkhayma.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin",
            role=UserRole.ADMIN,
            is_active=True,
        )
        session.add(admin)
        await session.commit()
        logger.info("Created admin user: admin@alkhayma.com / admin123")


async def seed_reviews():
    """Reviews require existing users and bookings (booking_id, user_id). Skipped in basic seed."""
    logger.info("Reviews require existing bookings and users; skipping. Use scripts/archive/seed_database.py for full seed.")

async def seed_all():
    """Run all seed functions"""
    logger.info("Starting database seeding...")
    
    try:
        await seed_rooms()
        await seed_products()
        await seed_admin()
        await seed_reviews()
        logger.info("Database seeding completed successfully!")
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(seed_all())
