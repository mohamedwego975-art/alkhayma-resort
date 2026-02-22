# 📋 متطلبات وتكوين المشروع

**آخر تحديث:** 22 فبراير 2026

---

## 📦 متطلبات النظام

### الحد الأدنى للتطوير

```
CPU:        2 نوى
RAM:        4 GB
Disk:       10 GB (SSD موصى به)
OS:         Linux / macOS / Windows 10+
```

### متطلبات الإنتاج

```
CPU:        4 نوى (8 موصى به)
RAM:        8 GB (16 موصى به)
Disk:       50 GB SSD
OS:         Ubuntu 20.04 LTS / Debian 11+
Bandwidth:  5 Mbps لأعلى
Uptime:     99.5%+ موثوقية
```

---

## 🛠️ البرامج والأدوات المطلوبة

### بيئة التطوير (Windows/Mac/Linux)

#### 1. Git

```bash
# Ubuntu/Debian
sudo apt install git

# macOS
brew install git

# Windows
# قم بتحميل من: https://git-scm.com
```

#### 2. Node.js & npm (17+)

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS
brew install node

# التحقق من الإصدار
node --version
npm --version
```

#### 3. Python 3.10+

```bash
# Ubuntu/Debian
sudo apt install python3.10 python3.10-venv python3-pip

# macOS
brew install python@3.10

# التحقق
python3 --version
pip3 --version
```

#### 4. PostgreSQL 15+

```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql

# التحقق
psql --version

# بدء الخدمة (Ubuntu)
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### 5. Redis 7+

```bash
# Ubuntu/Debian
sudo apt install redis-server

# macOS
brew install redis

# التحقق
redis-cli --version

# بدء الخدمة (Ubuntu)
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

#### 6. Docker & Docker Compose

```bash
# Ubuntu/Debian
sudo apt-get install docker.io docker-compose

# macOS
brew install docker docker-compose

# تشغيل بدون sudo (Linux)
sudo usermod -aG docker $USER
newgrp docker

# التحقق
docker --version
docker-compose --version
```

#### 7. IDE (اختياري لكن موصى به)

**VS Code:**

```bash
# Ubuntu/Debian
sudo snap install code --classic

# macOS
brew install visual-studio-code

# Windows
# قم بتحميل من: https://code.visualstudio.com
```

**الإضافات الموصى بها:**

- Pylance (Python)
- Vetur (Vue)
- REST Client
- Docker
- GitLens

---

## 🔐 ملفات البيئة (.env)

### تنسيق .env.example

```env
# ========================================
# DATABASE CONFIGURATION
# ========================================
DATABASE_URL=postgresql://user:password@localhost:5432/alkhayma
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=alkhayma

# ========================================
# REDIS CONFIGURATION
# ========================================
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=your_redis_password

# ========================================
# JWT & AUTHENTICATION
# ========================================
JWT_SECRET_KEY=your_super_secure_random_key_here_min_32_chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# ========================================
# APPLICATION SETTINGS
# ========================================
APP_NAME=الخيمة ريسورت
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO

# ========================================
# CORS CONFIGURATION
# ========================================
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
CORS_CREDENTIALS=True
CORS_METHODS=["*"]
CORS_HEADERS=["*"]

# ========================================
# EMAIL CONFIGURATION
# ========================================
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SENDER_EMAIL=noreply@alkhayma-resort.com
SENDER_NAME=الخيمة ريسورت

# ========================================
# PAYMENT INTEGRATION
# ========================================
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
PAYMOB_API_KEY=your_paymob_key

# ========================================
# AI & CHATBOT
# ========================================
OPENAI_API_KEY=sk-...
HUGGINGFACE_API_KEY=hf_...

# ========================================
# EXTERNAL SERVICES
# ========================================
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# ========================================
# N8N CONFIGURATION
# ========================================
N8N_HOST=localhost
N8N_PORT=5678
N8N_ENCRYPTION_KEY=your_encryption_key

# ========================================
# FRONTEND CONFIGURATION
# ========================================
VITE_API_URL=http://localhost:8000/api
VITE_AI_URL=http://localhost:8001
VITE_APP_NAME=الخيمة ريسورت

# ========================================
# MONITORING
# ========================================
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
GRAFANA_PASSWORD=admin_password
```

### إنشاء مفتاح سري آمن

```bash
# على Linux/macOS
openssl rand -hex 32

# على Windows (PowerShell)
[Convert]::ToBase64String(([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32)))
```

---

## 🔑 خطوات المصادقة

### 1. إعداد المصادقة الأساسية

```bash
# في الملف: backend/core/security.py
# سيتم العثور على:
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
```

### 2. كلمات المرور الآمنة

```python
# تشفير كلمة مرور
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash("user_password")

# التحقق من كلمة مرور
is_valid = pwd_context.verify("user_password", hashed_password)
```

### 3. إنشاء رموز JWT

```python
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### 4. التحقق من الرموز

```python
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id
```

---

## 🔐 ممارسات الأمان

### تصنيفات البيانات الحساسة

| البيانات          | الحساسية      | المعالجة                 |
| ----------------- | ------------- | ------------------------ |
| كلمات المرور      | 🔴 جداً عالية | تشفير bcrypt + Salt      |
| رموز JWT          | 🔴 عالية جداً | تخزين في Secure HttpOnly |
| مفاتيح API        | 🔴 عالية جداً | متغيرات البيئة فقط       |
| بيانات المدفوعات  | 🔴 عالية جداً | SSL/TLS + PCI DSS        |
| بيانات المستخدمين | 🟠 عالية      | تشفير في قاعدة البيانات  |
| بيانات الحجوزات   | 🟡 متوسطة     | سجلات الوصول             |

### إجراءات الأمان المطلوبة

- [ ] استخدام HTTPS/TLS في الإنتاج
- [ ] تعيين رؤوس الحماية (Security Headers)
- [ ] تفعيل CORS بشكل صحيح
- [ ] معدل التحديد (Rate Limiting)
- [ ] التحقق من صحة الإدخال (Input Validation)
- [ ] تعقيم البيانات (SQL Injection Prevention)
- [ ] حماية CSRF (Cross-Site Request Forgery)
- [ ] حماية XSS (Cross-Site Scripting)
- [ ] جدران الحماية (Web Application Firewall)
- [ ] المراقبة والتنبيهات

---

## 🌍 متطلبات البيئات المختلفة

### بيئة التطوير (Development)

```env
ENVIRONMENT=development
DEBUG=True
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
DATABASE_URL=postgresql://postgres:password@localhost:5432/alkhayma
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=dev-secret-key-not-secure
```

**الخصائص:**

- تسجيل مفصل (Verbose Logging)
- Hot Reload مفعل
- CORS متساهل
- بدون HTTPS
- بيانات اختبارية

### بيئة الاختبار (Testing)

```env
ENVIRONMENT=testing
DEBUG=False
DATABASE_URL=postgresql://postgres:password@localhost:5432/alkhayma_test
REDIS_URL=redis://localhost:6379/1
JWT_SECRET_KEY=test-secret-key
```

**الخصائص:**

- قاعدة بيانات منفصلة للاختبارات
- بيانات اختبارية معدة
- تسجيل محدود
- Hot Reload معطل

### بيئة التجميع (Staging)

```env
ENVIRONMENT=staging
DEBUG=False
CORS_ORIGINS=["https://staging.yourdomain.com"]
DATABASE_URL=postgresql://user:password@staging-db:5432/alkhayma
REDIS_URL=redis://staging-redis:6379/0
JWT_SECRET_KEY=staging-secret-key-secure
SSL_CERTIFICATE=/etc/ssl/staging.crt
SSL_KEY=/etc/ssl/staging.key
```

**الخصائص:**

- قريبة من الإنتاج
- تسجيل معتدل
- HTTPS مفعل
- بيانات حقيقية (نسخة اختبار)

### بيئة الإنتاج (Production)

```env
ENVIRONMENT=production
DEBUG=False
CORS_ORIGINS=["https://yourdomain.com"]
DATABASE_URL=postgresql://user:secure_password@prod-db.internal:5432/alkhayma
REDIS_URL=redis://prod-redis.internal:6379/0
JWT_SECRET_KEY=production-super-secure-random-key-min-32-chars
SSL_CERTIFICATE=/etc/ssl/alkhayma.crt
SSL_KEY=/etc/ssl/alkhayma.key
LOG_LEVEL=WARNING
BACKUP_ENABLED=True
MONITORING_ENABLED=True
```

**الخصائص:**

- HTTPS إلزامي (SSL/TLS)
- CORS مقيد
- تسجيل محدود (Log Rotation)
- مراقبة نشطة
- نسخ احتياطية آلية
- معدل تحديد عالي

---

## 📋 قائمة التحقق من التثبيت

### قبل التطوير

- [ ] تثبيت Git
- [ ] تثبيت Node.js 18+
- [ ] تثبيت Python 3.10+
- [ ] تثبيت PostgreSQL 15+
- [ ] تثبيت Redis 7+
- [ ] تثبيت Docker و Docker Compose
- [ ] تشغيل PostgreSQL و Redis
- [ ] استنساخ المشروع
- [ ] نسخ .env.example إلى .env.dev
- [ ] تثبيت مكتبات Backend
- [ ] تثبيت مكتبات Frontend
- [ ] تشغيل الترحيلات
- [ ] ملء البيانات الأساسية

### قبل النشر للاختبار

- [ ] جميع الاختبارات تمر
- [ ] لا توجد أخطاء TypeScript
- [ ] لا توجد تحذيرات Linter
- [ ] الـ Frontend يبنى بنجاح
- [ ] الـ API يعمل بشكل صحيح
- [ ] قاعدة البيانات متصلة
- [ ] البيانات الأساسية موجودة
- [ ] متغيرات البيئة صحيحة

### قبل النشر للإنتاج

- [ ] نسخة احتياطية من البيانات
- [ ] SSL/TLS شهادة صالحة
- [ ] متغيرات البيئة محدثة
- [ ] كلمات المرور قوية (32+ أحرف)
- [ ] مقاييس الأداء تم ضبطها
- [ ] تسجيل الأخطاء مفعل
- [ ] المراقبة والتنبيهات مفعلة
- [ ] خطة التعافي من الكوارث جاهزة
- [ ] إجراءات النسخ الاحتياطي الآلية

---

## 🔧 أوامر الإعداد السريع

### على Linux/Mac:

```bash
# تثبيت جميع المتطلبات
./scripts/setup.sh

# أو يدويًا:
# 1. Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head

# 2. Frontend
cd ../frontend
npm install

# 3. AI Service
cd ../ai-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### على Windows:

```cmd
# 1. Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head

# 2. Frontend
cd ..\frontend
npm install

# 3. AI Service
cd ..\ai-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

**تم الإنشاء:** 22 فبراير 2026
**الإصدار:** 1.0.0
