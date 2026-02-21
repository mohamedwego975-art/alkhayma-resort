#!/bin/bash

echo "🔍 Testing Database & Redis Connection..."
echo ""

# Test PostgreSQL
echo "Testing PostgreSQL..."
docker exec alkhayma-resort-db-1 pg_isready -U postgres && echo "✅ PostgreSQL is ready" || echo "❌ PostgreSQL failed"

# Test Redis
echo ""
echo "Testing Redis..."
docker exec alkhayma-resort-redis-1 redis-cli ping && echo "✅ Redis is ready" || echo "❌ Redis failed"

echo ""
echo "✅ Services are running!"
