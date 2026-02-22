#!/bin/bash
#
# Al-Khayma Beach Resort - Development Startup Script with PostgreSQL & Redis
# This script initializes the development environment with Docker services
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Al-Khayma Beach Resort - Dev Setup   ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker is running${NC}"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose not found. Please install it.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker Compose is available${NC}"
echo ""

# Check if .env.dev exists, if not create it
if [ ! -f ".env.dev" ]; then
    echo -e "${YELLOW}⚠️  .env.dev not found. Creating from template...${NC}"
    cat > .env.dev << 'EOF'
# Development environment variables
DB_USER=resort_user
DB_PASS=strong_password_123!
DB_NAME=resort_db
DB_HOST=localhost
DB_PORT=5432
DATABASE_URL=postgresql+asyncpg://resort_user:strong_password_123!@localhost:5432/resort_db

REDIS_URL=redis://localhost:6379/0

SECRET_KEY=dev-secret-key-change-in-production-64-chars-long-min
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

ENVIRONMENT=development
DEBUG=true
USE_SQLITE=false

FRONTEND_URL=http://localhost:5173
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

LOG_LEVEL=DEBUG
EOF
    echo -e "${GREEN}✅ Created .env.dev${NC}"
fi

# Function to wait for PostgreSQL
wait_for_postgres() {
    echo -e "${YELLOW}⏳ Waiting for PostgreSQL to be ready...${NC}"
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if docker-compose -f docker-compose.dev.yml exec -T db pg_isready -U resort_user -d resort_db > /dev/null 2>&1; then
            echo -e "${GREEN}✅ PostgreSQL is ready!${NC}"
            return 0
        fi
        echo -n "."
        sleep 1
        ((attempt++))
    done
    
    echo -e "${RED}❌ PostgreSQL failed to start within ${max_attempts} seconds${NC}"
    return 1
}

# Function to wait for Redis
wait_for_redis() {
    echo -e "${YELLOW}⏳ Waiting for Redis to be ready...${NC}"
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if docker-compose -f docker-compose.dev.yml exec -T redis redis-cli ping > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Redis is ready!${NC}"
            return 0
        fi
        echo -n "."
        sleep 1
        ((attempt++))
    done
    
    echo -e "${RED}❌ Redis failed to start within ${max_attempts} seconds${NC}"
    return 1
}

# Start infrastructure services
echo -e "${BLUE}🚀 Starting infrastructure services...${NC}"
docker-compose -f docker-compose.dev.yml up -d db redis

# Wait for services
wait_for_postgres
wait_for_redis

echo ""
echo -e "${BLUE}📊 Database Status:${NC}"
docker-compose -f docker-compose.dev.yml ps db redis
echo ""

# Check backend virtual environment
echo -e "${BLUE}🔧 Setting up Backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Created virtual environment${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
if ! python -c "import fastapi" 2>/dev/null; then
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Dependencies installed${NC}"
fi

echo -e "${GREEN}✅ Backend environment ready${NC}"

# Run database migrations
echo ""
echo -e "${BLUE}🔄 Running database migrations...${NC}"

# Use SQLAlchemy create_all for initial setup
python -c "
import asyncio
from app.core.database import engine, Base
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
asyncio.run(create_tables())
print('✅ Tables created successfully')
"

# Seed database
echo ""
echo -e "${BLUE}🌱 Seeding database...${NC}"
python -m app.core.seed_data 2>/dev/null || echo -e "${YELLOW}⚠️  Seed skipped or already done${NC}"

cd ..

# Start services
echo ""
echo -e "${BLUE}🚀 Starting services...${NC}"
echo ""

# Start Backend
echo -e "${YELLOW}🔧 Starting Backend (Port 8000)...${NC}"
cd backend
export DB_USER=resort_user
export DB_PASS=strong_password_123!
export DB_NAME=resort_db
export DB_HOST=localhost
export DB_PORT=5432
export REDIS_URL=redis://localhost:6379/0
export USE_SQLITE=false
export ENVIRONMENT=development
export SECRET_KEY=dev-secret-key-change-in-production-64-chars-long-min
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

sleep 3

if ps -p $BACKEND_PID > /dev/null; then
    echo -e "${GREEN}✅ Backend started successfully${NC}"
    echo -e "   API: http://localhost:8000"
    echo -e "   Docs: http://localhost:8000/api/docs"
else
    echo -e "${RED}❌ Failed to start backend${NC}"
fi

echo ""

# Start Frontend
echo -e "${YELLOW}🎨 Starting Frontend (Port 5173)...${NC}"
cd frontend
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📦 Installing frontend dependencies...${NC}"
    npm install
    echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
fi

npm run dev -- --host 0.0.0.0 --port 5173 &
FRONTEND_PID=$!
cd ..

sleep 3

if ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${GREEN}✅ Frontend started successfully${NC}"
    echo -e "   App: http://localhost:5173"
else
    echo -e "${RED}❌ Failed to start frontend${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ✅ Setup Complete!                    ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}Services:${NC}"
echo -e "  🐘 PostgreSQL: localhost:5432"
echo -e "  🔴 Redis:      localhost:6379"
echo -e "  ⚡ Backend:    http://localhost:8000"
echo -e "  🎨 Frontend:   http://localhost:5173"
echo -e "  📚 API Docs:   http://localhost:8000/api/docs"
echo ""
echo -e "${BLUE}Test Accounts:${NC}"
echo -e "  Admin:    admin@alkhayma.com / admin123"
echo -e "  Manager:  manager@alkhayma.com / manager123"
echo -e "  Guest:    test@example.com / test123"
echo ""
echo -e "${YELLOW}Commands:${NC}"
echo -e "  View logs:     docker-compose -f docker-compose.dev.yml logs -f"
echo -e "  Stop services: docker-compose -f docker-compose.dev.yml down"
echo -e "  Reset DB:      docker-compose -f docker-compose.dev.yml down -v"
echo ""
echo -e "Press Ctrl+C to stop all servers"
echo ""

# Wait for both processes
wait
