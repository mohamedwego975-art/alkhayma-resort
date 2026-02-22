# 🏖️ الخيمة Beach Resort - Complete Booking System

Full-stack resort booking platform with AI chatbot and automation workflows.

## 🏗️ Architecture

```
alkhayma-resort/
├── backend/           # FastAPI + SQLAlchemy + PostgreSQL
│   ├── app/
│   │   ├── api/           # API endpoints (consolidated in endpoints/)
│   │   ├── core/          # Database, config, security, deps
│   │   ├── models/        # SQLAlchemy models
│   │   ├── repositories/  # Data access layer
│   │   ├── schemas/       # Pydantic schemas
│   │   └── services/      # Business logic
│   └── alembic/         # Database migrations
├── frontend/          # Vue 3 + TypeScript + Tailwind
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   ├── layouts/       # Layout components
│   │   ├── stores/        # Pinia stores
│   │   ├── api/           # API client
│   │   └── router/        # Vue Router config
│   └── public/          # Static assets
├── ai-service/        # LangChain + GPT Chatbot
├── n8n-workflows/     # WhatsApp + Email Automation
├── n8n-setup/         # Professional N8N Docker Setup
├── docs/              # Documentation
│   ├── INDEX.md         # فهرس التوثيق (ابدأ هنا)
│   ├── architecture.md, deployment.md, maintenance.md, requirements.md
│   ├── api/             # مراجع الـ API
│   ├── guides/          # أدلة البدء والإعداد
│   ├── backend/, frontend/, database/
│   └── archive/        # توثيق مراحل المشروع (أرشفة)
├── backend/scripts/   # سكربتات تشغيلية (seed, reset_admin)
├── monitoring/        # Prometheus + Grafana
└── nginx/             # Production Nginx Config
```

## 🚀 Quick Start

### Development
```bash
# 1. Start infrastructure
cd n8n-setup && ./setup.sh

# 2. Start backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# 3. Start AI service
cd ai-service && source venv/bin/activate && python chatbot.py

# 4. Start frontend
cd frontend && npm run dev
```

### Production
```bash
# Configure environment
cp .env.prod .env
# Edit .env with production values

# Deploy
./deploy.sh
```

## 📚 Documentation

- **[📑 فهرس التوثيق الكامل](docs/INDEX.md)** — ابدأ من هنا (عربي)
- [Guides & Quick Starts](docs/guides/)
- [Architecture](docs/architecture.md) · [Deployment](docs/deployment.md) · [Maintenance](docs/maintenance.md)
- [Frontend](docs/frontend/) · [Backend](docs/backend/) · [Database](docs/database/)

## 📊 Current Status

### ✅ Completed Phases
- **Phase 1**: AI Chatbot Service (FastAPI on port 8001)
- **Phase 3**: N8N Automation Workflows (4 workflows + Docker setup)
- **Phase 4**: Integration Test Suite (6/6 tests passing)

### 🔄 In Progress
- **Phase 2**: Database Models & Migrations
- **Phase 4**: Frontend-Backend Integration
- **Phase 5**: Production Optimization

### 📋 TODO
- Complete all SQLAlchemy models
- Implement all API endpoints
- Build Vue 3 frontend pages
- Performance optimization
- Production deployment

## 🧪 Testing

```bash
# Backend tests
cd backend && pytest tests/ -v

# Frontend tests
cd frontend && npm run test

# Integration tests
cd backend && pytest tests/test_integration.py -v
```

## 📈 Monitoring

- **Backend**: http://localhost:8000/metrics
- **AI Service**: http://localhost:8001/health
- **N8N**: http://localhost:5678
- **Health Check**: ./health-check.sh

## 🔧 Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Redis, Alembic
- **Frontend**: Vue 3, TypeScript, Tailwind CSS, Pinia
- **AI**: LangChain, OpenAI GPT, Redis Memory
- **Automation**: N8N, Twilio, Gmail
- **Infrastructure**: Docker, Nginx, Prometheus
- **Payments**: Paymob, Stripe

## 📞 Support

For issues or questions, check the health-check.sh output and logs.
