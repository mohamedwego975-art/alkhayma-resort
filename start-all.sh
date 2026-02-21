#!/bin/bash
# Start All Services

echo "🚀 Starting الخيمة Beach Resort Services"
echo "============================================================"
echo ""

# Check if tmux is available
if ! command -v tmux &> /dev/null; then
    echo "⚠️  tmux not found. Starting services in background..."
    echo ""
    
    # Start backend
    cd "$(dirname "$0")"
    ./start-backend.sh > logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo "✅ Backend started (PID: $BACKEND_PID)"
    
    # Wait for backend
    sleep 3
    
    # Start frontend
    ./start-frontend.sh > logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo "✅ Frontend started (PID: $FRONTEND_PID)"
    
    echo ""
    echo "Services running:"
    echo "  Backend:  http://localhost:8000"
    echo "  Frontend: http://localhost:5173"
    echo ""
    echo "To stop services:"
    echo "  kill $BACKEND_PID $FRONTEND_PID"
    
else
    echo "Starting services in tmux sessions..."
    echo ""
    
    # Start backend in tmux
    tmux new-session -d -s alkhayma-backend "cd $(dirname "$0") && ./start-backend.sh"
    echo "✅ Backend started in tmux session: alkhayma-backend"
    
    # Wait for backend
    sleep 3
    
    # Start frontend in tmux
    tmux new-session -d -s alkhayma-frontend "cd $(dirname "$0") && ./start-frontend.sh"
    echo "✅ Frontend started in tmux session: alkhayma-frontend"
    
    echo ""
    echo "Services running:"
    echo "  Backend:  http://localhost:8000"
    echo "  Frontend: http://localhost:5173"
    echo ""
    echo "To view logs:"
    echo "  tmux attach -t alkhayma-backend"
    echo "  tmux attach -t alkhayma-frontend"
    echo ""
    echo "To stop services:"
    echo "  tmux kill-session -t alkhayma-backend"
    echo "  tmux kill-session -t alkhayma-frontend"
fi

echo ""
echo "============================================================"
