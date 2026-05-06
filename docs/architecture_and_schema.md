# BondhuTime Architecture & Database Schema

## Architecture Overview

The system is designed as a modern, decoupled SaaS platform.

- **Backend:** FastAPI (Python) for high performance, async capabilities, and auto-generated API documentation (Swagger/OpenAPI).
- **Database:** PostgreSQL for robust relational data, JSONB support for flexible metadata, and PostGIS for location-based machine querying.
- **Frontend (Web):** Next.js (React) for SEO optimization, fast rendering, and responsive UI.
- **Mobile App:** React Native or PWA sharing the same backend API.
- **Infrastructure:** Linux (Ubuntu) server, Nginx as a reverse proxy, Docker containers for deployment, and a CI/CD pipeline (e.g., GitHub Actions).

## Core Modules & Microservices

1. **Auth & IAM Service:** JWT generation, role-based access control, OTP verification.
2. **User & Profile Service:** User data management, settings, and roles.
3. **Cycle Tracking Service:** Menstrual logging, predictions, history.
4. **Machine Fleet Management:** Machine health, stock, location, and heartbeat.
5. **Commerce Service:** Orders, payments (QR/In-app), shop management.
6. **Communication Service:** Messaging (Inbox), notifications.

## Database Schema (PostgreSQL)

```sql
-- Enums
CREATE TYPE user_role AS ENUM ('user', 'admin', 'doctor', 'shop', 'machine');
CREATE TYPE machine_status AS ENUM ('healthy', 'warning', 'critical', 'offline');
CREATE TYPE order_status AS ENUM ('pending', 'completed', 'failed', 'refunded');

-- Users & Authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone_number VARCHAR(20) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    address TEXT,
    role user_role DEFAULT 'user',
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE -- Soft delete
);

-- Cycle Tracker
CREATE TABLE cycle_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE,
    flow_intensity VARCHAR(50),
    symptoms JSONB, -- To store dynamic symptoms (cramps, mood, etc.)
    notes TEXT,
    is_irregular BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Machines
CREATE TABLE machines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    machine_code VARCHAR(100) UNIQUE NOT NULL,
    auth_token VARCHAR(255) NOT NULL, -- For machine heartbeat authentication
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    address TEXT NOT NULL,
    zone VARCHAR(100),
    status machine_status DEFAULT 'offline',
    stock_level JSONB, -- e.g., {"pads": 50, "tampons": 20}
    last_heartbeat TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Machine Logs (Immutable)
CREATE TABLE machine_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    machine_id UUID REFERENCES machines(id),
    log_type VARCHAR(50), -- e.g., 'restock', 'error', 'heartbeat', 'dispense'
    payload JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Products (Shop/Machine)
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Orders
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    machine_id UUID REFERENCES machines(id), -- Null if shop order
    total_amount DECIMAL(10, 2) NOT NULL,
    status order_status DEFAULT 'pending',
    payment_method VARCHAR(50), -- e.g., 'qr_code', 'in_app'
    transaction_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Order Items
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price_at_time DECIMAL(10, 2) NOT NULL
);

-- Inbox / Messages
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id UUID REFERENCES users(id),
    receiver_id UUID REFERENCES users(id),
    content TEXT NOT NULL,
    read_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Notifications
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50), -- e.g., 'cycle_alert', 'order_update'
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```
