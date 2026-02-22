"""
Comprehensive database seeding script for Al-Khayma Resort
Creates all necessary test data for development and testing
"""

import asyncio
from datetime import datetime, timedelta
from sqlalchemy import select, func
from app.core.database import AsyncSessionLocal, engine, Base
from app.models import (
    Room, Product, User, Booking, Payment, BlogPost,
    RoomType, RoomStatus, ProductType, BookingStatus,
    PaymentStatus, PaymentMethod, UserRole
)
from app.core.security import get_password_hash


async def create_tables():
    """Create all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created")


async def seed_rooms(session):
    """Seed rooms data"""
    result = await session.execute(select(func.count()).select_from(Room))
    count = result.scalar()
    
    if count > 0:
        print(f"   ℹ️  Rooms already exist ({count} found)")
        return
    
    rooms = [
        Room(
            room_number="101",
            room_type=RoomType.DELUXE,
            status=RoomStatus.AVAILABLE,
            price_per_night=150.0,
            capacity=2,
            description_en="Luxury sea view room with king bed and modern amenities",
            description_ar="غرفة فاخرة بإطلالة بحرية مع سرير كينج ومرافق حديثة",
            amenities='{"wifi": true, "ac": true, "tv": true, "minibar": true, "seaView": true}',
            is_active=True,
            rating=4.5,
            review_count=28
        ),
        Room(
            room_number="102",
            room_type=RoomType.DELUXE,
            status=RoomStatus.AVAILABLE,
            price_per_night=150.0,
            capacity=2,
            description_en="Luxury sea view room with twin beds",
            description_ar="غرفة فاخرة بإطلالة بحرية مع سريرين مفردين",
            amenities='{"wifi": true, "ac": true, "tv": true, "minibar": true, "seaView": true}',
            is_active=True,
            rating=4.3,
            review_count=22
        ),
        Room(
            room_number="201",
            room_type=RoomType.SUITE,
            status=RoomStatus.AVAILABLE,
            price_per_night=250.0,
            capacity=4,
            description_en="Premium suite with separate living area and private balcony",
            description_ar="جناح فاخر مع منطقة معيشة منفصلة وشرفة خاصة",
            amenities='{"wifi": true, "ac": true, "tv": true, "minibar": true, "jacuzzi": true, "balcony": true, "seaView": true}',
            is_active=True,
            rating=4.8,
            review_count=45
        ),
        Room(
            room_number="202",
            room_type=RoomType.SUITE,
            status=RoomStatus.OCCUPIED,
            price_per_night=280.0,
            capacity=4,
            description_en="Presidential suite with ocean view and butler service",
            description_ar="جناح رئاسي بإطلالة على المحيط وخدمة الخادم الشخصي",
            amenities='{"wifi": true, "ac": true, "tv": true, "minibar": true, "jacuzzi": true, "balcony": true, "seaView": true, "butler": true}',
            is_active=True,
            rating=4.9,
            review_count=38
        ),
        Room(
            room_number="301",
            room_type=RoomType.STANDARD,
            status=RoomStatus.AVAILABLE,
            price_per_night=80.0,
            capacity=2,
            description_en="Comfortable room with garden view",
            description_ar="غرفة مريحة بإطلالة على الحديقة",
            amenities='{"wifi": true, "ac": true, "tv": true}',
            is_active=True,
            rating=4.0,
            review_count=15
        ),
        Room(
            room_number="302",
            room_type=RoomType.STANDARD,
            status=RoomStatus.MAINTENANCE,
            price_per_night=75.0,
            capacity=2,
            description_en="Cozy room perfect for couples",
            description_ar="غرفة مريحة مثالية للأزواج",
            amenities='{"wifi": true, "ac": true, "tv": true}',
            is_active=False,
            rating=3.8,
            review_count=12
        ),
    ]
    
    for room in rooms:
        session.add(room)
    
    await session.commit()
    print(f"   ✅ Added {len(rooms)} rooms")


async def seed_products(session):
    """Seed products (beach spots, activities, services)"""
    result = await session.execute(select(func.count()).select_from(Product))
    count = result.scalar()
    
    if count > 0:
        print(f"   ℹ️  Products already exist ({count} found)")
        return
    
    products = [
        Product(
            name="VIP Beach Cabana",
            name_ar="كابانا شاطئ VIP",
            description="Private beach cabana with premium amenities and dedicated service",
            description_ar="كابانا شاطئ خاص مع مرافق متميزة وخدمة مخصصة",
            base_price=65.0,
            product_type=ProductType.BEACH,
            is_active=True,
            max_quantity=10
        ),
        Product(
            name="Standard Beach Spot",
            name_ar="مكان شاطئ عادي",
            description="Beach umbrella and comfortable chairs",
            description_ar="مظلة وكراسي مريحة على الشاطئ",
            base_price=25.0,
            product_type=ProductType.BEACH,
            is_active=True,
            max_quantity=50
        ),
        Product(
            name="Sunset Dinner Package",
            name_ar="باقة عشاء الغروب",
            description="Romantic beachfront dinner for two with candlelight",
            description_ar="عشاء رومانسي على الشاطئ لشخصين مع شموع",
            base_price=150.0,
            product_type=ProductType.ACTIVITY,
            is_active=True,
            max_quantity=20
        ),
        Product(
            name="Snorkeling Adventure",
            name_ar="مغامرة الغطس",
            description="Guided snorkeling tour with professional equipment",
            description_ar="جولة غطس بمرشد مع معدات احترافية",
            base_price=45.0,
            product_type=ProductType.ACTIVITY,
            is_active=True,
            max_quantity=30
        ),
        Product(
            name="Jet Ski Rental",
            name_ar="تأجير جيت سكي",
            description="30-minute jet ski experience with instructor",
            description_ar="تجربة جيت سكي لمدة 30 دقيقة مع مدرب",
            base_price=60.0,
            product_type=ProductType.ACTIVITY,
            is_active=True,
            max_quantity=8
        ),
        Product(
            name="Spa Massage",
            name_ar="مساج سبا",
            description="60-minute relaxing full-body massage",
            description_ar="مساج استرخائي للجسم كامل لمدة 60 دقيقة",
            base_price=80.0,
            product_type=ProductType.SERVICE,
            is_active=True,
            max_quantity=15
        ),
    ]
    
    for product in products:
        session.add(product)
    
    await session.commit()
    print(f"   ✅ Added {len(products)} products")


async def seed_users(session):
    """Seed users (admin and test users)"""
    result = await session.execute(select(func.count()).select_from(User))
    count = result.scalar()
    
    if count > 0:
        print(f"   ℹ️  Users already exist ({count} found)")
        return
    
    users = [
        User(
            email="admin@alkhayma.com",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            is_active=True,
            phone="+20 100 000 0000"
        ),
        User(
            email="manager@alkhayma.com",
            full_name="Hotel Manager",
            hashed_password=get_password_hash("manager123"),
            role=UserRole.STAFF,
            is_active=True,
            phone="+20 100 000 0001"
        ),
        User(
            email="test@example.com",
            full_name="Test Guest",
            hashed_password=get_password_hash("test123"),
            role=UserRole.GUEST,
            is_active=True,
            phone="+20 100 123 4567"
        ),
        User(
            email="john.doe@gmail.com",
            full_name="John Doe",
            hashed_password=get_password_hash("password123"),
            role=UserRole.GUEST,
            is_active=True,
            phone="+1 555 123 4567"
        ),
        User(
            email="sarah.smith@yahoo.com",
            full_name="Sarah Smith",
            hashed_password=get_password_hash("password123"),
            role=UserRole.GUEST,
            is_active=True,
            phone="+44 7700 900123"
        ),
    ]
    
    for user in users:
        session.add(user)
    
    await session.commit()
    print(f"   ✅ Added {len(users)} users")


async def seed_blog_posts(session):
    """Seed blog posts"""
    result = await session.execute(select(func.count()).select_from(BlogPost))
    count = result.scalar()
    
    if count > 0:
        print(f"   ℹ️  Blog posts already exist ({count} found)")
        return
    
    posts = [
        BlogPost(
            title="Top 5 Beach Activities in Red Sea",
            title_ar="أفضل 5 أنشطة شاطئية في البحر الأحمر",
            slug="top-5-beach-activities",
            content="Discover the most exciting water sports and beach activities available at our resort. From snorkeling to jet skiing, there's something for everyone...",
            content_ar="اكتشف أبرز الرياضات المائية والأنشطة الشاطئية المتوفرة في منتجعنا. من الغطس إلى الجيت سكي، هناك شيء للجميع...",
            excerpt="Discover exciting water sports and beach activities for the whole family",
            excerpt_ar="اكتشف الرياضات المائية والأنشطة الشاطئية المثيرة للعائلة",
            author="Resort Team",
            is_published=True,
            featured_image="https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800",
            category="Activities",
            tags="beach,water sports,snorkeling,family"
        ),
        BlogPost(
            title="Planning the Perfect Beach Wedding",
            title_ar="تخطيط حفل زفاف شاطئي مثالي",
            slug="perfect-beach-wedding",
            content="Getting married on the beach is a magical experience. Here's our complete guide to planning your dream wedding...",
            content_ar="الزواج على الشاطئ هو تجربة ساحرة. إليك دليلنا الكامل لتخطيط حفل زفاف أحلامك...",
            excerpt="A complete guide to planning your dream wedding on the beach",
            excerpt_ar="دليل كامل لتخطيط حفل زفاف أحلامك على الشاطئ",
            author="Events Team",
            is_published=True,
            featured_image="https://images.unsplash.com/photo-1519741497674-611481863552?w=800",
            category="Events",
            tags="wedding,beach,romance,events"
        ),
        BlogPost(
            title="Luxury Dining Experience at Al-Bahr Restaurant",
            title_ar="تجربة طعام فاخرة في مطعم البحر",
            slug="luxury-dining-experience",
            content="Our restaurant offers authentic Egyptian and international cuisine with a stunning sea view...",
            content_ar="يقدم مطعمنا المأكولات المصرية الأصيلة والعالمية مع إطلالة بحرية خلابة...",
            excerpt="Explore our world-class cuisine and dining facilities",
            excerpt_ar="استكشف مطبخنا العالمي ومرافق الطعام",
            author="Chef Ahmed",
            is_published=True,
            featured_image="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
            category="Dining",
            tags="restaurant,dining,cuisine,food"
        ),
    ]
    
    for post in posts:
        session.add(post)
    
    await session.commit()
    print(f"   ✅ Added {len(posts)} blog posts")


async def seed_all():
    """Main seeding function"""
    print("🌱 Starting database seeding...")
    print()
    
    # Create tables
    await create_tables()
    print()
    
    async with AsyncSessionLocal() as session:
        # Seed all data
        await seed_rooms(session)
        await seed_products(session)
        await seed_users(session)
        await seed_blog_posts(session)
        
        print()
        print("=" * 50)
        print("🎉 Database seeding completed successfully!")
        print("=" * 50)
        print()
        print("Test Accounts:")
        print("  Admin: admin@alkhayma.com / admin123")
        print("  Manager: manager@alkhayma.com / manager123")
        print("  Guest: test@example.com / test123")
        print()


if __name__ == "__main__":
    asyncio.run(seed_all())
