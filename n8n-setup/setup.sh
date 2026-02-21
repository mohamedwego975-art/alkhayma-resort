#!/bin/bash

# الخيمة Beach Resort - N8N Professional Setup Script
# تثبيت n8n بطريقة احترافية مع Docker

set -e

echo "🏖 الخيمة Beach Resort - N8N Professional Setup"
echo "================================================"

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

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    print_status "Docker installed successfully"
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Installing..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    print_status "Docker Compose installed successfully"
fi

# Create directories
print_info "Creating directory structure..."
mkdir -p ssl
mkdir -p n8n-credentials
mkdir -p backups
mkdir -p logs

# Generate self-signed SSL certificate (for development)
if [ ! -f "ssl/cert.pem" ]; then
    print_info "Generating SSL certificate..."
    openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes \
        -subj "/C=EG/ST=South Sinai/L=Sharm El Sheikh/O=AlKhayma Resort/CN=automation.alkhayma-resort.com"
    print_status "SSL certificate generated"
fi

# Create environment file
print_info "Creating environment configuration..."
cat > .env << EOF
# الخيمة Beach Resort - N8N Environment Configuration
COMPOSE_PROJECT_NAME=alkhayma-n8n

# N8N Configuration
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=AlKhayma2026!
N8N_ENCRYPTION_KEY=resort-encryption-key-2026-$(openssl rand -hex 16)

# Database Configuration
POSTGRES_DB=n8n
POSTGRES_USER=n8n
POSTGRES_PASSWORD=$(openssl rand -base64 32)

# Redis Configuration
REDIS_PASSWORD=$(openssl rand -base64 32)

# Domain Configuration
DOMAIN=automation.alkhayma-resort.com
WEBHOOK_URL=https://automation.alkhayma-resort.com/

# Timezone
TIMEZONE=Africa/Cairo
EOF

print_status "Environment file created"

# Create credentials template
print_info "Creating credentials template..."
cat > n8n-credentials/credentials-template.json << EOF
{
  "twilio": {
    "name": "Twilio Account",
    "type": "twilioApi",
    "data": {
      "accountSid": "YOUR_TWILIO_ACCOUNT_SID",
      "authToken": "YOUR_TWILIO_AUTH_TOKEN"
    }
  },
  "gmail": {
    "name": "Gmail Account", 
    "type": "gmailOAuth2",
    "data": {
      "clientId": "YOUR_GMAIL_CLIENT_ID",
      "clientSecret": "YOUR_GMAIL_CLIENT_SECRET",
      "refreshToken": "YOUR_GMAIL_REFRESH_TOKEN"
    }
  },
  "airtable": {
    "name": "Airtable",
    "type": "airtableTokenApi", 
    "data": {
      "apiToken": "YOUR_AIRTABLE_API_TOKEN",
      "baseId": "YOUR_AIRTABLE_BASE_ID"
    }
  },
  "openai": {
    "name": "OpenAI API",
    "type": "openAiApi",
    "data": {
      "apiKey": "YOUR_OPENAI_API_KEY"
    }
  },
  "backend": {
    "name": "Backend API Auth",
    "type": "httpHeaderAuth",
    "data": {
      "name": "Authorization",
      "value": "Bearer YOUR_BACKEND_API_TOKEN"
    }
  }
}
EOF

print_status "Credentials template created"

# Create backup script
print_info "Creating backup script..."
cat > backup.sh << 'EOF'
#!/bin/bash

# N8N Backup Script
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)

echo "🔄 Starting N8N backup..."

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup N8N data
docker-compose exec -T n8n n8n export:workflow --backup --output=/tmp/workflows_$DATE.json
docker cp n8n-resort:/tmp/workflows_$DATE.json "$BACKUP_DIR/"

# Backup database
docker-compose exec -T postgres pg_dump -U n8n n8n > "$BACKUP_DIR/database_$DATE.sql"

# Backup credentials (encrypted)
docker cp n8n-resort:/home/node/.n8n/credentials.json "$BACKUP_DIR/credentials_$DATE.json" 2>/dev/null || echo "No credentials to backup"

# Compress backup
tar -czf "$BACKUP_DIR/n8n_backup_$DATE.tar.gz" -C "$BACKUP_DIR" workflows_$DATE.json database_$DATE.sql credentials_$DATE.json 2>/dev/null

# Clean up individual files
rm -f "$BACKUP_DIR/workflows_$DATE.json" "$BACKUP_DIR/database_$DATE.sql" "$BACKUP_DIR/credentials_$DATE.json"

echo "✅ Backup completed: n8n_backup_$DATE.tar.gz"

# Keep only last 7 backups
find "$BACKUP_DIR" -name "n8n_backup_*.tar.gz" -type f -mtime +7 -delete
EOF

chmod +x backup.sh
print_status "Backup script created"

# Create monitoring script
print_info "Creating monitoring script..."
cat > monitor.sh << 'EOF'
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
EOF

chmod +x monitor.sh
print_status "Monitoring script created"

# Start services
print_info "Starting N8N services..."
docker-compose up -d

# Wait for services to be ready
print_info "Waiting for services to start..."
sleep 30

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    print_status "N8N services started successfully!"
    
    echo ""
    echo "🎉 N8N Professional Setup Complete!"
    echo "=================================="
    echo ""
    echo "📱 Access Information:"
    echo "   URL: http://localhost:5678"
    echo "   Username: admin"
    echo "   Password: AlKhayma2026!"
    echo ""
    echo "🔧 Management Commands:"
    echo "   Start:    docker-compose up -d"
    echo "   Stop:     docker-compose down"
    echo "   Logs:     docker-compose logs -f n8n"
    echo "   Backup:   ./backup.sh"
    echo "   Monitor:  ./monitor.sh"
    echo ""
    echo "📁 Next Steps:"
    echo "   1. Configure credentials in n8n interface"
    echo "   2. Import workflows from ../n8n-workflows/"
    echo "   3. Test webhook endpoints"
    echo "   4. Set up SSL certificate for production"
    echo ""
    print_warning "Remember to update credentials in n8n-credentials/credentials-template.json"
    
else
    print_error "Failed to start N8N services. Check logs with: docker-compose logs"
    exit 1
fi
