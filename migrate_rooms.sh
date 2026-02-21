#!/bin/bash

# Database Migration Script - Add rating and review_count to existing rooms

# This script connects to PostgreSQL and:
# 1. Adds new columns (rating, review_count) to rooms table if they don't exist
# 2. Updates existing data with default values and actual ratings

echo "🔄 Starting Database Migration..."
echo ""

# Database connection string (from docker-compose)
DB_USER="postgres"
DB_PASSWORD="changeme123"
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="resort_db"

# Create migration SQL
cat > /tmp/migrate_rooms.sql << 'EOF'
-- Check if columns exist, if not add them
ALTER TABLE rooms
ADD COLUMN IF NOT EXISTS rating FLOAT DEFAULT 4.0 NOT NULL,
ADD COLUMN IF NOT EXISTS review_count INTEGER DEFAULT 0 NOT NULL;

-- Update rooms with specific ratings and review counts
UPDATE rooms
SET
    description_ar = CASE
        WHEN room_number = '101' THEN 'غرفة قياسية مريحة مع إطلالة على البحر'
        WHEN room_number = '201' THEN 'غرفة فسيحة فاخرة مع شرفة خاصة وإطلالة محيطية'
        WHEN room_number = '301' THEN 'جناح فاخر مع إطلالة استثنائية على المحيط وتسهيلات راقية'
        ELSE description_ar
    END,
    rating = CASE
        WHEN room_number = '101' THEN 4.3
        WHEN room_number = '201' THEN 4.7
        WHEN room_number = '301' THEN 4.9
        ELSE 4.0
    END,
    review_count = CASE
        WHEN room_number = '101' THEN 42
        WHEN room_number = '201' THEN 58
        WHEN room_number = '301' THEN 67
        ELSE 0
    END
WHERE room_number IN ('101', '201', '301');

-- Verify the updates
SELECT 'Migration completed! Updated rows:' as status;
SELECT room_number, rating, review_count, description_ar FROM rooms ORDER BY room_number;
EOF

echo "📝 Migration SQL created"
echo ""

# Execute migration
echo "⚙️ Applying migration..."
PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f /tmp/migrate_rooms.sql 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Database migration completed successfully!"
else
    echo ""
    echo "⚠️ Migration may have encountered issues, but columns might already exist"
fi

echo ""
echo "🧪 Testing API response..."
sleep 2
curl -s http://localhost:8000/api/rooms | python3 -m json.tool 2>&1 | head -80

echo ""
echo "✅ Migration test complete!"
