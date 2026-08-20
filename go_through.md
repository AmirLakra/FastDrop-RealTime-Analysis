# QuickDrop Project Go-Through

This document explains the project in a beginner-friendly way.

## Step 2: Create Python virtual environment

This step is about setting up an isolated Python environment for the project.

Why we need it:
- Different projects may need different package versions.
- A virtual environment keeps this project clean and avoids conflicts.
- This project uses packages like FastAPI, Pydantic, Faker, NumPy, psycopg, and Kafka libraries.

Relevant files:
- [requirements.txt](requirements.txt)
- [.venv](.venv)

Commands:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

What each command does:

- `python -m venv .venv`
  - creates a folder named `.venv`
  - this folder stores the virtual environment

- `.~\.venv\Scripts\Activate.ps1`
  - activates the environment
  - after this, the terminal uses the project’s Python instead of the system Python

- `pip install -r requirements.txt`
  - reads [requirements.txt](requirements.txt)
  - installs all required libraries

What is inside [requirements.txt](requirements.txt)?
It contains libraries like:
- fastapi
- uvicorn
- pydantic
- pydantic-settings
- psycopg
- faker
- numpy
- pandas
- confluent-kafka
- pytest
- websockets

These libraries are used for:
- creating the backend API
- generating fake data
- connecting to PostgreSQL
- sending/receiving Kafka messages
- running tests
- real-time WebSocket communication

Simple beginner explanation:
- Step 2 is basically: “Install a clean Python environment so the project can run correctly.”

## Step 3: Generate customers, products, and agents

This is the first real data generation step.

Relevant files:
- [data_generator/generator.py](data_generator/generator.py)
- [common/schemas.py](common/schemas.py)
- [common/config.py](common/config.py)
- [common/cities.py](common/cities.py)

What is being generated?
- Customers
- Delivery agents
- Products

These are not random junk data. They are realistic objects structured for a delivery platform.

The project uses Pydantic models to define them.
Open [common/schemas.py](common/schemas.py).

Here are the main models:

- `Customer`
- `DeliveryAgent`
- `Product`
- `OrderEvent`

Example:

```python
class Customer(BaseModel):
    customer_id: str
    customer_name: str
    phone: str
    city: str
    registration_date: date
    customer_type: CustomerType
    ordering_score: float
```

This means:
- every customer has:
  - id
  - name
  - phone
  - city
  - registration date
  - customer type
  - ordering score

And for agents:

```python
class DeliveryAgent(BaseModel):
    agent_id: str
    agent_name: str
    phone: str
    vehicle_type: VehicleType
    city: str
    rating: float
    joining_date: date
    efficiency_score: float
```

This means:
- each agent has a city, rating, vehicle type, and performance score.

And for products:

```python
class Product(BaseModel):
    product_id: str
    product_name: str
    category: ProductCategory
    price: float
    store_name: str
```

This means:
- each product has a category like Food, Groceries, Pharmacy, etc.

Now let’s look at the generator file:
- [data_generator/generator.py](data_generator/generator.py)

Important class:

```python
class QuickDropGenerator:
```

Inside `__init__`:

```python
self.customers = self._generate_customers()
self.agents = self._generate_agents()
self.products = self._generate_products()
```

This means:
- when the generator object is created, it immediately generates:
  - customers
  - agents
  - products

The generator also uses settings from [common/config.py](common/config.py), such as:
- number of customers
- number of agents
- number of products
- supported cities

Example:

```python
number_of_customers: int = 500
number_of_agents: int = 80
number_of_products: int = 120
```

So by default, the app will generate:
- 500 customers
- 80 delivery agents
- 120 products

How customer generation works
Look at the method:

```python
def _generate_customers(self) -> dict[str, Customer]:
```

This method:
- loops through the desired number of customers
- picks a random city from supported cities
- picks a customer type:
  - Premium
  - Regular
  - Occasional
- gives them a realistic ordering score
- creates a `Customer` object
- stores it in a dictionary

Example logic:

```python
customer_type = self.random.choices(
    [CustomerType.premium, CustomerType.regular, CustomerType.occasional],
    weights=[0.18, 0.57, 0.25],
    k=1,
)[0]
```

This means:
- 18% are premium
- 57% are regular
- 25% are occasional

This is realistic business simulation.

How agent generation works
Method:

```python
def _generate_agents(self) -> dict[str, DeliveryAgent]:
```

This method:
- creates each agent with a random city
- chooses a vehicle type:
  - Bike
  - Scooter
  - Bicycle
- gives the agent a rating
- gives the agent an efficiency score
- stores them in a dictionary

How product generation works
Method:

```python
def _generate_products(self) -> dict[str, Product]:
```

This method:
- picks category randomly
- uses pre-defined product names for each category
- assigns price based on category
- stores products in a dictionary

Example categories:
- Food
- Groceries
- Pharmacy
- Electronics
- Bakery
- Beverages

This is important because orders later will reference a product by `product_id`.

How city support works
The city system lives in:
- [common/cities.py](common/cities.py)

It contains city metadata:
- Bengaluru
- Delhi
- Mumbai
- Hyderabad
- Pune
- Kolkata
- Chennai
- Bhubaneswar

This helps the generator:
- choose cities with realistic demand
- generate coordinates for delivery locations
- distribute orders based on city popularity

Example:

```python
CITY_SPECS = {
    "Bengaluru": CitySpec("Bengaluru", 12.9716, 77.5946, 1.35),
    ...
}
```

The `demand_multiplier` gives some cities more order activity than others.

Why Step 3 matters
This step creates the master data before order generation.

Why is this necessary?
Because orders will later reference:
- a customer
- an agent
- a product

Without customers, agents, and products, orders would have no real entities to connect to.

So the flow is:
- generate master data
- then generate orders using those entities

Very simple beginner summary:
- Step 2 = set up the Python environment
- Step 3 = create the base population of the app:
  - customers
  - agents
  - products

## Final beginner summary

The overall flow is:
1. Set up Python environment
2. Create realistic customer, agent, and product records
3. Use them to generate realistic orders later

This keeps the project grounded in realistic business entities before streaming, storing, and analyzing the data.
