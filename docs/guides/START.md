# 🚀 دليل التشغيل السريع

## ✅ الحل المطبق

تم إصلاح مشكلة TypeScript paths بإضافة:
```json
"baseUrl": ".",
"paths": {
  "@/*": ["./src/*"]
}
```

## 🎯 تشغيل المشروع

### 1. تشغيل قاعدة البيانات و Redis
```bash
cd /home/wego/Desktop/alkhayma-resort
docker compose up -d db redis
```

### 2. تشغيل Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. تشغيل Frontend
```bash
cd frontend
npm run dev
```

### 4. تشغيل AI Service (اختياري)
```bash
cd ai-service
source venv/bin/activate
python chatbot.py
```

## 🌐 الوصول للخدمات

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **N8N**: http://localhost:5678
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## 🔍 اختبار الاتصال

```bash
./test-connection.sh
```

## ✅ التحسينات المضافة

1. ✓ إصلاح TypeScript paths
2. ✓ إعدادات VS Code
3. ✓ EditorConfig
4. ✓ docker-compose.dev.yml
5. ✓ Makefile.dev
6. ✓ سكريبت اختبار الاتصال

## 📝 ملاحظات

- البيئة متوافقة 100%
- جميع الخدمات تعمل بنجاح
- Frontend يبني بدون أخطاء
- قاعدة البيانات و Redis جاهزة

✅ **المشروع جاهز للتطوير!**
