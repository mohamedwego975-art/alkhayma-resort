# 🛠️ إجراءات الصيانة والإدارة

**آخر تحديث:** 22 فبراير 2026
**المسؤول:** فريق DevOps

---

## 📅 الجدول الزمني للصيانة

### ✅ يومي (Daily)

| المهمة                         | الوقت        | التردد  | المسؤول        |
| ------------------------------ | ------------ | ------- | -------------- |
| فحص سجلات الأخطاء              | 08:00 صباحًا | كل صباح | DevOps         |
| التحقق من الخوادم              | 08:15 صباحًا | كل ساعة | Monitoring Bot |
| نسخة احتياطية من DB            | 02:00 صباحًا | يومي    | Auto Script    |
| تنظيف النسخ الاحتياطية القديمة | 03:00 صباحًا | أسبوعي  | Auto Script    |

### 📅 أسبوعي (Weekly)

```
الاثنين:
  - تقرير الأداء الأسبوعي
  - مراجعة الترافيك

الأربعاء:
  - تحديث المكتبات الأمنية الطفيفة
  - تنظيف قاعدة البيانات

الجمعة:
  - اجتماع الفريق التقني
  - تحديث التوثيق
```

### 🔄 شهري (Monthly)

```
الأسبوع الأول:
  - تحديث كامل للنظام
  - اختبار الاستعادة من النسخ الاحتياطية
  - مراجعة الأمان

الأسبوع الثاني:
  - تحليل الأداء التفصيلي
  - تحسين الاستعلامات البطيئة

الأسبوع الثالث:
  - اختبارات التحميل
  - مراجعة سياسة النسخ الاحتياطية

الأسبوع الرابع:
  - جلسة استعراض الكود
  - تحديث دليل التشغيل
```

### 🏗️ ربع سنوي (Quarterly)

- إعادة بناء الفهارس (Reindex)
- تحديث البنية الأساسية
- اختبار الكوارث
- مراجعة الأمان الشاملة
- تحديث خطط التعافي

---

## 🔍 فحوصات الصحة (Health Checks)

### نص برمجي للفحوصات الروتينية

```bash
#!/bin/bash
# health-check-full.sh
# فحص شامل لصحة النظام

echo "========================================="
echo "فحص صحة النظام الشامل"
echo "========================================="

# 1. فحص الخدمات
echo "1️⃣ فحص الخدمات..."
for service in postgresql redis nginx docker; do
  if systemctl is-active --quiet $service; then
    echo "   ✅ $service يعمل"
  else
    echo "   ❌ $service متوقف - يجب بدؤه!"
    systemctl restart $service
  fi
done

# 2. فحص قاعدة البيانات
echo ""
echo "2️⃣ فحص قاعدة البيانات..."
psql -U postgres -d alkhayma -c "SELECT COUNT(*) FROM users;" > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "   ✅ قاعدة البيانات متصلة"
else
  echo "   ❌ فشل الاتصال بقاعدة البيانات"
fi

# 3. فحص Redis
echo ""
echo "3️⃣ فحص Redis..."
redis-cli ping > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "   ✅ Redis متصل"
else
  echo "   ❌ فشل الاتصال بـ Redis"
fi

# 4. فحص الخوادم
echo ""
echo "4️⃣ فحص الخوادم..."
curl -s http://localhost:8000/health > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "   ✅ Backend يعمل"
else
  echo "   ❌ Backend لا يستجيب"
fi

curl -s http://localhost:5173 > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "   ✅ Frontend يعمل"
else
  echo "   ⚠️  Frontend قد لا يعمل (قد يكون في الإنتاج)"
fi

# 5. فحص المساحة
echo ""
echo "5️⃣ فحص المساحة..."
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -lt 80 ]; then
  echo "   ✅ المساحة كافية: ${DISK_USAGE}%"
else
  echo "   ⚠️  التنبيه: الاستخدام ${DISK_USAGE}%"
fi

echo ""
echo "========================================="
echo "✅ اكتمل فحص الصحة"
echo "========================================="
```

---

## 📊 النسخ الاحتياطية (Backups)

### استراتيجية النسخ الاحتياطية

```
النسخ الساخنة (Hot Backup):
├─ يومي (Daily) - كل 24 ساعة
│  └─ الاحتفاظ: آخر 7 أيام
├─ أسبوعي (Weekly) - كل 7 أيام
│  └─ الاحتفاظ: آخر 4 أسابيع
└─ شهري (Monthly) - كل 30 يوم
   └─ الاحتفاظ: آخر 12 شهر

النسخ الباردة (Cold Backup):
├─ على جهاز خارجي
├─ تشفير AES-256
└─ تحديث شهري
```

### أماكن تخزين النسخ الاحتياطية

```
المحلي (Local):
├─ /var/backups/alkhayma/
├─ السعة: 500 GB
└─ الاحتفاظ: آخر 30 يوم

السحابة (Cloud - Amazon S3):
├─ s3://alkhayma-backups/
├─ الاحتفاظ: آخر 12 شهر
└─ التكرار: 3 مناطق

خارج الموقع (Off-site):
├─ NAS في مكتب آخر
├─ تحديث أسبوعي
└─ التشفير: نعم
```

### نص برمجي للنسخ الاحتياطية

```bash
#!/bin/bash
# backup-full.sh

BACKUP_DIR="/var/backups/alkhayma"
DB_NAME="alkhayma"
DB_USER="postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "🔄 بدء النسخة الاحتياطية: $TIMESTAMP"

# 1. نسخة احتياطية من قاعدة البيانات
echo "1️⃣ نسخة احتياطية من PostgreSQL..."
pg_dump -U $DB_USER -d $DB_NAME > "$BACKUP_DIR/db_$TIMESTAMP.sql"
gzip "$BACKUP_DIR/db_$TIMESTAMP.sql"
echo "   ✅ تم إنشاء: db_$TIMESTAMP.sql.gz"

# 2. نسخة احتياطية من الملفات المهمة
echo "2️⃣ نسخة احتياطية من الملفات..."
tar -czf "$BACKUP_DIR/files_$TIMESTAMP.tar.gz" \
  /home/app/alkhayma-resort/backend/uploads \
  /home/app/alkhayma-resort/.env \
  /etc/nginx/sites-available/alkhayma
echo "   ✅ تم إنشاء: files_$TIMESTAMP.tar.gz"

# 3. رفع إلى S3
echo "3️⃣ رفع إلى AWS S3..."
aws s3 cp "$BACKUP_DIR/db_$TIMESTAMP.sql.gz" \
  "s3://alkhayma-backups/database/$TIMESTAMP.sql.gz" \
  --sse AES256
aws s3 cp "$BACKUP_DIR/files_$TIMESTAMP.tar.gz" \
  "s3://alkhayma-backups/files/$TIMESTAMP.tar.gz" \
  --sse AES256
echo "   ✅ تم الرفع إلى S3"

# 4. حذف النسخ القديمة (أكثر من 30 يوم)
echo "4️⃣ تنظيف النسخ القديمة..."
find "$BACKUP_DIR" -name "db_*.sql.gz" -mtime +30 -delete
find "$BACKUP_DIR" -name "files_*.tar.gz" -mtime +30 -delete
echo "   ✅ تم حذف النسخ القديمة"

# 5. إرسال التنبيه
echo "5️⃣ إرسال التنبيه..."
echo "✅ تمت النسخة الاحتياطية بنجاح في $TIMESTAMP" | \
  mail -s "Alkhayma Backup Success" devops@alkhayma.com

echo ""
echo "✅ اكتملت النسخة الاحتياطية"
```

### استعادة النسخة الاحتياطية

```bash
#!/bin/bash
# restore-backup.sh

BACKUP_FILE=$1
DB_NAME="alkhayma"
DB_USER="postgres"

if [ -z "$BACKUP_FILE" ]; then
  echo "الرجاء تحديد ملف النسخة الاحتياطية"
  echo "الاستخدام: ./restore-backup.sh <backup_file.sql.gz>"
  exit 1
fi

echo "⚠️  تحذير: سيتم حذف قاعدة البيانات الحالية!"
read -p "هل أنت متأكد؟ (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
  echo "تم الإلغاء"
  exit 1
fi

echo "🔄 بدء الاستعادة من: $BACKUP_FILE"

# 1. حذف قاعدة البيانات الحالية
echo "1️⃣ حذف قاعدة البيانات الحالية..."
psql -U $DB_USER -c "DROP DATABASE IF EXISTS $DB_NAME;"

# 2. إنشاء قاعدة بيانات جديدة
echo "2️⃣ إنشاء قاعدة بيانات جديدة..."
psql -U $DB_USER -c "CREATE DATABASE $DB_NAME;"

# 3. استعادة البيانات
echo "3️⃣ استعادة البيانات من النسخة الاحتياطية..."
gunzip -c "$BACKUP_FILE" | psql -U $DB_USER -d $DB_NAME

echo ""
echo "✅ اكتملت الاستعادة"
```

---

## 📈 المراقبة والتنبيهات

### مؤشرات الأداء الرئيسية (KPIs)

```
النظام:
├─ CPU Usage: يجب أن يكون < 70%
├─ RAM Usage: يجب أن يكون < 80%
├─ Disk Usage: يجب أن يكون < 85%
└─ Network Bandwidth: يجب أن يكون < 80%

قاعدة البيانات:
├─ Connection Pool: < 100 اتصال
├─ Query Time: < 100ms (متوسط)
├─ Slow Queries: 0 في الساعة
└─ Replication Lag: 0 ثانية

الخطأ:
├─ Error Rate: < 0.5%
├─ Response Time: < 500ms (p95)
├─ Availability: > 99.5%
└─ API Uptime: > 99.9%
```

### إعدادات التنبيهات

```yaml
# prometheus/alerts.yml
groups:
  - name: system_alerts
    rules:
      # التنبيهات الحرجة
      - alert: HighCPUUsage
        expr: node_cpu_usage > 0.9
        for: 5m
        annotations:
          severity: critical
          message: "استخدام CPU مرتفع: {{ $value }}"

      - alert: HighMemoryUsage
        expr: node_memory_usage > 0.85
        for: 5m
        annotations:
          severity: warning
          message: "استخدام الذاكرة مرتفع: {{ $value }}"

      - alert: DiskSpaceLow
        expr: node_disk_available < 0.15
        for: 5m
        annotations:
          severity: critical
          message: "مساحة القرص منخفضة: {{ $value }}"

      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.005
        for: 5m
        annotations:
          severity: warning
          message: "معدل الأخطاء مرتفع: {{ $value }}"

      - alert: ServiceDown
        expr: up{job="alkhayma"} == 0
        for: 1m
        annotations:
          severity: critical
          message: "الخدمة متوقفة!"
```

---

## 🚨 استكشاف الأخطاء

### المشاكل الشائعة والحلول

#### 1. قاعدة البيانات بطيئة

```bash
# 1. تحقق من الاتصالات
psql -U postgres -d alkhayma -c "SELECT count(*) FROM pg_stat_activity;"

# 2. قتل الاتصالات المعلقة
psql -U postgres -d alkhayma -c "
  SELECT pg_terminate_backend(pid)
  FROM pg_stat_activity
  WHERE datname = 'alkhayma'
  AND state != 'active'
  AND query_start < now() - interval '1 hour';
"

# 3. إعادة بناء الفهارس
REINDEX DATABASE alkhayma;

# 4. تنظيف الجداول الميتة
VACUUM ANALYZE;
```

#### 2. مشاكل الذاكرة

```bash
# 1. فحص استخدام الذاكرة
free -h

# 2. قتل العمليات الثقيلة
ps aux | sort -k3 -r | head -5  # حسب CPU
ps aux | sort -k4 -r | head -5  # حسب Memory

# 3. مسح ذاكرة التخزين المؤقت
sync && echo 3 > /proc/sys/vm/drop_caches

# 4. فحص استخدام الذاكرة من Docker
docker stats
```

#### 3. مشاكل الشبكة

```bash
# 1. فحص الاتصالات النشطة
netstat -tuln | grep LISTEN

# 2. فحص الموارد المفتوحة
lsof -i :8000  # Backend
lsof -i :5173  # Frontend
lsof -i :5432  # PostgreSQL

# 3. فحص التأخير (Latency)
ping -c 4 localhost
```

#### 4. مشاكل الملفات والأذونات

```bash
# 1. فحص أذونات البيانات
ls -la /var/lib/postgresql/

# 2. إعادة تعيين الأذونات
sudo chown -R postgres:postgres /var/lib/postgresql/
sudo chmod 700 /var/lib/postgresql/

# 3. فحص مساحة القرص
df -h /
du -sh /var/lib/postgresql/
```

---

## 🔄 تحديث النظام

### خطوات التحديث الآمنة

```bash
#!/bin/bash
# safe-update.sh

echo "⚠️  ستقوم بتحديث النظام!"
read -p "هل تريد المتابعة؟ (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
  exit 1
fi

# 1. إنشاء نسخة احتياطية
echo "1️⃣ إنشاء نسخة احتياطية..."
./backup-full.sh

# 2. إيقاف الخدمات
echo "2️⃣ إيقاف الخدمات..."
docker-compose stop

# 3. تحديث المكتبات
echo "3️⃣ تحديث المكتبات..."
pip install -r backend/requirements.txt --upgrade
npm install --upgrade frontend/

# 4. تطبيق الترحيلات
echo "4️⃣ تطبيق الترحيلات..."
cd backend && alembic upgrade head

# 5. إعادة بدء الخدمات
echo "5️⃣ إعادة بدء الخدمات..."
docker-compose up -d

# 6. التحقق من الصحة
echo "6️⃣ التحقق من الصحة..."
sleep 10
./health-check-full.sh

echo ""
echo "✅ اكتمل التحديث بنجاح"
```

---

## 📝 السجلات والتدقيق (Logs & Audit)

### مواقع السجلات

```
Backend (FastAPI):
├─ /home/app/alkhayma-resort/backend/logs/
├─ app.log - سجل التطبيق
├─ error.log - الأخطاء فقط
└─ access.log - طلبات HTTP

Frontend (Vue.js):
├─ /var/log/frontend/
├─ build.log - سجل البناء
└─ runtime.log - أخطاء التشغيل

Database (PostgreSQL):
├─ /var/log/postgresql/
├─ postgresql.log - عام
└─ postgresql-YYYY-MM-DD.log

System:
├─ /var/log/syslog
├─ /var/log/auth.log
└─ /var/log/nginx/

Docker:
├─ docker logs <container_id>
└─ docker logs -f <container_id>
```

### عرض السجلات

```bash
# آخر 100 سطر
tail -n 100 /var/log/syslog

# تتبع السجل في الوقت الفعلي
tail -f /var/log/syslog

# البحث عن خطأ معين
grep -i error /var/log/syslog

# عرض آخر ساعة
journalctl --since "1 hour ago"

# من Docker
docker logs -f alkhayma-backend
```

---

## 📞 جهات الاتصال والدعم

| الدور             | الاسم        | البريد               | الهاتف         | التوفر      |
| ----------------- | ------------ | -------------------- | -------------- | ----------- |
| DevOps Lead       | أحمد محمد    | ahmed@alkhayma.com   | +966-50-XXXX   | 24/7        |
| Database Admin    | فاطمة علي    | fatima@alkhayma.com  | +966-50-YYYY   | 08:00-18:00 |
| Backend Lead      | محمود السعيد | mahmoud@alkhayma.com | +966-50-ZZZZ   | 09:00-17:00 |
| Frontend Lead     | سارة أحمد    | sarah@alkhayma.com   | +966-50-WWWW   | 09:00-17:00 |
| Emergency Support | فريق Support | support@alkhayma.com | +966-920-XXXXX | 24/7        |

---

**آخر تحديث:** 22 فبراير 2026
**الإصدار:** 1.0.0
