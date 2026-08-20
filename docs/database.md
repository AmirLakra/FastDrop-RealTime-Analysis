# Database

PostgreSQL stores both the normalized delivery model and analytical views.

Core tables:

- `customers`
- `delivery_agents`
- `products`
- `orders`

Analytical schemas:

- `raw`
- `analytics`
- `dashboard`

The schema and views live in:

- `database/schema.sql`
- `database/views.sql`

