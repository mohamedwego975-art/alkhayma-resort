"""
Complete Integration Test Suite for الخيمة Beach Resort
Tests full booking flow, concurrency, pricing, admin analytics, RBAC, and auth
"""
import asyncio
import pytest
import httpx
from datetime import datetime, timedelta
from typing import Dict, Any
import uuid


@pytest.fixture
async def client():
    """Async HTTP client for testing"""
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        yield client


@pytest.fixture
async def guest_user(client):
    """Create and return guest user credentials"""
    user_data = {
        "email": f"guest_{uuid.uuid4().hex[:8]}@test.com",
        "password": "TestPass123!",
        "full_name": "Test Guest",
        "phone": "+201234567890"
    }
    
    response = await client.post("/api/auth/register", json=user_data)
    assert response.status_code == 201
    
    # Login to get token
    login_response = await client.post("/api/auth/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    return {
        "email": user_data["email"],
        "password": user_data["password"],
        "token": token,
        "headers": {"Authorization": f"Bearer {token}"}
    }


@pytest.fixture
async def admin_user(client):
    """Create and return admin user credentials"""
    user_data = {
        "email": f"admin_{uuid.uuid4().hex[:8]}@test.com",
        "password": "AdminPass123!",
        "full_name": "Test Admin",
        "phone": "+201234567891",
        "role": "admin"
    }
    
    response = await client.post("/api/auth/register", json=user_data)
    assert response.status_code == 201
    
    # Login to get token
    login_response = await client.post("/api/auth/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    return {
        "email": user_data["email"],
        "password": user_data["password"],
        "token": token,
        "headers": {"Authorization": f"Bearer {token}"}
    }


@pytest.mark.asyncio
async def test_full_booking_flow(client, guest_user):
    """Test complete booking flow from product selection to loyalty points"""
    
    # 1. Register guest user (done in fixture)
    headers = guest_user["headers"]
    
    # 2. GET /api/products?type=room → pick first room
    products_response = await client.get("/api/products?type=room")
    assert products_response.status_code == 200
    rooms = products_response.json()
    assert len(rooms) > 0
    room = rooms[0]
    room_id = room["id"]
    
    # 3. GET /api/products/{id}/price?check_in=+7days&check_out=+10days
    check_in = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    check_out = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
    
    price_response = await client.get(
        f"/api/products/{room_id}/price?check_in={check_in}&check_out={check_out}"
    )
    assert price_response.status_code == 200
    price_data = price_response.json()
    assert "final_price" in price_data
    
    # 4. GET /api/availability → confirm available
    availability_response = await client.get(
        f"/api/availability?product_id={room_id}&check_in={check_in}&check_out={check_out}"
    )
    assert availability_response.status_code == 200
    availability = availability_response.json()
    assert availability["available"] == True
    
    # 5. POST /api/bookings → confirm 201 + idempotency_key
    idempotency_key = str(uuid.uuid4())
    booking_data = {
        "product_id": room_id,
        "check_in": check_in,
        "check_out": check_out,
        "guests": 2,
        "special_requests": "Sea view please"
    }
    
    booking_response = await client.post(
        "/api/bookings",
        json=booking_data,
        headers={**headers, "Idempotency-Key": idempotency_key}
    )
    assert booking_response.status_code == 201
    booking = booking_response.json()
    booking_id = booking["id"]
    assert booking["status"] == "pending"
    
    # 6. POST same request with same idempotency_key → confirm 409
    duplicate_response = await client.post(
        "/api/bookings",
        json=booking_data,
        headers={**headers, "Idempotency-Key": idempotency_key}
    )
    assert duplicate_response.status_code == 409
    
    # 7. Simulate payment webhook → confirm booking.status=confirmed
    webhook_data = {
        "booking_id": booking_id,
        "payment_status": "completed",
        "transaction_id": f"txn_{uuid.uuid4().hex[:8]}"
    }
    
    webhook_response = await client.post("/api/webhooks/payment", json=webhook_data)
    assert webhook_response.status_code == 200
    
    # Verify booking status updated
    booking_check = await client.get(f"/api/bookings/{booking_id}", headers=headers)
    assert booking_check.status_code == 200
    assert booking_check.json()["status"] == "confirmed"
    
    # 8. GET /api/loyalty/profile → confirm points earned
    loyalty_response = await client.get("/api/loyalty/profile", headers=headers)
    assert loyalty_response.status_code == 200
    loyalty_data = loyalty_response.json()
    assert loyalty_data["points"] > 0


@pytest.mark.asyncio
async def test_overbooking_prevention(client):
    """Test concurrent booking prevention with capacity limits"""
    
    # Create test users
    users = []
    for i in range(20):
        user_data = {
            "email": f"user_{i}_{uuid.uuid4().hex[:8]}@test.com",
            "password": "TestPass123!",
            "full_name": f"Test User {i}",
            "phone": f"+20123456{i:04d}"
        }
        
        register_response = await client.post("/api/auth/register", json=user_data)
        assert register_response.status_code == 201
        
        login_response = await client.post("/api/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        token = login_response.json()["access_token"]
        users.append({"Authorization": f"Bearer {token}"})
    
    # Get a room with limited capacity
    products_response = await client.get("/api/products?type=room")
    room = products_response.json()[0]
    room_id = room["id"]
    
    # Set capacity to 2 for testing
    await client.patch(
        f"/api/admin/products/{room_id}",
        json={"capacity": 2},
        headers=users[0]  # Assume first user is admin for simplicity
    )
    
    check_in = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    check_out = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
    
    # Create 20 concurrent booking requests
    async def make_booking(headers):
        try:
            response = await client.post(
                "/api/bookings",
                json={
                    "product_id": room_id,
                    "check_in": check_in,
                    "check_out": check_out,
                    "guests": 1
                },
                headers=headers
            )
            return response.status_code
        except Exception:
            return 500
    
    # Execute concurrent requests
    results = await asyncio.gather(*[make_booking(user) for user in users])
    
    # Assert: exactly 2 succeed (201), rest get 409
    success_count = sum(1 for status in results if status == 201)
    conflict_count = sum(1 for status in results if status == 409)
    
    assert success_count == 2, f"Expected 2 successful bookings, got {success_count}"
    assert conflict_count == 18, f"Expected 18 conflicts, got {conflict_count}"
    
    # Assert: inventory.available == 0 (not negative)
    availability_response = await client.get(
        f"/api/availability?product_id={room_id}&check_in={check_in}&check_out={check_out}"
    )
    availability = availability_response.json()
    assert availability["available"] == False
    assert availability["remaining_capacity"] == 0


@pytest.mark.asyncio
async def test_pricing_rules(client):
    """Test all 5 pricing rules with known inputs"""
    
    # Get a room for testing
    products_response = await client.get("/api/products?type=room")
    room = products_response.json()[0]
    room_id = room["id"]
    base_price = room["base_price"]
    
    # Test 1: Weekend surcharge (Friday-Saturday)
    friday = datetime.now()
    while friday.weekday() != 4:  # Find next Friday
        friday += timedelta(days=1)
    saturday = friday + timedelta(days=1)
    
    weekend_response = await client.get(
        f"/api/products/{room_id}/price?check_in={friday.strftime('%Y-%m-%d')}&check_out={saturday.strftime('%Y-%m-%d')}"
    )
    weekend_price = weekend_response.json()["final_price"]
    expected_weekend = base_price * 1.3  # 30% weekend surcharge
    assert abs(weekend_price - expected_weekend) < 1, f"Weekend pricing failed: {weekend_price} vs {expected_weekend}"
    
    # Test 2: Peak season (December-January)
    dec_date = datetime(2026, 12, 15)
    jan_date = datetime(2027, 1, 15)
    
    peak_response = await client.get(
        f"/api/products/{room_id}/price?check_in={dec_date.strftime('%Y-%m-%d')}&check_out={jan_date.strftime('%Y-%m-%d')}"
    )
    peak_price = peak_response.json()["final_price"]
    expected_peak = base_price * 1.5 * 31  # 50% peak season surcharge * 31 days
    assert abs(peak_price - expected_peak) < 50, f"Peak season pricing failed: {peak_price} vs {expected_peak}"
    
    # Test 3: Early bird discount (30+ days advance)
    future_date = datetime.now() + timedelta(days=35)
    early_response = await client.get(
        f"/api/products/{room_id}/price?check_in={future_date.strftime('%Y-%m-%d')}&check_out={(future_date + timedelta(days=1)).strftime('%Y-%m-%d')}"
    )
    early_price = early_response.json()["final_price"]
    expected_early = base_price * 0.85  # 15% early bird discount
    assert abs(early_price - expected_early) < 1, f"Early bird pricing failed: {early_price} vs {expected_early}"
    
    # Test 4: Long stay discount (7+ nights)
    long_stay_response = await client.get(
        f"/api/products/{room_id}/price?check_in={(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}&check_out={(datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')}"
    )
    long_stay_price = long_stay_response.json()["final_price"]
    expected_long_stay = base_price * 0.9 * 8  # 10% long stay discount * 8 nights
    assert abs(long_stay_price - expected_long_stay) < 10, f"Long stay pricing failed: {long_stay_price} vs {expected_long_stay}"
    
    # Test 5: Last minute discount (within 3 days)
    tomorrow = datetime.now() + timedelta(days=1)
    last_minute_response = await client.get(
        f"/api/products/{room_id}/price?check_in={tomorrow.strftime('%Y-%m-%d')}&check_out={(tomorrow + timedelta(days=1)).strftime('%Y-%m-%d')}"
    )
    last_minute_price = last_minute_response.json()["final_price"]
    expected_last_minute = base_price * 0.8  # 20% last minute discount
    assert abs(last_minute_price - expected_last_minute) < 1, f"Last minute pricing failed: {last_minute_price} vs {expected_last_minute}"


@pytest.mark.asyncio
async def test_admin_analytics(client, admin_user, guest_user):
    """Test admin analytics with real booking data"""
    
    admin_headers = admin_user["headers"]
    guest_headers = guest_user["headers"]
    
    # Get a room
    products_response = await client.get("/api/products?type=room")
    room = products_response.json()[0]
    room_id = room["id"]
    base_price = room["base_price"]
    
    # Create 3 bookings
    total_expected_revenue = 0
    booking_ids = []
    
    for i in range(3):
        check_in = (datetime.now() + timedelta(days=7 + i)).strftime("%Y-%m-%d")
        check_out = (datetime.now() + timedelta(days=8 + i)).strftime("%Y-%m-%d")
        
        booking_response = await client.post(
            "/api/bookings",
            json={
                "product_id": room_id,
                "check_in": check_in,
                "check_out": check_out,
                "guests": 2
            },
            headers=guest_headers
        )
        assert booking_response.status_code == 201
        booking = booking_response.json()
        booking_ids.append(booking["id"])
        total_expected_revenue += booking["total_price"]
        
        # Simulate payment confirmation
        webhook_response = await client.post("/api/webhooks/payment", json={
            "booking_id": booking["id"],
            "payment_status": "completed",
            "transaction_id": f"txn_{uuid.uuid4().hex[:8]}"
        })
        assert webhook_response.status_code == 200
    
    # GET /api/admin/analytics/overview → assert total_revenue matches
    analytics_response = await client.get("/api/admin/analytics/overview", headers=admin_headers)
    assert analytics_response.status_code == 200
    analytics = analytics_response.json()
    
    assert "total_revenue" in analytics
    # Allow for small floating point differences
    assert abs(analytics["total_revenue"] - total_expected_revenue) < 1


@pytest.mark.asyncio
async def test_rbac(client, guest_user, admin_user):
    """Test Role-Based Access Control"""
    
    guest_headers = guest_user["headers"]
    admin_headers = admin_user["headers"]
    
    # Guest user → GET /api/admin/analytics → 403
    guest_analytics_response = await client.get("/api/admin/analytics/overview", headers=guest_headers)
    assert guest_analytics_response.status_code == 403
    
    # Admin user → GET /api/admin/analytics → 200
    admin_analytics_response = await client.get("/api/admin/analytics/overview", headers=admin_headers)
    assert admin_analytics_response.status_code == 200


@pytest.mark.asyncio
async def test_auth_flow(client):
    """Test complete authentication flow"""
    
    # Register
    user_data = {
        "email": f"auth_test_{uuid.uuid4().hex[:8]}@test.com",
        "password": "TestPass123!",
        "full_name": "Auth Test User",
        "phone": "+201234567890"
    }
    
    register_response = await client.post("/api/auth/register", json=user_data)
    assert register_response.status_code == 201
    
    # Login
    login_response = await client.post("/api/auth/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Access protected endpoint
    profile_response = await client.get("/api/auth/profile", headers=headers)
    assert profile_response.status_code == 200
    
    # Logout
    logout_response = await client.post("/api/auth/logout", headers=headers)
    assert logout_response.status_code == 200
    
    # Access protected endpoint after logout → 401
    protected_response = await client.get("/api/auth/profile", headers=headers)
    assert protected_response.status_code == 401


if __name__ == "__main__":
    # Run tests with: pytest -v backend/tests/test_integration.py
    pass
