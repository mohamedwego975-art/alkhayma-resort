import asyncio
from datetime import date, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, Base, engine
from app.models import Product, ProductType, User, UserRole, Package, PackageItem, Inventory, Recommendation


async def get_or_create_user(session: AsyncSession, email: str, **kwargs):
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        user = User(email=email, **kwargs)
        session.add(user)
        await session.flush()
    return user


async def get_or_create_product(session: AsyncSession, slug: str, **kwargs):
    result = await session.execute(select(Product).where(Product.slug == slug))
    product = result.scalar_one_or_none()
    if not product:
        product = Product(slug=slug, **kwargs)
        session.add(product)
        await session.flush()
    return product


async def get_or_create_package(session: AsyncSession, slug: str, **kwargs):
    result = await session.execute(select(Package).where(Package.slug == slug))
    package = result.scalar_one_or_none()
    if not package:
        package = Package(slug=slug, **kwargs)
        session.add(package)
        await session.flush()
    return package


async def seed_users(session: AsyncSession):
    print("Seeding users...")
    await get_or_create_user(
        session,
        email="admin@alkhaima.com",
        password_hash="$2b$12$hashed_password_placeholder",
        full_name="Super Admin",
        role=UserRole.superadmin,
        is_active=True
    )


async def seed_products(session: AsyncSession):
    print("Seeding products...")
    
    products_data = [
        # Rooms
        {"slug": "standard-room", "name": "Standard Room", "name_ar": "غرفة قياسية", "type": ProductType.room, "base_price": 100, "capacity": 2},
        {"slug": "deluxe-sea-view", "name": "Deluxe Sea View", "name_ar": "ديلوكس إطلالة بحرية", "type": ProductType.room, "base_price": 180, "capacity": 3},
        {"slug": "honeymoon-suite", "name": "Honeymoon Suite", "name_ar": "جناح شهر العسل", "type": ProductType.room, "base_price": 350, "capacity": 2},
        {"slug": "family-suite", "name": "Family Suite", "name_ar": "جناح عائلي", "type": ProductType.room, "base_price": 280, "capacity": 6},
        
        # Beach
        {"slug": "normal-beach", "name": "Normal Beach", "name_ar": "شاطئ عادي", "type": ProductType.beach, "base_price": 20, "capacity": 80},
        {"slug": "vip-beach", "name": "VIP Beach", "name_ar": "شاطئ VIP", "type": ProductType.beach, "base_price": 65, "capacity": 20},
        
        # Restaurant & Cafe
        {"slug": "resort-restaurant", "name": "Resort Restaurant", "name_ar": "مطعم المنتجع", "type": ProductType.restaurant, "base_price": 50, "capacity": 60},
        {"slug": "resort-cafe", "name": "Resort Cafe", "name_ar": "مقهى المنتجع", "type": ProductType.cafe, "base_price": 15, "capacity": 30},
        
        # Water Activities
        {"slug": "banana-boat", "name": "Banana Boat", "name_ar": "قارب الموز", "type": ProductType.water_activity, "base_price": 35, "capacity": 8, "min_age": 5},
        {"slug": "tube-ride", "name": "Tube Ride", "name_ar": "ركوب الأنبوب", "type": ProductType.water_activity, "base_price": 30, "capacity": 4, "min_age": 6},
        {"slug": "parasailing", "name": "Parasailing", "name_ar": "المظلة الشراعية", "type": ProductType.water_activity, "base_price": 75, "capacity": 2, "min_age": 12},
        
        # Events
        {"slug": "morning-yoga", "name": "Morning Yoga", "name_ar": "يوغا الصباح", "type": ProductType.event, "base_price": 15, "capacity": 15},
        {"slug": "zumba", "name": "Zumba", "name_ar": "زومبا", "type": ProductType.event, "base_price": 15, "capacity": 20},
        {"slug": "birthday-party", "name": "Birthday Party", "name_ar": "حفلة عيد ميلاد", "type": ProductType.event, "base_price": 250, "capacity": 30},
        {"slug": "sunset-dinner", "name": "Sunset Dinner", "name_ar": "عشاء الغروب", "type": ProductType.event, "base_price": 80, "capacity": 12},
    ]
    
    for data in products_data:
        await get_or_create_product(session, **data)


async def seed_packages(session: AsyncSession):
    print("Seeding packages...")
    
    packages_data = [
        {
            "slug": "romantic-escape",
            "name": "Romantic Escape",
            "name_ar": "هروب رومانسي",
            "discount_percent": 18,
            "items": ["honeymoon-suite", "vip-beach", "sunset-dinner"]
        },
        {
            "slug": "family-adventure",
            "name": "Family Adventure",
            "name_ar": "مغامرة عائلية",
            "discount_percent": 12,
            "items": ["family-suite", "normal-beach", "banana-boat"]
        },
        {
            "slug": "adrenaline-rush",
            "name": "Adrenaline Rush",
            "name_ar": "اندفاع الأدرينالين",
            "discount_percent": 15,
            "items": ["parasailing", "tube-ride", "banana-boat"]
        },
        {
            "slug": "wellness-retreat",
            "name": "Wellness Retreat",
            "name_ar": "خلوة العافية",
            "discount_percent": 10,
            "items": ["deluxe-sea-view", "morning-yoga", "resort-cafe"]
        },
    ]
    
    for pkg_data in packages_data:
        items_slugs = pkg_data.pop("items")
        package = await get_or_create_package(session, **pkg_data)
        
        # Check if items already exist
        result = await session.execute(
            select(PackageItem).where(PackageItem.package_id == package.id)
        )
        existing_items = result.scalars().all()
        
        if not existing_items:
            for item_slug in items_slugs:
                result = await session.execute(select(Product).where(Product.slug == item_slug))
                product = result.scalar_one()
                
                package_item = PackageItem(package_id=package.id, product_id=product.id, quantity=1)
                session.add(package_item)


async def seed_recommendations(session: AsyncSession):
    print("Seeding recommendations...")
    
    recommendations_data = [
        {"title": "Best for Couples", "title_ar": "الأفضل للأزواج", "product_slug": "honeymoon-suite", "sort_order": 1},
        {"title": "Family Favorite", "title_ar": "المفضل للعائلات", "product_slug": "family-suite", "sort_order": 2},
        {"title": "Thrilling Experience", "title_ar": "تجربة مثيرة", "product_slug": "parasailing", "sort_order": 3},
    ]
    
    for rec_data in recommendations_data:
        product_slug = rec_data.pop("product_slug")
        result = await session.execute(select(Product).where(Product.slug == product_slug))
        product = result.scalar_one()
        
        result = await session.execute(
            select(Recommendation).where(Recommendation.product_id == product.id)
        )
        existing = result.scalar_one_or_none()
        
        if not existing:
            recommendation = Recommendation(product_id=product.id, **rec_data)
            session.add(recommendation)


async def seed_inventory(session: AsyncSession):
    print("Seeding inventory...")
    
    result = await session.execute(select(Product))
    products = result.scalars().all()
    
    start_date = date.today()
    
    for product in products:
        for day_offset in range(365):
            inventory_date = start_date + timedelta(days=day_offset)
            
            result = await session.execute(
                select(Inventory).where(
                    Inventory.product_id == product.id,
                    Inventory.date == inventory_date
                )
            )
            existing = result.scalar_one_or_none()
            
            if not existing:
                if product.type == ProductType.beach:
                    total_capacity = 20 if "vip" in product.slug else 80
                else:
                    total_capacity = product.capacity
                
                inventory = Inventory(
                    product_id=product.id,
                    date=inventory_date,
                    total_capacity=total_capacity,
                    available=total_capacity,
                    booked=0
                )
                session.add(inventory)


async def create_tables():
    print("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await create_tables()
    
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await seed_users(session)
            await seed_products(session)
            await seed_packages(session)
            await seed_recommendations(session)
            await seed_inventory(session)
        
        await session.commit()
    
    print("\n✅ Seeding completed successfully!")
    print("\nRun these SQL queries to validate:")
    print("  SELECT type, COUNT(*) FROM products GROUP BY type;")
    print("  SELECT COUNT(*) FROM inventory;")
    print("  SELECT COUNT(*) FROM packages;")


if __name__ == "__main__":
    asyncio.run(main())
