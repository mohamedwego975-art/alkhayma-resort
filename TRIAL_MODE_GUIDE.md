# 🏖️ AlKhayma Beach Resort - دليل الوضع التجريبي
# Trial Mode Deployment Guide

## 📋 نظرة عامة / Overview

هذا المشروع الآن في **الوضع التجريبي** مع جميع الخدمات الأساسية مُفعلة:

| الخدمة | الحالة | الوصف |
|--------|--------|-------|
| 📧 Gmail/SMTP | ✅ مفعل | إرسال إيميلات التأكيد والتذكير |
| 💬 WhatsApp (Twilio) | ✅ مفعل | إشعارات واتساب للنزلاء |
| 🗺 Google Maps | ✅ مفعل | خريطة المنتجع والموقع |
| 🔄 N8N Automation | ✅ مفعل | أتمتة workflows |
| 📈 Monitoring | ✅ مفعل | Prometheus + Grafana |
| 🔁 CI/CD Pipeline | ✅ مفعل | GitHub Actions |

## 🚀 البدء السريع / Quick Start

### 1. تشغيل الوضع التجريبي

```bash
# نسخ ملف الإعدادات
cp .env.example .env

# تعديل المتغيرات في .env
nano .env

# تشغيل الوضع التجريبي
./trial-mode.sh
```

### 2. الوصول للخدمات

| الخدمة | الرابط | بيانات الدخول |
|--------|--------|---------------|
| 🌐 Frontend | http://localhost:5173 | - |
| ⚙️ Backend API | http://localhost:8000 | - |
| 📚 API Docs | http://localhost:8000/docs | - |
| 📊 Grafana | http://localhost:3000 | admin/changeme123 |
| 📈 Prometheus | http://localhost:9090 | - |
| 🔄 N8N | http://localhost:5678 | admin/AlKhayma2026! |

## 🔧 الإعدادات المطلوبة / Required Configuration

### 1. إعدادات البريد الإلكتروني (Gmail/SMTP)

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

> ⚠️ **ملاحظة**: يجب استخدام "App Password" من حساب Google، وليس كلمة المرور العادية.
> [كيفية إنشاء App Password](https://support.google.com/accounts/answer/185833)

### 2. إعدادات WhatsApp (Twilio)

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

> 📱 **Twilio Sandbox**: للاختبار، استخدم رقم Sandbox. للإنتاج، اطلب موافقة Twilio.

### 3. إعدادات Google Maps

```env
VITE_GOOGLE_MAPS_API_KEY=AIzaxxxxxxxxxxxxxxxxxxx
```

> 🗺 [الحصول على API Key](https://developers.google.com/maps/documentation/javascript/get-api-key)

### 4. إعدادات OpenAI (للـ AI Service)

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 📁 الهيكل الجديد / New Structure

```
alkhayma-resort/
├── 📧 Email Service
│   └── backend/app/services/email.py          # خدمة الإيميل
├── 💬 WhatsApp Service
│   └── backend/app/services/whatsapp.py      # خدمة الواتساب
├── 🗺 Google Maps
│   ├── frontend/src/components/ResortMap.vue  # خريطة المنتجع
│   └── frontend/src/pages/LocationPage.vue    # صفحة الموقع
├── 🔄 N8N Automation
│   ├── n8n-setup/docker-compose.yml           # إعداد N8N
│   ├── n8n-setup/deploy-workflows.sh          # نشر workflows
│   └── n8n-workflows/*.json                 # ملفات workflows
├── 📈 Monitoring
│   ├── monitoring/docker-compose.yml          # Prometheus + Grafana
│   └── monitoring/start.sh                    # سكريبت التشغيل
├── 🔁 CI/CD
│   └── .github/workflows/ci-cd.yml            # GitHub Actions
└── 🚀 Trial Mode
    ├── trial-mode.sh                          # مشغل الوضع التجريبي
    └── .env.example                           # قالب الإعدادات
```

## 🎯 API Endpoints الجديدة

### إشعارات / Notifications

```bash
# إرسال إيميل
POST /api/notifications/email/send
{
  "to_email": "guest@example.com",
  "subject": "Booking Confirmation",
  "html_content": "<h1>Thank you!</h1>"
}

# إرسال رسالة واتساب
POST /api/notifications/whatsapp/send
{
  "to_number": "+201234567890",
  "message": "Your booking is confirmed!"
}

# إرسال تأكيد الحجز (إيميل + واتساب)
POST /api/notifications/booking/confirmation
{
  "to_email": "guest@example.com",
  "to_whatsapp": "+201234567890",
  "guest_name": "Ahmed",
  "booking_id": "BK-12345",
  "room_name": "Ocean Suite",
  "check_in": "2026-03-01",
  "check_out": "2026-03-05",
  "total_amount": 1500.00
}

# حالة خدمات الإشعارات
GET /api/notifications/status
```

## 🔄 N8N Workflows المتاحة

1. **booking_confirmed.json** - إشعار تأكيد الحجز
2. **check_in_reminder.json** - تذكير قبل الوصول
3. **post_stay_review.json** - طلب مراجعة بعد الإقامة
4. **marketing_weekly.json** - رسائل تسويقية أسبوعية

## 📊 Monitoring Dashboards

### Grafana Dashboards

- **System Resources** - استهلاك CPU والذاكرة
- **API Performance** - أداء الـ Backend
- **Booking Metrics** - إحصائيات الحجوزات
- **Revenue Tracking** - تتبع الإيرادات

### Prometheus Metrics

```
# API Response Time
http_request_duration_seconds

# Error Rate
http_requests_total{status=~"5.."}

# Active Bookings
booking_active_total

# Revenue
payment_total{status="completed"}
```

## 🧪 الاختبار / Testing

### اختبار الإيميل

```bash
curl -X POST http://localhost:8000/api/notifications/email/send \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "your-email@gmail.com",
    "subject": "Test Email",
    "html_content": "<h1>Test from AlKhayma Resort!</h1>"
  }'
```

### اختبار WhatsApp

```bash
curl -X POST http://localhost:8000/api/notifications/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{
    "to_number": "+201234567890",
    "message": "Test WhatsApp message from AlKhayma Resort!"
  }'
```

## 🔐 Security Checklist

- [ ] تغيير كلمة مرور Grafana الافتراضية
- [ ] تغيير كلمة مرور N8N الافتراضية
- [ ] استخدام App Password للـ Gmail (ليس كلمة المرور العادية)
- [ ] تفعيل Two-Factor Authentication في Twilio
- [ ] تقييد API Keys بالـ IP المناسب
- [ ] استخدام HTTPS في الإنتاج
- [ ] تفعيل Rate Limiting

## 📚 مستندات إضافية

- [N8N Setup Guide](./n8n-setup/README.md)
- [Payment Integration](./backend/PAYMENT_INTEGRATION.md)
- [Frontend Documentation](./FRONTEND_README.md)

## 💬 الدعم

للأسئلة أو المشاكل:
- 📧 Email: support@alkhayma-resort.com
- 💬 WhatsApp: +20 XXX XXX XXXX

---

**🏖️ AlKhayma Beach Resort - Where Luxury Meets the Sea** 🌊
