CREATE OR REPLACE VIEW analytics.order_metrics AS
SELECT
    DATE_TRUNC('hour', order_timestamp) AS hour_bucket,
    COUNT(*) AS total_orders,
    SUM(total_amount) FILTER (WHERE order_status <> 'CANCELLED') AS total_revenue,
    AVG(total_amount) FILTER (WHERE order_status <> 'CANCELLED') AS average_order_value,
    AVG(EXTRACT(EPOCH FROM (delivery_timestamp - order_timestamp)) / 60)
        FILTER (WHERE delivery_timestamp IS NOT NULL) AS average_delivery_minutes
FROM orders
GROUP BY 1;

CREATE OR REPLACE VIEW analytics.agent_metrics AS
SELECT
    agent_id,
    COUNT(*) FILTER (WHERE order_status = 'DELIVERED') AS delivered_orders,
    SUM(total_amount) FILTER (WHERE order_status <> 'CANCELLED') AS revenue_handled
FROM orders
GROUP BY 1;

CREATE OR REPLACE VIEW analytics.customer_metrics AS
SELECT
    customer_id,
    COUNT(*) AS total_orders,
    SUM(total_amount) FILTER (WHERE order_status <> 'CANCELLED') AS total_revenue
FROM orders
GROUP BY 1;

CREATE OR REPLACE VIEW analytics.product_metrics AS
SELECT
    product_id,
    SUM(quantity) AS quantity_sold,
    SUM(total_amount) FILTER (WHERE order_status <> 'CANCELLED') AS total_revenue
FROM orders
GROUP BY 1;

CREATE OR REPLACE VIEW analytics.city_metrics AS
SELECT
    city,
    COUNT(*) AS total_orders,
    SUM(total_amount) FILTER (WHERE order_status <> 'CANCELLED') AS total_revenue,
    AVG(distance_km) AS average_distance
FROM orders
GROUP BY 1;

