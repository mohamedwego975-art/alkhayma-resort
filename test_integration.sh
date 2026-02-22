#!/bin/bash
# Phase 5 Step 3: Full Stack Integration Testing

echo "============================================================"
echo "🔗 FULL STACK INTEGRATION TESTING"
echo "============================================================"
echo ""

BASE_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:5173"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

test_endpoint() {
    local name="$1"
    local url="$2"
    local expected="$3"

    echo -n "Testing: $name ... "

    response=$(curl -s "$url" 2>/dev/null)

    if [ -z "$response" ]; then
        echo -e "${RED}❌ FAILED${NC} (No response)"
        ((FAILED++))
        return 1
    fi

    if [ -n "$expected" ]; then
        if echo "$response" | grep -q "$expected"; then
            echo -e "${GREEN}✅ PASSED${NC}"
            ((PASSED++))
            return 0
        else
            echo -e "${RED}❌ FAILED${NC} (Expected: $expected)"
            ((FAILED++))
            return 1
        fi
    else
        echo -e "${GREEN}✅ PASSED${NC}"
        ((PASSED++))
        return 0
    fi
}

# Check Backend
echo "1️⃣ Backend Health Check"
if ! curl -s "$BASE_URL/api/health" > /dev/null 2>&1; then
    echo -e "${RED}❌ Backend not running on port 8000${NC}"
    echo ""
    echo "Start backend:"
    echo "  cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
    exit 1
fi
echo -e "${GREEN}✅ Backend is running${NC}"
echo ""

# Check Frontend
echo "2️⃣ Frontend Health Check"
if ! curl -s "$FRONTEND_URL" > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Frontend not running on port 5173${NC}"
    echo ""
    echo "Start frontend:"
    echo "  cd frontend && npm run dev"
    echo ""
    FRONTEND_RUNNING=false
else
    echo -e "${GREEN}✅ Frontend is running${NC}"
    FRONTEND_RUNNING=true
fi
echo ""

# API Tests
echo "3️⃣ API Endpoint Tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_endpoint "Health endpoint" "$BASE_URL/api/health" "status"
test_endpoint "Get all rooms" "$BASE_URL/api/rooms" "room_number"
test_endpoint "Get beach products" "$BASE_URL/api/products?product_type=beach" "beach"
test_endpoint "Get water activities" "$BASE_URL/api/products?product_type=water_activity" "water_activity"

echo ""

# Authentication Test
echo "4️⃣ Authentication Test"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@alkhayma.com","password":"admin123"}' 2>/dev/null)

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    echo -e "Admin login: ${GREEN}✅ PASSED${NC}"
    ((PASSED++))
    TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
    echo "Token: ${TOKEN:0:20}..."
else
    echo -e "Admin login: ${RED}❌ FAILED${NC}"
    ((FAILED++))
fi

echo ""

# Data Validation
echo "5️⃣ Data Validation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ROOMS=$(curl -s "$BASE_URL/api/rooms" 2>/dev/null)
ROOM_COUNT=$(echo "$ROOMS" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)

if [ "$ROOM_COUNT" = "6" ]; then
    echo -e "Room count (6): ${GREEN}✅ PASSED${NC}"
    ((PASSED++))
else
    echo -e "Room count ($ROOM_COUNT/6): ${RED}❌ FAILED${NC}"
    ((FAILED++))
fi

PRODUCTS=$(curl -s "$BASE_URL/api/products?product_type=beach" 2>/dev/null)
PRODUCT_COUNT=$(echo "$PRODUCTS" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)

if [ "$PRODUCT_COUNT" = "2" ]; then
    echo -e "Beach products (2): ${GREEN}✅ PASSED${NC}"
    ((PASSED++))
else
    echo -e "Beach products ($PRODUCT_COUNT/2): ${RED}❌ FAILED${NC}"
    ((FAILED++))
fi

echo ""

# Frontend Tests (if running)
if [ "$FRONTEND_RUNNING" = true ]; then
    echo "6️⃣ Frontend Integration"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    test_endpoint "Homepage loads" "$FRONTEND_URL" "الخيمة"
    test_endpoint "Rooms page exists" "$FRONTEND_URL/rooms"
    test_endpoint "Beach page exists" "$FRONTEND_URL/beach"

    echo ""
fi

# Summary
echo "============================================================"
echo "📊 TEST SUMMARY"
echo "============================================================"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo "Total:  $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED${NC}"
    echo "============================================================"
    exit 0
else
    echo -e "${RED}❌ SOME TESTS FAILED${NC}"
    echo "============================================================"
    exit 1
fi
