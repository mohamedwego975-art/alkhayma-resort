#!/bin/bash
# Start Backend Server

cd "$(dirname "$0")/backend"

echo "🚀 Starting Backend Server..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Activate virtual environment
source venv/bin/activate

# Start uvicorn
echo "Starting uvicorn on http://0.0.0.0:8000"
echo ""
echo "Press Ctrl+C to stop"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
