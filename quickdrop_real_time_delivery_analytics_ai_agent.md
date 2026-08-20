# QuickDrop Real-Time Delivery Analytics Platform

## AI Agent Project Specification

### 1. Project Objective

Build a complete beginner-friendly, production-style **real-time
delivery analytics platform** for a fictional delivery application named
**QuickDrop**.

The system must:

1.  Generate realistic delivery/order data continuously using Python.
2.  Stream order events in real time using Apache Kafka.
3.  Consume and validate Kafka events.
4.  Store raw and structured data in PostgreSQL.
5.  Calculate real-time and historical business/operational KPIs.
6.  Expose analytics through a FastAPI backend.
7.  Push live KPI updates to the frontend using WebSockets.
8.  Display a real-time analytics dashboard using React.
9.  Display delivery locations on an interactive map.
10. Support filtering, historical analysis, agent/customer/product
    analytics, and alerts.
11. Be containerized using Docker/Docker Compose.
12. Include tests, documentation, logging, configuration management, and
    a clean GitHub-ready structure.

The project should be implemented incrementally. Do not attempt to build
the entire system at once.

------------------------------------------------------------------------

# 2. Primary Technology Stack

Use the following stack unless there is a strong technical reason to
change it:

## Backend / Data

-   Python 3.12+
-   Faker
-   NumPy
-   Pandas where useful
-   confluent-kafka
-   PostgreSQL
-   psycopg / SQLAlchemy
-   FastAPI
-   Pydantic
-   WebSockets

## Frontend

-   React
-   Vite
-   JavaScript or TypeScript
-   Recharts or another lightweight charting library
-   Leaflet / React Leaflet for maps

## Infrastructure

-   Docker
-   Docker Compose
-   Apache Kafka
-   Kafka UI if useful for local development

## Development

-   Git
-   GitHub
-   pytest
-   python-dotenv or Pydantic Settings

Do not introduce Spark, Flink, Redis, Kubernetes, Airflow, or cloud
infrastructure in the MVP. They may be proposed as future enhancements
only.

------------------------------------------------------------------------

# 3. High-Level Architecture

The target architecture is:

``` text
                    ┌─────────────────────────┐
                    │ Python Data Simulator   │
                    │ Faker + NumPy           │
                    └────────────┬────────────┘
                                 │
                                 │ JSON Events
                                 ▼
                    ┌─────────────────────────┐
                    │      Apache Kafka       │
                    │       orders topic      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     Python Consumer      │
                    │ validation + processing  │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       PostgreSQL        │
                    │ raw + analytics tables  │
                    └────────────┬────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
           ┌────────────────┐       ┌────────────────┐
           │   KPI Engine   │       │ SQL Analytics  │
           │     Python     │       │ views/queries  │
           └───────┬────────┘       └───────┬────────┘
                   │                        │
                   └───────────┬────────────┘
                               ▼
                    ┌─────────────────────────┐
                    │        FastAPI          │
                    │ REST API + WebSockets   │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │         React           │
                    │   Real-Time Dashboard   │
                    └─────────────────────────┘
```

------------------------------------------------------------------------

# 4. Important Development Rule

Build the project in phases.

Do not generate all code simultaneously.

At the end of every phase:

1.  Explain what was built.
2.  Show the files created or modified.
3.  Show how to run the phase.
4.  Provide validation/testing commands.
5.  Confirm expected output.
6.  Identify the next phase.
7.  Do not proceed to the next major phase until the current phase is
    logically complete.

Assume the developer is a beginner.

Explain important concepts before using them.

------------------------------------------------------------------------

# 5. Project Phases

## Phase 1 --- Project Setup

Create the repository structure:

``` text
quickdrop-analytics/
│
├── data_generator/
├── kafka/
├── database/
├── analytics/
├── backend/
├── frontend/
├── tests/
├── docker/
├── docs/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── docker-compose.yml
```

Set up:

-   Python virtual environment
-   requirements.txt
-   environment variables
-   Git repository
-   basic README
-   Docker Compose skeleton

Do not implement business logic yet.

------------------------------------------------------------------------

# 6. Phase 2 --- Data Model

Design the following entities:

## Customers

``` text
customer_id
customer_name
phone
city
registration_date
customer_type
```

Customer types:

``` text
Premium
Regular
Occasional
```

## Delivery Agents

``` text
agent_id
agent_name
phone
vehicle_type
city
rating
joining_date
```

Vehicle types:

``` text
Bike
Scooter
Bicycle
```

## Products

``` text
product_id
product_name
category
price
store_name
```

Categories may include:

``` text
Food
Groceries
Pharmacy
Electronics
Bakery
Beverages
```

## Orders

``` text
order_id
customer_id
agent_id
product_id
quantity
unit_price
total_amount
order_timestamp
pickup_timestamp
delivery_timestamp
promised_delivery_timestamp
delivery_latitude
delivery_longitude
distance_km
order_status
payment_method
event_timestamp
```

Order statuses:

``` text
PLACED
ACCEPTED
PICKED_UP
DELIVERED
CANCELLED
```

Payment methods:

``` text
UPI
CARD
CASH
WALLET
```

------------------------------------------------------------------------

# 7. Phase 3 --- Realistic Python Data Generator

Build a Python data simulator.

It must generate:

-   Customers
-   Delivery agents
-   Products
-   Orders

The generator must create realistic relationships rather than completely
independent random values.

For example:

``` text
total_amount = quantity * unit_price
```

Delivery duration should generally increase with distance.

Example concept:

``` text
delivery_time =
base preparation time
+ travel time based on distance
+ random traffic factor
```

Customer ordering frequency should vary.

Some customers should order frequently, while others should order
occasionally.

Delivery agents should have different performance levels.

Cities should have different demand patterns.

------------------------------------------------------------------------

# 8. Geographic Data

Use realistic city coordinates.

Initially support:

``` text
Bengaluru
Delhi
Mumbai
Hyderabad
Pune
Kolkata
Chennai
Bhubaneswar
```

Generate delivery coordinates around each city.

Do not use fake coordinates that are obviously invalid.

The generated coordinates will later be displayed on the dashboard map.

------------------------------------------------------------------------

# 9. Data Generator Requirements

The generator must support configuration such as:

``` text
ORDERS_PER_SECOND
NUMBER_OF_CUSTOMERS
NUMBER_OF_AGENTS
NUMBER_OF_PRODUCTS
SUPPORTED_CITIES
```

Example:

``` python
ORDERS_PER_SECOND = 5
```

It should continuously generate orders.

Also support a finite test mode:

``` text
python generate_data.py --count 10000
```

and streaming mode:

``` text
python generate_stream.py --rate 5
```

------------------------------------------------------------------------

# 10. Phase 4 --- PostgreSQL

Create PostgreSQL schemas:

``` text
raw
analytics
dashboard
```

Recommended tables:

``` text
raw.orders
analytics.order_metrics
analytics.agent_metrics
analytics.customer_metrics
analytics.product_metrics
analytics.city_metrics
dashboard.kpi_summary
dashboard.hourly_metrics
dashboard.agent_summary
dashboard.product_summary
dashboard.city_summary
```

For the core relational model also create:

``` text
customers
delivery_agents
products
orders
```

Use:

-   primary keys
-   foreign keys
-   appropriate numeric/date/time types
-   indexes
-   constraints

Use UTC timestamps internally where practical.

------------------------------------------------------------------------

# 11. Database Design Rules

Do not store everything as text.

Use appropriate types:

``` text
IDs              VARCHAR
quantity         INTEGER
price            NUMERIC
latitude         DOUBLE PRECISION
longitude        DOUBLE PRECISION
timestamps       TIMESTAMPTZ
rating           NUMERIC
distance         NUMERIC
```

Create indexes on commonly queried columns such as:

``` text
order_timestamp
customer_id
agent_id
product_id
city
order_status
```

Avoid unnecessary indexes.

------------------------------------------------------------------------

# 12. Phase 5 --- SQL Analytics

Before adding Kafka, prove that the analytical model works with
PostgreSQL.

Create SQL queries for:

## Business KPIs

-   Total orders
-   Total revenue
-   Average order value
-   Delivered orders
-   Cancelled orders
-   Cancellation rate

## Delivery KPIs

-   Average delivery time
-   Average delivery distance
-   On-time delivery rate
-   Average preparation time
-   Average travel time

## Agent KPIs

-   Orders delivered per agent
-   Average delivery time per agent
-   Distance travelled per agent
-   Revenue handled per agent
-   Agent rating

## Customer KPIs

-   Orders per customer
-   Revenue per customer
-   Average order value per customer
-   Repeat customers
-   Top customers

## Product KPIs

-   Most ordered products
-   Highest revenue products
-   Quantity sold
-   Revenue by category
-   Average product price

## Location KPIs

-   Orders by city
-   Revenue by city
-   Average delivery time by city
-   Average distance by city

## Time KPIs

-   Orders per minute
-   Orders per 5 minutes
-   Orders per hour
-   Revenue per hour
-   Peak order hours

Use:

-   GROUP BY
-   JOIN
-   CTEs
-   CASE
-   aggregate functions
-   window functions
-   date/time functions

Create reusable SQL views where appropriate.

------------------------------------------------------------------------

# 13. Phase 6 --- Kafka

Use Apache Kafka for real-time event streaming.

For the MVP create:

``` text
orders
```

topic.

Later optionally add:

``` text
delivery_events
payments
```

The Python simulator should become the Kafka producer.

Flow:

``` text
Python Simulator
      ↓
Kafka Producer
      ↓
orders topic
```

Each event should be JSON.

Example:

``` json
{
  "order_id": "ORD100001",
  "customer_id": "C1001",
  "agent_id": "A1001",
  "product_id": "P1001",
  "quantity": 2,
  "unit_price": 280.00,
  "total_amount": 560.00,
  "city": "Bengaluru",
  "distance_km": 6.4,
  "order_timestamp": "2026-08-16T08:30:00Z",
  "event_timestamp": "2026-08-16T08:30:01Z",
  "order_status": "PLACED"
}
```

------------------------------------------------------------------------

# 14. Kafka Producer

Create:

``` text
kafka/producer.py
```

Requirements:

-   Connect to Kafka using environment variables.
-   Serialize events as JSON.
-   Produce continuously.
-   Use delivery callbacks/logging.
-   Handle connection failures gracefully.
-   Do not hard-code credentials or broker addresses.
-   Support configurable topic name.
-   Support configurable generation rate.

------------------------------------------------------------------------

# 15. Kafka Consumer

Create:

``` text
kafka/consumer.py
```

Flow:

``` text
Kafka
  ↓
Consumer
  ↓
Validate event
  ↓
Transform event
  ↓
Insert PostgreSQL
```

Consumer responsibilities:

1.  Consume JSON event.
2.  Validate required fields.
3.  Validate data types.
4.  Reject malformed events.
5.  Log malformed events.
6.  Insert valid events into PostgreSQL.
7.  Handle duplicate events safely where possible.
8.  Commit Kafka offsets only after successful processing.
9.  Handle temporary database failures.
10. Provide useful logs.

Use a dead-letter strategy for invalid messages if practical.

------------------------------------------------------------------------

# 16. Phase 7 --- Real-Time KPI Engine

Build:

``` text
analytics/kpi_engine.py
```

The KPI engine must calculate metrics from incoming data.

At minimum:

``` text
total_orders
total_revenue
average_order_value
delivered_orders
cancelled_orders
cancellation_rate
average_delivery_time
average_distance
on_time_delivery_rate
active_agents
orders_per_minute
orders_last_5_minutes
revenue_last_5_minutes
```

Use rolling windows where appropriate.

Do not repeatedly scan huge raw datasets if a more efficient incremental
approach is practical.

For the MVP, correctness is more important than premature optimization.

------------------------------------------------------------------------

# 17. Dashboard Metrics Table

Create a table such as:

``` text
dashboard.kpi_summary
```

Possible columns:

``` text
updated_at
total_orders
total_revenue
average_order_value
average_delivery_minutes
cancellation_rate
on_time_delivery_rate
active_agents
orders_per_minute
orders_last_5_minutes
revenue_last_5_minutes
```

The table should be optimized for dashboard reads.

------------------------------------------------------------------------

# 18. Historical Analytics

Create analytical views/tables for:

``` text
daily_sales
hourly_sales
daily_orders
agent_performance
customer_summary
product_summary
city_summary
delivery_performance
```

The frontend should be able to query historical data independently from
live metrics.

------------------------------------------------------------------------

# 19. Phase 8 --- FastAPI Backend

Create:

``` text
backend/main.py
backend/routes/
backend/websocket/
```

Implement REST endpoints:

``` text
GET /api/health
GET /api/kpis
GET /api/orders
GET /api/orders/recent
GET /api/agents
GET /api/products
GET /api/customers
GET /api/cities
GET /api/analytics/hourly
GET /api/analytics/daily
GET /api/analytics/delivery
```

Use query parameters for filtering.

Examples:

``` text
/api/orders?city=Bengaluru
/api/orders?status=DELIVERED
/api/agents?city=Mumbai
```

Validate all inputs.

Do not expose database credentials through API responses.

------------------------------------------------------------------------

# 20. WebSocket API

Create:

``` text
/ws/dashboard
```

The WebSocket should send updated dashboard metrics.

Example payload:

``` json
{
  "type": "kpi_update",
  "timestamp": "2026-08-16T09:00:01Z",
  "data": {
    "total_orders": 12540,
    "total_revenue": 2484300,
    "average_order_value": 198.11,
    "average_delivery_minutes": 30.4,
    "cancellation_rate": 4.7,
    "orders_per_minute": 21
  }
}
```

The connection should handle:

-   disconnects
-   reconnects
-   multiple clients
-   exceptions
-   heartbeat/keepalive if necessary

------------------------------------------------------------------------

# 21. Phase 9 --- React Dashboard

Build a professional dashboard.

Suggested structure:

``` text
frontend/src/
│
├── components/
│   ├── KpiCard
│   ├── RevenueChart
│   ├── OrdersChart
│   ├── DeliveryChart
│   ├── AgentTable
│   ├── ProductTable
│   ├── RecentOrders
│   └── DeliveryMap
│
├── pages/
│   └── Dashboard
│
├── services/
│   ├── api.js
│   └── websocket.js
│
└── App.jsx
```

------------------------------------------------------------------------

# 22. Dashboard Layout

Create:

## Header

``` text
QuickDrop
Real-Time Delivery Analytics
Live indicator
Last updated timestamp
```

## KPI cards

``` text
Total Orders
Revenue
Average Order Value
Average Delivery Time
Cancellation Rate
On-Time Rate
Active Agents
Orders/Minute
```

## Charts

Include:

1.  Orders over time
2.  Revenue over time
3.  Delivery time trend
4.  Orders by city
5.  Revenue by category
6.  Agent performance

## Tables

Include:

-   Recent orders
-   Top agents
-   Top customers
-   Top products

## Map

Show:

-   delivery locations
-   order density
-   optionally status-based markers

------------------------------------------------------------------------

# 23. Real-Time Frontend Behavior

The dashboard must not require manual refresh for live KPIs.

When a new event is processed:

``` text
Python
 ↓
Kafka
 ↓
Consumer
 ↓
PostgreSQL
 ↓
KPI Engine
 ↓
FastAPI WebSocket
 ↓
React
```

The React dashboard updates automatically.

Historical filters may use REST API requests.

------------------------------------------------------------------------

# 24. Dashboard Filters

Implement filters for:

``` text
Date range
City
Order status
Category
Product
Delivery agent
Customer type
```

Filtering should update relevant charts/tables.

Keep filtering logic clean and avoid duplicating API code.

------------------------------------------------------------------------

# 25. Phase 10 --- Alerts

Implement rule-based alerts first.

Examples:

``` text
Cancellation rate > 15%
Average delivery time > 45 minutes
Orders per minute > configured threshold
Revenue per hour > configured threshold
Delivery delay significantly above normal
```

Example alert:

``` text
HIGH DELIVERY DELAY

City: Bengaluru
Current average: 62 minutes
Normal average: 29 minutes
Increase: 113%
```

Display alerts on the dashboard.

Do not implement ML anomaly detection until the rule-based system works.

------------------------------------------------------------------------

# 26. Phase 11 --- Anomaly Detection

After the MVP is stable, optionally add:

-   rolling mean
-   rolling standard deviation
-   z-score
-   Isolation Forest

Potential anomalies:

``` text
Unusual order spike
Unusual cancellation spike
Unusual delivery time
Unusual revenue drop
Unusual distance
```

Keep anomaly detection modular so it can be disabled without breaking
the core platform.

------------------------------------------------------------------------

# 27. Phase 12 --- Docker

Create Docker containers for:

``` text
PostgreSQL
Kafka
Kafka UI
Backend
Frontend
Data generator
Consumer
KPI engine
```

Use Docker Compose for local development.

The final developer experience should ideally be:

``` bash
docker compose up -d
```

followed by the documented commands needed to start application
services.

Provide health checks where practical.

------------------------------------------------------------------------

# 28. Environment Variables

Never hard-code secrets or environment-specific configuration.

Create:

``` text
.env.example
```

Example variables:

``` text
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=

KAFKA_BOOTSTRAP_SERVERS=
KAFKA_TOPIC=
KAFKA_GROUP_ID=

API_HOST=
API_PORT=

VITE_API_URL=
VITE_WS_URL=
```

Never commit `.env`.

------------------------------------------------------------------------

# 29. Testing

Create tests for:

## Data generation

-   valid customer IDs
-   valid product prices
-   valid timestamps
-   valid coordinates
-   valid order relationships

## Analytics

-   revenue calculation
-   average order value
-   cancellation rate
-   delivery time
-   on-time rate

## API

-   health endpoint
-   KPI endpoint
-   filtering
-   invalid parameters

## WebSocket

-   connection
-   message format
-   reconnect behavior where practical

## Consumer

-   valid event
-   invalid event
-   duplicate event
-   database failure behavior

Use pytest.

------------------------------------------------------------------------

# 30. Logging

Use Python's `logging` module.

Logs should include:

``` text
timestamp
service
log level
message
order/event ID where relevant
```

Examples:

``` text
INFO  Kafka producer connected
INFO  Order ORD100001 published
INFO  Order ORD100001 inserted
WARNING Invalid order event
ERROR PostgreSQL connection failed
```

Do not log sensitive information unnecessarily.

------------------------------------------------------------------------

# 31. Error Handling

The system must fail gracefully.

Handle:

-   Kafka unavailable
-   PostgreSQL unavailable
-   malformed JSON
-   missing fields
-   duplicate events
-   WebSocket disconnect
-   API database timeout
-   frontend WebSocket disconnect

Do not silently swallow exceptions.

Use meaningful error messages.

------------------------------------------------------------------------

# 32. Data Quality Rules

Validate:

``` text
order_id is not null
customer_id exists
agent_id exists
product_id exists
quantity > 0
price >= 0
distance_km >= 0
latitude valid
longitude valid
delivery_timestamp >= order_timestamp
```

Invalid records should be logged and rejected or routed to a dead-letter
mechanism.

------------------------------------------------------------------------

# 33. Performance Requirements

Do not optimize prematurely.

First make the system correct.

After the MVP works, test:

``` text
1 event/sec
10 events/sec
50 events/sec
100 events/sec
```

Measure:

-   producer throughput
-   consumer throughput
-   database insert latency
-   KPI processing latency
-   API response time
-   WebSocket update latency

Do not claim "real-time" performance numbers without measuring them.

------------------------------------------------------------------------

# 34. Security Requirements

Even though this is a portfolio project:

-   Keep secrets in environment variables.
-   Validate API input.
-   Use parameterized SQL / ORM queries.
-   Never construct SQL using unsafe string concatenation.
-   Do not expose database credentials.
-   Restrict CORS appropriately for production.
-   Avoid logging secrets.
-   Validate WebSocket input if client messages are accepted.
-   Use HTTPS/WSS in production.

------------------------------------------------------------------------

# 35. Documentation

Create:

``` text
README.md
docs/architecture.md
docs/database.md
docs/kafka.md
docs/api.md
docs/dashboard.md
docs/setup.md
```

README must contain:

1.  Project overview
2.  Architecture diagram
3.  Technology stack
4.  Features
5.  Project structure
6.  Prerequisites
7.  Installation
8.  Environment setup
9.  Docker setup
10. How to generate data
11. How to start Kafka
12. How to start consumer
13. How to start backend
14. How to start frontend
15. API documentation
16. KPI definitions
17. Screenshots section
18. Testing
19. Future improvements

------------------------------------------------------------------------

# 36. Git Strategy

Use meaningful commits.

Examples:

``` text
feat: add project structure
feat: implement synthetic data generator
feat: add PostgreSQL schema
feat: add SQL analytics
feat: add Kafka producer
feat: add Kafka consumer
feat: implement KPI engine
feat: add FastAPI APIs
feat: add dashboard websocket
feat: create React dashboard
feat: add delivery map
feat: add alerts
chore: dockerize services
test: add analytics tests
docs: update setup guide
```

Do not commit:

``` text
.env
venv/
node_modules/
__pycache__/
*.log
```

------------------------------------------------------------------------

# 37. MVP Definition

The MVP is complete only when this pipeline works end-to-end:

``` text
Python simulator
       ↓
Kafka
       ↓
Kafka consumer
       ↓
PostgreSQL
       ↓
KPI calculation
       ↓
FastAPI
       ↓
WebSocket
       ↓
React
```

The dashboard must show live:

``` text
Total Orders
Revenue
Average Order Value
Average Delivery Time
Cancellation Rate
Orders Per Minute
```

and at least:

``` text
Orders over time
Revenue over time
Delivery time chart
Recent orders table
Delivery map
```

------------------------------------------------------------------------

# 38. Final Version Definition

The final project should include:

-   Synthetic real-time data generation
-   Kafka event streaming
-   PostgreSQL storage
-   Data validation
-   SQL analytics
-   Real-time KPI engine
-   Historical analytics
-   FastAPI REST APIs
-   WebSocket live updates
-   React dashboard
-   Interactive map
-   Filtering
-   Agent analytics
-   Customer analytics
-   Product analytics
-   City analytics
-   Rule-based alerts
-   Optional anomaly detection
-   Docker Compose
-   Automated tests
-   Logging
-   Documentation
-   GitHub-ready repository

------------------------------------------------------------------------

# 39. Future Enhancements

Only after the core project works, consider:

``` text
Apache Spark
Apache Flink
Redis
Airflow
Prometheus
Grafana
Data warehouse
dbt
AWS
Azure
GCP
Kubernetes
ML demand forecasting
ML ETA prediction
Customer churn prediction
Dynamic delivery pricing
```

These are optional extensions, not MVP requirements.

------------------------------------------------------------------------

# 40. AI Agent Behavior

You are the software engineering agent responsible for implementing this
project.

Follow these rules:

1.  Act as a senior software engineer mentoring a beginner.
2.  Explain concepts before introducing unfamiliar technologies.
3.  Build incrementally.
4.  Do not skip setup or validation.
5.  Do not generate fake successful test results.
6.  Do not claim that something works unless it has been tested or
    clearly state that it is unverified.
7.  Prefer simple, maintainable solutions over unnecessary complexity.
8.  Use environment variables for configuration.
9.  Use clean architecture and separation of concerns.
10. Avoid unnecessary dependencies.
11. Write production-quality but beginner-readable code.
12. Add comments only where they improve understanding.
13. Use type hints in Python.
14. Use meaningful names.
15. Handle errors explicitly.
16. Include tests for important logic.
17. Keep frontend, backend, streaming, database, and analytics
    responsibilities separated.
18. Do not introduce advanced technologies before the basic system is
    working.
19. When modifying existing code, inspect the relevant files before
    changing them.
20. Never overwrite working code blindly.
21. When a command fails, diagnose the error before proposing another
    command.
22. Keep a running implementation status.
23. At the end of each phase, provide exact commands to run.
24. If a decision has multiple valid approaches, choose the simplest
    appropriate approach and explain the tradeoff.
25. Ask for clarification only when a decision genuinely blocks
    implementation; otherwise make a reasonable engineering decision and
    continue.

------------------------------------------------------------------------

# 41. Required Implementation Order

Implement exactly in this general order:

``` text
1. Project setup
2. Python environment
3. Data model
4. Synthetic data generator
5. PostgreSQL schema
6. Load/test static data
7. SQL analytics
8. Kafka infrastructure
9. Kafka producer
10. Kafka consumer
11. PostgreSQL streaming ingestion
12. KPI engine
13. Dashboard analytics tables/views
14. FastAPI REST API
15. WebSocket
16. React dashboard
17. Charts
18. Map
19. Filters
20. Alerts
21. Tests
22. Dockerization
23. Documentation
24. Performance testing
25. Optional advanced analytics
26. Deployment
```

------------------------------------------------------------------------

# 42. First Task for the AI Agent

Do NOT implement the entire project immediately.

Start with **Phase 1: Project Setup**.

First:

1.  Explain the architecture in beginner-friendly terms.
2.  Create the project directory structure.
3.  Create the Python virtual environment instructions.
4.  Create `requirements.txt`.
5.  Create `.gitignore`.
6.  Create `.env.example`.
7.  Create a minimal `README.md`.
8.  Create a basic Docker Compose skeleton.
9.  Explain every important file.
10. Provide commands to verify the setup.

After Phase 1 is complete, move to Phase 2.

------------------------------------------------------------------------

# 43. Success Criteria

The project is successful when a developer can run the documented setup
and observe:

``` text
Python continuously creates orders
            ↓
Kafka receives events
            ↓
Consumer processes events
            ↓
PostgreSQL receives records
            ↓
KPIs update
            ↓
FastAPI exposes analytics
            ↓
React dashboard receives WebSocket updates
            ↓
Dashboard updates without browser refresh
```

The final application should look and behave like a small real-time
analytics platform for a delivery company rather than merely a static
dashboard.

# End of Specification
