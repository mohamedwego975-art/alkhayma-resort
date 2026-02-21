import asyncio
from app.core.database import AsyncSessionLocal
from app.repositories import RoomRepository, ProductRepository
from app.models.room import RoomType, RoomStatus
from app.models.product import ProductType


async def seed_data():
    async with AsyncSessionLocal() as db:
        # Seed Rooms
        room_repo = RoomRepository(db)
        rooms_data = [
            {
                "room_number": "101",
                "room_type": RoomType.STANDARD,
                "status": RoomStatus.AVAILABLE,
                "price_per_night": 150.0,
                "capacity": 2,
                "description_en": "Comfortable standard room with sea view",
                "description_ar": "غرفة قياسية مريحة مع إطلالة على البحر",
                "amenities": '{"wifi": true, "tv": true, "ac": true}',
                "is_active": True,
                "rating": 4.3,
                "review_count": 42,
            },
            {
                "room_number": "201",
                "room_type": RoomType.DELUXE,
                "status": RoomStatus.AVAILABLE,
                "price_per_night": 250.0,
                "capacity": 3,
                "description_en": "Spacious deluxe room with balcony",
                "description_ar": "غرفة فسيحة فاخرة مع شرفة خاصة وإطلالة محيطية",
                "amenities": '{"wifi": true, "tv": true, "ac": true, "minibar": true}',
                "is_active": True,
                "rating": 4.7,
                "review_count": 58,
            },
            {
                "room_number": "301",
                "room_type": RoomType.SUITE,
                "status": RoomStatus.AVAILABLE,
                "price_per_night": 400.0,
                "capacity": 4,
                "description_en": "Luxury suite with ocean view",
                "description_ar": "جناح فاخر مع إطلالة استثنائية على المحيط وتسهيلات راقية",
                "amenities": '{"wifi": true, "tv": true, "ac": true, "minibar": true, "jacuzzi": true}',
                "is_active": True,
                "rating": 4.9,
                "review_count": 67,
            },
        ]

        for room_data in rooms_data:
            try:
                await room_repo.create(room_data)
                print(f"✅ Created room {room_data['room_number']}")
            except Exception as e:
                print(f"⚠️  Room {room_data['room_number']} might already exist")

        # Seed Products
        product_repo = ProductRepository(db)
        products_data = [
            {
                "name": "Beach Umbrella Rental",
                "name_ar": "تأجير مظلة شاطئ",
                "description": "Daily beach umbrella rental",
                "type": ProductType.BEACH,
                "price": 20.0,
                "stock": 50,
                "is_active": True,
                "slug": "beach-umbrella",
            },
            {
                "name": "Snorkeling Set",
                "name_ar": "طقم غطس",
                "description": "Complete snorkeling equipment",
                "type": ProductType.WATER_ACTIVITY,
                "price": 35.0,
                "stock": 30,
                "is_active": True,
                "slug": "snorkeling-set",
            },
            {
                "name": "Spa Massage (60min)",
                "name_ar": "مساج سبا (60 دقيقة)",
                "description": "Relaxing full body massage",
                "type": ProductType.EVENT,
                "price": 100.0,
                "stock": 10,
                "is_active": True,
                "slug": "spa-massage-60",
            },
        ]

        for product_data in products_data:
            try:
                await product_repo.create(product_data)
                print(f"✅ Created product {product_data['name']}")
            except Exception as e:
                print(f"⚠️  Product {product_data['name']} might already exist")

        print("\n🎉 Seed data completed!")


if __name__ == "__main__":
    asyncio.run(seed_data())
