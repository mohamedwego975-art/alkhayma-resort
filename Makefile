.PHONY: help dev build test clean deploy health

# Default target
help:
	@echo "🏖️  الخيمة Beach Resort - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  make dev      - Start development environment"
	@echo "  make build    - Build all services"
	@echo "  make test     - Run all tests"
	@echo ""
	@echo "Production:"
	@echo "  make deploy   - Deploy to production"
	@echo "  make health   - Check system health"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean    - Clean up containers and volumes"
	@echo "  make logs     - Show service logs"

# Development environment
dev:
	@echo "🚀 Starting development environment..."
	docker-compose up --build -d
	@echo "✅ Services started:"
	@echo "   Backend:    http://localhost:8000"
	@echo "   AI Service: http://localhost:8001"
	@echo "   Frontend:   http://localhost:5173"
	@echo "   Database:   localhost:5432"
	@echo "   Redis:      localhost:6379"

# Build all services
build:
	@echo "🔨 Building all services..."
	docker-compose build --no-cache

# Run tests
test:
	@echo "🧪 Running tests..."
	cd backend && source venv/bin/activate && pytest tests/ -v
	cd frontend && npm run test

# Production deployment
deploy:
	@echo "🚀 Deploying to production..."
	./deploy.sh

# Health check
health:
	@echo "🏥 Checking system health..."
	./health-check.sh

# Show logs
logs:
	docker-compose logs -f --tail=100

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	docker-compose down -v
	docker system prune -f
	@echo "✅ Cleanup complete"

# Database operations
db-migrate:
	@echo "📊 Running database migrations..."
	cd backend && source venv/bin/activate && alembic upgrade head

db-seed:
	@echo "🌱 Seeding database..."
	cd backend && source venv/bin/activate && python seed_data.py

# Quick setup for new developers
setup:
	@echo "⚡ Setting up development environment..."
	cp .env.example .env
	cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
	cd ai-service && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
	cd frontend && npm install
	@echo "✅ Setup complete! Run 'make dev' to start."
