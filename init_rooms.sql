CREATE TABLE IF NOT EXISTS rooms (
    id SERIAL PRIMARY KEY,
    room_number VARCHAR NOT NULL UNIQUE,
    room_type VARCHAR NOT NULL DEFAULT 'STANDARD',
    status VARCHAR NOT NULL DEFAULT 'AVAILABLE',
    price_per_night FLOAT NOT NULL,
    capacity INTEGER NOT NULL,
    description_en TEXT,
    description_ar TEXT,
    amenities TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    rating FLOAT NOT NULL DEFAULT 4.0,
    review_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS ix_rooms_id ON rooms(id);
CREATE INDEX IF NOT EXISTS ix_rooms_room_number ON rooms(room_number);

INSERT INTO alembic_version (version_num) VALUES ('edb175a1de9f')
ON CONFLICT DO NOTHING;

-- Seed initial room data
INSERT INTO rooms (room_number, room_type, status, price_per_night, capacity, description_en, description_ar, amenities, is_active, rating, review_count)
VALUES
    ('101', 'STANDARD', 'AVAILABLE', 150.0, 2, 'Comfortable standard room with sea view', 'غرفة قياسية مريحة مع إطلالة على البحر', '{"wifi": true, "tv": true, "ac": true}', true, 4.3, 42),
    ('201', 'DELUXE', 'AVAILABLE', 250.0, 3, 'Spacious deluxe room with balcony', 'غرفة فسيحة فاخرة مع شرفة خاصة وإطلالة محيطية', '{"wifi": true, "tv": true, "ac": true, "minibar": true}', true, 4.7, 58),
    ('301', 'SUITE', 'AVAILABLE', 400.0, 4, 'Luxury suite with ocean view', 'جناح فاخر مع إطلالة استثنائية على المحيط وتسهيلات راقية', '{"wifi": true, "tv": true, "ac": true, "minibar": true, "jacuzzi": true}', true, 4.9, 67)
ON CONFLICT (room_number) DO NOTHING;

SELECT COUNT(*) as room_count FROM rooms;
