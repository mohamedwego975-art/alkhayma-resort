#!/bin/bash
# Start monitoring stack (Prometheus + Grafana)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📊 AlKhayma Beach Resort - Monitoring Stack"
echo "==========================================="

# Create Grafana provisioning directories
mkdir -p grafana/provisioning/datasources
mkdir -p grafana/provisioning/dashboards
mkdir -p grafana/dashboards

# Create datasource configuration
cat > grafana/provisioning/datasources/prometheus.yml << 'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: false
EOF

# Create dashboard provider configuration
cat > grafana/provisioning/dashboards/dashboard.yml << 'EOF'
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    editable: true
    options:
      path: /var/lib/grafana/dashboards
EOF

# Create resort monitoring dashboard
cat > grafana/dashboards/resort-dashboard.json << 'EOF'
{
  "dashboard": {
    "title": "AlKhayma Resort - System Monitoring",
    "tags": ["resort", "monitoring"],
    "timezone": "Africa/Cairo",
    "schemaVersion": 36,
    "refresh": "30s",
    "panels": [
      {
        "id": 1,
        "title": "API Response Time",
        "type": "stat",
        "targets": [
          {
            "expr": "avg(http_request_duration_seconds{job=\"backend\"})",
            "legendFormat": "Avg Response Time"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "s",
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 0.5},
                {"color": "red", "value": 1.0}
              ]
            }
          }
        },
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
      },
      {
        "id": 2,
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{job=\"backend\"}[5m])",
            "legendFormat": "Requests/sec"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
      },
      {
        "id": 3,
        "title": "Error Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(http_requests_total{job=\"backend\",status=~\"5..\"}[5m])",
            "legendFormat": "Error Rate"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percentunit",
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 0.01},
                {"color": "red", "value": 0.05}
              ]
            }
          }
        },
        "gridPos": {"h": 8, "w": 8, "x": 0, "y": 8}
      },
      {
        "id": 4,
        "title": "Active Bookings",
        "type": "stat",
        "targets": [
          {
            "expr": "booking_active_total",
            "legendFormat": "Active"
          }
        ],
        "gridPos": {"h": 8, "w": 8, "x": 8, "y": 8}
      },
      {
        "id": 5,
        "title": "Revenue Today",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(payment_total{status=\"completed\"})",
            "legendFormat": "Revenue"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "currencyUSD"
          }
        },
        "gridPos": {"h": 8, "w": 8, "x": 16, "y": 8}
      },
      {
        "id": 6,
        "title": "System Resources",
        "type": "graph",
        "targets": [
          {
            "expr": "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
            "legendFormat": "CPU Usage %"
          },
          {
            "expr": "(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100",
            "legendFormat": "Memory Usage %"
          }
        ],
        "gridPos": {"h": 8, "w": 24, "x": 0, "y": 16}
      }
    ]
  }
}
EOF

echo "✅ Grafana dashboards configured"
echo ""
echo "🚀 Starting monitoring stack..."
docker-compose up -d

echo ""
echo "📊 Monitoring Stack Started!"
echo "==========================="
echo "🔗 Prometheus: http://localhost:9090"
echo "📈 Grafana:     http://localhost:3000"
echo "   User: admin"
echo "   Pass: changeme123"
echo ""
echo "⚠️  IMPORTANT: Change default Grafana password in production!"
