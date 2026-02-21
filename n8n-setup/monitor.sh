#!/bin/bash

# N8N Monitoring Script
echo "📊 N8N System Status"
echo "==================="

# Check container status
echo "🐳 Container Status:"
docker-compose ps

echo ""
echo "💾 Resource Usage:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

echo ""
echo "📈 N8N Metrics:"
curl -s http://localhost:5678/metrics 2>/dev/null | grep -E "(n8n_|http_)" | head -10 || echo "Metrics not available"

echo ""
echo "🔍 Recent Logs (last 20 lines):"
docker-compose logs --tail=20 n8n
