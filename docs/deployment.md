# 🚀 دليل النشر والإنتاج

**آخر تحديث:** 22 فبراير 2026
**الإصدار:** 1.0.0

---

## 📋 متطلبات ما قبل النشر

### ✅ قائمة التحقق من الجاهزية

```
الكود:
☐ جميع الاختبارات تمر: npm test && pytest
☐ لا توجد أخطاء TypeScript: npm run type-check
☐ الكود نظيف (Linting): npm run lint
☐ الـ Build بدون أخطاء: npm run build
☐ مراجعة الكود اكتملت

الأمان:
☐ تم مراجعة متغيرات البيئة
☐ لا توجد بيانات حساسة في الكود
☐ تحديث جميع المكتبات الأمنية
☐ مراجعة الأذونات والصلاحيات
☐ شهادات SSL صالحة

قاعدة البيانات:
☐ النسخة الاحتياطية تمت بنجاح
☐ الترحيلات تمت على staging
☐ البيانات الأساسية موجودة
☐ الفهارس محسنة

البنية التحتية:
☐ الخوادم جاهزة
☐ قدرة النسخ الاحتياطية متوفرة
☐ المراقبة مفعلة
☐ نطاق DNS محدث
```

---

## 🌍 خيارات النشر

### 1. النشر على Linux مباشر

#### متطلبات الخادم

```bash
# OS: Ubuntu 20.04 LTS أو أحدث
# RAM: 8 GB على الأقل
# CPU: 4 نوى
# Disk: 50 GB SSD

# التحقق من البيئة
uname -a  # Linux kernel
cat /etc/os-release  # Ubuntu version
free -h  # RAM available
df -h  # Disk space
```

#### خطوات النشر المباشر

```bash
#!/bin/bash
# deploy-direct.sh

set -e

echo "🚀 بدء نشر مباشر على الإنتاج"

# 1. تحديث النظام
echo "1️⃣ تحديث النظام..."
sudo apt update && sudo apt upgrade -y

# 2. قم باستنساخ المشروع
echo "2️⃣ استنساخ المشروع..."
cd /home/app
git clone https://github.com/yourusername/alkhayma-resort.git
cd alkhayma-resort

# 3. إعداد المتغيرات
echo "3️⃣ إعداد متغيرات البيئة..."
cp .env.example .env.prod
# تحرير .env.prod وإدخال البيانات الحقيقية
nano .env.prod

# 4. إعداد Backend
echo "4️⃣ إعداد Backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head  # تطبيق الترحيلات
cd ..

# 5. إعداد Frontend
echo "5️⃣ إعداد Frontend..."
cd frontend
npm ci  # استخدام معطيات محددة من package-lock.json
npm run build  # بناء مُحسّن للإنتاج
cd ..

# 6. إعداد الخدمات
echo "6️⃣ إعداد خدمات systemd..."
sudo cp deploy/alkhayma-backend.service /etc/systemd/system/
sudo cp deploy/alkhayma-frontend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable alkhayma-backend
sudo systemctl enable alkhayma-frontend

# 7. إعداد Nginx
echo "7️⃣ إعداد Nginx..."
sudo cp deploy/nginx.prod.conf /etc/nginx/sites-available/alkhayma
sudo ln -sf /etc/nginx/sites-available/alkhayma /etc/nginx/sites-enabled/
sudo nginx -t  # اختبار الإعدادات
sudo systemctl restart nginx

# 8. إعداد SSL
echo "8️⃣ إعداد SSL/TLS..."
sudo certbot certonly --nginx -d yourdomain.com
# تحديث /etc/nginx/sites-available/alkhayma بشهادات SSL

# 9. بدء الخدمات
echo "9️⃣ بدء الخدمات..."
sudo systemctl start alkhayma-backend
sudo systemctl start alkhayma-frontend
sudo systemctl restart nginx

# 10. فحص الصحة
echo "🔟 فحص الصحة..."
curl -s https://yourdomain.com/health
echo ""
echo "✅ اكتمل النشر بنجاح!"
```

#### ملف خدمة systemd (Backend)

```ini
# /etc/systemd/system/alkhayma-backend.service

[Unit]
Description=Alkhayma Resort Backend
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=app
WorkingDirectory=/home/app/alkhayma-resort/backend
Environment="PATH=/home/app/alkhayma-resort/backend/venv/bin"
Environment="DATABASE_URL=postgresql://..."
Environment="REDIS_URL=redis://..."
ExecStart=/home/app/alkhayma-resort/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

### 2. النشر بـ Docker و Docker Compose

#### بناء صور Docker

```dockerfile
# Dockerfile.prod (Backend)

FROM python:3.10-slim

WORKDIR /app

# تثبيت المتطلبات
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود
COPY backend/ .

# تشغيل التطبيق
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# Dockerfile.prod (Frontend)

FROM node:18-alpine AS builder

WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ .
RUN npm run build

# مرحلة الإنتاج
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY frontend/nginx.prod.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose للإنتاج

```yaml
# docker-compose.prod.yml

version: "3.9"

services:
  # PostgreSQL
  postgres:
    image: postgres:15-alpine
    container_name: alkhayma-postgres
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    networks:
      - alkhayma-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Redis
  redis:
    image: redis:7-alpine
    container_name: alkhayma-redis
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - alkhayma-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # FastAPI Backend
  backend:
    build:
      context: .
      dockerfile: Dockerfile.prod
    container_name: alkhayma-backend
    environment:
      DATABASE_URL: ${DATABASE_URL}
      REDIS_URL: ${REDIS_URL}
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
      ENVIRONMENT: production
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - alkhayma-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Vue.js Frontend
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.prod
    container_name: alkhayma-frontend
    depends_on:
      - backend
    networks:
      - alkhayma-network
    healthcheck:
      test:
        ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: alkhayma-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.prod.conf:/etc/nginx/conf.d/default.conf
      - ./ssl:/etc/nginx/ssl
      - ./logs/nginx:/var/log/nginx
    depends_on:
      - frontend
      - backend
    networks:
      - alkhayma-network
    restart: unless-stopped

  # AI Service
  ai-service:
    build:
      context: ./ai-service
    container_name: alkhayma-ai
    environment:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      HUGGINGFACE_API_KEY: ${HUGGINGFACE_API_KEY}
    depends_on:
      - backend
    networks:
      - alkhayma-network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  alkhayma-network:
    driver: bridge
```

#### نشر Docker Compose

```bash
#!/bin/bash
# deploy-docker.sh

echo "🐳 نشر باستخدام Docker Compose"

# 1. التأكد من وجود Docker
command -v docker >/dev/null 2>&1 || {
  echo "Docker غير مثبت. يرجى تثبيت Docker أولاً."
  exit 1
}

# 2. بناء الصور
echo "1️⃣ بناء الصور..."
docker-compose -f docker-compose.prod.yml build

# 3. إنشاء وتشغيل الحاويات
echo "2️⃣ تشغيل الحاويات..."
docker-compose -f docker-compose.prod.yml up -d

# 4. تطبيق الترحيلات
echo "3️⃣ تطبيق الترحيلات..."
docker-compose -f docker-compose.prod.yml exec backend \
  alembic upgrade head

# 5. ملء البيانات الأساسية
echo "4️⃣ ملء البيانات الأساسية..."
docker-compose -f docker-compose.prod.yml exec backend \
  python quick_seed.py

# 6. فحص الصحة
echo "5️⃣ فحص الصحة..."
sleep 10
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs --tail=20

echo ""
echo "✅ اكتمل النشر بنجاح!"
echo "🌐 الموقع متاح على: https://yourdomain.com"
```

### 3. النشر على الخدمات السحابية

#### AWS EC2 or DigitalOcean

```bash
# 1. تثبيت Docker على Droplet/EC2

# 2. استنساخ المشروع
git clone https://github.com/yourname/alkhayma-resort.git
cd alkhayma-resort

# 3. إعداد متغيرات البيئة
cp .env.example .env.prod

# 4. نشر باستخدام Docker
docker-compose -f docker-compose.prod.yml up -d

# 5. إعداد النطاق
# غيّر A record للإشارة إلى IP الخادم
```

---

## 🔒 إعداد SSL/TLS

### باستخدام Let's Encrypt

```bash
#!/bin/bash
# setup-ssl.sh

DOMAIN="yourdomain.com"
EMAIL="admin@yourdomain.com"

echo "🔐 إعداد SSL/TLS باستخدام Let's Encrypt"

# 1. تثبيت Certbot
sudo apt install certbot python3-certbot-nginx -y

# 2. الحصول على الشهادة
sudo certbot certonly --nginx \
  -d $DOMAIN \
  -d www.$DOMAIN \
  --email $EMAIL \
  --agree-tos \
  -n

# 3. إعادة تكوين Nginx
sudo systemctl reload nginx

# 4. تفعيل التجديد الآلي
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# 5. التحقق من التجديد
sudo certbot renew --dry-run

echo "✅ تم إعداد SSL/TLS بنجاح"
echo "📁 الشهادات في: /etc/letsencrypt/live/$DOMAIN/"
```

### تكوين Nginx مع SSL

```nginx
# /etc/nginx/sites-available/alkhayma

upstream backend {
    server localhost:8000;
}

upstream frontend {
    server localhost:5173;
}

# إعادة التوجيه من HTTP إلى HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # رؤوس الأمان
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # شهادات SSL
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # إعدادات SSL آمنة
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API Backend
    location /api/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # تجنب مشاكل Timeout
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css text/xml application/json application/javascript application/xml+rss;
    gzip_min_length 1000;
}
```

---

## 📊 المراقبة والسجلات

### إعداد Prometheus

```yaml
# prometheus.yml

global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: "alkhayma-backend"
    static_configs:
      - targets: ["localhost:8000"]

  - job_name: "node"
    static_configs:
      - targets: ["localhost:9100"]

  - job_name: "postgres"
    static_configs:
      - targets: ["localhost:9187"]
```

### إعداد Grafana

```
المتغيرات المهمة:
├─ CPU Usage
├─ Memory Usage
├─ Disk Usage
├─ Request Rate
├─ Error Rate
├─ Response Time
└─ Database Connections
```

---

## 🔄 تحديثات الإنتاج

### نموذج التحديث الآمن

```
التحديث الآمن (Zero Downtime):
│
├─ نشر على staging
├─ التحقق من الاختبارات
├─ نسخة احتياطية من البيانات
├─ تحديث Database (مع إمكانية التراجع)
├─ تحديث Backend (مع Blue-Green deployment)
├─ تحديث Frontend
├─ فحص الصحة
└─ المراقبة لمدة ساعة
```

### نص برمجي للتحديث الآمن

```bash
#!/bin/bash
# safe-deploy.sh

set -e

echo "🚀 نشر آمن (Zero Downtime)"

# 1. فحص الحالة الحالية
echo "1️⃣ فحص الحالة الحالية..."
docker-compose -f docker-compose.prod.yml ps

# 2. نسخة احتياطية
echo "2️⃣ إنشاء نسخة احتياطية..."
docker-compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U postgres alkhayma > backup_$(date +%Y%m%d_%H%M%S).sql

# 3. سحب الكود الجديد
echo "3️⃣ سحب الكود الجديد..."
git pull origin main

# 4. بناء الصور الجديدة
echo "4️⃣ بناء الصور الجديدة..."
docker-compose -f docker-compose.prod.yml build

# 5. تحديث الخدمات واحدة تلو الأخرى
echo "5️⃣ تحديث الخدمات..."
docker-compose -f docker-compose.prod.yml up -d postgres redis
sleep 10
docker-compose -f docker-compose.prod.yml up -d backend
sleep 10
docker-compose -f docker-compose.prod.yml up -d frontend

# 6. التحقق من الترحيلات
echo "6️⃣ التحقق من الترحيلات..."
docker-compose -f docker-compose.prod.yml exec backend \
  alembic upgrade head

# 7. فحص الصحة
echo "7️⃣ فحص الصحة..."
sleep 10
docker-compose -f docker-compose.prod.yml logs --tail=20

# 8. التحقق من المؤشرات
echo "8️⃣ التحقق من مؤشرات الأداء..."
curl -s https://yourdomain.com/api/health | jq .

echo ""
echo "✅ اكتمل النشر بنجاح!"
```

---

## 🆘 خطة التعافي من الكوارث

### الحالات الطارئة

| المشكلة               | المؤشرات         | الحل                          |
| --------------------- | ---------------- | ----------------------------- |
| قاعدة البيانات متعطلة | لا يمكن الاتصال  | استعادة من نسخة احتياطية      |
| تسرب الذاكرة          | استخدام RAM 100% | إعادة تشغيل الخدمة            |
| حملة DDoS             | طلبات مفرطة      | تفعيل WAF، تقليل معدل التحديث |
| خطأ في النشر          | أخطاء 500        | التراجع إلى الإصدار السابق    |
| فقدان البيانات        | البيانات مفقودة  | استعادة من نسخة احتياطية      |

### إجراءات الطوارئ

```bash
#!/bin/bash
# emergency-rollback.sh

echo "🚨 تفعيل إجراء الطوارئ"

# 1. إيقاف الخدمات
echo "1️⃣ إيقاف الخدمات..."
docker-compose -f docker-compose.prod.yml down

# 2. التراجع إلى الإصدار السابق
echo "2️⃣ التراجع إلى الإصدار السابق..."
git checkout main~1

# 3. بناء واستخدام الصور السابقة
echo "3️⃣ بناء الصور السابقة..."
docker-compose -f docker-compose.prod.yml build

# 4. استعادة من نسخة احتياطية إن لزم الأمر
read -p "هل تريد استعادة من نسخة احتياطية؟ (yes/no): " restore
if [ "$restore" = "yes" ]; then
  echo "4️⃣ استعادة البيانات..."
  # تشغيل restore-backup.sh
  ./restore-backup.sh <backup_file>
fi

# 5. إعادة تشغيل الخدمات
echo "5️⃣ إعادة تشغيل الخدمات..."
docker-compose -f docker-compose.prod.yml up -d

echo ""
echo "✅ تم إكمال إجراء الطوارئ"
```

---

**آخر تحديث:** 22 فبراير 2026
**الإصدار:** 1.0.0
