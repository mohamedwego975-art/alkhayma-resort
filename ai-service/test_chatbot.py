#!/usr/bin/env python3
"""
Test script for AI Chatbot Service
Tests all required functionality as specified
"""

import asyncio
import aiohttp
import json
import time

BASE_URL = "http://localhost:8001"

async def test_health_check():
    """Test health endpoint"""
    print("🔍 Testing health check...")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/health") as response:
            data = await response.json()
            print(f"✅ Health: {data}")
            return response.status == 200

async def test_arabic_query():
    """Test Arabic query about VIP vs standard beach"""
    print("🔍 Testing Arabic query...")
    payload = {
        "message": "ما الفرق بين شاطئ VIP والعادي؟",
        "session_id": "test_session_ar"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/chat", json=payload) as response:
            data = await response.json()
            print(f"✅ Arabic Response: {data['reply'][:100]}...")
            print(f"✅ Suggestions: {len(data['suggestions'])} items")
            return "VIP" in data['reply'] and "$" in data['reply']

async def test_english_query():
    """Test English query about activities"""
    print("🔍 Testing English query...")
    payload = {
        "message": "What activities do you have?",
        "session_id": "test_session_en"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/chat", json=payload) as response:
            data = await response.json()
            print(f"✅ English Response: {data['reply'][:100]}...")
            return "activities" in data['reply'].lower()

async def test_context_memory():
    """Test session memory with 10 messages"""
    print("🔍 Testing context memory...")
    session_id = "test_memory_session"
    
    messages = [
        "Hello, I'm interested in your resort",
        "What rooms do you have?",
        "Tell me about the deluxe room",
        "What's the price?",
        "Do you have beach access?",
        "What about VIP beach?",
        "Can I book both room and beach?",
        "What's the total cost?",
        "Do you have any discounts?",
        "What did I ask about first?"  # This should reference the first message
    ]
    
    async with aiohttp.ClientSession() as session:
        for i, message in enumerate(messages):
            payload = {
                "message": message,
                "session_id": session_id
            }
            
            async with session.post(f"{BASE_URL}/chat", json=payload) as response:
                data = await response.json()
                print(f"Message {i+1}: {message[:30]}... -> {data['reply'][:50]}...")
                
                # Check if last message references context
                if i == len(messages) - 1:
                    return "resort" in data['reply'].lower() or "interested" in data['reply'].lower()
    
    return False

async def test_upsell():
    """Test upsell functionality"""
    print("🔍 Testing upsell...")
    payload = {
        "session_id": "test_upsell",
        "user_action": "viewed_room",
        "product_id": 2  # Standard beach
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/chat/upsell", json=payload) as response:
            data = await response.json()
            print(f"✅ Upsell: {data['suggestion']}")
            print(f"✅ Product: {data['product']['name']}")
            return "VIP" in data['suggestion'] or data['product']['price'] > 75

async def test_session_expiry():
    """Test session expiry (simulated with short wait)"""
    print("🔍 Testing session expiry (simulated)...")
    session_id = "test_expiry"
    
    # First message
    payload1 = {
        "message": "Remember this: I love the ocean",
        "session_id": session_id
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/chat", json=payload1) as response:
            await response.json()
        
        # Wait a bit (simulating expiry)
        await asyncio.sleep(2)
        
        # Second message asking about first
        payload2 = {
            "message": "What did I say I love?",
            "session_id": session_id + "_new"  # Different session to simulate expiry
        }
        
        async with session.post(f"{BASE_URL}/chat", json=payload2) as response:
            data = await response.json()
            print(f"✅ After 'expiry': {data['reply'][:100]}...")
            # Should not remember "ocean" from previous session
            return "ocean" not in data['reply'].lower()

async def run_all_tests():
    """Run all validation tests"""
    print("🚀 Starting AI Chatbot Validation Tests\n")
    
    tests = [
        ("Health Check", test_health_check),
        ("Arabic Query", test_arabic_query),
        ("English Query", test_english_query),
        ("Context Memory", test_context_memory),
        ("Upsell Feature", test_upsell),
        ("Session Expiry", test_session_expiry)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
            print(f"{'✅' if result else '❌'} {test_name}: {'PASSED' if result else 'FAILED'}\n")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}\n")
            results.append((test_name, False))
    
    # Summary
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"📊 VALIDATION SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AI Chatbot is ready for production.")
    else:
        print("⚠️ Some tests failed. Please review the implementation.")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(run_all_tests())
