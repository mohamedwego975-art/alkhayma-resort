#!/bin/bash
# Phase 5 Step 2: HTTP Endpoint Testing

echo "============================================================"
echo "🧪 HTTP ENDPOINT TESTING"
echo "============================================================"
echo ""

BASE_URL="http://localhost:8000"

# Check if backend is running
if ! curl -s "$BASE_URL/health" > /dev/null 2>&1; then
    echo "❌ Backend is not running on port 8000"
    echo ""
    echo "Start backend first:"
    echo "  cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
    exit 1
fi

echo "✅ Backend is running"
echo ""

# Test 1: Health Check
echo "1️⃣ GET /health"
curl -s "$BASE_URL/health" | python3 -m json.tool
echo ""

# Test 2: Get Rooms
echo "2️⃣ GET /api/products?type=room"
curl -s "$BASE_URL/api/products?type=room" | python3 -m json.tool | head -30
echo "   ... (truncated)"
echo ""

# Test 3: Get Beach Products
echo "3️⃣ GET /api/products?type=beach"
curl -s "$BASE_URL/api/products?type=beach" | python3 -m json.tool | head -20
echo ""

# Test 4: Get Water Activities
echo "4️⃣ GET /api/products?type=water_activity"
ACTIVITIES=$(curl -s "$BASE_URL/api/products?type=water_activity")
COUNT=$(echo "$ACTIVITIES" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")
echo "   ✅ Found $COUNT water activities"
echo ""

# Test 5: Get Specific Product
echo "5️⃣ GET /api/products/1"
curl -s "$BASE_URL/api/products/1" | python3 -m json.tool | head -15
echo ""

echo "============================================================"
echo "✅ ALL HTTP ENDPOINT TESTS COMPLETED"
echo "============================================================"
