#!/bin/bash

# الخيمة Beach Resort - Stop Development Services
# This script stops all running development services

set -e

echo "🛑 الخيمة Beach Resort - Stopping Development Services"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to kill process by PID file
kill_service() {
    local service_name=$1
    local pid_file=$2
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
            print_status "$service_name stopped (PID: $pid)"
        else
            print_warning "$service_name was not running"
        fi
        rm -f "$pid_file"
    else
        print_warning "No PID file found for $service_name"
    fi
}

# Stop services using PID files
kill_service "Backend" ".backend.pid"
kill_service "AI Service" ".ai-service.pid"
kill_service "Frontend" ".frontend.pid"

# Kill any remaining processes by name
print_warning "Killing any remaining processes..."

# Kill uvicorn processes (backend)
pkill -f "uvicorn app.main:app" 2>/dev/null || true

# Kill Python processes running chatbot.py (AI service)
pkill -f "python chatbot.py" 2>/dev/null || true

# Kill npm/node processes (frontend)
pkill -f "npm run dev" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true

# Clean up log files
if [ -f "backend.log" ]; then
    rm backend.log
fi

if [ -f "ai-service.log" ]; then
    rm ai-service.log
fi

if [ -f "frontend.log" ]; then
    rm frontend.log
fi

print_status "All services stopped and cleaned up!"
echo ""
echo "🔄 To start services again, run: ./start.sh"
