# Payment Integration - الخيمة Beach Resort

## Overview

Dual payment gateway integration supporting:
- **Paymob** (Primary) - Egyptian market, EGP currency
- **Stripe** (Secondary) - International market, USD/multi-currency

## Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  POST /api/payments/initiate/{booking_id}│
│  Body: {gateway: "paymob", currency: "EGP"}│
└──────┬──────────────────────────────────┘
       │
       ▼
┌──────────────────────┐
│  Payment Gateway     │
│  Service Layer       │
├──────────────────────┤
│ • PaymobGateway      │
│ • StripeGateway      │
└──────┬───────────────┘
       │
       ├─────────────────┐
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│   Paymob    │   │   Stripe    │
│   API       │   │   API       │
└─────────────┘   └─────────────┘
       │                 │
       │ (Webhook)       │ (Webhook)
       ▼                 ▼
┌─────────────────────────────────┐
│  POST /api/payments/webhook/*   │
│  • Verify signature             │
│  • Update payment status        │
│  • Confirm booking              │
│  • Fire n8n webhook             │
└─────────────────────────────────┘
```

## Database Schema

```sql
CREATE TYPE payment_gateway AS ENUM ('paymob', 'stripe');
CREATE TYPE payment_status AS ENUM ('pending', 'success', 'failed', 'refunded');

CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL UNIQUE REFERENCES bookings(id),
    gateway payment_gateway NOT NULL,
    status payment_status NOT NULL DEFAULT 'pending',
    amount NUMERIC(10, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    gateway_order_id VARCHAR(255),      -- Paymob order ID
    gateway_payment_id VARCHAR(255),    -- Payment key/intent ID
    payment_data JSONB NOT NULL,        -- Full gateway response
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE payment_webhook_logs (
    id SERIAL PRIMARY KEY,
    gateway payment_gateway NOT NULL,
    payload JSONB NOT NULL,
    signature VARCHAR(500),
    is_valid BOOLEAN NOT NULL DEFAULT false,
    processed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
```

## API Endpoints

### 1. Initiate Payment

```http
POST /api/payments/initiate/{booking_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "gateway": "paymob",  // or "stripe"
  "currency": "EGP"     // or "USD"
}
```

**Response (Paymob):**
```json
{
  "payment_id": 1,
  "gateway": "paymob",
  "amount": "230.00",
  "currency": "EGP",
  "paymob_data": {
    "payment_url": "https://accept.paymob.com/api/acceptance/iframes/...",
    "payment_key": "ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5...",
    "order_id": "123456789"
  }
}
```

**Response (Stripe):**
```json
{
  "payment_id": 2,
  "gateway": "stripe",
  "amount": "230.00",
  "currency": "USD",
  "stripe_data": {
    "client_secret": "pi_3ABC123_secret_xyz",
    "payment_intent_id": "pi_3ABC123"
  }
}
```

### 2. Paymob Webhook

```http
POST /api/payments/webhook/paymob
Content-Type: application/json

{
  "id": 123456,
  "success": true,
  "order": {
    "merchant_order_id": 1
  },
  "hmac": "calculated_signature",
  ...
}
```

### 3. Stripe Webhook

```http
POST /api/payments/webhook/stripe
Stripe-Signature: t=1234567890,v1=signature_hash

{
  "type": "payment_intent.succeeded",
  "data": {
    "object": {
      "id": "pi_3ABC123",
      "metadata": {
        "booking_id": "1"
      }
    }
  }
}
```

### 4. Cancel Booking & Refund (Admin Only)

```http
POST /api/payments/bookings/{booking_id}/cancel
Authorization: Bearer {admin_token}
```

**Response:**
```json
{
  "booking_id": 1,
  "status": "cancelled",
  "refund_initiated": true
}
```

## Paymob Integration

### Flow

1. **Authenticate**: Get auth token using API key
2. **Create Order**: Register order with amount and booking ID
3. **Get Payment Key**: Generate payment key with billing data
4. **Redirect**: Send user to Paymob iframe with payment key

### Configuration

```python
# .env
PAYMOB_API_KEY=your_api_key
PAYMOB_INTEGRATION_ID=your_integration_id
PAYMOB_HMAC_SECRET=your_hmac_secret
```

### Webhook Verification

Paymob uses HMAC-SHA512 signature:

```python
concat_string = (
    f"{amount_cents}{created_at}{currency}{error_occured}"
    f"{has_parent_transaction}{id}{integration_id}{is_3d_secure}"
    f"{is_auth}{is_capture}{is_refunded}{is_standalone_payment}"
    f"{is_voided}{order_id}{owner}{pending}{pan}{sub_type}{type}{success}"
)

calculated_hmac = hmac.new(
    PAYMOB_HMAC_SECRET.encode(),
    concat_string.encode(),
    hashlib.sha512
).hexdigest()
```

### Testing

Use Paymob sandbox:
- Test cards: https://docs.paymob.com/docs/testing-cards
- Webhook testing: Use ngrok to expose local endpoint

## Stripe Integration

### Flow

1. **Create PaymentIntent**: Initialize payment with amount and metadata
2. **Return Client Secret**: Send to frontend for Stripe.js
3. **Frontend Confirms**: User completes payment in browser
4. **Webhook Confirms**: Backend receives `payment_intent.succeeded`

### Configuration

```python
# .env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### Webhook Verification

Stripe provides built-in verification:

```python
import stripe

stripe.Webhook.construct_event(
    payload,
    signature_header,
    STRIPE_WEBHOOK_SECRET
)
```

### Testing

```bash
# Install Stripe CLI
stripe listen --forward-to localhost:8000/api/payments/webhook/stripe

# Trigger test events
stripe trigger payment_intent.succeeded
```

## Payment States

```
pending → success → (refunded)
        ↘ failed
```

- **pending**: Payment initiated, awaiting completion
- **success**: Payment confirmed by gateway
- **failed**: Payment declined/failed
- **refunded**: Payment refunded by admin

## Booking Status Integration

Payment status automatically updates booking:

```python
if payment.status == PaymentStatus.success:
    booking.status = BookingStatus.confirmed
    # Fire n8n webhook for confirmation email
```

## Security

### 1. Signature Verification
All webhooks verify cryptographic signatures before processing.

### 2. Idempotency
- One payment per booking (unique constraint)
- Webhook logs prevent duplicate processing

### 3. Atomic Transactions
Payment creation and booking update in single transaction.

### 4. Webhook Logging
All webhook attempts logged with:
- Full payload
- Signature
- Validation result
- Processing status

## Error Handling

### Client Errors (4xx)

- **400**: Booking not pending / Payment already exists
- **404**: Booking not found
- **422**: Invalid gateway/currency

### Gateway Errors (502)

- Paymob/Stripe API unavailable
- Invalid credentials
- Network timeout

### Example:

```json
{
  "detail": "Paymob authentication failed: Invalid API key"
}
```

## Testing

```bash
# Run integration test
cd /home/wego/Desktop/resort-platform/backend
source venv/bin/activate
python test_payment_integration.py
```

**Test Coverage:**
- ✅ Payment initiation (both gateways)
- ✅ Duplicate payment prevention
- ✅ Webhook signature validation
- ✅ Invalid signature rejection
- ✅ Payment record creation

## Production Checklist

### Paymob
- [ ] Replace test API key with production key
- [ ] Update integration ID for production
- [ ] Configure production HMAC secret
- [ ] Set up production webhook URL
- [ ] Test with real cards in production mode

### Stripe
- [ ] Replace `sk_test_` with `sk_live_` key
- [ ] Update webhook secret for production endpoint
- [ ] Enable required webhook events:
  - `payment_intent.succeeded`
  - `payment_intent.payment_failed`
- [ ] Configure Stripe Dashboard settings
- [ ] Test with real cards

### Infrastructure
- [ ] Expose webhook endpoints with HTTPS
- [ ] Configure firewall rules for gateway IPs
- [ ] Set up monitoring for webhook failures
- [ ] Configure retry logic for failed webhooks
- [ ] Set up alerts for payment anomalies

### Compliance
- [ ] PCI DSS compliance (if storing card data)
- [ ] GDPR compliance for payment data
- [ ] Terms of service for refunds
- [ ] Privacy policy for payment processing

## Monitoring

### Key Metrics

```sql
-- Payment success rate
SELECT 
    gateway,
    COUNT(*) FILTER (WHERE status = 'success') * 100.0 / COUNT(*) as success_rate
FROM payments
WHERE created_at > NOW() - INTERVAL '24 hours'
GROUP BY gateway;

-- Failed webhooks
SELECT COUNT(*) 
FROM payment_webhook_logs 
WHERE is_valid = false 
  AND created_at > NOW() - INTERVAL '1 hour';

-- Pending payments (stuck)
SELECT * 
FROM payments 
WHERE status = 'pending' 
  AND created_at < NOW() - INTERVAL '1 hour';
```

### Alerts

- Payment success rate < 95%
- Webhook validation failures > 5/hour
- Pending payments > 1 hour old
- Gateway API errors > 10/hour

## Support

### Paymob
- Docs: https://docs.paymob.com
- Support: support@paymob.com
- Dashboard: https://accept.paymob.com

### Stripe
- Docs: https://stripe.com/docs
- Support: https://support.stripe.com
- Dashboard: https://dashboard.stripe.com

## License

Proprietary - الخيمة Beach Resort
