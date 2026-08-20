# Architecture

QuickDrop has two useful execution paths:

1. Demo mode: the backend generates live orders in memory, computes metrics, and pushes them directly to the dashboard.
2. Production-style path: the generator publishes orders to Kafka, the consumer validates them, PostgreSQL stores them, analytics views aggregate them, and FastAPI serves the results.

That split makes the repo beginner-friendly without losing the real system design.

