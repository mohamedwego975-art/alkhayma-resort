#!/bin/bash

# الخيمة Beach Resort - Development Startup Script
# This script starts all services for development

set -e

echo "🏖️  الخيمة Beach Resort - Starting Development Environment"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if .env exists
if [ ! -f .env ]; then
    print_warning ".env file not found. Copying from .env.example..."
    cp .env.example .env
    print_info "Please edit .env file with your configuration"
fi

# Start PostgreSQL and Redis if not running
print_info "Checking database services..."
if ! pgrep -x "postgres" > /dev/null; then
    print_warning "PostgreSQL not running. Please start it manually."
fi

if ! pgrep -x "redis-server" > /dev/null; then
    print_warning "Redis not running. Please start it manually."
fi

# Start Backend
print_info "Starting Backend Service (Port 8000)..."
cd backend
if [ ! -d "venv" ]; then
    print_info "Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

# Run database migrations
print_info "Running database migrations..."
alembic upgrade head

# Start backend in background
nohup python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..
print_status "Backend started (PID: $BACKEND_PID)"

# Start AI Service
print_info "Starting AI Service (Port 8001)..."
cd ai-service
if [ ! -d "venv" ]; then
    print_info "Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

# Start AI service in background
nohup python chatbot.py > ../ai-service.log 2>&1 &
AI_PID=$!
cd ..
print_status "AI Service started (PID: $AI_PID)"

# Start Frontend
print_info "Starting Frontend (Port 5173)..."
cd frontend
if [ ! -d "node_modules" ]; then
    print_info "Installing npm dependencies..."
    npm install
fi

# Start frontend in background
nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
print_status "Frontend started (PID: $FRONTEND_PID)"

# Wait for services to start
print_info "Waiting for services to initialize..."
sleep 5

# Health checks
print_info "Performing health checks..."

# Check backend
if curl -s http://localhost:8000/health > /dev/null; then
    print_status "Backend is healthy"
else
    print_error "Backend health check failed"
fi

# Check AI service
if curl -s http://localhost:8001/health > /dev/null; then
    print_status "AI Service is healthy"
else
    print_error "AI Service health check failed"
fi

# Check frontend
if curl -s http://localhost:5173 > /dev/null; then
    print_status "Frontend is healthy"
else
    print_error "Frontend health check failed"
fi

echo ""
echo "🎉 Development environment is ready!"
echo "=================================================="
echo -e "${GREEN}🌐 Frontend:${NC}    http://localhost:5173"
echo -e "${GREEN}🔧 Backend API:${NC} http://localhost:8000"
echo -e "${GREEN}🤖 AI Service:${NC}  http://localhost:8001"
echo -e "${GREEN}📊 API Docs:${NC}    http://localhost:8000/docs"
echo ""
echo -e "${BLUE}📝 Logs:${NC}"
echo "  Backend:    tail -f backend.log"
echo "  AI Service: tail -f ai-service.log"
echo "  Frontend:   tail -f frontend.log"
echo ""
echo -e "${YELLOW}🛑 To stop all services:${NC} ./stop.sh"
echo ""

# Save PIDs for stop script
echo "$BACKEND_PID" > .backend.pid
echo "$AI_PID" > .ai-service.pid
echo "$FRONTEND_PID" > .frontend.pid

print_status "All services started successfully!"
