# 🗺️ QuickDrop Project Roadmap

Whether you are building this project from scratch, or trying to learn how all the pieces fit together, this roadmap outlines the logical, step-by-step phases of development. 

Building a real-time streaming platform can be overwhelming if you try to do it all at once. By following this roadmap, you tackle one isolated piece of the architecture at a time.

---

## 🛑 Phase 1: Foundation & Setup
Before writing any business logic, you need a solid foundation.
* **Initialize Repository:** Create the folder structure (`backend/`, `frontend/`, `kafka/`, `database/`, etc.).
* **Environment Setup:** Set up a Python virtual environment (`.venv`) and install dependencies via `requirements.txt`.
* **Configuration:** Create a `.env` file to hold database passwords and Kafka ports safely.
* **Docker Skeleton:** Create a `docker-compose.yml` file to run PostgreSQL and Kafka locally so you don't have to install them manually on your machine.

---

## 🏗️ Phase 2: The Data Model
You cannot build analytics without knowing what your data looks like.
* **Define Entities:** Map out the properties for `Customers`, `Delivery Agents`, and `Products`.
* **Define the Fact Table:** Map out the `Orders` event. What is the lifecycle of an order? (PLACED -> PICKED_UP -> DELIVERED).
* **Pydantic Schemas:** Write these models in Python (`common/schemas.py`) so the code can validate data later.

---

## 🎲 Phase 3: The Data Simulator
Since we don't have a live production app, we need to fake it realistically.
* **Generate Master Data:** Write Python scripts using the `Faker` library to generate thousands of fake users, agents, and products.
* **Generate Realistic Orders:** Write a loop that picks a random customer and product, calculates a fake distance, and estimates a realistic delivery time based on that distance (`data_generator/generator.py`).
* **Test the Stream:** Run the generator in the terminal just to watch fake JSON orders print to the screen.

---

## 🗄️ Phase 4: Database & SQL Analytics
Now that we have data, we need a place to put it and analyze it.
* **PostgreSQL Setup:** Create three schemas: `raw` (for raw data), `analytics` (for heavy queries), and `dashboard` (for fast UI summaries).
* **Create Tables:** Write the SQL `CREATE TABLE` scripts for all the entities you designed in Phase 2 (`database/schema.sql`).
* **Write Analytical Views:** Write advanced SQL queries (using `GROUP BY`, `JOIN`, and aggregations) to calculate total revenue, average delivery times, and top agents (`database/views.sql`).

---

## 🚀 Phase 5: Kafka Streaming (The Pipeline)
It's time to connect the data simulator to the database using an event stream.
* **The Producer:** Modify your data simulator to push the JSON orders into an Apache Kafka topic instead of just printing them to the screen (`kafka/producer.py`).
* **The Consumer:** Write a backend Python script that listens to the Kafka topic. When it hears an order, it validates it with Pydantic, and executes an `INSERT INTO` SQL command to save it into PostgreSQL (`kafka/consumer.py`).
* **Resilience Testing:** Turn off the database, send some orders to Kafka, and turn the database back on to ensure the consumer gracefully handles errors without losing data.

---

## ⚙️ Phase 6: Real-Time KPI Engine
If we query the database every second for live updates, the database will crash. We need a middleman.
* **In-Memory Tracking:** Build a Python engine (`analytics/kpi_engine.py`) that watches the stream of orders and keeps a running tally of "revenue in the last 5 minutes" and "active agents".
* **Dashboard Snapshots:** Have this engine generate a tiny, optimized JSON snapshot of current metrics that the frontend can read instantly.

---

## 🔌 Phase 7: FastAPI Backend & WebSockets
We need to expose our database and KPI engine to the internet.
* **REST APIs:** Build standard `GET` endpoints in FastAPI (e.g., `/api/orders` or `/api/agents`) so the frontend can load historical data.
* **WebSockets:** Create a persistent `ws://` endpoint. Whenever the KPI Engine generates a new snapshot, push that JSON payload through the WebSocket directly to the browser.

---

## 💻 Phase 8: The React Dashboard
The final step is to make it look beautiful.
* **UI Scaffolding:** Set up a React app using Vite and TailwindCSS (or vanilla CSS).
* **WebSocket Integration:** Write React hooks to connect to the FastAPI WebSocket. When data arrives, save it to React state.
* **Data Visualization:** Hook up the React state to `Recharts` to draw live line graphs and bar charts.
* **Live Map:** Hook up the React state to `Leaflet` to plot the `delivery_latitude` and `longitude` of active orders on an interactive map.

---

## 🎓 Next Steps (Future Enhancements)
Once the MVP (Minimum Viable Product) is built, here is the roadmap for scaling it to enterprise level:
1. **Machine Learning:** Add a Python microservice that reads the Kafka stream and predicts "Estimated Time of Delivery" using a trained ML model.
2. **Cloud Migration:** Move Kafka to Confluent Cloud or AWS MSK, and move PostgreSQL to Amazon RDS.
3. **Authentication:** Add JWT (JSON Web Tokens) so only authorized managers can view the React dashboard.
