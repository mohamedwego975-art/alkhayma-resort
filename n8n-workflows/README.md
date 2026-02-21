# N8N Automation Workflows - الخيمة Beach Resort

## Overview
4 automated workflows for WhatsApp + Email marketing and customer communication.

## Workflows

### 1. booking_confirmed.json
**Trigger:** Webhook POST `/webhook/booking-confirmed`
**Actions:**
- Send WhatsApp confirmation (Arabic)
- Send HTML email with booking details
- Create CRM contact in Airtable
- Wait 1 hour → Send preparation tips

### 2. check_in_reminder.json  
**Trigger:** Cron (every hour)
**Actions:**
- Query backend for tomorrow's bookings
- Send WhatsApp + Email reminders 24h before check-in
- Include location map and instructions

### 3. post_stay_review.json
**Trigger:** Webhook POST `/webhook/checkout-completed`
**Actions:**
- Wait 24 hours after checkout
- Send review request via WhatsApp
- Wait 48 hours → Send reminder if no review submitted

### 4. marketing_weekly.json
**Trigger:** Cron (Monday 10am)
**Actions:**
- Check occupancy rate from analytics API
- If < 60%: Generate GPT promotional message
- Send to past guests (last 6 months) via WhatsApp + Email

## Setup Instructions

### 1. Install n8n
```bash
npm install -g n8n
# or
npx n8n start --tunnel
```

### 2. Import Workflows
1. Open n8n at http://localhost:5678
2. Go to Workflows → Import from File
3. Import each JSON file from this directory

### 3. Configure Credentials

#### Twilio (WhatsApp)
- Account SID
- Auth Token  
- WhatsApp number: +1234567890

#### Gmail
- OAuth2 credentials
- Enable Gmail API

#### Airtable (CRM)
- API Token
- Base ID
- Table: "Customers"

#### Backend API
- HTTP Header Auth
- Authorization: Bearer admin-token

#### OpenAI
- API Key for GPT message generation

### 4. Test Workflows

Run validation script:
```bash
python3 test_workflows.py
```

Manual webhook tests:
```bash
# Test booking confirmation
curl -X POST http://localhost:5678/webhook/booking-confirmed \
  -H "Content-Type: application/json" \
  -d '{
    "booking_id": 123,
    "user_name": "أحمد محمد", 
    "user_phone": "+201234567890",
    "user_email": "ahmed@example.com",
    "product_name": "VIP Beach Access",
    "check_in": "2026-02-22",
    "total_price": 150.0,
    "booking_reference": "KH-2026-001"
  }'

# Test checkout completion
curl -X POST http://localhost:5678/webhook/checkout-completed \
  -H "Content-Type: application/json" \
  -d '{
    "booking_reference": "KH-2026-001",
    "user_id": 123,
    "user_name": "أحمد محمد",
    "user_phone": "+201234567890", 
    "user_email": "ahmed@example.com"
  }'
```

## Message Templates

### WhatsApp Messages (Arabic)
- **Booking Confirmation:** "مرحباً {name}! تم تأكيد حجزك في الخيمة 🏖"
- **Check-in Reminder:** "تذكير: موعدك في الخيمة غداً ☀️"
- **Review Request:** "كيف كانت إقامتك في الخيمة؟ 🌟"
- **Marketing:** GPT-generated with 20% discount offer

### Email Templates
- Responsive HTML design
- Arabic/English support
- Booking details, maps, QR codes
- Resort branding with gradients

## Integration Points

### Backend API Endpoints Required:
- `GET /api/admin/bookings?check_in={date}&status=confirmed`
- `GET /api/admin/analytics/overview`
- `GET /api/admin/users?status=guest&last_stay_within=6months`
- `GET /api/reviews/check/{booking_reference}`

### Webhook Triggers:
- `/webhook/booking-confirmed` (from payment success)
- `/webhook/checkout-completed` (from admin panel)

## Monitoring

Check workflow execution in n8n:
1. Go to Executions tab
2. Monitor success/failure rates
3. Check logs for errors
4. Set up email alerts for failures

## Production Deployment

1. Use n8n Docker container
2. Set environment variables for credentials
3. Configure reverse proxy (nginx)
4. Enable SSL certificates
5. Set up monitoring and backups
