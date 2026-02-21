#!/bin/bash

# Import workflows to n8n automatically
echo "🔄 Importing workflows to n8n..."

# Wait for n8n to be fully ready
sleep 10

# Copy workflows to n8n container
docker cp ../n8n-workflows/booking_confirmed.json n8n-resort:/tmp/
docker cp ../n8n-workflows/check_in_reminder.json n8n-resort:/tmp/
docker cp ../n8n-workflows/post_stay_review.json n8n-resort:/tmp/
docker cp ../n8n-workflows/marketing_weekly.json n8n-resort:/tmp/

# Import workflows using n8n CLI
docker exec n8n-resort n8n import:workflow --input=/tmp/booking_confirmed.json
docker exec n8n-resort n8n import:workflow --input=/tmp/check_in_reminder.json
docker exec n8n-resort n8n import:workflow --input=/tmp/post_stay_review.json
docker exec n8n-resort n8n import:workflow --input=/tmp/marketing_weekly.json

echo "✅ Workflows imported successfully!"
echo "🌐 Access n8n at: http://localhost:5678"
echo "👤 Username: admin"
echo "🔑 Password: AlKhayma2026!"
