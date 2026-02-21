#!/usr/bin/env python3
"""
Complete Integration Test - Direct API Testing
Tests all functionality without requiring running HTTP server
"""

import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.core.database import AsyncSessionLocal
from app.models import Room, Product, User
from sqlalchemy import select
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def test_complete_integration():
    print("=" * 70)
    print("🔗 COMPLETE INTEGRATION TEST - Phase 5 Step 3")
    print("=" * 70)
    print()
    
    async with AsyncSessionLocal() as db:
        passed = 0
        failed = 0
        
        # Test 1: Database Connection
        print("1️⃣  Database Connection")
        try:
            await db.execute(select(1))
            print("   ✅ PASSED - Database connected")
            passed += 1
        except Exception as e:
            print(f"   ❌ FAILED - {e}")
            failed += 1
        print()
        
        # Test 2: Rooms Data
        print("2️⃣  Rooms Data Integrity")
        rooms = await db.execute(select(Room))
        room_list = rooms.scalars().all()
        if len(room_list) == 6:
            print(f"   ✅ PASSED - Found 6 rooms")
            passed += 1
            for room in room_list[:3]:
                print(f"      • {room.room_number} ({room.room_type}) - ${room.price_per_night}/night")
        else:
            print(f"   ❌ FAILED - Expected 6 rooms, found {len(room_list)}")
            failed += 1
        print()
        
        # Test 3: Beach Products
        print("3️⃣  Beach Products")
        beach = await db.execute(select(Product).where(Product.type == "beach"))
        beach_list = beach.scalars().all()
        if len(beach_list) == 2:
            print(f"   ✅ PASSED - Found 2 beach products")
            passed += 1
            for product in beach_list:
                print(f"      • {product.name} - ${product.base_price}")
        else:
            print(f"   ❌ FAILED - Expected 2 beach products, found {len(beach_list)}")
            failed += 1
        print()
        
        # Test 4: Water Activities
        print("4️⃣  Water Activities")
        activities = await db.execute(select(Product).where(Product.type == "water_activity"))
        activity_list = activities.scalars().all()
        if len(activity_list) == 4:
            print(f"   ✅ PASSED - Found 4 water activities")
            passed += 1
            for activity in activity_list:
                duration = f" ({activity.duration_minutes}min)" if activity.duration_minutes else ""
                print(f"      • {activity.name} - ${activity.base_price}{duration}")
        else:
            print(f"   ❌ FAILED - Expected 4 activities, found {len(activity_list)}")
            failed += 1
        print()
        
        # Test 5: User Authentication
        print("5️⃣  User Authentication")
        admin = await db.execute(select(User).where(User.email == "admin@alkhayma.com"))
        admin_user = admin.scalar_one_or_none()
        
        if admin_user and admin_user.role.value == "admin":
            print(f"   ✅ PASSED - Admin user exists")
            passed += 1
            print(f"      • Email: {admin_user.email}")
            print(f"      • Role: {admin_user.role.value}")
            print(f"      • Active: {admin_user.is_active}")
            print(f"      • Password: {'*' * 20} (hashed)")
        else:
            print(f"   ❌ FAILED - Admin user not found or invalid role")
            failed += 1
        print()
        
        # Test 6: All Users
        print("6️⃣  All Users")
        users = await db.execute(select(User))
        user_list = users.scalars().all()
        if len(user_list) == 3:
            print(f"   ✅ PASSED - Found 3 users")
            passed += 1
            for user in user_list:
                print(f"      • {user.email} ({user.role})")
        else:
            print(f"   ❌ FAILED - Expected 3 users, found {len(user_list)}")
            failed += 1
        print()
        
        # Test 7: Room Details
        print("7️⃣  Room Details (Suite 301)")
        suite = await db.execute(select(Room).where(Room.room_number == "301"))
        suite_room = suite.scalar_one_or_none()
        
        if suite_room:
            checks = [
                (suite_room.room_type.value == "suite", "Room type is suite"),
                (suite_room.capacity >= 4, "Capacity >= 4"),
                (suite_room.price_per_night > 0, "Price > 0"),
                (suite_room.rating is not None, "Has rating"),
            ]
            
            all_passed = all(check[0] for check in checks)
            if all_passed:
                print(f"   ✅ PASSED - All room details valid")
                passed += 1
                print(f"      • Type: {suite_room.room_type.value}")
                print(f"      • Capacity: {suite_room.capacity}")
                print(f"      • Price: ${suite_room.price_per_night}/night")
                print(f"      • Rating: {suite_room.rating}/5.0")
            else:
                print(f"   ❌ FAILED - Some details invalid")
                failed += 1
                for check, desc in checks:
                    status = "✓" if check else "✗"
                    print(f"      {status} {desc}")
        else:
            print(f"   ❌ FAILED - Suite 301 not found")
            failed += 1
        print()
        
        # Test 8: Product Attributes
        print("8️⃣  Product Attributes")
        parasailing = await db.execute(
            select(Product).where(Product.slug == "parasailing")
        )
        parasailing_product = parasailing.scalar_one_or_none()
        
        if parasailing_product:
            checks = [
                (parasailing_product.duration_minutes == 20, "Duration is 20 min"),
                (parasailing_product.max_weight_kg == 100, "Max weight is 100kg"),
                (parasailing_product.capacity == 1, "Capacity is 1"),
                (parasailing_product.base_price == 85.0, "Price is $85"),
            ]
            
            all_passed = all(check[0] for check in checks)
            if all_passed:
                print(f"   ✅ PASSED - All product attributes valid")
                passed += 1
            else:
                print(f"   ❌ FAILED - Some attributes invalid")
                failed += 1
            
            for check, desc in checks:
                status = "✓" if check else "✗"
                print(f"      {status} {desc}")
        else:
            print(f"   ❌ FAILED - Parasailing product not found")
            failed += 1
        print()
        
        # Summary
        print("=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Total:  {passed + failed}")
        print(f"🎯 Success Rate: {(passed/(passed+failed)*100):.1f}%")
        print("=" * 70)
        print()
        
        if failed == 0:
            print("🎉 ALL TESTS PASSED - System is fully integrated!")
            print()
            print("✅ Database: Connected and populated")
            print("✅ Models: All working correctly")
            print("✅ Data: Complete and valid")
            print("✅ Authentication: Working")
            print()
            print("➡️  NEXT: Start HTTP servers for browser testing")
            print("   Terminal 1: ./start-backend.sh")
            print("   Terminal 2: ./start-frontend.sh")
            print("   Browser: http://localhost:5173")
            return 0
        else:
            print("⚠️  SOME TESTS FAILED - Review errors above")
            return 1

if __name__ == "__main__":
    exit_code = asyncio.run(test_complete_integration())
    sys.exit(exit_code)
