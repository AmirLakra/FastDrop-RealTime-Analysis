from __future__ import annotations

import random
from collections import defaultdict
from datetime import UTC, date, datetime, timedelta

from common.cities import demand_weight, random_coordinate
from common.config import Settings
from common.schemas import (
    Customer,
    CustomerType,
    DeliveryAgent,
    OrderEvent,
    OrderStatus,
    PaymentMethod,
    Product,
    ProductCategory,
    VehicleType,
)

try:
    from faker import Faker
except ImportError:  # pragma: no cover
    Faker = None


FIRST_NAMES = ["Aarav", "Neha", "Arjun", "Sana", "Rohan", "Anaya", "Kabir", "Mira"]
LAST_NAMES = ["Sharma", "Patel", "Rao", "Das", "Singh", "Mehta", "Khan", "Nair"]
STORE_PREFIXES = ["Daily", "Urban", "Fresh", "Metro", "Quick", "Prime", "Swift", "Smart"]
STORE_SUFFIXES = ["Mart", "Kitchen", "Pharmacy", "Foods", "Store", "Corner", "Bazaar"]
PRODUCT_CATALOG = {
    ProductCategory.food: ["Paneer Bowl", "Chicken Wrap", "Biryani Box", "Pasta Meal"],
    ProductCategory.groceries: ["Rice Pack", "Fruit Basket", "Milk Combo", "Household Kit"],
    ProductCategory.pharmacy: ["Vitamin Pack", "Pain Relief Kit", "Cold Care Box", "First Aid Pack"],
    ProductCategory.electronics: ["Power Bank", "Earbuds", "Phone Cable", "Smart Bulb"],
    ProductCategory.bakery: ["Chocolate Cake", "Croissant Box", "Bread Loaf", "Cookie Pack"],
    ProductCategory.beverages: ["Cold Brew", "Juice Crate", "Tea Pack", "Energy Drink"],
}
PRICE_BANDS = {
    ProductCategory.food: (140, 420),
    ProductCategory.groceries: (90, 380),
    ProductCategory.pharmacy: (120, 520),
    ProductCategory.electronics: (250, 1800),
    ProductCategory.bakery: (80, 340),
    ProductCategory.beverages: (60, 260),
}


class QuickDropGenerator:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.random = random.Random(42)
        self.faker = Faker("en_IN") if Faker else None
        if self.faker:
            self.faker.seed_instance(42)

        self.customer_counter = 1000
        self.agent_counter = 1000
        self.product_counter = 1000
        self.order_counter = 100000

        self.customers = self._generate_customers()
        self.agents = self._generate_agents()
        self.products = self._generate_products()

        self.customers_by_city = self._group_by_city(self.customers.values())
        self.agents_by_city = self._group_by_city(self.agents.values())
        self.product_ids = list(self.products.keys())

    def _group_by_city(self, items):
        grouped = defaultdict(list)
        for item in items:
            grouped[item.city].append(item)
        return grouped

    def _name(self) -> str:
        if self.faker:
            return self.faker.name()
        return f"{self.random.choice(FIRST_NAMES)} {self.random.choice(LAST_NAMES)}"

    def _phone(self) -> str:
        if self.faker:
            return self.faker.phone_number()
        return f"+91-9{self.random.randint(100000000, 999999999)}"

    def _store(self) -> str:
        return f"{self.random.choice(STORE_PREFIXES)} {self.random.choice(STORE_SUFFIXES)}"

    def _generate_customers(self) -> dict[str, Customer]:
        result: dict[str, Customer] = {}
        cities = self.settings.supported_city_list
        weights = [demand_weight(city) for city in cities]
        for _ in range(self.settings.number_of_customers):
            self.customer_counter += 1
            customer_type = self.random.choices(
                [CustomerType.premium, CustomerType.regular, CustomerType.occasional],
                weights=[0.18, 0.57, 0.25],
                k=1,
            )[0]
            ordering_score = {
                CustomerType.premium: self.random.uniform(2.6, 4.8),
                CustomerType.regular: self.random.uniform(1.3, 3.4),
                CustomerType.occasional: self.random.uniform(0.4, 1.6),
            }[customer_type]
            city = self.random.choices(cities, weights=weights, k=1)[0]
            customer = Customer(
                customer_id=f"C{self.customer_counter}",
                customer_name=self._name(),
                phone=self._phone(),
                city=city,
                registration_date=date.today() - timedelta(days=self.random.randint(20, 900)),
                customer_type=customer_type,
                ordering_score=round(ordering_score, 2),
            )
            result[customer.customer_id] = customer
        return result

    def _generate_agents(self) -> dict[str, DeliveryAgent]:
        result: dict[str, DeliveryAgent] = {}
        cities = self.settings.supported_city_list
        weights = [demand_weight(city) for city in cities]
        for _ in range(self.settings.number_of_agents):
            self.agent_counter += 1
            city = self.random.choices(cities, weights=weights, k=1)[0]
            agent = DeliveryAgent(
                agent_id=f"A{self.agent_counter}",
                agent_name=self._name(),
                phone=self._phone(),
                vehicle_type=self.random.choices(
                    [VehicleType.bike, VehicleType.scooter, VehicleType.bicycle],
                    weights=[0.44, 0.36, 0.20],
                    k=1,
                )[0],
                city=city,
                rating=round(self.random.uniform(3.8, 5.0), 2),
                joining_date=date.today() - timedelta(days=self.random.randint(40, 1200)),
                efficiency_score=round(self.random.uniform(0.78, 1.28), 2),
            )
            result[agent.agent_id] = agent
        return result

    def _generate_products(self) -> dict[str, Product]:
        result: dict[str, Product] = {}
        categories = list(ProductCategory)
        for _ in range(self.settings.number_of_products):
            self.product_counter += 1
            category = self.random.choice(categories)
            min_price, max_price = PRICE_BANDS[category]
            product = Product(
                product_id=f"P{self.product_counter}",
                product_name=self.random.choice(PRODUCT_CATALOG[category]),
                category=category,
                price=round(self.random.uniform(min_price, max_price), 2),
                store_name=self._store(),
            )
            result[product.product_id] = product
        return result

    def generate_order(self, *, backfill: bool = False) -> OrderEvent:
        self.order_counter += 1
        cities = self.settings.supported_city_list
        weights = [demand_weight(city) for city in cities]
        city = self.random.choices(cities, weights=weights, k=1)[0]

        customer = self.random.choices(
            self.customers_by_city[city],
            weights=[item.ordering_score for item in self.customers_by_city[city]],
            k=1,
        )[0]
        agent = self.random.choice(self.agents_by_city[city])
        product = self.products[self.random.choice(self.product_ids)]

        quantity = self.random.choices([1, 2, 3, 4], weights=[0.46, 0.33, 0.15, 0.06], k=1)[0]
        unit_price = product.price
        total_amount = round(quantity * unit_price, 2)

        now = datetime.now(UTC)
        offset_minutes = self.random.randint(0, 720) if backfill else self.random.randint(0, 6)
        order_timestamp = now - timedelta(minutes=offset_minutes)
        distance_km = round(self.random.uniform(0.9, 12.5) * demand_weight(city) / 1.1, 2)
        prep_minutes = self.random.uniform(6, 15) + quantity * self.random.uniform(1.2, 2.2)
        traffic_factor = self.random.uniform(0.9, 1.45)
        vehicle_factor = {
            VehicleType.bike: 0.95,
            VehicleType.scooter: 1.0,
            VehicleType.bicycle: 1.25,
        }[agent.vehicle_type]
        travel_minutes = (
            distance_km * self.random.uniform(3.4, 5.8) * traffic_factor * vehicle_factor
        ) / agent.efficiency_score
        delivery_minutes = prep_minutes + travel_minutes
        promised_minutes = delivery_minutes * self.random.uniform(1.02, 1.18)

        status = self.random.choices(
            [
                OrderStatus.delivered,
                OrderStatus.picked_up,
                OrderStatus.accepted,
                OrderStatus.placed,
                OrderStatus.cancelled,
            ],
            weights=[0.68, 0.09, 0.08, 0.09, 0.06] if not backfill else [0.82, 0.02, 0.02, 0.02, 0.12],
            k=1,
        )[0]

        pickup_timestamp = order_timestamp + timedelta(minutes=round(prep_minutes))
        promised_delivery_timestamp = order_timestamp + timedelta(minutes=round(promised_minutes))
        delivery_timestamp = None

        if status == OrderStatus.delivered:
            delivery_timestamp = order_timestamp + timedelta(minutes=round(delivery_minutes))
        elif status == OrderStatus.cancelled:
            pickup_timestamp = None
        elif status in {OrderStatus.placed, OrderStatus.accepted}:
            pickup_timestamp = None

        latitude, longitude = random_coordinate(city, radius_km=max(2.0, distance_km))

        return OrderEvent(
            order_id=f"ORD{self.order_counter}",
            customer_id=customer.customer_id,
            agent_id=agent.agent_id,
            product_id=product.product_id,
            city=city,
            quantity=quantity,
            unit_price=unit_price,
            total_amount=total_amount,
            order_timestamp=order_timestamp,
            pickup_timestamp=pickup_timestamp,
            delivery_timestamp=delivery_timestamp,
            promised_delivery_timestamp=promised_delivery_timestamp,
            delivery_latitude=latitude,
            delivery_longitude=longitude,
            distance_km=distance_km,
            order_status=status,
            payment_method=self.random.choice(list(PaymentMethod)),
            event_timestamp=now if not backfill else order_timestamp + timedelta(seconds=self.random.randint(0, 50)),
        )

    def generate_batch(self, count: int, *, backfill: bool = False) -> list[OrderEvent]:
        return [self.generate_order(backfill=backfill) for _ in range(count)]

