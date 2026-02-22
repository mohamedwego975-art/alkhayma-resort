# 🚀 دليل البدء السريع للمطورين الجدد

**آخر تحديث:** 22 فبراير 2026
**الإصدار:** 1.0.0

---

## ⚡ البدء في أقل من 10 دقائق

### متطلبات مسبقة (5 دقائق)

```bash
# تأكد من تثبيت المتطلبات:
node --version        # v18+ مطلوب
python3 --version     # 3.10+ مطلوب
git --version         # أي إصدار
docker --version      # اختياري
```

### ليس لديك المتطلبات؟

انظر [PROJECT_SETUP.md](PROJECT_SETUP.md#-البرامج-والأدوات-المطلوبة) للتثبيت

---

## 1️⃣ استنساخ المشروع (دقيقة واحدة)

```bash
# انسخ في المجلد المطلوب
git clone https://github.com/yourname/alkhayma-resort.git
cd alkhayma-resort

# تحديث الكود (إذا كنت عضوًا في الفريق)
git pull origin main
```

---

## 2️⃣ إعداد البيئة (دقيقة واحدة)

```bash
# إنشاء ملف البيئة من النموذج
cp .env.example .env

# يمكنك الاستخدام كما هو أو تعديل المقيم التالية:
# DATABASE_URL           - قاعدة البيانات (افتراضي صحيح)
# JWT_SECRET_KEY         - مفتاح سري آمن
# API ports and URLs     - المنافذ والعناوين
```

---

## 3️⃣ تشغيل الخدمات (دقيقتان)

### الخيار أ: Using Docker (الأسهل)

```bash
# بدء جميع الخدمات
docker-compose up -d

# الانتظار 30 ثانية للبدء
sleep 30

# التحقق من الحالة
docker-compose ps
```

### الخيار ب: Manual Setup (التحكم الكامل)

```bash
# Terminal 1: PostgreSQL
sudo systemctl start postgresql
# أو إذا كنت على macOS: brew services start postgresql

# Terminal 2: Redis
redis-server
# أو على macOS: brew services start redis

# Terminal 3: Backend
cd backend
python3 -m venv venv
source venv/bin/activate  # على Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 4: Frontend
cd frontend
npm install
npm run dev
```

---

## 4️⃣ فتح التطبيق (دقيقة واحدة)

```
🌐 الواجهة الأمامية:    http://localhost:5173
📚 مستندات API:         http://localhost:8000/docs
🛠️ Admin Tools:         http://localhost:8000/admin
```

### حسابات الاختبار

```
البريد:     admin@example.com
كلمة المرور: password123

الدور:      Admin (صلاحيات كاملة)
```

---

## 🎯 أول صفحات للاستكشاف

### 1. الصفحة الرئيسية

```
http://localhost:5173/
```

- تخطيض عام للموقع
- زر الدخول والتسجيل

### 2. لوحة التحكم

```
http://localhost:5173/admin/dashboard
```

- إحصائيات الحجوزات
- الإيرادات
- معدل الإشغال

### 3. إدارة الغرف

```
http://localhost:5173/admin/rooms
```

- قائمة جميع الغرف
- إضافة/تعديل/حذف الغرف

### 4. إدارة الحجوزات

```
http://localhost:5173/admin/bookings
```

- قائمة جميع الحجوزات
- تحديث حالة الحجز

### 5. مرجع API

```
http://localhost:8000/docs
```

- تفاعلي مع جميع النقاط الطرفية
- اختبر الطلبات مباشرة

---

## 🔧 المهام الشائعة

### إضافة ميزة جديدة

```bash
# 1. إنشاء فرع جديد
git checkout -b feature/my-new-feature

# 2. قم بالتطوير
# (عدل الملفات حسب الحاجة)

# 3. اختبر التغييرات
npm run dev      # Frontend
pytest           # Backend

# 4. قم بـ Commit
git add .
git commit -m "feat: إضافة ميزة جديدة"

# 5. ادفع للفرع
git push origin feature/my-new-feature

# 6. أنشئ Pull Request على GitHub
```

### تشغيل الاختبارات

```bash
# اختبارات Frontend
cd frontend
npm test

# اختبارات Backend
cd backend
pytest -v

# اختبارات التكامل
pytest tests/integration/

# اختبارات الأداء
pytest -m performance
```

### عرض السجلات

```bash
# Backend logs
docker logs alkhayma-backend -f

# Frontend logs
# (تحقق من console في المتصفح - F12)

# Database logs
sudo tail -f /var/log/postgresql.log
```

### إعادة تعيين قاعدة البيانات

```bash
# حذف جميع البيانات وإعادة الإنشاء
cd backend
python
>>> from app.main import init_db
>>> init_db()

# أو باستخدام Docker
docker-compose exec postgres psql -U postgres -d alkhayma -f /backups/init_db.sql
```

---

## 📁 بنية المجلدات الرئيسية

### Frontend

```
frontend/src/
├── api/                    # طبقة التكامل API
│   ├── auth.ts            # مصادقة
│   ├── rooms.ts           # الغرف
│   ├── bookings.ts        # الحجوزات
│   └── ...
├── pages/                 # الصفحات
│   ├── admin/             # صفحات المسؤول
│   ├── user/              # صفحات المستخدم
│   └── public/            # صفحات عامة
├── components/            # مكونات Vue
├── stores/                # Pinia stores (الحالة)
├── i18n/                  # التعريب (AR/EN)
└── App.vue                # المكون الرئيسي
```

### Backend

```
backend/app/
├── main.py                # نقطة الدخول
├── api/endpoints/         # النقاط الطرفية
│   ├── auth.py
│   ├── rooms.py
│   └── ...
├── models/                # نماذج قاعدة البيانات
├── schemas/               # Pydantic schemas
├── services/              # منطق الأعمال
├── core/                  # الإعدادات
└── utils/                 # أدوات مساعدة
```

---

## 🔐 كيفية الوصول الآمن

### توليد مفتاح سري جديد

```python
import secrets
import string

# للتطوير
dev_key = secrets.token_urlsafe(32)
print(f"JWT_SECRET_KEY={dev_key}")

# للإنتاج (استخدم طولًا أطول)
prod_key = secrets.token_urlsafe(64)
print(f"JWT_SECRET_KEY={prod_key}")
```

### اختبار المصادقة

```bash
# 1. الحصول على رمز
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password123"}'

# 2. استخدام الرمز
curl http://localhost:8000/api/users/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📊 مراقبة الأداء

### على المتصفح (Chrome DevTools)

```
1. افتح DevTools (F12)
2. → Performance tab
3. → التقط الملف الشاخص
4. في الشريط الجانبي الأيسر:
   - Main thread
   - Frames
   - Screenshot
```

### على الخادم

```bash
# استهلاك الموارد
free -h                    # الذاكرة
df -h                      # مساحة القرص
top -b -n 1                # العمليات

# الشبكة
netstat -tuln              # الاتصالات
ss -s                      # إحصائيات المقابس
```

---

## 🆘 حل المشاكل الشائعة

### "لا يمكن الاتصال بـ PostgreSQL"

```bash
# تحقق من حالة الخدمة
sudo systemctl status postgresql

# أعد تشغيلها
sudo systemctl restart postgresql

# أو مع Docker
docker-compose restart postgres
sleep 5
```

### "المنفذ 5173 قيد الاستخدام"

```bash
# اعثر على العملية التي تستخدم المنفذ
lsof -i :5173

# اقتل العملية
kill -9 <PID>

# أو استخدم منفذ مختلف
npm run dev -- --port 5174
```

### "أخطاء في البناء (Build Errors)"

```bash
# سجل التخزين مؤقت
npm cache clean --force

# أعد التثبيت
rm -rf node_modules package-lock.json
npm install

# جرب البناء
npm run build
```

### "لا توجد رسائل على الواجهة الأمامية"

```bash
# امسح ذاكرة المتصفح المؤقتة
# DevTools في Chrome:
# 1. Applications → Storage
# 2. "Clear site data"

# أو في سطر الأوامر (إعادة تشغيل dev server)
^C  # اضغط Ctrl+C
npm run dev
```

---

## 📚 الموارد التعليمية

### للمبتدئين

- [Vue.js Guide](https://vuejs.org/guide/introduction.html)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [SQL Basics](https://www.w3schools.com/sql/)
- [REST APIs](https://www.restapitutorial.com/)

### للمتقدمين

- [Vue.js Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [FastAPI Advanced](https://fastapi.tiangolo.com/advanced/)
- [PostgreSQL Optimization](https://www.postgresql.org/docs/current/performance.html)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

## 📋 قائمة التحقق للمطورين الجدد

### اليوم الأول

- [ ] استنساخ المشروع
- [ ] إعداد البيئة الكاملة
- [ ] تشغيل جميع الخدمات
- [ ] فتح التطبيق والتحقق من عدم وجود أخطاء
- [ ] قراءة [ARCHITECTURE.md](ARCHITECTURE.md)

### الأسبوع الأول

- [ ] قراءة كود نموذجي في Frontend و Backend
- [ ] إضافة ميزة صغيرة (مثل عنصر واجهة)
- [ ] تشغيل الاختبارات الموجودة
- [ ] فهم دورة حياة الطلب
- [ ] التعرف على فريق التطوير

### الشهر الأول

- [ ] إكمال مهام متعددة
- [ ] فهم البنية المعمارية بالكامل
- [ ] المساهمة بميزة كاملة
- [ ] مراجعة كود من فريق آخر
- [ ] فهم نمط الأمان والاختبار

---

## 💬 الأسئلة الشائعة

### س: أين أجد توثيق API؟

**ج:** زيارة http://localhost:8000/docs أو اقرأ [ADMIN_API_REFERENCE.md](ADMIN_API_REFERENCE.md)

### س: كيف أضيف دعماً لغة جديدة؟

**ج:** اعتمد على [دليل التعريب](ARCHITECTURE.md#-التعريب-i18n)

### س: هل يمكنني تطوير بدون Docker؟

**ج:** نعم! اتبع [الخيار ب في القسم 3](#الخيار-ب-manual-setup-التحكم-الكامل)

### س: ما هي أفضل الممارسات للكود؟

**ج:** اقرأ `.eslintrc` و `black.toml` و `pyproject.toml`

### س: كيف أقوم بـ Deploy إلى الإنتاج؟

**ج:** اقرأ [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 🤝 المساهمة

### خطوات المساهمة

```bash
# 1. انتقل إلى الفرع الرئيسي
git checkout main

# 2. اسحب من الخادم البعيد
git pull origin main

# 3. أنشئ فرع نسختك
git checkout -b feature/your-feature

# 4. قم بالتغييرات والاختبارات
# ...

# 5. قم بـ Commit بماركان واضح
git commit -m "type: وصف موجز

تفاصيل أطول إذا لزم الأمر.
"

# 6. ادفع إلى الخادم البعيد
git push origin feature/your-feature

# 7. أنشئ Pull Request على GitHub
```

### قواعس الكود

- استخدم **TypeScript الصارم** في Frontend
- استخدم **Type hints** في Backend
- كتب **اختبارات** لكل ميزة جديدة
- اتبع **Naming conventions** (camelCase للـ JS، snake_case للـ Python)

---

## 📞 احصل على المساعدة

### قنوات الدعم

1. **Slack**: #alkhayma-dev
2. **Email**: devteam@alkhayma.com
3. **GitHub Issues**: github.com/yourname/alkhayma-resort/issues
4. **Team Wiki**: https://wiki.alkhayma.com

### الوثائق الأخرى المفيدة

- [PROJECT_SETUP.md](PROJECT_SETUP.md) - متطلبات التثبيت
- [ARCHITECTURE.md](ARCHITECTURE.md) - البنية الكاملة
- [DEPLOYMENT.md](DEPLOYMENT.md) - نشر الإنتاج
- [MAINTENANCE.md](MAINTENANCE.md) - الصيانة اليومية

---

## ✅ الخطوات التالية

بعد إكمال البدء السريع:

1. **هناك اجتماع تعريفي** مع فريقك
2. **اختر مهمة سهلة** من GitHub Issues
3. **ابدأ بـ PR صغيرة** لفهم العملية
4. **شارك أسئلتك** مع الفريق

---

**تهانينا! 🎉 أنت الآن جزء من فريق التطوير!**

إذا واجهت أي مشاكل، لا تتردد في الاتصال بـ:

- **Tech Lead**: ahmed@alkhayma.com
- **DevOps**: fatima@alkhayma.com

---

**آخر تحديث:** 22 فبراير 2026
**الإصدار:** 1.0.0
