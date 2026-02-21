#!/bin/bash

# الخيمة Beach Resort - Production Deployment Script
set -e

echo "🏖 الخيمة Beach Resort - Production Deployment"
echo "=============================================="

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root"
   exit 1
fi

# Deployment Configuration
PROJECT_DIR="/var/www/alkhaima-resort"
BACKUP_DIR="/var/backups/alkhaima-resort"
SERVICE_USER="alkhaima"

echo "📋 DEPLOYMENT CHECKLIST"
echo "======================="

# Check environment file
if [ ! -f ".env.prod" ]; then
    echo "❌ .env.prod file not found"
    exit 1
fi

# Validate environment variables
echo "🔍 Validating environment variables..."
source .env.prod

required_vars=(
    "DATABASE_URL"
    "REDIS_URL"
    "SECRET_KEY"
    "PAYMOB_API_KEY"
    "STRIPE_SECRET_KEY"
    "OPENAI_API_KEY"
)

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ] || [ "${!var}" = "CHANGE_ME" ] || [[ "${!var}" == *"CHANGE_ME"* ]]; then
        echo "❌ Environment variable $var is not set or contains CHANGE_ME"
        exit 1
    fi
done

echo "✅ Environment variables validated"

# Build frontend
echo "🏗️ Building frontend..."
cd frontend
npm ci --production
npm run build

# Check bundle sizes
echo "📦 Checking bundle sizes..."
find dist/assets -name "*.js" -size +500k -exec echo "⚠️ Large bundle: {}" \;

cd ..

# Backend setup
echo "🔧 Setting up backend..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Database migration
echo "🗄️ Running database migrations..."
python seed_data.py

# Run tests
echo "🧪 Running tests..."
pytest tests/ -v --tb=short

cd ..

# Create systemd service
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/alkhaima-backend.service > /dev/null <<EOF
[Unit]
Description=الخيمة Beach Resort Backend
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$PROJECT_DIR/backend
Environment=PATH=$PROJECT_DIR/backend/venv/bin
EnvironmentFile=$PROJECT_DIR/.env.prod
ExecStart=$PROJECT_DIR/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Create AI service
sudo tee /etc/systemd/system/alkhaima-ai.service > /dev/null <<EOF
[Unit]
Description=الخيمة Beach Resort AI Service
After=network.target redis.service

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$PROJECT_DIR/ai-service
Environment=PATH=$PROJECT_DIR/ai-service/venv/bin
EnvironmentFile=$PROJECT_DIR/.env.prod
ExecStart=$PROJECT_DIR/ai-service/venv/bin/python chatbot.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Deploy files
echo "📁 Deploying files..."
sudo mkdir -p $PROJECT_DIR
sudo cp -r . $PROJECT_DIR/
sudo chown -R $SERVICE_USER:$SERVICE_USER $PROJECT_DIR

# Configure Nginx
echo "🌐 Configuring Nginx..."
sudo cp nginx.prod.conf /etc/nginx/sites-available/alkhaima-resort
sudo ln -sf /etc/nginx/sites-available/alkhaima-resort /etc/nginx/sites-enabled/
sudo nginx -t

# Start services
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable alkhaima-backend alkhaima-ai
sudo systemctl start alkhaima-backend alkhaima-ai
sudo systemctl reload nginx

# Health checks
echo "🏥 Running health checks..."
sleep 5

if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend health check passed"
else
    echo "❌ Backend health check failed"
    exit 1
fi

if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ AI service health check passed"
else
    echo "❌ AI service health check failed"
    exit 1
fi

# Setup monitoring
echo "📊 Setting up monitoring..."
# Add Prometheus scrape config
sudo tee -a /etc/prometheus/prometheus.yml > /dev/null <<EOF

  - job_name: 'alkhaima-backend'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    scrape_interval: 15s

  - job_name: 'alkhaima-ai'
    static_configs:
      - targets: ['localhost:8001']
    metrics_path: '/metrics'
    scrape_interval: 30s
EOF

sudo systemctl reload prometheus

echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo "======================"
echo "🌐 Website: https://alkhaima-resort.com"
echo "📊 Metrics: http://localhost:8000/metrics"
echo "🤖 AI Service: http://localhost:8001"
echo "📈 Grafana: http://localhost:3000"
echo ""
echo "📋 Post-deployment tasks:"
echo "1. Configure SSL certificates"
echo "2. Set up automated backups"
echo "3. Configure monitoring alerts"
echo "4. Test all functionality"
echo ""
echo "✅ الخيمة Beach Resort is now live!"
