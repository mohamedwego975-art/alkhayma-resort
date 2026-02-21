import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import uuid


@pytest.mark.asyncio
async def test_complete_auth_flow():
    """Test complete authentication flow: register → login → access protected endpoint"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Generate unique email
        unique_email = f"user_{uuid.uuid4().hex[:8]}@test.com"
        
        # 1. Register
        register_response = await client.post(
            "/auth/register",
            json={
                "email": unique_email,
                "password": "SecurePass123",
                "full_name": "Test User",
                "phone": "0501234567"
            }
        )
        assert register_response.status_code == 201
        user_data = register_response.json()
        assert user_data["email"] == unique_email
        assert user_data["role"] == "customer"
        assert user_data["is_active"] is True
        
        # 2. Login
        login_response = await client.post(
            "/auth/login",
            json={
                "email": unique_email,
                "password": "SecurePass123"
            }
        )
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
        
        # 3. Access protected endpoint
        me_response = await client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token_data['access_token']}"}
        )
        assert me_response.status_code == 200
        me_data = me_response.json()
        assert me_data["email"] == unique_email
        assert me_data["full_name"] == "Test User"
        
        print(f"✅ Complete auth flow successful for {unique_email}")


@pytest.mark.asyncio
async def test_invalid_credentials():
    """Test login with invalid credentials"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/auth/login",
            json={
                "email": "nonexistent@test.com",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401
        print("✅ Invalid credentials properly rejected")


@pytest.mark.asyncio
async def test_unauthorized_access():
    """Test accessing protected endpoint without token"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/auth/me")
        assert response.status_code == 401  # HTTPBearer returns 401
        print("✅ Unauthorized access properly blocked")
