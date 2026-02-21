import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_auth_validation():
    """Simple validation test for authentication system"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Test 1: Health check
        health = await client.get("/health")
        assert health.status_code == 200
        print("✅ Health check passed")
        
        # Test 2: Register with admin user (from seed)
        # We'll use the seeded admin to test login
        login_response = await client.post(
            "/auth/login",
            json={
                "email": "admin@alkhaima.com",
                "password": "$2b$12$hashed_password_placeholder"  # This won't work, but let's see the error
            }
        )
        print(f"Login status: {login_response.status_code}")
        print(f"Login response: {login_response.json()}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_auth_validation())
