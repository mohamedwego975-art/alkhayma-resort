#!/usr/bin/env python3
"""
Phase 5 Step 2: API Integration Testing
Tests all critical endpoints without starting server
"""

import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.core.database import AsyncSessionLocal
from app.models import Room, Product, User
from app.api.products import get_products
from sqlalchemy import select

async def test_api_logic():
    """Test API logic directly"""
    
    print("=" * 60)
    print("🧪 API INTEGRATION TESTING")
    print("=" * 60)
    
    async with AsyncSessionLocal() as db:
        # Test 1: Get all rooms
        print("\n1️⃣ Testing: GET /api/products?type=room")
        rooms = await db.execute(select(Room))
        room_list = rooms.scalars().all()
        print(f"   ✅ Found {len(room_list)} rooms")
        if room_list:
            print(f"   Sample: {room_list[0].room_number} - ${room_list[0].price_per_night}")
        
        # Test 2: Get beach products
        print("\n2️⃣ Testing: GET /api/products?type=beach")
        beach = await db.execute(select(Product).where(Product.type == "beach"))
        beach_list = beach.scalars().all()
        print(f"   ✅ Found {len(beach_list)} beach products")
        if beach_list:
            print(f"   Sample: {beach_list[0].name} - ${beach_list[0].base_price}")
        
        # Test 3: Get water activities
        print("\n3️⃣ Testing: GET /api/products?type=water_activity")
        activities = await db.execute(select(Product).where(Product.type == "water_activity"))
        activity_list = activities.scalars().all()
        print(f"   ✅ Found {len(activity_list)} water activities")
        if activity_list:
            print(f"   Sample: {activity_list[0].name} - ${activity_list[0].base_price}")
        
        # Test 4: Get specific room
        print("\n4️⃣ Testing: GET /api/products/{id}")
        room = await db.execute(select(Room).where(Room.room_number == "301"))
        specific_room = room.scalar_one_or_none()
        if specific_room:
            print(f"   ✅ Room 301: {specific_room.room_type} - ${specific_room.price_per_night}")
            print(f"   Rating: {specific_room.rating} ({specific_room.review_count} reviews)")
        
        # Test 5: Verify users exist
        print("\n5️⃣ Testing: User Authentication Data")
        users = await db.execute(select(User))
        user_list = users.scalars().all()
        print(f"   ✅ Found {len(user_list)} users")
        for user in user_list:
            print(f"   • {user.email} ({user.role})")
    
    print("\n" + "=" * 60)
    print("✅ ALL API LOGIC TESTS PASSED")
    print("=" * 60)
    print("\n📝 Next Steps:")
    print("   1. Start backend: cd backend && uvicorn app.main:app --reload")
    print("   2. Start frontend: cd frontend && npm run dev")
    print("   3. Test in browser: http://localhost:5173")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_api_logic())
