from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class CustomerType(str, Enum):
    premium = "Premium"
    regular = "Regular"
    occasional = "Occasional"


class VehicleType(str, Enum):
    bike = "Bike"
    scooter = "Scooter"
    bicycle = "Bicycle"


class ProductCategory(str, Enum):
    food = "Food"
    groceries = "Groceries"
    pharmacy = "Pharmacy"
    electronics = "Electronics"
    bakery = "Bakery"
    beverages = "Beverages"


class OrderStatus(str, Enum):
    placed = "PLACED"
    accepted = "ACCEPTED"
    picked_up = "PICKED_UP"
    delivered = "DELIVERED"
    cancelled = "CANCELLED"


class PaymentMethod(str, Enum):
    upi = "UPI"
    card = "CARD"
    cash = "CASH"
    wallet = "WALLET"


class Customer(BaseModel):
    customer_id: str
    customer_name: str
    phone: str
    city: str
    registration_date: date
    customer_type: CustomerType
    ordering_score: float = Field(ge=0.1, le=5.0)


class DeliveryAgent(BaseModel):
    agent_id: str
    agent_name: str
    phone: str
    vehicle_type: VehicleType
    city: str
    rating: float = Field(ge=1.0, le=5.0)
    joining_date: date
    efficiency_score: float = Field(ge=0.6, le=1.4)


class Product(BaseModel):
    product_id: str
    product_name: str
    category: ProductCategory
    price: float = Field(ge=0)
    store_name: str


class OrderEvent(BaseModel):
    order_id: str
    customer_id: str
    agent_id: str
    product_id: str
    city: str
    quantity: int = Field(gt=0)
    unit_price: float = Field(ge=0)
    total_amount: float = Field(ge=0)
    order_timestamp: datetime
    pickup_timestamp: datetime | None = None
    delivery_timestamp: datetime | None = None
    promised_delivery_timestamp: datetime | None = None
    delivery_latitude: float = Field(ge=-90, le=90)
    delivery_longitude: float = Field(ge=-180, le=180)
    distance_km: float = Field(ge=0)
    order_status: OrderStatus
    payment_method: PaymentMethod
    event_timestamp: datetime

    @field_validator("total_amount")
    @classmethod
    def validate_total_amount(cls, value: float, info) -> float:
        quantity = info.data.get("quantity")
        unit_price = info.data.get("unit_price")
        if quantity is not None and unit_price is not None:
            expected = round(quantity * unit_price, 2)
            if round(value, 2) != expected:
                raise ValueError("total_amount must equal quantity * unit_price")
        return round(value, 2)


class KpiSummary(BaseModel):
    updated_at: datetime
    total_orders: int
    total_revenue: float
    average_order_value: float
    delivered_orders: int
    cancelled_orders: int
    cancellation_rate: float
    average_delivery_minutes: float
    average_distance: float
    on_time_delivery_rate: float
    active_agents: int
    orders_per_minute: int
    orders_last_5_minutes: int
    revenue_last_5_minutes: float


class ChartPoint(BaseModel):
    label: str
    orders: int = 0
    revenue: float = 0
    average_delivery_minutes: float = 0


class CityMetric(BaseModel):
    city: str
    total_orders: int
    total_revenue: float
    average_delivery_minutes: float
    average_distance: float
    cancellation_rate: float


class CategoryMetric(BaseModel):
    category: str
    total_orders: int
    total_revenue: float


class AgentMetric(BaseModel):
    agent_id: str
    agent_name: str
    city: str
    deliveries: int
    average_delivery_minutes: float
    revenue_handled: float
    rating: float


class CustomerMetric(BaseModel):
    customer_id: str
    customer_name: str
    city: str
    total_orders: int
    total_revenue: float
    average_order_value: float
    customer_type: CustomerType


class ProductMetric(BaseModel):
    product_id: str
    product_name: str
    category: ProductCategory
    quantity_sold: int
    total_revenue: float


class LocationPoint(BaseModel):
    order_id: str
    city: str
    latitude: float
    longitude: float
    status: OrderStatus
    amount: float


class Alert(BaseModel):
    level: Literal["info", "warning", "critical"]
    title: str
    body: str
    city: str | None = None


class DashboardSnapshot(BaseModel):
    timestamp: datetime
    filters_applied: dict[str, str | int | None]
    kpis: KpiSummary
    hourly_metrics: list[ChartPoint]
    daily_metrics: list[ChartPoint]
    delivery_metrics: list[CityMetric]
    revenue_by_category: list[CategoryMetric]
    top_agents: list[AgentMetric]
    top_customers: list[CustomerMetric]
    top_products: list[ProductMetric]
    recent_orders: list[OrderEvent]
    locations: list[LocationPoint]
    alerts: list[Alert]


class DashboardSocketMessage(BaseModel):
    type: Literal["kpi_update"]
    timestamp: datetime
    data: DashboardSnapshot


class DashboardFilters(BaseModel):
    city: str | None = None
    status: OrderStatus | None = None
    category: ProductCategory | None = None
    product_id: str | None = None
    agent_id: str | None = None
    customer_type: CustomerType | None = None
    start_date: date | None = None
    end_date: date | None = None
    limit: int = Field(default=25, ge=1, le=200)
