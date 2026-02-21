# دليل بيئة التطوير

## البيئة الحالية
- Ubuntu 24.04 LTS
- Python 3.12.3
- Node.js v20.20.0
- Docker 29.2.1
- Docker Compose v5.0.2

## التحسينات المضافة

### 1. ملفات الإعدادات
- `.editorconfig` - توحيد إعدادات المحرر
- `.vscode/settings.json` - إعدادات VS Code
- `docker-compose.dev.yml` - بيئة تطوير محسنة
- `Makefile.dev` - أوامر مختصرة

### 2. أدوات التطوير
- PgAdmin على المنفذ 5050
- Hot reload للـ Backend و Frontend
- Volume mounting للتطوير السريع

## الاستخدام

### بدء التطوير
```bash
make -f Makefile.dev dev-up
```

### إيقاف التطوير
```bash
make -f Makefile.dev dev-down
```

### عرض اللوجات
```bash
make -f Makefile.dev dev-logs
```

### تنظيف الملفات المؤقتة
```bash
make -f Makefile.dev clean
```

## الوصول للخدمات
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PgAdmin: http://localhost:5050
  - Email: admin@resort.local
  - Password: admin123
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## التوصيات
1. استخدم VS Code مع الإضافات الموصى بها
2. فعّل auto-format on save
3. استخدم Python virtual environment للتطوير المحلي
4. راجع `.env.example` وأنشئ `.env` الخاص بك

## الخطوات التالية
1. تحديث ملف `.env`
2. تشغيل `make -f Makefile.dev dev-up`
3. تطبيق migrations: `cd backend && alembic upgrade head`
4. البدء في التطوير!
