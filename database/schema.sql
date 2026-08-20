CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS dashboard;

CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR PRIMARY KEY,
    customer_name VARCHAR NOT NULL,
    phone VARCHAR NOT NULL,
    city VARCHAR NOT NULL,
    registration_date DATE NOT NULL,
    customer_type VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS delivery_agents (
    agent_id VARCHAR PRIMARY KEY,
    agent_name VARCHAR NOT NULL,
    phone VARCHAR NOT NULL,
    vehicle_type VARCHAR NOT NULL,
    city VARCHAR NOT NULL,
    rating NUMERIC(3, 2) NOT NULL,
    joining_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR PRIMARY KEY,
    product_name VARCHAR NOT NULL,
    category VARCHAR NOT NULL,
    price NUMERIC(12, 2) NOT NULL CHECK (price >= 0),
    store_name VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR NOT NULL REFERENCES customers(customer_id),
    agent_id VARCHAR NOT NULL REFERENCES delivery_agents(agent_id),
    product_id VARCHAR NOT NULL REFERENCES products(product_id),
    city VARCHAR NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12, 2) NOT NULL CHECK (unit_price >= 0),
    total_amount NUMERIC(12, 2) NOT NULL CHECK (total_amount >= 0),
    order_timestamp TIMESTAMPTZ NOT NULL,
    pickup_timestamp TIMESTAMPTZ NULL,
    delivery_timestamp TIMESTAMPTZ NULL,
    promised_delivery_timestamp TIMESTAMPTZ NULL,
    delivery_latitude DOUBLE PRECISION NOT NULL CHECK (delivery_latitude BETWEEN -90 AND 90),
    delivery_longitude DOUBLE PRECISION NOT NULL CHECK (delivery_longitude BETWEEN -180 AND 180),
    distance_km NUMERIC(8, 2) NOT NULL CHECK (distance_km >= 0),
    order_status VARCHAR NOT NULL,
    payment_method VARCHAR NOT NULL,
    event_timestamp TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.orders (
    raw_id BIGSERIAL PRIMARY KEY,
    order_payload JSONB NOT NULL,
    received_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS dashboard.kpi_summary (
    updated_at TIMESTAMPTZ PRIMARY KEY,
    total_orders INTEGER NOT NULL,
    total_revenue NUMERIC(14, 2) NOT NULL,
    average_order_value NUMERIC(12, 2) NOT NULL,
    average_delivery_minutes NUMERIC(12, 2) NOT NULL,
    cancellation_rate NUMERIC(8, 2) NOT NULL,
    on_time_delivery_rate NUMERIC(8, 2) NOT NULL,
    active_agents INTEGER NOT NULL,
    orders_per_minute INTEGER NOT NULL,
    orders_last_5_minutes INTEGER NOT NULL,
    revenue_last_5_minutes NUMERIC(14, 2) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_orders_order_timestamp ON orders(order_timestamp);
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_agent_id ON orders(agent_id);
CREATE INDEX IF NOT EXISTS idx_orders_product_id ON orders(product_id);
CREATE INDEX IF NOT EXISTS idx_orders_city ON orders(city);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(order_status);

