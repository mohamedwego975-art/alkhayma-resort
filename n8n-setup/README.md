# الخيمة Beach Resort - N8N Professional Setup

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Nginx       │    │      N8N        │    │   PostgreSQL    │
│   (Reverse      │────│   (Automation   │────│   (Database)    │
│    Proxy)       │    │    Engine)      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │     Redis       │              │
         └──────────────│   (Session      │──────────────┘
                        │    Cache)       │
                        └─────────────────┘
```

## 🚀 Quick Start

```bash
cd n8n-setup
chmod +x setup.sh
./setup.sh
```

## 📋 Features

### ✅ Production Ready
- **Docker Compose** multi-container setup
- **PostgreSQL** database for persistence
- **Redis** for session management
- **Nginx** reverse proxy with SSL
- **Auto-restart** policies

### 🔒 Security
- Basic authentication enabled
- SSL/TLS encryption
- Rate limiting (API: 10req/s, Webhooks: 100req/s)
- Security headers (XSS, CSRF protection)
- Encrypted credentials storage

### 📊 Monitoring & Backup
- Health check endpoints
- Metrics collection
- Automated daily backups
- Log rotation
- Resource monitoring

### 🌍 Localization
- Arabic timezone (Africa/Cairo)
- Arabic locale support
- Bilingual workflow support

## 🔧 Configuration

### Environment Variables
```bash
# Authentication
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=AlKhayma2026!

# Database
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=postgres
DB_POSTGRESDB_DATABASE=n8n

# Webhooks
WEBHOOK_URL=https://automation.alkhayma-resort.com/
```

### Required Credentials
1. **Twilio** - WhatsApp messaging
2. **Gmail** - Email notifications  
3. **Airtable** - CRM integration
4. **OpenAI** - GPT message generation
5. **Backend API** - Resort system integration

## 📁 Directory Structure

```
n8n-setup/
├── docker-compose.yml      # Main container configuration
├── nginx.conf             # Reverse proxy configuration
├── setup.sh              # Automated setup script
├── backup.sh              # Backup automation
├── monitor.sh             # System monitoring
├── .env                   # Environment variables
├── ssl/                   # SSL certificates
├── n8n-credentials/       # Credential templates
├── backups/              # Automated backups
└── logs/                 # Application logs
```

## 🔄 Management Commands

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f n8n
```

### Backup Data
```bash
./backup.sh
```

### Monitor System
```bash
./monitor.sh
```

### Update N8N
```bash
docker-compose pull
docker-compose up -d
```

## 🌐 Access Points

- **Main Interface**: http://localhost:5678
- **Webhooks**: http://localhost:5678/webhook/
- **Health Check**: http://localhost:5678/health
- **Metrics**: http://localhost:5678/metrics

## 🔐 Security Checklist

- [ ] Change default passwords
- [ ] Configure SSL certificates
- [ ] Set up firewall rules
- [ ] Enable log monitoring
- [ ] Configure backup retention
- [ ] Test webhook security
- [ ] Verify rate limiting

## 🚨 Troubleshooting

### Common Issues

**Port 5678 already in use:**
```bash
sudo lsof -i :5678
sudo kill -9 <PID>
```

**Database connection failed:**
```bash
docker-compose logs postgres
docker-compose restart postgres
```

**SSL certificate issues:**
```bash
# Regenerate certificate
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes
```

**Memory issues:**
```bash
# Increase Docker memory limit
docker system prune -a
```

## 📈 Performance Tuning

### Database Optimization
```sql
-- PostgreSQL tuning
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
```

### N8N Optimization
```yaml
environment:
  - N8N_PAYLOAD_SIZE_MAX=16MB
  - N8N_BINARY_DATA_TTL=60
  - N8N_EXECUTION_DATA_SAVE_ON_ERROR=none
  - N8N_EXECUTION_DATA_SAVE_ON_SUCCESS=none
```

## 🔄 Backup Strategy

- **Automated**: Daily backups at 2 AM
- **Retention**: 7 days local, 30 days remote
- **Components**: Workflows, credentials, database
- **Compression**: gzip for space efficiency
- **Verification**: Automated backup testing

## 📞 Support

For technical support:
- Check logs: `docker-compose logs`
- Monitor resources: `./monitor.sh`
- Backup data: `./backup.sh`
- Restart services: `docker-compose restart`

---

**الخيمة Beach Resort** - Professional Automation Platform 🏖️
