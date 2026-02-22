#!/usr/bin/env python3
"""
Booking Engine Concurrency Test
Simulates 10 concurrent requests for same product with capacity=2
Only 2 should succeed, others should get 409 (not 500)
"""
import asyncio
import uuid
from datetime import date, timedelta
from httpx import AsyncClient, ASGITransport
from app.main import app


async def make_booking(client: AsyncClient, token: str, product_id: int, request_num: int):
    """Make a single booking request"""
    check_in = date.today() + timedelta(days=10)
    check_out = check_in + timedelta(days=2)
    
    response = await client.post(
        "/api/bookings",
        json={
            "product_id": product_id,
            "check_in": str(check_in),
            "check_out": str(check_out),
            "quantity": 1,
            "addons": [],
            "idempotency_key": f"test_{uuid.uuid4().hex}_{request_num}",
            "notes": f"Concurrent test request #{request_num}"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    return {
        "request_num": request_num,
        "status_code": response.status_code,
        "response": response.json() if response.status_code != 500 else response.text
    }


async def main():
    print("=" * 70)
    print("BOOKING ENGINE CONCURRENCY TEST")
    print("=" * 70)
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", timeout=30.0) as client:
        
        # Step 1: Register and login
        print("\n1️⃣  Setting up test user...")
        unique_email = f"concurrency_{uuid.uuid4().hex[:8]}@test.com"
        
        register_response = await client.post(
            "/api/auth/register",
            json={
                "email": unique_email,
                "password": "TestPass123!",
                "full_name": "Concurrency Test User"
            }
        )
        
        if register_response.status_code != 201:
            print(f"   ❌ Registration failed: {register_response.status_code}")
            return False
        
        token = register_response.json()["access_token"]
        print(f"   ✅ User registered and authenticated")
        
        # Step 2: Find a product with capacity=2 (Standard Room)
        product_id = 1  # Standard Room has capacity=2
        print(f"\n2️⃣  Using Product ID: {product_id} (Standard Room, capacity=2)")
        
        # Step 3: Launch 10 concurrent booking requests
        print(f"\n3️⃣  Launching 10 concurrent booking requests...")
        print(f"   Expected: 2 succeed (201), 8 fail with 409 (not 500)")
        
        tasks = [
            make_booking(client, token, product_id, i)
            for i in range(1, 11)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Step 4: Analyze results
        print(f"\n4️⃣  Results:")
        
        success_count = 0
        conflict_count = 0
        error_500_count = 0
        other_errors = 0
        
        for result in results:
            if isinstance(result, Exception):
                print(f"   Request failed with exception: {result}")
                other_errors += 1
                continue
            
            req_num = result["request_num"]
            status = result["status_code"]
            
            if status == 201:
                success_count += 1
                print(f"   ✅ Request #{req_num}: SUCCESS (201)")
            elif status == 409:
                conflict_count += 1
                detail = result["response"].get("detail", "")
                print(f"   ⚠️  Request #{req_num}: CONFLICT (409) - {detail[:50]}")
            elif status == 500:
                error_500_count += 1
                print(f"   ❌ Request #{req_num}: SERVER ERROR (500)")
            else:
                other_errors += 1
                print(f"   ⚠️  Request #{req_num}: OTHER ({status})")
        
        print(f"\n" + "=" * 70)
        print(f"CONCURRENCY TEST RESULTS")
        print(f"=" * 70)
        print(f"   Successful bookings (201): {success_count}")
        print(f"   Conflicts (409): {conflict_count}")
        print(f"   Server errors (500): {error_500_count}")
        print(f"   Other errors: {other_errors}")
        print(f"=" * 70)
        
        # Validation
        if success_count == 2 and error_500_count == 0:
            print(f"\n✅ TEST PASSED!")
            print(f"   - Exactly 2 bookings succeeded")
            print(f"   - No 500 errors (proper locking)")
            print(f"   - {conflict_count} requests properly rejected with 409")
            return True
        else:
            print(f"\n❌ TEST FAILED!")
            if success_count != 2:
                print(f"   - Expected 2 successes, got {success_count}")
            if error_500_count > 0:
                print(f"   - Got {error_500_count} server errors (should be 0)")
            return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
