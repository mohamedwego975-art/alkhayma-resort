# Contributing to الخيمة Beach Resort

Thank you for your interest in contributing to الخيمة Beach Resort booking system!

## 🚀 Quick Start

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd resort-platform
   make setup
   ```

2. **Start Development**
   ```bash
   ./start.sh
   # or
   make dev
   ```

## 📁 Project Structure

```
resort-platform/
├── backend/           # FastAPI + SQLAlchemy
│   ├── app/
│   │   ├── api/       # API routes
│   │   ├── models/    # Database models
│   │   ├── core/      # Core configuration
│   │   └── main.py    # FastAPI app
│   ├── tests/         # Backend tests
│   └── alembic/       # Database migrations
├── frontend/          # Vue 3 + TypeScript
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── stores/    # Pinia stores
│   │   └── api/       # API client
│   └── tests/         # Frontend tests
├── ai-service/        # LangChain chatbot
├── n8n-workflows/     # Automation workflows
└── monitoring/        # Prometheus + Grafana
```

## 🛠️ Development Guidelines

### Code Style

**Backend (Python)**
- Follow PEP 8
- Use type hints
- Write docstrings for functions
- Use async/await for database operations

**Frontend (TypeScript/Vue)**
- Use TypeScript strict mode
- Follow Vue 3 Composition API
- Use Tailwind CSS for styling
- Write unit tests for components

### Database Changes

1. Create migration:
   ```bash
   cd backend
   alembic revision --autogenerate -m "Description"
   ```

2. Apply migration:
   ```bash
   alembic upgrade head
   ```

### Testing

**Backend Tests**
```bash
cd backend
pytest tests/ -v
```

**Frontend Tests**
```bash
cd frontend
npm run test
```

**Integration Tests**
```bash
cd backend
pytest tests/test_integration.py -v
```

## 🔄 Git Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code
   - Add tests
   - Update documentation

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new booking feature"
   ```

4. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format

Use conventional commits:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

## 🌐 Internationalization (i18n)

All user-facing text must support Arabic and English:

**Backend**
```python
# Use language parameter in responses
def get_message(key: str, lang: str = "en") -> str:
    messages = {
        "en": {"welcome": "Welcome"},
        "ar": {"welcome": "أهلاً وسهلاً"}
    }
    return messages.get(lang, {}).get(key, key)
```

**Frontend**
```typescript
// Use i18n composable
const { t } = useI18n()
const message = t('welcome')
```

## 🐛 Bug Reports

When reporting bugs, include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details
- Screenshots if applicable

## 💡 Feature Requests

For new features:
- Describe the use case
- Explain the expected behavior
- Consider implementation complexity
- Check if it aligns with project goals

## 📋 Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] i18n support added
- [ ] No breaking changes (or documented)
- [ ] Commit messages follow convention

## 🔒 Security

- Never commit sensitive data (API keys, passwords)
- Use environment variables for configuration
- Follow security best practices
- Report security issues privately

## 📞 Getting Help

- Check existing issues and documentation
- Ask questions in discussions
- Join our development chat
- Review code examples in the codebase

## 🎯 Development Phases

The project follows a structured development approach:

1. **Phase 1**: AI Chatbot Service ✅
2. **Phase 2**: Database & Backend APIs 🔄
3. **Phase 3**: N8N Automation Workflows ✅
4. **Phase 4**: Frontend Development 🔄
5. **Phase 5**: Production Deployment ✅

Focus contributions on the current active phase for maximum impact.

---

Thank you for contributing to الخيمة Beach Resort! 🏖️
