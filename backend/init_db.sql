-- Create ENUM types
CREATE TYPE userrole AS ENUM ('guest', 'admin', 'staff');
CREATE TYPE bookingstatus AS ENUM ('pending', 'confirmed', 'cancelled', 'completed');
CREATE TYPE producttype AS ENUM ('room', 'activity', 'service');

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR NOT NULL,
    phone VARCHAR,
    role userrole DEFAULT 'guest',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    name_ar VARCHAR NOT NULL,
    description TEXT,
    description_ar TEXT,
    type producttype NOT NULL,
    base_price FLOAT NOT NULL,
    capacity INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Bookings table
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    product_id INTEGER REFERENCES products(id) NOT NULL,
    check_in TIMESTAMP WITH TIME ZONE NOT NULL,
    check_out TIMESTAMP WITH TIME ZONE NOT NULL,
    guests INTEGER DEFAULT 1,
    total_price FLOAT NOT NULL,
    status bookingstatus DEFAULT 'pending',
    special_requests TEXT,
    idempotency_key VARCHAR UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Payments table
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER REFERENCES bookings(id) NOT NULL,
    amount FLOAT NOT NULL,
    currency VARCHAR DEFAULT 'EGP',
    payment_method VARCHAR,
    transaction_id VARCHAR UNIQUE,
    status VARCHAR DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Inventory table
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) NOT NULL,
    available INTEGER NOT NULL,
    reserved INTEGER DEFAULT 0,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Loyalty profiles table
CREATE TABLE loyalty_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    points INTEGER DEFAULT 0,
    tier VARCHAR DEFAULT 'Bronze',
    total_spent FLOAT DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Audit logs table
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR NOT NULL,
    resource VARCHAR NOT NULL,
    resource_id VARCHAR,
    details TEXT,
    ip_address VARCHAR,
    user_agent VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_bookings_user_id ON bookings(user_id);
CREATE INDEX idx_bookings_product_id ON bookings(product_id);
CREATE INDEX idx_bookings_idempotency_key ON bookings(idempotency_key);
CREATE INDEX idx_payments_booking_id ON payments(booking_id);
CREATE INDEX idx_payments_transaction_id ON payments(transaction_id);

-- Insert sample data
INSERT INTO products (name, name_ar, description, description_ar, type, base_price, capacity) VALUES
('Deluxe Sea View Room', 'غرفة ديلوكس بإطلالة بحرية', 'Spacious room with stunning sea view', 'غرفة واسعة بإطلالة بحرية خلابة', 'room', 1500.0, 2),
('Standard Room', 'غرفة عادية', 'Comfortable standard room', 'غرفة عادية مريحة', 'room', 1000.0, 2),
('Snorkeling Trip', 'رحلة غطس', 'Half-day snorkeling adventure', 'مغامرة غطس لنصف يوم', 'activity', 300.0, 10),
('Spa Treatment', 'علاج سبا', 'Relaxing spa treatment', 'علاج سبا مريح', 'service', 500.0, 1);

INSERT INTO inventory (product_id, available) VALUES
(1, 5), (2, 10), (3, 20), (4, 3);
