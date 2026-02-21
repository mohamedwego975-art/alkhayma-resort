#!/bin/bash

# Production Health Check Script
echo "🏥 الخيمة Beach Resort - Health Check"
echo "===================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check services
services=("alkhaima-backend" "alkhaima-ai" "nginx" "postgresql" "redis")

for service in "${services[@]}"; do
    if systemctl is-active --quiet $service; then
        echo -e "✅ $service: ${GREEN}RUNNING${NC}"
    else
        echo -e "❌ $service: ${RED}STOPPED${NC}"
    fi
done

# Check endpoints
echo ""
echo "🌐 Endpoint Health Checks:"

endpoints=(
    "http://localhost:8000/health:Backend"
    "http://localhost:8001/health:AI Service"
    "http://localhost/health:Frontend"
)

for endpoint in "${endpoints[@]}"; do
    url=$(echo $endpoint | cut -d: -f1)
    name=$(echo $endpoint | cut -d: -f2)
    
    if curl -f -s $url > /dev/null; then
        echo -e "✅ $name: ${GREEN}HEALTHY${NC}"
    else
        echo -e "❌ $name: ${RED}UNHEALTHY${NC}"
    fi
done

# Check database connections
echo ""
echo "🗄️ Database Connections:"
db_connections=$(sudo -u postgres psql -t -c "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';" 2>/dev/null || echo "0")
echo "Active connections: $db_connections"

# Check Redis
echo ""
echo "📦 Redis Status:"
if redis-cli ping > /dev/null 2>&1; then
    echo -e "✅ Redis: ${GREEN}CONNECTED${NC}"
    redis_memory=$(redis-cli info memory | grep used_memory_human | cut -d: -f2 | tr -d '\r')
    echo "Memory usage: $redis_memory"
else
    echo -e "❌ Redis: ${RED}DISCONNECTED${NC}"
fi

# Check disk space
echo ""
echo "💾 Disk Usage:"
df -h / | tail -1 | awk '{print "Root partition: " $3 "/" $2 " (" $5 " used)"}'

# Check memory
echo ""
echo "🧠 Memory Usage:"
free -h | grep Mem | awk '{print "Memory: " $3 "/" $2 " (" int($3/$2*100) "% used)"}'

# Check load average
echo ""
echo "⚡ System Load:"
uptime | awk -F'load average:' '{print "Load average:" $2}'

echo ""
echo "Health check completed at $(date)"
