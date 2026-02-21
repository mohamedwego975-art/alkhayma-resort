# 🚀 Quick Start Guide - الخيمة Beach Resort

## Prerequisites

- Python 3.12+ with venv
- Node.js 18+ with npm
- PostgreSQL 14+
- Git

---

## 🏃 Quick Start (3 Commands)

```bash
# 1. Start Backend
./start-backend.sh

# 2. Start Frontend (in new terminal)
./start-frontend.sh

# 3. Run Tests (in new terminal)
./test_integration.sh
```

---

## 📋 Detailed Setup

### 1. Database Setup

Database is already configured and seeded with:
- ✅ 6 rooms (standard, deluxe, suite)
- ✅ 6 products (beach access, water activities)
- ✅ 3 users (admin, staff, guest)

**Test credentials:**
- Admin: `admin@alkhayma.com` / `password123`
- Staff: `staff@alkhayma.com` / `password123`
- Guest: `guest@test.com` / `password123`

### 2. Backend Setup

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Or use the script:**
```bash
./start-backend.sh
```

**Verify:**
```bash
curl http://localhost:8000/health
```

### 3. Frontend Setup

```bash
cd frontend
npm run dev
```

**Or use the script:**
```bash
./start-frontend.sh
```

**Access:** http://localhost:5173

---

## 🧪 Testing

### Run All Tests
```bash
./test_integration.sh
```

### Individual Tests

**Database Logic:**
```bash
cd backend
source venv/bin/activate
cd ..
python test_api.py
```

**HTTP Endpoints:**
```bash
./test_endpoints.sh
```

**Manual API Tests:**
```bash
# Get rooms
curl http://localhost:8000/api/products?type=room | jq

# Get beach products
curl http://localhost:8000/api/products?type=beach | jq

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@alkhayma.com","password":"password123"}' | jq
```

---

## 📁 Project Structure

```
alkhayma-resort/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Config, database
│   │   ├── models/      # SQLAlchemy models
│   │   └── repositories/
│   ├── venv/            # Python virtual environment
│   └── seed_production.py
├── frontend/            # Vue 3 frontend
│   ├── src/
│   │   ├── api/        # API client
│   │   ├── components/ # Vue components
│   │   ├── pages/      # Page components
│   │   ├── stores/     # Pinia stores
│   │   └── i18n/       # Translations (AR/EN)
│   └── package.json
├── start-backend.sh     # Backend startup script
├── start-frontend.sh    # Frontend startup script
├── start-all.sh         # Start all services
├── test_api.py          # Database logic tests
├── test_endpoints.sh    # HTTP endpoint tests
└── test_integration.sh  # Full integration tests
```

---

## 🌐 URLs

| Service  | URL                      | Description           |
|----------|--------------------------|----------------------|
| Frontend | http://localhost:5173    | Vue 3 application    |
| Backend  | http://localhost:8000    | FastAPI server       |
| API Docs | http://localhost:8000/docs | Swagger UI         |
| Health   | http://localhost:8000/health | Health check     |

---

## 🔧 Common Commands

### Backend

```bash
# Activate venv
cd backend && source venv/bin/activate

# Run migrations
alembic upgrade head

# Seed database
python seed_production.py

# Start server
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Type check
npm run type-check
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill process if needed
kill -9 <PID>
```

### Frontend won't start
```bash
# Check if port 5173 is in use
lsof -i :5173

# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Database connection error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -U postgres -d alkhayma_resort
```

### Pinia error
Already fixed in commit `25b9373b`. If you see it:
```bash
cd frontend
git pull
npm install
```

---

## 📊 Current Status

### Phase 5: Data Population & Integration Testing

- ✅ Step 1: Database Seeding (Completed)
- ✅ Step 2: API Integration Testing (Completed)
- 🔄 Step 3: Full Stack Integration (In Progress)

### What's Working

- ✅ Backend API (all endpoints)
- ✅ Database (PostgreSQL with sample data)
- ✅ Frontend (Vue 3 + TypeScript)
- ✅ Authentication (JWT)
- ✅ i18n (Arabic/English)

### What Needs Testing

- ⏳ Frontend-Backend data flow
- ⏳ Booking widget functionality
- ⏳ User authentication flow
- ⏳ Error handling
- ⏳ Mobile responsiveness

---

## 📞 Support

For issues or questions, check:
- `PHASE5_STEP2_COMPLETED.md` - API testing documentation
- `DATABASE_STATUS.md` - Database schema and status
- `FRONTEND_REVIEW.md` - Frontend architecture

---

## 🎯 Next Steps

1. Start both services
2. Run integration tests
3. Test in browser
4. Fix any issues found
5. Proceed to Phase 6 (AI Integration)
