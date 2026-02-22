# 📋 دليل تنظيم وادارة مشروع الخيمة ريسورت

**آخر تحديث:** 22 فبراير 2026
**الحالة:** جاهز للإنتاج ✅

---

## 📦 احتياجات المشروع

### المتطلبات الأساسية

#### للتطوير (Development):

```
- Node.js 18+
- Python 3.10+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose
```

#### للإنتاج (Production):

```
- Ubuntu 20.04 LTS أو أحدث
- Docker & Docker Compose
- Nginx (للـ Reverse Proxy)
- SSL/TLS Certificate (Let's Encrypt)
- منظومة المراقبة (Prometheus + Grafana)
```

---

## 🗂️ هيكل المشروع المنظم

```
alkhayma-resort/
│
├── 📘 DOCUMENTATION
│   ├── README.md                          (نظرة عامة)
│   ├── SETUP.md                          (تعليمات التثبيت)
│   ├── ARCHITECTURE.md                   (البنية المعمارية)
│   ├── API_REFERENCE.md                  (مرجع الـ API)
│   ├── DEPLOYMENT.md                     (نشر الإنتاج)
│   ├── PHASE5_COMPLETE.md               (ملخص المرحلة 5)
│   ├── ADMIN_API_REFERENCE.md           (مرجع API الإدارة)
│   └── docs/                             (وثائق تفصيلية)
│       ├── backend/                      (وثائق الخادم)
│       ├── frontend/                     (وثائق الواجهة)
│       ├── database/                     (وثائق قاعدة البيانات)
│       └── guides/                       (أدلة سريعة)
│
├── 🔧 CONFIGURATION
│   ├── .env.example                      (مثال على المتغيرات)
│   ├── .env.dev                          (متغيرات التطوير)
│   ├── .env.prod                         (متغيرات الإنتاج)
│   ├── .editorconfig                     (إعدادات المحرر)
│   ├── .gitignore                        (ملفات Git المتجاهلة)
│   └── .vscode/                          (إعدادات VS Code)
│
├── 🏗️ INFRASTRUCTURE
│   ├── docker-compose.yml                (البيئة الأساسية)
│   ├── docker-compose.dev.yml            (بيئة التطوير)
│   ├── docker-compose.prod.yml           (بيئة الإنتاج)
│   ├── nginx/                            (إعدادات Nginx)
│   │   ├── conf.d/                       (ملفات الإعدادات)
│   │   └── ssl/                          (شهادات SSL)
│   ├── monitoring/                       (Prometheus + Grafana)
│   │   ├── docker-compose.yml
│   │   ├── prometheus.yml
│   │   └── grafana/
│   └── nginx.prod.conf                   (إعدادات الإنتاج)
│
├── ⚙️ BACKEND (FastAPI + PostgreSQL)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                       (نقطة الدخول)
│   │   ├── api/
│   │   │   ├── admin.py                  (نقاط نهاية الإدارة)
│   │   │   ├── analytics.py              (التحليلات)
│   │   │   └── endpoints/                (مجلد النقاط النهائية)
│   │   │       ├── auth.py               (المصادقة)
│   │   │       ├── bookings.py           (الحجوزات)
│   │   │       ├── rooms.py              (الغرف)
│   │   │       ├── products.py           (المنتجات)
│   │   │       └── ...
│   │   ├── core/
│   │   │   ├── config.py                 (الإعدادات)
│   │   │   ├── database.py               (الاتصال بقاعدة البيانات)
│   │   │   ├── security.py               (الحماية وتشفير كلمات المرور)
│   │   │   └── deps.py                   (التبعيات)
│   │   ├── models/                       (نماذج SQLAlchemy)
│   │   │   ├── user.py
│   │   │   ├── room.py
│   │   │   ├── booking.py
│   │   │   └── ...
│   │   ├── repositories/                 (طبقة الوصول للبيانات)
│   │   │   ├── base.py
│   │   │   ├── user.py
│   │   │   ├── room.py
│   │   │   └── ...
│   │   ├── schemas/                      (نماذج Pydantic)
│   │   │   ├── auth.py
│   │   │   ├── room.py
│   │   │   ├── booking.py
│   │   │   └── ...
│   │   └── services/                     (منطق الأعمال)
│   │       ├── email_service.py
│   │       ├── payment_service.py
│   │       └── ...
│   ├── alembic/                          (ترحيلات قاعدة البيانات)
│   ├── tests/                            (اختبارات الوحدة)
│   ├── requirements.txt                  (مكتبات Python)
│   ├── Dockerfile                        (صورة Docker)
│   └── README.md                         (توثيق الخادم)
│
├── 💻 FRONTEND (Vue 3 + TypeScript)
│   ├── src/
│   │   ├── main.ts                       (نقطة الدخول)
│   │   ├── App.vue                       (المكون الرئيسي)
│   │   ├── api/                          (عملاء الـ API)
│   │   │   ├── auth.ts
│   │   │   ├── rooms.ts
│   │   │   ├── bookings.ts
│   │   │   └── ...
│   │   ├── components/                   (مكونات قابلة لإعادة الاستخدام)
│   │   │   ├── common/
│   │   │   ├── forms/
│   │   │   └── ...
│   │   ├── pages/                        (صفحات التطبيق)
│   │   │   ├── HomePage.vue
│   │   │   ├── BookingPage.vue
│   │   │   ├── admin/                    (صفحات الإدارة)
│   │   │   │   ├── DashboardOverview.vue
│   │   │   │   ├── RoomsManagement.vue
│   │   │   │   ├── UsersManagement.vue
│   │   │   │   └── ...
│   │   │   └── ...
│   │   ├── layouts/                      (تخطيطات الصفحات)
│   │   ├── router/                       (جداول التوجيه)
│   │   ├── stores/                       (متاجر Pinia)
│   │   ├── i18n/                         (الترجمات)
│   │   │   └── locales/
│   │   │       ├── en.json              (الإنجليزية)
│   │   │       └── ar.json              (العربية)
│   │   └── styles/                       (الأنماط العامة)
│   ├── public/                           (الملفات الثابتة)
│   ├── package.json                      (مكتبات Node.js)
│   ├── tsconfig.json                     (إعدادات TypeScript)
│   ├── tailwind.config.ts                (إعدادات Tailwind CSS)
│   ├── vite.config.ts                    (إعدادات Vite)
│   ├── Dockerfile                        (صورة Docker)
│   └── README.md                         (توثيق الواجهة)
│
├── 🤖 AI SERVICE (LangChain Chatbot)
│   ├── chatbot.py                        (محرك الدردشة)
│   ├── sentiment.py                      (تحليل المشاعر)
│   ├── requirements.txt                  (مكتبات Python)
│   ├── Dockerfile
│   └── test_chatbot.py                   (اختبارات)
│
├── 🔧 N8N AUTOMATION
│   ├── n8n-setup/                        (إعداد N8N احترافي)
│   │   ├── setup.sh                      (سكريبت التثبيت)
│   │   ├── docker-compose.yml
│   │   ├── nginx.conf
│   │   └── ssl/                          (شهادات SSL)
│   └── n8n-workflows/                    (سير العمل)
│       ├── booking_confirmed.json        (تأكيد الحجز)
│       ├── check_in_reminder.json        (تذكير Check-in)
│       ├── marketing_weekly.json         (البريد التسويقي)
│       └── post_stay_review.json         (طلب التقييم)
│
├── 📊 MONITORING
│   ├── docker-compose.yml                (Prometheus + Grafana)
│   ├── prometheus.yml                    (إعدادات المراقبة)
│   └── grafana/                          (لوحات التحكم)
│
├── 🧪 TESTING & SCRIPTS
│   ├── tests/
│   │   ├── test_api.py                   (اختبارات الـ API)
│   │   ├── test_integration.py           (اختبارات التكامل)
│   │   └── ...
│   ├── scripts/
│   │   ├── start-dev.sh                  (بدء التطوير)
│   │   ├── health-check.sh               (فحص الصحة)
│   │   └── ...
│   └── Makefile                          (أوامر التطوير)
│
└── 📄 ROOT FILES
    ├── start.sh / start-all.sh          (سكريبتات البدء)
    ├── stop.sh                          (إيقاف الخدمات)
    ├── deploy.sh                        (نشر الإنتاج)
    ├── docker-compose.yml               (التكوين الأساسي)
    └── .env.example                     (مثال الإعدادات)
```

---

## 🚀 كيفية التشغيل

### 1️⃣ بيئة التطوير (Development)

#### الخطوة 1: إعداد المتغيرات البيئية

```bash
cp .env.example .env.dev
# عدّل المتغيرات حسب احتياجك
nano .env.dev
```

#### الخطوة 2: بدء الخدمات الأساسية

```bash
cd n8n-setup
./setup.sh
```

أو باستخدام Docker:

```bash
docker-compose -f docker-compose.dev.yml up -d db redis
```

#### الخطوة 3: إعداد الخادم (Backend)

```bash
cd backend
python -m venv venv
source venv/bin/activate  (على Linux/Mac)
# أو: venv\Scripts\activate (على Windows)

pip install -r requirements.txt
# تشغيل الترحيلات
alembic upgrade head

# بدء الخادم
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**الخادم سيكون متاحاً على:** `http://localhost:8000`
**توثيق API:** `http://localhost:8000/docs`

#### الخطوة 4: بدء خدمة الذكاء الاصطناعي

```bash
cd ai-service
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python chatbot.py
```

#### الخطوة 5: بدء الواجهة الأمامية

```bash
cd frontend
npm install
npm run dev
```

**الواجهة ستكون متاحة على:** `http://localhost:5173`

#### الخطوة 6 (اختيارية): بدء خدمة المراقبة

```bash
cd monitoring
docker-compose up -d
```

**المراقبة:**

- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

---

### 2️⃣ بيئة الإنتاج (Production)

#### الخطوة 1: إعداد الملقم (Server)

```bash
# على Ubuntu 20.04+
sudo apt update
sudo apt install docker.io docker-compose git nginx certbot python3-certbot-nginx

# أضف المستخدم الحالي إلى مجموعة docker
sudo usermod -aG docker $USER
newgrp docker
```

#### الخطوة 2: استنساخ المشروع

```bash
git clone https://github.com/yourusername/alkhayma-resort.git
cd alkhayma-resort
```

#### الخطوة 3: إعداد شهادة SSL

```bash
sudo certbot certonly --standalone -d yourdomain.com
```

#### الخطوة 4: تجهيز ملف البيئة

```bash
cp .env.example .env.prod
# عدّل القيم الحساسة
nano .env.prod
```

#### الخطوة 5: النشر

```bash
# باستخدام سكريبت النشر
./deploy.sh

# أو يدويًا:
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

#### الخطوة 6: التحقق من الصحة

```bash
curl http://localhost:8000/api/health
```

---

## 🔧 إدارة المشروع

### أوامر مفيدة

#### استخدام Make (الطريقة الموصى بها)

```bash
# عرض جميع الأوامر المتاحة
make help

# بدء البيئة الكاملة
make dev-start

# إيقاف البيئة
make dev-stop

# إعادة تشغيل البيئة
make dev-restart

# عرض السجلات
make dev-logs

# تشغيل الاختبارات
make test

# تنسيق الكود
make format

# فحص جودة الكود
make lint
```

#### Docker Compose مباشرة

```bash
# بدء الخدمات
docker-compose -f docker-compose.dev.yml up -d

# إيقاف الخدمات
docker-compose -f docker-compose.dev.yml down

# عرض السجلات
docker-compose -f docker-compose.dev.yml logs -f backend

# إعادة بناء الصور
docker-compose -f docker-compose.dev.yml build --no-cache
```

---

## 📊 المنافذ والخدمات

### بيئة التطوير:

```
Frontend:           http://localhost:5173
Backend API:        http://localhost:8000
PostgreSQL:         localhost:5432
Redis:              localhost:6379
Prometheus:         http://localhost:9090
Grafana:            http://localhost:3000
N8N:                http://localhost:5678
```

### بيئة الإنتاج:

```
Frontend:           https://yourdomain.com
Backend API:        https://yourdomain.com/api
PostgreSQL:         localhost:5432 (داخلي فقط)
Redis:              localhost:6379 (داخلي فقط)
```

---

## 🗃️ إدارة قاعدة البيانات

### إنشاء ترحيل جديد

```bash
cd backend
alembic revision --autogenerate -m "اسم الترحيل"
alembic upgrade head
```

### استرجاع البيانات

```bash
docker-compose -f docker-compose.dev.yml exec db pg_dump -U postgres alkhayma > backup.sql
```

### استعادة البيانات

```bash
cat backup.sql | docker-compose -f docker-compose.dev.yml exec -T db psql -U postgres alkhayma
```

---

## 🔐 إدارة المصادقة والأمان

### متغيرات الأمان المهمة:

```bash
# في .env
DATABASE_URL=postgresql://user:password@localhost/alkhayma
JWT_SECRET_KEY=your-secure-random-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# فتح مفتاح سري جديد (على Linux):
openssl rand -hex 32
```

### إعادة تعيين كلمة المرور

```bash
cd backend
# تشغيل سكريبت إعادة التعيين
python reset_admin.py
```

---

## 📈 المراقبة والسجلات

### عرض السجلات:

```bash
# جميع السجلات
docker-compose logs -f

# سجلات الخادم فقط
docker-compose logs -f backend

# عدد معين من الأسطر
docker-compose logs --tail=50 backend
```

### قاعدة البيانات:

```bash
# الدخول إلى PostgreSQL
docker-compose exec db psql -U postgres -d alkhayma

# الأوامر المفيدة:
\dt                 -- عرض الجداول
\d table_name       -- وصف الجدول
SELECT * FROM table_name LIMIT 10;
\q                  -- الخروج
```

### Redis:

```bash
# الدخول إلى Redis
docker-compose exec redis redis-cli

# الأوامر المفيدة:
KEYS *              -- عرض جميع المفاتيح
GET key_name        -- قراءة قيمة
FLUSHDB             -- حذف جميع المفاتيح
EXIT                -- الخروج
```

---

## 🧪 الاختبار

### اختبارات الوحدة (Backend):

```bash
cd backend
pytest tests/ -v
pytest tests/test_auth.py -v  # اختبار محدد
```

### اختبارات التكامل:

```bash
cd backend
pytest tests/test_integration.py -v
```

### اختبار الـ API يدويًا:

```bash
# تسجيل الدخول
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "password"}'

# الحصول على جميع الغرف
curl -X GET http://localhost:8000/api/rooms
```

---

## 🔄 سير العمل اليومي

### الصباح:

```bash
# بدء جميع الخدمات
make dev-start

# أو:
./start-all.sh
```

### أثناء العمل:

```bash
# فحص الصحة
./health-check.sh

# عرض السجلات إذا حدثت مشاكل
docker-compose logs -f backend
```

### نهاية اليوم:

```bash
# إيقاف الخدمات
make dev-stop

# أو:
./stop.sh
```

---

## 📋 قائمة الاختبارات قبل النشر

- [ ] جميع الاختبارات تمر بنجاح
- [ ] لا توجد أخطاء TypeScript
- [ ] الـ Frontend بناء بنجاح
- [ ] الـ Backend متاح على `http://localhost:8000/api/health`
- [ ] قاعدة البيانات متصلة
- [ ] جميع البيانات الأساسية موجودة
- [ ] SSL/TLS محدث
- [ ] متغيرات البيئة مضبوطة بشكل صحيح

---

## 🆘 استكشاف الأخطاء

### مشكلة: البوابة مأخوذة (Port already in use)

```bash
# لينكس/ماك:
lsof -i :8000
kill -9 <PID>

# أو تغيير البوابة في .env
PORT=8001
```

### مشكلة: قاعدة البيانات لا تتصل

```bash
# التحقق من حالة PostgreSQL
docker-compose ps db

# إعادة تشغيل قاعدة البيانات
docker-compose restart db

# مسح البيانات وإعادة الإنشاء
docker-compose down -v
docker-compose up -d db
```

### مشكلة: الذاكرة الكاملة

```bash
# تنظيف Docker
docker system prune -a

# حذف البيانات غير المستخدمة
docker volume prune
```

---

## 📞 معلومات التواصل والدعم

- **المستودع:** https://github.com/yourusername/alkhayma-resort
- **توثيق الـ API:** `http://localhost:8000/docs`
- **توثيق الإدارة:** `ADMIN_API_REFERENCE.md`

---

## 📄 ملفات إضافية مهمة

- `PHASE5_COMPLETE.md` - ملخص المرحلة الخامسة (Dashboard + Admin)
- `ADMIN_API_REFERENCE.md` - مرجع API الإدارة مع أمثلة cURL
- `API_REFERENCE.md` - مرجع API الكامل (تحت الإنشاء)

---

**تم الإنشاء:** 22 فبراير 2026
**الإصدار:** 1.0.0
**الحالة:** جاهز للإنتاج ✅
