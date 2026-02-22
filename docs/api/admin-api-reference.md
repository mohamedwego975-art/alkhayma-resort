# Admin API Quick Reference Guide

## Base URL

```
http://localhost:8000/api
```

## Authentication

All admin endpoints require JWT Bearer token:

```bash
curl -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     http://localhost:8000/api/endpoint
```

---

## 🏨 Rooms Management

### List All Rooms

```bash
GET /rooms/admin/all?skip=0&limit=10

Response:
[
  {
    "id": 1,
    "room_number": "101",
    "room_type": "standard",
    "status": "available",
    "price_per_night": 150.0,
    "capacity": 2,
    "is_active": true
  }
]
```

### Create Room

```bash
POST /rooms/admin
Content-Type: application/json

Body:
{
  "room_number": "201",
  "room_type": "deluxe",
  "status": "available",
  "price_per_night": 250.0,
  "capacity": 3,
  "description_en": "Deluxe sea view room",
  "description_ar": "غرفة فاخرة مع إطلالة بحرية",
  "is_active": true
}

Response: 201 Created
{
  "id": 2,
  "room_number": "201",
  ...
}
```

### Update Room

```bash
PATCH /rooms/admin/1
Content-Type: application/json

Body: (all fields optional)
{
  "price_per_night": 300.0,
  "capacity": 4,
  "description_en": "Updated description"
}

Response: 200 OK
```

### Update Room Status

```bash
PATCH /rooms/admin/1/status
Content-Type: application/json

Body:
{
  "status": "occupied"
}

Status values: "available", "occupied", "maintenance"
```

### Toggle Room Active

```bash
PATCH /rooms/admin/1/active
Content-Type: application/json

Body:
{
  "is_active": false
}
```

### Delete Room

```bash
DELETE /rooms/admin/1

Response: 204 No Content
```

---

## 👥 User Management

### List All Users

```bash
GET /auth/admin/users?skip=0&limit=10

Response:
[
  {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "phone": "+20123456789",
    "role": "guest",
    "is_active": true,
    "created_at": "2026-02-22T10:30:00"
  }
]
```

### Update User Info

```bash
PATCH /auth/admin/users/1
Content-Type: application/json

Body: (only these fields editable)
{
  "full_name": "Jane Doe",
  "phone": "+20987654321",
  "role": "admin"
}

Note: email and password cannot be changed here
```

### Deactivate User

```bash
PATCH /auth/admin/users/1/active
Content-Type: application/json

Body:
{
  "is_active": false
}
```

### Delete User

```bash
DELETE /auth/admin/users/1

Response: 204 No Content

Note: Cannot delete own admin account
```

---

## 📦 Product Management

### List All Products

```bash
GET /products/admin/all?skip=0&limit=10

Response:
[
  {
    "id": 1,
    "name": "Beach Package",
    "name_ar": "باقة الشاطئ",
    "description": "Full day beach access",
    "type": "addon",
    "base_price": 50.0,
    "capacity": 4,
    "is_active": true
  }
]
```

### Create Product

```bash
POST /products/admin
Content-Type: application/json

Body:
{
  "name": "Spa Package",
  "name_ar": "باقة سبا",
  "description": "Relaxing spa treatment",
  "description_ar": "علاج سبا مريح",
  "type": "addon",
  "base_price": 75.0,
  "capacity": 1,
  "is_active": true
}

Response: 201 Created
```

### Update Product

```bash
PATCH /products/admin/1
Content-Type: application/json

Body:
{
  "base_price": 85.0,
  "capacity": 2
}
```

### Toggle Product Active

```bash
PATCH /products/admin/1/active
Content-Type: application/json

Body:
{
  "is_active": false
}
```

### Delete Product

```bash
DELETE /products/admin/1

Response: 204 No Content
```

---

## 📊 Analytics & Dashboard

### Dashboard Summary

```bash
GET /analytics/dashboard

Response:
{
  "today_revenue": 1500.50,
  "month_revenue": 45000.00,
  "active_bookings": 12,
  "total_customers": 245,
  "occupancy_rate": 78.5,
  "occupied_rooms": 47,
  "available_rooms": 13,
  "last_updated": "2026-02-22T15:30:00"
}
```

### Revenue Metrics

```bash
GET /analytics/revenue?days=30

Response:
{
  "total": 45000.00,
  "daily_breakdown": [
    {"date": "2026-02-22", "revenue": 1500.50},
    ...
  ],
  "by_payment_method": [
    {"method": "credit_card", "count": 25, "total": 3750.00},
    ...
  ],
  "period_days": 30
}
```

### Occupancy Metrics

```bash
GET /analytics/occupancy?days=30

Response:
{
  "total_rooms": 60,
  "occupied": 47,
  "available": 13,
  "occupancy_rate": 78.5,
  "by_room_type": [
    {
      "room_type": "standard",
      "total": 30,
      "occupied": 24,
      "available": 6,
      "rate": 80.0
    },
    ...
  ],
  "recent_bookings": 156,
  "period_days": 30
}
```

---

## 📅 Booking Management (Pre-existing)

### List All Bookings

```bash
GET /bookings/admin/all?skip=0&limit=10
```

### Update Booking Status

```bash
PATCH /bookings/admin/1/status
Content-Type: application/json

Body:
{
  "status": "confirmed"
}

Status values: "pending", "confirmed", "checked_in", "checked_out", "cancelled"
```

---

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Invalid status: invalid_status"
}
```

### 401 Unauthorized

```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden

```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found

```json
{
  "detail": "Room not found"
}
```

### 409 Conflict

```json
{
  "detail": "Room number 101 already exists"
}
```

---

## Pagination

All list endpoints support pagination:

```bash
GET /endpoint?skip=0&limit=10

Parameters:
- skip: Number of items to skip (default: 0)
- limit: Number of items to return (default: 100, max: 200)

Response is always List[ItemResponse]
```

---

## Validation Rules

### Room Creation

- room_number: Required, unique, 1-50 chars
- room_type: Required (standard, deluxe, suite, villa)
- status: Required (available, occupied, maintenance)
- price_per_night: Required, > 0
- capacity: Required, 1-20
- is_active: Optional, defaults to false

### User Update

- full_name: Optional, string
- phone: Optional, string
- role: Optional (guest, staff, admin)
- Cannot update: email, password, hashed_password

### Product Creation

- name: Required, string
- type: Required, string
- base_price: Required, >= 0
- capacity: Required, >= 1
- is_active: Optional, defaults to true

---

## Common Workflows

### Add New Room & Activate It

```bash
# 1. Create room
POST /rooms/admin
Body: { room_number: "301", ... }
Response: { id: 3, is_active: false }

# 2. Activate room
PATCH /rooms/admin/3/active
Body: { is_active: true }
Response: { id: 3, is_active: true }
```

### Deactivate User & Verify

```bash
# 1. Deactivate
PATCH /auth/admin/users/5/active
Body: { is_active: false }

# 2. Verify
GET /auth/admin/users
Response includes user with is_active: false
```

### Check Dashboard & Get Details

```bash
# 1. Dashboard overview
GET /analytics/dashboard

# 2. Get details for occupied rooms
GET /rooms/admin/all
Filter for those with status: "occupied"

# 3. Revenue breakdown
GET /analytics/revenue?days=30
```

---

## Rate Limiting & Performance

- Pagination limits:
  - Min skip: 0
  - Max limit: 200
  - Default limit: 100
- Response times: <100ms (uncached)
- Concurrent requests: No limit enforced (add if needed)

---

## Admin Roles

### Admin (Full Access)

- Create, read, update, delete all resources
- Manage users and admins
- View analytics
- Change settings
- Cannot delete own account

### Staff (Limited Access)

- Read all resources
- Update status fields
- View analytics (basic)
- Cannot create/delete resources
- Cannot manage users

### Guest (Guest Only)

- Create bookings
- View own bookings
- Leave reviews
- Cannot access admin endpoints

---

## Implementation Notes

- All datetime fields are UTC with timezone info
- All prices are floats (2 decimal places)
- Phone numbers stored as strings (validation on client)
- Status fields use lowercase enums
- Capacity is integer (persons)
- All admin actions logged with admin user ID
- Timestamps include created_at and updated_at

---

**Last Updated:** February 22, 2026
**Version:** 1.0.0
**Status:** Production Ready ✅
