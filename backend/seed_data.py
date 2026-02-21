"""
Complete seed script for الخيمة Beach Resort
Creates all tables and seeds with sample data
"""
import asyncio
from datetime import datetime, timedelta, date
from decimal import Decimal
from app.core.database import AsyncSessionLocal, engine, Base
from app.models.product import Product, ProductType
from app.models.inventory import Inventory
from app.models.package import Package, PackageItem
from app.models.user import User, UserRole
from app.models.booking import Booking, BookingItem, BookingStatus
from app.models.payment import Payment, PaymentGateway, PaymentStatus
from app.models.review import Review, SentimentLabel
from app.models.loyalty import LoyaltyAccount, LoyaltyTransaction, LoyaltyTier, LoyaltyTransactionType
from app.models.audit import AuditLog
from app.models.blog import BlogPost
from sqlalchemy import select
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_or_create(session, model, **kwargs):
    """Get existing record or create new one"""
    defaults = kwargs.pop('defaults', {})
    result = await session.execute(select(model).filter_by(**kwargs))
    instance = result.scalar_one_or_none()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs, **defaults)
        session.add(instance)
        return instance, True

async def seed_database():
    """Seed database with all required data"""
    
    # Create all tables first
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as session:
        try:
            # 1. Create superadmin user
            admin_user, created = await get_or_create(
                session, User,
                email="admin@alkhaima.com",
                defaults={
                    "hashed_password": pwd_context.hash("AlKhayma2026!"),
                    "full_name": "الخيمة Admin",
                    "phone": "+201234567890",
                    "role": UserRole.SUPERADMIN,
                    "is_active": True
                }
            )
            if created:
                print("✅ Superadmin user created")
            
            # 2. Create products
            products_data = [
                # Rooms
                {
                    "name": "Deluxe Sea View Room",
                    "name_ar": "غرفة ديلوكس بإطلالة بحرية",
                    "slug": "deluxe-sea-view-room",
                    "type": ProductType.ROOM,
                    "base_price": Decimal("1500.00"),
                    "capacity": 2,
                    "description": "Spacious room with stunning sea view and premium amenities",
                    "description_ar": "غرفة واسعة بإطلالة بحرية خلابة ووسائل راحة فاخرة",
                    "amenities": {"wifi": True, "ac": True, "minibar": True, "balcony": True},
                    "tags": {"luxury": True, "sea_view": True}
                },
                {
                    "name": "Standard Room",
                    "name_ar": "غرفة عادية",
                    "slug": "standard-room",
                    "type": ProductType.ROOM,
                    "base_price": Decimal("1000.00"),
                    "capacity": 2,
                    "description": "Comfortable standard room with essential amenities",
                    "description_ar": "غرفة عادية مريحة مع وسائل الراحة الأساسية",
                    "amenities": {"wifi": True, "ac": True},
                    "tags": {"standard": True}
                },
                {
                    "name": "Family Suite",
                    "name_ar": "جناح عائلي",
                    "slug": "family-suite",
                    "type": ProductType.ROOM,
                    "base_price": Decimal("2500.00"),
                    "capacity": 4,
                    "description": "Spacious family suite with separate living area",
                    "description_ar": "جناح عائلي واسع مع منطقة معيشة منفصلة",
                    "amenities": {"wifi": True, "ac": True, "minibar": True, "living_room": True},
                    "tags": {"family": True, "suite": True}
                },
                {
                    "name": "Presidential Villa",
                    "name_ar": "فيلا رئاسية",
                    "slug": "presidential-villa",
                    "type": ProductType.ROOM,
                    "base_price": Decimal("5000.00"),
                    "capacity": 6,
                    "description": "Luxury villa with private pool and beach access",
                    "description_ar": "فيلا فاخرة مع مسبح خاص ووصول مباشر للشاطئ",
                    "amenities": {"wifi": True, "ac": True, "private_pool": True, "beach_access": True},
                    "tags": {"luxury": True, "villa": True, "private": True}
                },
                
                # Beach Services
                {
                    "name": "VIP Beach Cabana",
                    "name_ar": "كابانا شاطئ VIP",
                    "slug": "vip-beach-cabana",
                    "type": ProductType.BEACH,
                    "base_price": Decimal("300.00"),
                    "capacity": 4,
                    "description": "Private beach cabana with dedicated service",
                    "description_ar": "كابانا شاطئ خاصة مع خدمة مخصصة",
                    "duration_minutes": 480,  # 8 hours
                    "amenities": {"shade": True, "service": True, "drinks": True},
                    "tags": {"vip": True, "beach": True}
                },
                {
                    "name": "Beach Umbrella & Chairs",
                    "name_ar": "مظلة وكراسي شاطئ",
                    "slug": "beach-umbrella-chairs",
                    "type": ProductType.BEACH,
                    "base_price": Decimal("100.00"),
                    "capacity": 2,
                    "description": "Standard beach umbrella with two chairs",
                    "description_ar": "مظلة شاطئ عادية مع كرسيين",
                    "duration_minutes": 480,  # 8 hours
                    "amenities": {"shade": True},
                    "tags": {"standard": True, "beach": True}
                },
                
                # Water Activities
                {
                    "name": "Snorkeling Trip",
                    "name_ar": "رحلة غطس",
                    "slug": "snorkeling-trip",
                    "type": ProductType.WATER_ACTIVITY,
                    "base_price": Decimal("250.00"),
                    "capacity": 12,
                    "description": "Half-day snorkeling adventure to coral reefs",
                    "description_ar": "مغامرة غطس لنصف يوم إلى الشعاب المرجانية",
                    "duration_minutes": 240,  # 4 hours
                    "min_age": 8,
                    "amenities": {"equipment": True, "guide": True, "transport": True},
                    "tags": {"adventure": True, "underwater": True}
                },
                {
                    "name": "Jet Ski Rental",
                    "name_ar": "تأجير جت سكي",
                    "slug": "jet-ski-rental",
                    "type": ProductType.WATER_ACTIVITY,
                    "base_price": Decimal("400.00"),
                    "capacity": 2,
                    "description": "Thrilling jet ski experience",
                    "description_ar": "تجربة جت سكي مثيرة",
                    "duration_minutes": 60,
                    "min_age": 16,
                    "max_weight_kg": 150,
                    "amenities": {"equipment": True, "safety_gear": True},
                    "tags": {"adventure": True, "speed": True}
                },
                {
                    "name": "Parasailing Adventure",
                    "name_ar": "مغامرة الطيران الشراعي",
                    "slug": "parasailing-adventure",
                    "type": ProductType.WATER_ACTIVITY,
                    "base_price": Decimal("350.00"),
                    "capacity": 1,
                    "description": "Soar above the Red Sea with parasailing",
                    "description_ar": "حلق فوق البحر الأحمر مع الطيران الشراعي",
                    "duration_minutes": 30,
                    "min_age": 12,
                    "max_weight_kg": 120,
                    "amenities": {"equipment": True, "safety_gear": True, "photos": True},
                    "tags": {"adventure": True, "aerial": True}
                },
                
                # Events
                {
                    "name": "Sunset Dinner Cruise",
                    "name_ar": "رحلة عشاء الغروب",
                    "slug": "sunset-dinner-cruise",
                    "type": ProductType.EVENT,
                    "base_price": Decimal("800.00"),
                    "capacity": 50,
                    "description": "Romantic dinner cruise with live entertainment",
                    "description_ar": "رحلة عشاء رومانسية مع ترفيه مباشر",
                    "duration_minutes": 180,  # 3 hours
                    "amenities": {"dinner": True, "entertainment": True, "drinks": True},
                    "tags": {"romantic": True, "dinner": True, "cruise": True}
                },
                {
                    "name": "Beach BBQ Night",
                    "name_ar": "ليلة شواء الشاطئ",
                    "slug": "beach-bbq-night",
                    "type": ProductType.EVENT,
                    "base_price": Decimal("450.00"),
                    "capacity": 100,
                    "description": "Traditional beach BBQ with live music",
                    "description_ar": "شواء شاطئ تقليدي مع موسيقى حية",
                    "duration_minutes": 240,  # 4 hours
                    "amenities": {"bbq": True, "music": True, "drinks": True},
                    "tags": {"traditional": True, "bbq": True, "music": True}
                },
                {
                    "name": "Desert Safari",
                    "name_ar": "رحلة سفاري الصحراء",
                    "slug": "desert-safari",
                    "type": ProductType.EVENT,
                    "base_price": Decimal("600.00"),
                    "capacity": 20,
                    "description": "Adventure desert safari with camel riding",
                    "description_ar": "رحلة سفاري صحراء مغامرة مع ركوب الجمال",
                    "duration_minutes": 360,  # 6 hours
                    "amenities": {"transport": True, "guide": True, "camel_ride": True, "dinner": True},
                    "tags": {"adventure": True, "desert": True, "cultural": True}
                },
                {
                    "name": "Wedding Package",
                    "name_ar": "باقة الزفاف",
                    "slug": "wedding-package",
                    "type": ProductType.EVENT,
                    "base_price": Decimal("15000.00"),
                    "capacity": 200,
                    "description": "Complete wedding package with decoration and catering",
                    "description_ar": "باقة زفاف كاملة مع الديكور والطعام",
                    "duration_minutes": 480,  # 8 hours
                    "amenities": {"decoration": True, "catering": True, "photography": True, "music": True},
                    "tags": {"wedding": True, "luxury": True, "complete": True}
                }
            ]
            
            created_products = []
            for product_data in products_data:
                product, created = await get_or_create(
                    session, Product,
                    slug=product_data["slug"],
                    defaults=product_data
                )
                if created:
                    created_products.append(product)
                    print(f"✅ Product created: {product.name}")
            
            await session.commit()
            
            # 3. Create packages
            packages_data = [
                {
                    "name": "Honeymoon Package",
                    "name_ar": "باقة شهر العسل",
                    "slug": "honeymoon-package",
                    "description": "Romantic getaway for couples",
                    "discount_pct": Decimal("15.00"),
                    "tags": {"romantic": True, "couple": True},
                    "items": [
                        {"product_slug": "deluxe-sea-view-room", "quantity": 1, "is_required": True},
                        {"product_slug": "sunset-dinner-cruise", "quantity": 1, "is_required": True},
                        {"product_slug": "vip-beach-cabana", "quantity": 1, "is_required": False}
                    ]
                },
                {
                    "name": "Adventure Package",
                    "name_ar": "باقة المغامرة",
                    "slug": "adventure-package",
                    "description": "Action-packed activities for thrill seekers",
                    "discount_pct": Decimal("20.00"),
                    "tags": {"adventure": True, "activities": True},
                    "items": [
                        {"product_slug": "standard-room", "quantity": 1, "is_required": True},
                        {"product_slug": "snorkeling-trip", "quantity": 1, "is_required": True},
                        {"product_slug": "jet-ski-rental", "quantity": 1, "is_required": True},
                        {"product_slug": "parasailing-adventure", "quantity": 1, "is_required": False}
                    ]
                },
                {
                    "name": "Family Fun Package",
                    "name_ar": "باقة المرح العائلي",
                    "slug": "family-fun-package",
                    "description": "Perfect package for families with children",
                    "discount_pct": Decimal("25.00"),
                    "tags": {"family": True, "children": True},
                    "items": [
                        {"product_slug": "family-suite", "quantity": 1, "is_required": True},
                        {"product_slug": "beach-umbrella-chairs", "quantity": 2, "is_required": True},
                        {"product_slug": "snorkeling-trip", "quantity": 1, "is_required": False},
                        {"product_slug": "beach-bbq-night", "quantity": 1, "is_required": False}
                    ]
                }
            ]
            
            for package_data in packages_data:
                items_data = package_data.pop("items")
                package, created = await get_or_create(
                    session, Package,
                    slug=package_data["slug"],
                    defaults=package_data
                )
                
                if created:
                    print(f"✅ Package created: {package.name}")
                    
                    # Add package items
                    for item_data in items_data:
                        product_slug = item_data.pop("product_slug")
                        product_result = await session.execute(
                            select(Product).filter_by(slug=product_slug)
                        )
                        product = product_result.scalar_one()
                        
                        package_item = PackageItem(
                            package_id=package.id,
                            product_id=product.id,
                            **item_data
                        )
                        session.add(package_item)
            
            await session.commit()
            
            # 4. Generate inventory for next 365 days
            today = date.today()
            for i in range(365):
                current_date = today + timedelta(days=i)
                
                for product in created_products:
                    if product.type == ProductType.ROOM:
                        total_capacity = product.capacity
                    elif product.type == ProductType.BEACH:
                        total_capacity = 20 if "vip" in product.slug else 80
                    else:
                        total_capacity = product.capacity
                    
                    inventory, created = await get_or_create(
                        session, Inventory,
                        product_id=product.id,
                        date=current_date,
                        defaults={
                            "total_capacity": total_capacity,
                            "available": total_capacity,
                            "booked": 0
                        }
                    )
            
            await session.commit()
            print("✅ Inventory generated for 365 days")
            
            # 5. Create loyalty account for admin
            loyalty_account, created = await get_or_create(
                session, LoyaltyAccount,
                user_id=admin_user.id,
                defaults={
                    "points_balance": 1000,
                    "tier": LoyaltyTier.VIP,
                    "lifetime_points": 1000
                }
            )
            if created:
                print("✅ Admin loyalty account created")
            
            await session.commit()
            print("🎉 Database seeded successfully!")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error seeding database: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(seed_database())
