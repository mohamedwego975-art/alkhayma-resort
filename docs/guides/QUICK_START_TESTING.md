# دليل اختبار الاتصال - Quick Start Guide

## 🚀 ابدأ الاختبار بسرعة

### المتطلبات

```bash
Node.js (v16+)
Python 3.9+
PostgreSQL 15+
Redis 7+
Docker (اختياري)
```

---

## 📦 التثبيت السريع

### 1. تشغيل الخدمات بـ Docker (الأسهل)

```bash
cd /home/wego/Desktop/alkhayma-resort

# تشغيل جميع الخدمات
docker-compose -f docker-compose.dev.yml up -d

# التحقق من الخدمات
docker-compose -f docker-compose.dev.yml ps
```

### 2. أو تشغيلها يدوياً

#### تشغيل الـ Backend

```bash
cd backend

# تثبيت المتطلبات
pip install -r requirements.txt

# تشغيل الخادم
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### تشغيل الـ Frontend

```bash
cd frontend

# تثبيت المتطلبات
npm install

# تشغيل الخادم
npm run dev
```

---

## ✅ اختبار الاتصال

### الخيار 1: استخدام Script التلقائي (موصى به)

```bash
cd /home/wego/Desktop/alkhayma-resort

# تشغيل اختبارات شاملة
bash test-database-connection.sh
```

**الإخراج المتوقع:**

```
✅ Backend is healthy
✅ Rooms endpoint working (3 rooms found)
✅ API client configured
✅ Proxy configured
✅ CORS configuration found
✅ Database configured
✅ Backend running on port 8000
✅ Frontend running on port 5173
✅ Valid JSON response
✅ All required fields present
✅ Fast response (14ms)
```

### الخيار 2: اختبارات يدوية بـ curl

#### 1. التحقق من صحة الخادم

```bash
curl http://localhost:8000/health
# الاستجابة المتوقعة: {"status":"healthy"}
```

#### 2. الحصول على جميع الغرف

```bash
curl http://localhost:8000/api/rooms | python3 -m json.tool

# الاستجابة المتوقعة: JSON مع 3 غرف
```

#### 3. الحصول على غرفة محددة

```bash
curl http://localhost:8000/api/rooms/1 | python3 -m json.tool

# الاستجابة المتوقعة: تفاصيل الغرفة رقم 1
```

#### 4. الحصول على الغرف المتاحة

```bash
curl "http://localhost:8000/api/rooms/available?check_in=2026-03-01&check_out=2026-03-05"

# الاستجابة المتوقعة: قائمة بالغرف المتاحة
```

### الخيار 3: استخدام Postman

#### الاستيراد

1. افتح Postman
2. اختر: File → Import
3. حدد: `postman-collection.json`
4. اضغط: Import

#### الاختبار

- جميع الـ endpoints موثقة وجاهزة
- انقر على أي endpoint واضغط Send
- لاحظ الاستجابة والوقت

---

## 🔗 الروابط المهمة

### الخوادم المحلية

| الخدمة       | الرابط                       | الوصف                 |
| ------------ | ---------------------------- | --------------------- |
| Frontend     | http://localhost:5173        | تطبيق Vue 3           |
| Backend API  | http://localhost:8000        | FastAPI Server        |
| API Docs     | http://localhost:8000/docs   | Swagger Documentation |
| Health Check | http://localhost:8000/health | حالة الخادم           |
| PgAdmin      | http://localhost:5050        | إدارة قاعدة البيانات  |

---

## 📊 فهم البيانات

### بنية البيانات

#### غرفة (Room)

```json
{
  "id": 1,
  "room_number": "101",
  "room_type": "standard",
  "status": "available",
  "price_per_night": 150.0,
  "capacity": 2,
  "description_en": "Comfortable standard room with sea view",
  "description_ar": null,
  "amenities": "{\"wifi\": true, \"tv\": true, \"ac\": true}",
  "is_active": true,
  "created_at": "2026-02-21T17:44:24.243101Z"
}
```

#### الحقول المتاحة

- `id`: معرّف فريد
- `room_number`: رقم الغرفة
- `room_type`: نوع الغرفة (standard, deluxe, suite)
- `price_per_night`: السعر الليلي
- `capacity`: عدد الضيوف
- `status`: حالة الغرفة (available, booked, maintenance)
- `amenities`: التسهيلات المتاحة

---

## 🔍 استكشاف الأخطاء

### المشكلة: Backend لا يستجيب

**الحل:**

```bash
# تحقق من العملية
lsof -i :8000

# إذا لم تظهر أي عملية، شغّل Backend
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### المشكلة: قاعدة البيانات غير متصلة

**الحل:**

```bash
# تحقق من PostgreSQL
docker ps | grep postgres

# أو ابدأ قاعدة البيانات
docker-compose -f docker-compose.dev.yml up db -d
```

### المشكلة: Frontend لا يتصل بـ Backend

**الحل:**

```bash
# تحقق من الـ Proxy في frontend/vite.config.ts
# تأكد من أن Target هو: http://localhost:8000

# أعد تشغيل Frontend
cd frontend
npm run dev
```

### المشكلة: CORS Error

**الحل:**

```python
# تحقق من CORS في backend/app/core/config.py
cors_origins: list[str] = [
    "http://localhost:3000",
    "http://localhost:5173"  # أضف اسم المضيف الخاص بك
]
```

---

## 📈 فحص الأداء

### أوقات الاستجابة المتوقعة

```
Health Check:           10-20ms ✅
Get All Rooms:          20-50ms ✅
Get Room by ID:         15-30ms ✅
Database Query:         5-15ms ✅
```

### قياس الأداء

```bash
# استخدم ab (Apache Bench)
ab -n 100 http://localhost:8000/api/rooms

# أو استخدم curl مع timing
curl -w "\nTime: %{time_total}s\n" http://localhost:8000/api/rooms
```

---

## 🔐 الأمان والمصادقة

### تعيين Bearer Token

```bash
# احصل على Token من endpoint تسجيل الدخول
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# الاستجابة:
# {"access_token": "eyJhbGciOiJIUzI1NiIs...", "token_type": "bearer"}

# استخدم Token في الطلبات الموثقة
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  http://localhost:8000/api/bookings/my-bookings
```

---

## 📝 نموذج اختبار شامل

### اختبار السيناريو الكامل

```bash
#!/bin/bash

echo "🚀 اختبار شامل للاتصال"
echo ""

# 1. التحقق من صحة الخادم
echo "1. Health Check..."
curl http://localhost:8000/health && echo ""

# 2. الحصول على الغرف
echo "2. Fetching Rooms..."
curl http://localhost:8000/api/rooms && echo ""

# 3. الحصول على غرفة محددة
echo "3. Get Room #1..."
curl http://localhost:8000/api/rooms/1 && echo ""

echo "✅ اختبار شامل مكتمل"
```

---

## 🎯 ملخص سريع

| المهمة         | الأمر                                            |
| -------------- | ------------------------------------------------ |
| تشغيل Docker   | `docker-compose -f docker-compose.dev.yml up -d` |
| اختبار الاتصال | `bash test-database-connection.sh`               |
| الفحص اليدوي   | `curl http://localhost:8000/health`              |
| عرض API Docs   | http://localhost:8000/docs                       |
| إدارة DB       | http://localhost:5050                            |

---

## 📚 الموارد الإضافية

### التقارير المتاحة

- `DATABASE_CONNECTION_AUDIT.md` - تقرير فحص شامل
- `DATABASE_IMPROVEMENTS.md` - توصيات التحسينات
- `DATABASE_AUDIT_SUMMARY.md` - ملخص النتائج

### الملفات الرئيسية

- `frontend/src/api/client.ts` - إعدادات API
- `backend/app/core/config.py` - إعدادات قاعدة البيانات
- `frontend/vite.config.ts` - إعدادات البروكسي

---

## ✅ Checklist الاستعداد

- [ ] تثبيت المتطلبات (Node, Python, Docker)
- [ ] تشغيل Docker Compose أو الخدمات اليدوية
- [ ] تشغيل اختبار الاتصال
- [ ] التحقق من جميع الخدمات
- [ ] فتح Frontend في المتصفح
- [ ] اختبار تحميل البيانات
- [ ] فحص الأداء
- [ ] استيراد Postman Collection (اختياري)

---

## 🎉 النتيجة النهائية

عند اكتمال جميع الخطوات بنجاح، بجب أن ترى:

```
✅ Backend Health: healthy
✅ Frontend: loading
✅ Database: connected
✅ API: responding
✅ Data: flowing correctly
```

**تهانينا! نظامك جاهز للاستخدام الفعلي! 🚀**

---

**للدعم والمساعدة: راجع التقارير المفصلة أعلاه**
