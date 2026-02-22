#!/usr/bin/env python3
"""
Comprehensive Seed Script for PostgreSQL
Populates the database with realistic test data for Al-Khayma Beach Resort
"""
import asyncio
import sys
from datetime import datetime, timedelta
from decimal import Decimal

sys.path.insert(0, '/home/wego/Desktop/alkhayma-resort/backend')

from app.core.database import AsyncSessionLocal, engine, Base
from app.models import (
    Room, Product, User, Booking, Payment, BlogPost,
    RoomType, RoomStatus, ProductType, BookingStatus,
    PaymentStatus, PaymentMethod, UserRole
)
from app.core.security import get_password_hash
from sqlalchemy import select, func

async def create_tables():
    """Create all database tables using SQLAlchemy metadata"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created successfully")

async def seed_rooms(session):
    """Seed rooms with realistic data"""
    result = await session.execute(select(func.count()).select_from(Room))
    count = result.scalar()
    
    if count > 0:
        print(f"ℹ️  Rooms already exist ({count} found), skipping...")
        return
    
    rooms = [
        # Deluxe Rooms - Sea View
        Room(
            room_number="101",
            room_type=RoomType.DELUXE,
            status=RoomStatus.AVAILABLE,
            price_per_night=Decimal("150.00"),
            capacity=2,
            description_en="Luxury sea view room with king-size bed, modern amenities, and private balcony overlooking the Red Sea.",
            description_ar="غرفة فاخرة بإطلالة بحرية مع سرير كينج، مرافق حديثة، وشرفة خاصة تطل على البحر الأحمر.",
            amenities='["wifi", "ac", "tv", "minibar", "sea_view", "balcony", "safe", "coffee_machine"]',
            is_active=True,
            rating=4.5,
            review_count=28,
            floor=1,
            bed_type="king"
        ),
        Room(
            room_number="102",
            room_type=RoomType.DELUXE,
            status=RoomStatus.AVAILABLE,
            price_per_night=Decimal("150.00"),
            capacity=2,
            description_en="Luxury sea view room with twin beds, perfect for friends or colleagues.",
            description_ar="غرفة فاخرة بإطلالة بحرية مع سريرين مفردين، مثالية للأصدقاء أو الزملاء.",
            amenities='["wifi", "ac", "tv", "minibar", "sea_view", "balcony", "safe"]',
            is_active=True,
            rating=4.3,
            review_count=22,
            floor=1,
            bed_type="twin"
        ),
        Room(
            room_number="103",
            room_type=RoomType.DELUXE,
            status=RoomStatus.OCCUPIED,
            price_per_night=Decimal("150.00"),
            capacity=2,
            description_en="Luxury sea view room with premium furnishings and ocean vista.",
            description_ar="غرفة فاخرة بإطلالة بحرية مع أثاث متميز وإطلالة على المحيط.",
            amenities='["wifi", "ac", "tv", "minibar", "sea_view", "balcony", "safe", "bathtub"]',
            is_active=True,
            rating=4.7,
            review_count=35,
            floor=1,
            bed_type="king"
        ),
        
        # Suite Rooms - Premium
        Room(
            room_number="201",
            room_type=RoomType.SUITE,
            status=RoomStatus.AVAILABLE,
            price_per_night=Decimal("250.00"),
            capacity=4,
            description_en="Premium suite with separate living area, private balcony, and panoramic sea views. Includes jacuzzi.",
            description_ar="جناح فاخر مع منطقة معيشة منفصلة، شرفة خاصة، وإطلالات بحرية بانورامية. يشمل جاكوزي.",
            amenities='["wifi", "ac", "tv", "minibar", "jacuzzi", "balcony", "sea_view", "living_room", "dining_area", "kitchenette", "safe"]',
            is_active=True,
            rating=4.8,
            review_count=45,
            floor=2,
            bed_type="king"
        ),
        Room(
            room_number="202",
            room_type=RoomType.SUITE,
            status=RoomStatus.AVAILABLE,
            price_per_night=Decimal("280.00"),
            capacity=4,
            description_en="Presidential suite with ocean view, butler service, private dining area, and luxury amenities.",
            description_ar="الجناح الرئاسي بإطلالة على المحيط، خدمة الخادم الشخصي، منطقة طعام خاصة، ومرافق فاخرة.",
            amenities='["wifi", "ac", "tv", "minibar", "jacuzzi", "balcony", "sea_view", "living_room", "dining_area", "kitchenette", "safe", "butler_service", "private_entrance"]',
            is_active=True,
            rating=4.9,
            review_count=38,
            floor=2,
            bed_type="king"
        ),
        
        # Standard Rooms - Garden View
        Room(
            room_number="301",
            room_type=RoomType.STANDARD,
            status=RoomStatus.AVAILABLE,
            price_per_night=Decimal("80.00"),
            capacity=2,
            description_en="Comfortable room with garden view, perfect for budget-conscious travelers.",
            description_ar="غرفة مريحة بإطلالة على الحديقة، مثالية للمسافرين ذوي الميزانية المحدودة.",
            amenities='["wifi", "ac", "tv", "garden_view"]',
            is_active=True,
            rating=4.0,
            review_count=15,
            floor=3,
            bed_type="queen"
        ),
        Room(
            room_number="302",
            room_type=RoomType.STANDARD,
            status=RoomStatus.MAINTENANCE,
            price_per_night=Decimal("75.00"),
            capacity=2,
            description_en="Cozy room perfect for couples, currently under renovation.",
            description_ar="غرفة مريحة مثالية للأزواج، تحت التجديد حالياً.",
            amenities='["wifi", "ac", "tv"]',
            is_active=False,
            rating=3.8,
            review_count=12,
            floor=3,
            bed_type="queen"
        ),
        
        # Family Rooms
        Room(
            room_number="401",
            room_type=RoomType.FAMILY,
            status=RoomStatus.AVAILABLE,
            price_per_night=Decimal("200.00"),
            capacity=6,
            description_en="Spacious family room with two bedrooms, living area, and garden access. Perfect for families.",
            description_ar="غرفة عائلية واسعة مع غرفتين، منطقة معيشة، ووصول للحديقة. مثالية للعائلات.",
            amenities='["wifi", "ac", "tv", "minibar", "garden_view", "living_room", "bathtub", "safe", "kids_amenities"]',
            is_active=True,
            rating=4.6,
            review_count=42,
            floor=4,
            bed_type="king_and_twin"
        ),
    ]
    
    for room in rooms:
        session.add(room)
    
    await session.commit()
    print(f"✅ Added {len(rooms)} rooms")

async def seed_products(session):
    """Seed products and services"""
    result = await session.execute(select(func.count()).select_from(Product))
    count = result.scalar()
    
    if count > 0:
        print(f"ℹ️  Products already exist ({count} found), skipping...")
        return
    
    products = [
        # Beach Services
        Product(
            name="VIP Beach Cabana",
            name_ar="كابانا شاطئ VIP",
            description="Private beach cabana with premium amenities, dedicated service, and prime beachfront location. Includes fresh towels, water, and fruit platter.",
            description_ar="كابانا شاطئ خاص مع مرافق متميزة، خدمة مخصصة، وموقع ممتاز على الواجهة البحرية. يتضمن مناشف طازجة، مياه، وطبق فواكه.",
            base_price=Decimal("65.00"),
            product_type=ProductType.BEACH,
            is_active=True,
            max_quantity=10,
            requires_booking=True,
            duration_minutes=480  # 8 hours
        ),
        Product(
            name="Standard Beach Spot",
            name_ar="مكان شاطئ عادي",
            description="Beach umbrella and comfortable chairs with shade. Perfect for a relaxing day by the sea.",
            description_ar="مظلة وكراسي مريحة على الشاطئ مع ظل. مثالي ليوم استرخاء بجانب البحر.",
            base_price=Decimal("25.00"),
            product_type=ProductType.BEACH,
            is_active=True,
            max_quantity=50,
            requires_booking=True,
            duration_minutes=480
        ),
        
        # Activities
        Product(
            name="Sunset Dinner Package",
            name_ar="باقة عشاء الغروب",
            description="Romantic beachfront dinner for two with candlelight, fresh seafood, and wine. Includes private table setup on the beach.",
            description_ar="عشاء رومانسي على الشاطئ لشخصين مع الشموع، مأكولات بحرية طازجة، ونبيذ. يتضمن طاولة خاصة على الشاطئ.",
            base_price=Decimal("150.00"),
            product_type=ProductType.ACTIVITY,
            is_active=True,
            max_quantity=20,
            requires_booking=True,
            duration_minutes=180
        ),
        Product(
            name="Snorkeling Adventure",
            name_ar="مغامرة الغطس",
            description="Guided snorkeling tour with professional equipment and instructor. Explore the beautiful coral reefs of the Red Sea.",
            description_ar="جولة غطس بمرشد مع معدات احترافية ومدرب. استكشف الشعاب المرجانية الجميلة في البحر الأحمر.",
            base_price=Decimal("45.00"),
            product_type=ProductType.ACTIVITY,
            is_active=True,
            max_quantity=30,
            requires_booking=True,
            duration_minutes=120
        ),
        Product(
            name="Jet Ski Rental",
            name_ar="تأجير جيت سكي",
            description="30-minute jet ski experience with safety briefing and instructor supervision. Fun and adrenaline on the water!",
            description_ar="تجربة جيت سكي لمدة 30 دقيقة مع إحاطة أمنية وإشراف مدرب. متعة وأدرينالين على الماء!",
            base_price=Decimal("60.00"),
            product_type=ProductType.ACTIVITY,
            is_active=True,
            max_quantity=8,
            requires_booking=True,
            duration_minutes=30
        ),
        Product(
            name="Sunset Cruise",
            name_ar="رحلة غروب الشمس",
            description="2-hour boat cruise with drinks and snacks. Watch the sunset from the water with beautiful views.",
            description_ar="رحلة قارب لمدة ساعتين مع المشروبات والوجبات الخفيفة. شاهد غروب الشمس من الماء مع إطلالات جميلة.",
            base_price=Decimal("85.00"),
            product_type=ProductType.ACTIVITY,
            is_active=True,
            max_quantity=25,
            requires_booking=True,
            duration_minutes=120
        ),
        Product(
            name="Beach Volleyball Tournament",
            name_ar="بطولة الكرة الطائرة الشاطئية",
            description="Join our weekly beach volleyball tournament. Equipment and refreshments provided. Fun for all skill levels!",
            description_ar="انضم إلى بطولتنا الأسبوعية للكرة الطائرة الشاطئية. المعدات والمشروبات مقدمة. متعة لجميع المستويات!",
            base_price=Decimal("15.00"),
            product_type=ProductType.ACTIVITY,
            is_active=True,
            max_quantity=40,
            requires_booking=True,
            duration_minutes=180
        ),
        
        # Spa Services
        Product(
            name="Spa Massage - 60min",
            name_ar="مساج سبا - 60 دقيقة",
            description="60-minute relaxing full-body massage with essential oils. Choose from Swedish, Deep Tissue, or Aromatherapy.",
            description_ar="مساج استرخائي للجسم كامل لمدة 60 دقيقة مع زيوت أساسية. اختر من السويدي، الأنسجة العميقة، أو العلاج بالروائح.",
            base_price=Decimal("80.00"),
            product_type=ProductType.SERVICE,
            is_active=True,
            max_quantity=15,
            requires_booking=True,
            duration_minutes=60
        ),
        Product(
            name="Spa Massage - 90min",
            name_ar="مساج سبا - 90 دقيقة",
            description="90-minute luxury spa experience including full-body massage, facial, and hot stone therapy.",
            description_ar="تجربة سبا فاخرة لمدة 90 دقيقة تشمل مساج كامل للجسم، علاج للوجه، وعلاج بالحجارة الساخنة.",
            base_price=Decimal("120.00"),
            product_type=ProductType.SERVICE,
            is_active=True,
            max_quantity=10,
            requires_booking=True,
            duration_minutes=90
        ),
        Product(
            name="Couples Spa Package",
            name_ar="باقة سبا للأزواج",
            description="Romantic couples massage in a private suite with champagne and chocolates. 90 minutes of pure bliss.",
            description_ar="مساج رومانسي للأزواج في جناح خاص مع شمبانيا وشوكولاتة. 90 دقيقة من النقاء.",
            base_price=Decimal("200.00"),
            product_type=ProductType.SERVICE,
            is_active=True,
            max_quantity=5,
            requires_booking=True,
            duration_minutes=90
        ),
        
        # Dining
        Product(
            name="Beach BBQ Buffet",
            name_ar="بوفيه شواء الشاطئ",
            description="All-you-can-eat beach BBQ with grilled meats, seafood, salads, and desserts. Live music included!",
            description_ar="بوفيه شواء شاطئ بلا حدود مع لحوم مشوية، مأكولات بحرية، سلطات، وحلويات. موسيقى حية مشمولة!",
            base_price=Decimal("55.00"),
            product_type=ProductType.SERVICE,
            is_active=True,
            max_quantity=100,
            requires_booking=True,
            duration_minutes=180
        ),
    ]
    
    for product in products:
        session.add(product)
    
    await session.commit()
    print(f"✅ Added {len(products)} products/services")

async def seed_users(session):
    """Seed users with different roles"""
    result = await session.execute(select(func.count()).select_from(User))
    count = result.scalar()
    
    if count > 0:
        print(f"ℹ️  Users already exist ({count} found), skipping...")
        return
    
    users = [
        # Admin
        User(
            email="admin@alkhayma.com",
            full_name="System Administrator",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            is_active=True,
            phone="+20 100 000 0000",
            email_verified=True,
            phone_verified=True,
            preferred_language="en",
            notifications_enabled=True
        ),
        # Staff
        User(
            email="manager@alkhayma.com",
            full_name="Hotel Manager",
            hashed_password=get_password_hash("manager123"),
            role=UserRole.STAFF,
            is_active=True,
            phone="+20 100 000 0001",
            email_verified=True,
            phone_verified=True,
            preferred_language="en",
            notifications_enabled=True
        ),
        User(
            email="reception@alkhayma.com",
            full_name="Reception Team",
            hashed_password=get_password_hash("reception123"),
            role=UserRole.STAFF,
            is_active=True,
            phone="+20 100 000 0002",
            email_verified=True,
            phone_verified=True,
            preferred_language="ar",
            notifications_enabled=True
        ),
        # Guests
        User(
            email="test@example.com",
            full_name="Test Guest",
            hashed_password=get_password_hash("test123"),
            role=UserRole.GUEST,
            is_active=True,
            phone="+20 100 123 4567",
            email_verified=True,
            phone_verified=True,
            preferred_language="en",
            notifications_enabled=True
        ),
        User(
            email="john.doe@gmail.com",
            full_name="John Doe",
            hashed_password=get_password_hash("password123"),
            role=UserRole.GUEST,
            is_active=True,
            phone="+1 555 123 4567",
            email_verified=True,
            phone_verified=False,
            preferred_language="en",
            notifications_enabled=True
        ),
        User(
            email="sarah.smith@yahoo.com",
            full_name="Sarah Smith",
            hashed_password=get_password_hash("password123"),
            role=UserRole.GUEST,
            is_active=True,
            phone="+44 7700 900123",
            email_verified=True,
            phone_verified=True,
            preferred_language="en",
            notifications_enabled=True
        ),
        User(
            email="ahmed.hassan@email.com",
            full_name="Ahmed Hassan",
            hashed_password=get_password_hash("password123"),
            role=UserRole.GUEST,
            is_active=True,
            phone="+20 100 987 6543",
            email_verified=True,
            phone_verified=True,
            preferred_language="ar",
            notifications_enabled=True
        ),
    ]
    
    for user in users:
        session.add(user)
    
    await session.commit()
    print(f"✅ Added {len(users)} users")

async def seed_blog_posts(session):
    """Seed blog posts"""
    result = await session.execute(select(func.count()).select_from(BlogPost))
    count = result.scalar()
    
    if count > 0:
        print(f"ℹ️  Blog posts already exist ({count} found), skipping...")
        return
    
    posts = [
        BlogPost(
            title="Top 5 Beach Activities in Red Sea",
            title_ar="أفضل 5 أنشطة شاطئية في البحر الأحمر",
            slug="top-5-beach-activities",
            content="""Discover the most exciting water sports and beach activities available at our resort. 
            From snorkeling to jet skiing, there's something for everyone.

            1. Snorkeling - Explore the coral reefs
            2. Jet Skiing - Feel the adrenaline
            3. Sunset Cruise - Romantic evening
            4. Beach Volleyball - Fun with friends
            5. Spa Treatment - Relax and unwind

            Book your activities now and make the most of your beach vacation!""",
            content_ar="""اكتشف أبرز الرياضات المائية والأنشطة الشاطئية المتوفرة في منتجعنا.
            من الغطس إلى الجيت سكي، هناك شيء للجميع.

            ١. الغطس - استكشف الشعاب المرجانية
            ٢. الجيت سكي - اشعر بالأدرينالين
            ٣. رحلة الغروب - مساء رومانسي
            ٤. الكرة الطائرة الشاطئية - متعة مع الأصدقاء
            ٥. علاج السبا - استرخِ واستجم

            احجز أنشطتك الآن واستفد إلى أقصى حد من إجازتك الشاطئية!""",
            excerpt="Discover exciting water sports and beach activities for the whole family",
            excerpt_ar="اكتشف الرياضات المائية والأنشطة الشاطئية المثيرة للعائلة",
            author="Resort Team",
            is_published=True,
            featured_image="https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800",
            category="Activities",
            tags="beach,water sports,snorkeling,family",
            view_count=1250,
            published_at=datetime.now() - timedelta(days=30)
        ),
        BlogPost(
            title="Planning the Perfect Beach Wedding",
            title_ar="تخطيط حفل زفاف شاطئي مثالي",
            slug="perfect-beach-wedding",
            content="""Getting married on the beach is a magical experience. Here's our complete guide to planning your dream wedding.

            Venue Selection - Choose the perfect spot
            Decor Ideas - Beach-themed decorations
            Catering - Fresh seafood and local cuisine
            Photography - Capture the magic
            Guest Comfort - Shade and refreshments

            Contact our events team for a personalized consultation.""",
            content_ar="""الزواج على الشاطئ هو تجربة ساحرة. إليك دليلنا الكامل لتخطيط حفل زفاف أحلامك.

            اختيار المكان - اختر المكان المثالي
            أفكار الديكور - ديكورات على طراز الشاطئ
            الطعام - مأكولات بحرية طازجة ومحلية
            التصوير - التقط السحر
            راحة الضيوف - ظل ومرطبات

            تواصل مع فريق الفعاليات للحصول على استشارة مخصصة.""",
            excerpt="A complete guide to planning your dream wedding on the beach",
            excerpt_ar="دليل كامل لتخطيط حفل زفاف أحلامك على الشاطئ",
            author="Events Team",
            is_published=True,
            featured_image="https://images.unsplash.com/photo-1519741497674-611481863552?w=800",
            category="Events",
            tags="wedding,beach,romance,events",
            view_count=890,
            published_at=datetime.now() - timedelta(days=45)
        ),
        BlogPost(
            title="Luxury Dining Experience at Al-Bahr Restaurant",
            title_ar="تجربة طعام فاخرة في مطعم البحر",
            slug="luxury-dining-experience",
            content="""Our signature restaurant offers authentic Egyptian and international cuisine with a stunning sea view.

            Menu Highlights:
            - Fresh Red Sea seafood
            - Traditional Egyptian dishes
            - International favorites
            - Vegetarian options
            - Signature cocktails

            Open daily from 7 AM to 11 PM. Reservations recommended.""",
            content_ar="""يقدم مطعمنا المميز المأكولات المصرية الأصيلة والعالمية مع إطلالة بحرية خلابة.

            أبرز القائمة:
            - مأكولات بحرية طازجة من البحر الأحمر
            - أطباق مصرية تقليدية
            - أطباق عالمية
            - خيارات نباتية
            - كوكتيلات مميزة

            مفتوح يومياً من ٧ صباحاً حتى ١١ مساءً. يُفضل الحجز.""",
            excerpt="Explore our world-class cuisine and dining facilities",
            excerpt_ar="استكشف مطبخنا العالمي ومرافق الطعام",
            author="Chef Ahmed",
            is_published=True,
            featured_image="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
            category="Dining",
            tags="restaurant,dining,cuisine,food",
            view_count=2100,
            published_at=datetime.now() - timedelta(days=15)
        ),
    ]
    
    for post in posts:
        session.add(post)
    
    await session.commit()
    print(f"✅ Added {len(posts)} blog posts")

async def seed_all():
    """Main seeding function"""
    print("=" * 60)
    print("🌱 Al-Khayma Beach Resort - Database Seeding")
    print("=" * 60)
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
        
        # Final summary
        print()
        print("=" * 60)
        print("🎉 Database seeding completed successfully!")
        print("=" * 60)
        print()
        
        # Get final counts
        r = await session.scalar(select(func.count()).select_from(Room))
        p = await session.scalar(select(func.count()).select_from(Product))
        u = await session.scalar(select(func.count()).select_from(User))
        b = await session.scalar(select(func.count()).select_from(BlogPost))
        
        print("Database Summary:")
        print(f"  🏨 Rooms: {r}")
        print(f"  🏖️  Products: {p}")
        print(f"  👥 Users: {u}")
        print(f"  📝 Blog Posts: {b}")
        print()
        print("Test Accounts:")
        print("  Admin: admin@alkhayma.com / admin123")
        print("  Manager: manager@alkhayma.com / manager123")
        print("  Reception: reception@alkhayma.com / reception123")
        print("  Guest: test@example.com / test123")
        print()

if __name__ == "__main__":
    asyncio.run(seed_all())
