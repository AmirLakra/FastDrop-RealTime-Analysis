# QuickDrop Real-Time Delivery Analytics Platform

QuickDrop is a full-stack portfolio project for a fictional delivery company. It simulates realistic order activity, prepares the project for Kafka and PostgreSQL streaming, serves analytics through FastAPI, and displays live KPIs in a modern React dashboard.

## What is included

- Realistic synthetic customers, agents, products, and orders
- Kafka producer and consumer modules
- PostgreSQL schema and analytics views
- FastAPI REST APIs and WebSocket stream
- Rule-based alerts
- React dashboard with filters, charts, tables, and a delivery map
- Docker Compose skeleton for local infrastructure
- Tests for generation, analytics, and API behavior

## Beginner-friendly architecture

1. `data_generator/` creates realistic delivery orders.
2. `kafka/` is ready to publish and consume those orders as live events.
3. `database/` defines PostgreSQL tables and reusable analytics views.
4. `analytics/` calculates KPI summaries and leaderboard metrics.
5. `backend/` exposes REST endpoints and pushes live dashboard updates over WebSockets.
6. `frontend/` renders the live analytics interface.

To keep the project usable even before Kafka and PostgreSQL are running, the backend also includes a demo mode that generates live orders in memory. That gives you an end-to-end dashboard right away, while still keeping the production-style Kafka and database modules in the repo.

## Project structure

```text
quickdrop-analytics/
├── analytics/
├── backend/
├── common/
├── data_generator/
├── database/
├── docker/
├── docs/
├── frontend/
├── kafka/
├── tests/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
└── requirements.txt
```

## Local setup

### Python

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Backend

```powershell
Copy-Item .env.example .env
uvicorn backend.main:app --reload
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

### Docker infrastructure

```powershell
docker compose up -d postgres kafka kafka-ui
```

## API endpoints

- `GET /api/health`
- `GET /api/dashboard`
- `GET /api/kpis`
- `GET /api/orders`
- `GET /api/orders/recent`
- `GET /api/agents`
- `GET /api/products`
- `GET /api/customers`
- `GET /api/cities`
- `GET /api/analytics/hourly`
- `GET /api/analytics/daily`
- `GET /api/analytics/delivery`
- `GET /api/alerts`
- `WS /ws/dashboard`

## Useful commands

Finite data generation:

```powershell
python data_generator/generate_data.py --count 100
```

Streaming generator to stdout:

```powershell
python data_generator/generate_stream.py --rate 5
```

Kafka producer:

```powershell
python kafka/producer.py --rate 5
```

Kafka consumer:

```powershell
python kafka/consumer.py
```

Run tests:

```powershell
pytest
```

## MVP note

The repo is organized to support the final Kafka -> PostgreSQL -> KPI -> FastAPI -> WebSocket -> React pipeline. In this environment, the live demo path uses the in-memory backend pipeline by default so the dashboard can update immediately without needing every external service to be running first.

