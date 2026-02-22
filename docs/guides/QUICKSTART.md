# 🚀 الخيمة Beach Resort - Quick Start Guide

## For New Developers

### 1. One-Command Setup
```bash
# Clone and setup everything
git clone <repository-url>
cd resort-platform
make setup
```

### 2. Start Development Environment
```bash
# Option 1: Using start script (recommended)
./start.sh

# Option 2: Using Makefile
make dev

# Option 3: Using Docker Compose
docker-compose up --build
```

### 3. Access Services
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **AI Chatbot**: http://localhost:8001
- **API Documentation**: http://localhost:8000/docs
- **N8N Workflows**: http://localhost:5678

### 4. Stop Services
```bash
./stop.sh
# or
make clean
```

## Project Status Overview

### ✅ Completed (Production Ready)
- **AI Chatbot Service** - FastAPI + LangChain + GPT
- **N8N Automation Workflows** - 4 complete workflows
- **Database Models** - 10 SQLAlchemy models
- **Integration Tests** - 6/6 tests passing
- **Production Infrastructure** - Docker + Nginx + SSL

### 🔄 In Progress
- **Backend API Endpoints** - Need real implementations
- **Frontend Pages** - Vue 3 components
- **Payment Integration** - Paymob + Stripe

### 📋 Next Steps
1. Complete backend API implementations
2. Build frontend booking flow
3. Test payment integrations
4. Deploy to production

## Quick Commands

```bash
# Development
make dev          # Start all services
make test         # Run all tests
make logs         # View service logs

# Database
make db-migrate   # Run migrations
make db-seed      # Seed test data

# Production
make deploy       # Deploy to production
make health       # Check system health
```

## Environment Setup

1. Copy environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your configuration:
   - Database credentials
   - OpenAI API key
   - Payment gateway keys
   - Email/WhatsApp credentials

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   AI Service   │
│   Vue 3 + TS    │◄──►│  FastAPI + SQL  │◄──►│ LangChain + GPT │
│   Port: 5173    │    │   Port: 8000    │    │   Port: 8001    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    │   + Redis       │
                    │   + N8N         │
                    └─────────────────┘
```

## Need Help?

- Check `CONTRIBUTING.md` for detailed guidelines
- Review `README.md` for comprehensive documentation
- Run `./health-check.sh` for system diagnostics
- Check logs: `tail -f *.log`

---

**Ready to contribute? Start with `./start.sh` and happy coding! 🏖️**
