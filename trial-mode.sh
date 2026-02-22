#!/bin/bash
# AlKhayma Beach Resort - Trial Mode Launcher
# هذا السكريبت يشغل المشروع في الوضع التجريبي

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="alkhayma-resort"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_banner() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                                                           ║"
    echo "║   🏖️  AlKhayma Beach Resort - الوضع التجريبي  🏖️        ║"
    echo "║                                                           ║"
    echo "║   Trial Mode / الوضع التجريبي                            ║"
    echo "║                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
}

# Check if .env file exists
check_env_file() {
    if [ ! -f "$SCRIPT_DIR/.env" ]; then
        log_warning "ملف .env غير موجود - سيتم إنشاؤه من .env.example"
        cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
        log_info "يرجى تعديل ملف .env وإضافة مفاتيح API المطلوبة"
    fi
}

# Check dependencies
check_dependencies() {
    log_info "التحقق من المتطلبات..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker غير مثبت. يرجى تثبيت Docker أولاً."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose غير مثبت. يرجى تثبيت Docker Compose أولاً."
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        log_warning "Node.js غير مثبت. سيتم استخدام Docker للـ frontend."
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_warning "Python3 غير مثبت. سيتم استخدام Docker للـ backend."
    fi
    
    log_success "جميع المتطلبات متوفرة"
}

# Start infrastructure services
start_infrastructure() {
    log_info "تشغيل خدمات البنية التحتية..."
    
    # Start PostgreSQL and Redis using Docker Compose
    cd "$SCRIPT_DIR"
    docker-compose -f docker-compose.dev.yml up -d db redis
    
    # Wait for PostgreSQL to be ready
    log_info "انتظار تشغيل PostgreSQL..."
    for i in {1..30}; do
        if docker-compose -f docker-compose.dev.yml exec -T db pg_isready -U postgres > /dev/null 2>&1; then
            log_success "PostgreSQL جاهز"
            break
        fi
        sleep 2
    done
    
    log_success "خدمات البنية التحتية تعمل"
}

# Start monitoring
start_monitoring() {
    if [ "${ENABLE_MONITORING:-true}" = "true" ]; then
        log_info "تشغيل نظام المراقبة (Prometheus + Grafana)..."
        cd "$SCRIPT_DIR/monitoring"
        
        # Create provisioning directories
        mkdir -p grafana/provisioning/datasources
        mkdir -p grafana/provisioning/dashboards
        mkdir -p grafana/dashboards
        
        # Start monitoring stack
        docker-compose up -d
        
        log_success "نظام المراقبة يعمل على:"
        log_info "  📊 Grafana:     http://localhost:3000"
        log_info "  📈 Prometheus: http://localhost:9090"
    fi
}

# Start N8N automation
start_n8n() {
    if [ "${ENABLE_N8N_AUTOMATION:-true}" = "true" ]; then
        log_info "تشغيل N8N للأتمتة..."
        cd "$SCRIPT_DIR/n8n-setup"
        
        # Create required directories
        mkdir -p n8n-credentials
        mkdir -p backups
        mkdir -p logs
        
        # Start N8N
        docker-compose up -d
        
        # Wait for N8N to be ready
        log_info "انتظار تشغيل N8N..."
        for i in {1..30}; do
            if curl -s http://localhost:5678/health > /dev/null 2>&1; then
                log_success "N8N جاهز"
                break
            fi
            sleep 2
        done
        
        # Deploy workflows
        log_info "نشر workflows..."
        if [ -f "deploy-workflows.sh" ]; then
            ./deploy-workflows.sh || log_warning "تعذر نشر workflows"
        fi
        
        log_success "N8N يعمل على: http://localhost:5678"
    fi
}

# Start backend
start_backend() {
    log_info "تشغيل Backend..."
    cd "$SCRIPT_DIR/backend"
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        log_info "إنشاء بيئة Python افتراضية..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    pip install -q -r requirements.txt
    
    # Run migrations
    alembic upgrade head || log_warning "تعذر تشغيل migrations"
    
    # Seed data if needed
    if [ "${SEED_DATA:-false}" = "true" ]; then
        python seed_data.py || log_warning "تعذر إضافة البيانات الأولية"
    fi
    
    # Start backend
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
    BACKEND_PID=$!
    echo $BACKEND_PID > "$SCRIPT_DIR/.backend.pid"
    
    log_success "Backend يعمل على: http://localhost:8000"
    log_info "📚 API Documentation: http://localhost:8000/docs"
}

# Start AI Service
start_ai_service() {
    log_info "تشغيل AI Service..."
    cd "$SCRIPT_DIR/ai-service"
    
    if [ -f "main.py" ]; then
        # Create virtual environment if it doesn't exist
        if [ ! -d "venv" ]; then
            python3 -m venv venv
        fi
        
        source venv/bin/activate
        pip install -q -r requirements.txt 2>/dev/null || log_warning "تعذر تثبيت متطلبات AI Service"
        
        # Start AI service
        python main.py &
        AI_PID=$!
        echo $AI_PID > "$SCRIPT_DIR/.ai-service.pid"
        
        log_success "AI Service يعمل على: http://localhost:8001"
    else
        log_warning "AI Service غير متوفر"
    fi
}

# Start frontend
start_frontend() {
    log_info "تشغيل Frontend..."
    cd "$SCRIPT_DIR/frontend"
    
    # Install dependencies
    npm install
    
    # Start development server
    npm run dev &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > "$SCRIPT_DIR/.frontend.pid"
    
    log_success "Frontend يعمل على: http://localhost:5173"
}

# Print status
print_status() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                  📊 حالة المشروع                        ║"
    echo "╠═══════════════════════════════════════════════════════════╣"
    echo "║                                                           ║"
    echo "║  🌐 Frontend:     http://localhost:5173                   ║"
    echo "║  ⚙️  Backend API:  http://localhost:8000                  ║"
    echo "║  📚 API Docs:     http://localhost:8000/docs            ║"
    echo "║  🤖 AI Service:   http://localhost:8001                 ║"
    echo "║                                                           ║"
    if [ "${ENABLE_MONITORING:-true}" = "true" ]; then
        echo "║  📊 Grafana:      http://localhost:3000                 ║"
        echo "║  📈 Prometheus:  http://localhost:9090                ║"
    fi
    if [ "${ENABLE_N8N_AUTOMATION:-true}" = "true" ]; then
        echo "║  🔄 N8N:         http://localhost:5678                  ║"
    fi
    echo "║                                                           ║"
    echo "║  💡 Features:                                             ║"
    if [ "${ENABLE_EMAIL_NOTIFICATIONS:-true}" = "true" ]; then
        echo "║     ✅ Email Notifications (Gmail/SMTP)                   ║"
    fi
    if [ "${ENABLE_WHATSAPP_NOTIFICATIONS:-true}" = "true" ]; then
        echo "║     ✅ WhatsApp (Twilio)                                  ║"
    fi
    echo "║     ✅ Google Maps Integration                            ║"
    if [ "${ENABLE_N8N_AUTOMATION:-true}" = "true" ]; then
        echo "║     ✅ N8N Automation                                   ║"
    fi
    if [ "${ENABLE_MONITORING:-true}" = "true" ]; then
        echo "║     ✅ Prometheus + Grafana Monitoring                    ║"
    fi
    echo "║                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    log_info "اضغط Ctrl+C لإيقاف جميع الخدمات"
    echo ""
}

# Cleanup function
cleanup() {
    echo ""
    log_warning "جاري إيقاف الخدمات..."
    
    # Kill processes
    for pid_file in "$SCRIPT_DIR"/*.pid; do
        if [ -f "$pid_file" ]; then
            kill $(cat "$pid_file") 2>/dev/null || true
            rm "$pid_file"
        fi
    done
    
    # Stop Docker containers
    cd "$SCRIPT_DIR"
    docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
    
    cd "$SCRIPT_DIR/monitoring"
    docker-compose down 2>/dev/null || true
    
    cd "$SCRIPT_DIR/n8n-setup"
    docker-compose down 2>/dev/null || true
    
    log_success "تم إيقاف جميع الخدمات"
    exit 0
}

# Set trap for cleanup
trap cleanup INT TERM

# Main function
main() {
    print_banner
    
    # Load environment variables
    if [ -f "$SCRIPT_DIR/.env" ]; then
        set -a
        source "$SCRIPT_DIR/.env"
        set +a
    fi
    
    check_env_file
    check_dependencies
    
    log_info "بدء تشغيل الوضع التجريبي..."
    echo ""
    
    # Start all services
    start_infrastructure
    start_monitoring
    start_n8n
    start_backend
    start_ai_service
    start_frontend
    
    # Wait a bit for all services to be ready
    sleep 5
    
    print_status
    
    # Keep script running
    while true; do
        sleep 1
    done
}

# Run main
main "$@"
