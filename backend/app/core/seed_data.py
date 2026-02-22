"""
Seed data script for الخيمة Beach Resort
Run this to populate the database with sample rooms, products, and testimonials
"""

import asyncio
import logging
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from app.core.database import engine, Base, get_db
from app.models.room import Room, RoomType
from app.models.product import Product, ProductCategory
from app.models.review import Review

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def seed_rooms():
    """Seed rooms with sample data"""
    async with async_session() as session:
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
                "room_type": RoomType.FAMILY,
                "description_en": "Family room with connecting rooms, perfect for families with children. Features garden views and kid-friendly amenities.",
                "description_ar": "غرفة عائلية مع غرف متصلة، مثالية للعائلات ذات الأطفال. تضم إطلالات على الحديقة ووسائل راحة مناسبة للأطفال.",
                "price_per_night": 180.00,
                "capacity": 4,
                "amenities": "WiFi,TV,AC,Mini Bar,Safe,Garden View,Connecting Rooms,Kids Amenities",
                "is_active": True
            },
            {
                "room_number": "401",
                "room_type": RoomType.PRESIDENTIAL,
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
    async with async_session() as session:
        result = await session.execute(select(Product))
        if result.scalars().first():
            logger.info("Products already seeded, skipping...")
            return
        
        products_data = [
            {
                "name": "VIP Beach Access",
                "description": "Private cabana with premium amenities including dedicated waiter service",
                "category": ProductCategory.ACTIVITY,
                "price": 65.00,
                "duration_hours": 8,
                "max_capacity": 10,
                "is_active": True
            },
            {
                "name": "Romantic Beach Dinner",
                "description": "Private candlelit dinner on the beach with personalized menu",
                "category": ProductCategory.DINING,
                "price": 150.00,
                "duration_hours": 3,
                "max_capacity": 2,
                "is_active": True
            },
            {
                "name": "Couples Spa Package",
                "description": "60-minute couples massage with aromatherapy and private suite",
                "category": ProductCategory.SPA,
                "price": 120.00,
                "duration_hours": 2,
                "max_capacity": 2,
                "is_active": True
            },
            {
                "name": "Sunset Yacht Cruise",
                "description": "2-hour private yacht cruise with champagne and canapés",
                "category": ProductCategory.ACTIVITY,
                "price": 300.00,
                "duration_hours": 2,
                "max_capacity": 8,
                "is_active": True
            },
            {
                "name": "Scuba Diving Experience",
                "description": "Beginner scuba diving with certified instructor and all equipment",
                "category": ProductCategory.ACTIVITY,
                "price": 85.00,
                "duration_hours": 3,
                "max_capacity": 4,
                "is_active": True
            },
            {
                "name": "Kids Club Day Pass",
                "description": "Full day of supervised activities for children aged 4-12",
                "category": ProductCategory.ACTIVITY,
                "price": 35.00,
                "duration_hours": 8,
                "max_capacity": 20,
                "is_active": True
            },
            {
                "name": "Airport Transfer - Premium",
                "description": "Private luxury car transfer from Sharm El Sheikh Airport",
                "category": ProductCategory.TRANSPORT,
                "price": 40.00,
                "duration_hours": 1,
                "max_capacity": 4,
                "is_active": True
            },
            {
                "name": "Desert Safari Adventure",
                "description": "4x4 desert safari with Bedouin dinner and stargazing",
                "category": ProductCategory.ACTIVITY,
                "price": 75.00,
                "duration_hours": 5,
                "max_capacity": 6,
                "is_active": True
            }
        ]
        
        for product_data in products_data:
            product = Product(**product_data)
            session.add(product)
        
        await session.commit()
        logger.info(f"Seeded {len(products_data)} products")

async def seed_reviews():
    """Seed sample reviews"""
    async with async_session() as session:
        result = await session.execute(select(Review))
        if result.scalars().first():
            logger.info("Reviews already seeded, skipping...")
            return
        
        reviews_data = [
            {
                "product_id": 1,
                "user_name": "Sarah Johnson",
                "rating": 5,
                "comment": "An absolutely magical experience. The staff went above and beyond to make our anniversary special. The beach is pristine and the rooms are luxurious.",
                "country": "United Kingdom",
                "is_approved": True
            },
            {
                "product_id": 1,
                "user_name": "Ahmed Hassan",
                "rating": 5,
                "comment": "Best vacation spot on the Red Sea! The VIP beach experience was worth every penny. Highly recommend for families and couples alike.",
                "country": "Egypt",
                "is_approved": True
            },
            {
                "product_id": 1,
                "user_name": "Marie Dupont",
                "rating": 5,
                "comment": "From booking to checkout, everything was perfect. The breakfast buffet is amazing, and the water activities kept my kids entertained all day.",
                "country": "France",
                "is_approved": True
            },
            {
                "product_id": 2,
                "user_name": "John Smith",
                "rating": 5,
                "comment": "The romantic dinner on the beach was unforgettable. Perfect proposal spot!",
                "country": "United States",
                "is_approved": True
            },
            {
                "product_id": 3,
                "user_name": "Emma Wilson",
                "rating": 5,
                "comment": "The spa treatment was heavenly. Professional staff and beautiful facilities.",
                "country": "Germany",
                "is_approved": True
            }
        ]
        
        for review_data in reviews_data:
            review = Review(**review_data)
            session.add(review)
        
        await session.commit()
        logger.info(f"Seeded {len(reviews_data)} reviews")

async def seed_all():
    """Run all seed functions"""
    logger.info("Starting database seeding...")
    
    try:
        await seed_rooms()
        await seed_products()
        await seed_reviews()
        logger.info("Database seeding completed successfully!")
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        raise

if __name__ == "__main__":
    # Import AsyncSession here to avoid circular imports
    from sqlalchemy.ext.asyncio import AsyncSession
    asyncio.run(seed_all())
