#!/bin/bash
# Development startup script for Al-Khayma Resort
# Run this to start both frontend and backend in development mode

set -e

echo "🚀 Starting Al-Khayma Resort Development Environment"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists node; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3.10+"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Function to cleanup processes on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Shutting down development servers...${NC}"
    pkill -f "uvicorn" || true
    pkill -f "vite" || true
    echo -e "${GREEN}✅ Cleanup complete${NC}"
}

trap cleanup EXIT

# Start Backend
echo -e "${YELLOW}🔧 Starting Backend (Port 8000)...${NC}"
cd "$PROJECT_ROOT/backend"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -q -r requirements.txt

# Run database migrations (if you have alembic)
# alembic upgrade head || true

# Start backend in background with SQLite for quick development
export USE_SQLITE=true
export LOG_LEVEL=DEBUG
export ENVIRONMENT=development
export SECRET_KEY=dev-secret-key-change-in-production

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug &
BACKEND_PID=$!

sleep 2

if ps -p $BACKEND_PID > /dev/null; then
    echo -e "${GREEN}✅ Backend started successfully${NC}"
    echo -e "   API: http://localhost:8000"
    echo -e "   Docs: http://localhost:8000/api/docs"
else
    echo -e "${RED}❌ Failed to start backend${NC}"
    exit 1
fi

echo ""

# Start Frontend
echo -e "${YELLOW}🎨 Starting Frontend (Port 5173)...${NC}"
cd "$PROJECT_ROOT/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

# Start frontend in background
npm run dev -- --host 0.0.0.0 --port 5173 &
FRONTEND_PID=$!

sleep 3

if ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${GREEN}✅ Frontend started successfully${NC}"
    echo -e "   App: http://localhost:5173"
else
    echo -e "${RED}❌ Failed to start frontend${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Development environment is ready!${NC}"
echo ""
echo "📍 Available URLs:"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/api/docs"
echo "   Health Check: http://localhost:8000/api/health"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for both processes
wait
