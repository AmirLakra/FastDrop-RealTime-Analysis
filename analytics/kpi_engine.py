from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime, timedelta

from common.config import Settings
from common.schemas import (
    AgentMetric,
    Alert,
    CategoryMetric,
    ChartPoint,
    CityMetric,
    Customer,
    CustomerMetric,
    DashboardFilters,
    DashboardSnapshot,
    DeliveryAgent,
    KpiSummary,
    LocationPoint,
    OrderEvent,
    OrderStatus,
    Product,
    ProductMetric,
)


class KpiEngine:
    def __init__(
        self,
        settings: Settings,
        customers: dict[str, Customer],
        agents: dict[str, DeliveryAgent],
        products: dict[str, Product],
    ) -> None:
        self.settings = settings
        self.customers = customers
        self.agents = agents
        self.products = products
        self.orders: list[OrderEvent] = []

    def ingest(self, order: OrderEvent) -> None:
        self.orders.append(order)
        self.orders.sort(key=lambda item: item.event_timestamp, reverse=True)

    def _non_cancelled(self, orders: list[OrderEvent]) -> list[OrderEvent]:
        return [order for order in orders if order.order_status != OrderStatus.cancelled]

    def _delivered(self, orders: list[OrderEvent]) -> list[OrderEvent]:
        return [order for order in orders if order.order_status == OrderStatus.delivered]

    def _delivery_minutes(self, order: OrderEvent) -> float:
        if order.delivery_timestamp is None:
            return 0.0
        return (order.delivery_timestamp - order.order_timestamp).total_seconds() / 60

    def filtered_orders(self, filters: DashboardFilters | None = None) -> list[OrderEvent]:
        filters = filters or DashboardFilters()
        orders = list(self.orders)

        if filters.city:
            orders = [order for order in orders if order.city == filters.city]
        if filters.status:
            orders = [order for order in orders if order.order_status == filters.status]
        if filters.product_id:
            orders = [order for order in orders if order.product_id == filters.product_id]
        if filters.agent_id:
            orders = [order for order in orders if order.agent_id == filters.agent_id]
        if filters.start_date:
            orders = [order for order in orders if order.order_timestamp.date() >= filters.start_date]
        if filters.end_date:
            orders = [order for order in orders if order.order_timestamp.date() <= filters.end_date]
        if filters.category:
            orders = [
                order for order in orders if self.products[order.product_id].category == filters.category
            ]
        if filters.customer_type:
            orders = [
                order
                for order in orders
                if self.customers[order.customer_id].customer_type == filters.customer_type
            ]
        return orders

    def snapshot(self, filters: DashboardFilters | None = None) -> DashboardSnapshot:
        filters = filters or DashboardFilters()
        orders = self.filtered_orders(filters)
        return DashboardSnapshot(
            timestamp=datetime.now(UTC),
            filters_applied=filters.model_dump(mode="json"),
            kpis=self._kpis(orders),
            hourly_metrics=self._hourly(orders),
            daily_metrics=self._daily(orders),
            delivery_metrics=self._city_metrics(orders),
            revenue_by_category=self._category_metrics(orders),
            top_agents=self._top_agents(orders),
            top_customers=self._top_customers(orders),
            top_products=self._top_products(orders),
            recent_orders=orders[: filters.limit],
            locations=self._locations(orders),
            alerts=self._alerts(orders),
        )

    def _kpis(self, orders: list[OrderEvent]) -> KpiSummary:
        now = datetime.now(UTC)
        delivered = self._delivered(orders)
        non_cancelled = self._non_cancelled(orders)
        revenue = round(sum(order.total_amount for order in non_cancelled), 2)
        cancellation_count = sum(1 for order in orders if order.order_status == OrderStatus.cancelled)
        recent_minute = [order for order in orders if order.event_timestamp >= now - timedelta(minutes=1)]
        recent_five = [order for order in orders if order.event_timestamp >= now - timedelta(minutes=5)]
        on_time = sum(
            1
            for order in delivered
            if order.promised_delivery_timestamp
            and order.delivery_timestamp
            and order.delivery_timestamp <= order.promised_delivery_timestamp
        )
        return KpiSummary(
            updated_at=now,
            total_orders=len(orders),
            total_revenue=revenue,
            average_order_value=round(revenue / len(non_cancelled), 2) if non_cancelled else 0.0,
            delivered_orders=len(delivered),
            cancelled_orders=cancellation_count,
            cancellation_rate=round((cancellation_count / len(orders)) * 100, 2) if orders else 0.0,
            average_delivery_minutes=round(
                sum(self._delivery_minutes(order) for order in delivered) / len(delivered), 2
            ) if delivered else 0.0,
            average_distance=round(
                sum(order.distance_km for order in non_cancelled) / len(non_cancelled), 2
            ) if non_cancelled else 0.0,
            on_time_delivery_rate=round((on_time / len(delivered)) * 100, 2) if delivered else 0.0,
            active_agents=len(
                {
                    order.agent_id
                    for order in orders
                    if order.event_timestamp >= now - timedelta(minutes=30)
                }
            ),
            orders_per_minute=len(recent_minute),
            orders_last_5_minutes=len(recent_five),
            revenue_last_5_minutes=round(
                sum(order.total_amount for order in self._non_cancelled(recent_five)), 2
            ),
        )

    def _hourly(self, orders: list[OrderEvent], hours: int = 12) -> list[ChartPoint]:
        now = datetime.now(UTC).replace(minute=0, second=0, microsecond=0)
        grouped: dict[str, list[OrderEvent]] = defaultdict(list)
        for order in orders:
            grouped[order.order_timestamp.strftime("%H:00")].append(order)

        points: list[ChartPoint] = []
        for offset in range(hours - 1, -1, -1):
            bucket_time = now - timedelta(hours=offset)
            label = bucket_time.strftime("%H:00")
            bucket = grouped.get(label, [])
            delivered = self._delivered(bucket)
            points.append(
                ChartPoint(
                    label=label,
                    orders=len(bucket),
                    revenue=round(sum(order.total_amount for order in self._non_cancelled(bucket)), 2),
                    average_delivery_minutes=round(
                        sum(self._delivery_minutes(order) for order in delivered) / len(delivered), 2
                    ) if delivered else 0.0,
                )
            )
        return points

    def _daily(self, orders: list[OrderEvent], days: int = 7) -> list[ChartPoint]:
        today = datetime.now(UTC).date()
        grouped: dict[str, list[OrderEvent]] = defaultdict(list)
        for order in orders:
            grouped[order.order_timestamp.date().isoformat()].append(order)

        points: list[ChartPoint] = []
        for offset in range(days - 1, -1, -1):
            day = today - timedelta(days=offset)
            label = day.isoformat()
            bucket = grouped.get(label, [])
            delivered = self._delivered(bucket)
            points.append(
                ChartPoint(
                    label=label[5:],
                    orders=len(bucket),
                    revenue=round(sum(order.total_amount for order in self._non_cancelled(bucket)), 2),
                    average_delivery_minutes=round(
                        sum(self._delivery_minutes(order) for order in delivered) / len(delivered), 2
                    ) if delivered else 0.0,
                )
            )
        return points

    def _city_metrics(self, orders: list[OrderEvent]) -> list[CityMetric]:
        grouped: dict[str, list[OrderEvent]] = defaultdict(list)
        for order in orders:
            grouped[order.city].append(order)

        metrics: list[CityMetric] = []
        for city, city_orders in grouped.items():
            delivered = self._delivered(city_orders)
            cancelled = sum(1 for order in city_orders if order.order_status == OrderStatus.cancelled)
            metrics.append(
                CityMetric(
                    city=city,
                    total_orders=len(city_orders),
                    total_revenue=round(
                        sum(order.total_amount for order in self._non_cancelled(city_orders)), 2
                    ),
                    average_delivery_minutes=round(
                        sum(self._delivery_minutes(order) for order in delivered) / len(delivered), 2
                    ) if delivered else 0.0,
                    average_distance=round(
                        sum(order.distance_km for order in city_orders) / len(city_orders), 2
                    ),
                    cancellation_rate=round((cancelled / len(city_orders)) * 100, 2),
                )
            )
        return sorted(metrics, key=lambda item: item.total_orders, reverse=True)

    def _category_metrics(self, orders: list[OrderEvent]) -> list[CategoryMetric]:
        grouped: dict[str, list[OrderEvent]] = defaultdict(list)
        for order in orders:
            grouped[self.products[order.product_id].category.value].append(order)
        return sorted(
            [
                CategoryMetric(
                    category=category,
                    total_orders=len(group),
                    total_revenue=round(
                        sum(order.total_amount for order in self._non_cancelled(group)), 2
                    ),
                )
                for category, group in grouped.items()
            ],
            key=lambda item: item.total_revenue,
            reverse=True,
        )

    def _top_agents(self, orders: list[OrderEvent]) -> list[AgentMetric]:
        grouped: dict[str, list[OrderEvent]] = defaultdict(list)
        for order in self._delivered(orders):
            grouped[order.agent_id].append(order)
        result: list[AgentMetric] = []
        for agent_id, group in grouped.items():
            agent = self.agents[agent_id]
            result.append(
                AgentMetric(
                    agent_id=agent_id,
                    agent_name=agent.agent_name,
                    city=agent.city,
                    deliveries=len(group),
                    average_delivery_minutes=round(
                        sum(self._delivery_minutes(order) for order in group) / len(group), 2
                    ),
                    revenue_handled=round(sum(order.total_amount for order in group), 2),
                    rating=agent.rating,
                )
            )
        return sorted(result, key=lambda item: item.deliveries, reverse=True)[:10]

    def _top_customers(self, orders: list[OrderEvent]) -> list[CustomerMetric]:
        grouped: dict[str, list[OrderEvent]] = defaultdict(list)
        for order in self._non_cancelled(orders):
            grouped[order.customer_id].append(order)
        result: list[CustomerMetric] = []
        for customer_id, group in grouped.items():
            customer = self.customers[customer_id]
            revenue = round(sum(order.total_amount for order in group), 2)
            result.append(
                CustomerMetric(
                    customer_id=customer_id,
                    customer_name=customer.customer_name,
                    city=customer.city,
                    total_orders=len(group),
                    total_revenue=revenue,
                    average_order_value=round(revenue / len(group), 2),
                    customer_type=customer.customer_type,
                )
            )
        return sorted(result, key=lambda item: item.total_revenue, reverse=True)[:10]

    def _top_products(self, orders: list[OrderEvent]) -> list[ProductMetric]:
        grouped: dict[str, list[OrderEvent]] = defaultdict(list)
        for order in self._non_cancelled(orders):
            grouped[order.product_id].append(order)
        result: list[ProductMetric] = []
        for product_id, group in grouped.items():
            product = self.products[product_id]
            result.append(
                ProductMetric(
                    product_id=product_id,
                    product_name=product.product_name,
                    category=product.category,
                    quantity_sold=sum(order.quantity for order in group),
                    total_revenue=round(sum(order.total_amount for order in group), 2),
                )
            )
        return sorted(result, key=lambda item: item.total_revenue, reverse=True)[:10]

    def _locations(self, orders: list[OrderEvent]) -> list[LocationPoint]:
        return [
            LocationPoint(
                order_id=order.order_id,
                city=order.city,
                latitude=order.delivery_latitude,
                longitude=order.delivery_longitude,
                status=order.order_status,
                amount=order.total_amount,
            )
            for order in orders[:40]
        ]

    def _alerts(self, orders: list[OrderEvent]) -> list[Alert]:
        if not orders:
            return []
        kpis = self._kpis(orders)
        alerts: list[Alert] = []
        if kpis.cancellation_rate > self.settings.alert_cancellation_rate_threshold:
            alerts.append(
                Alert(
                    level="critical",
                    title="Cancellation rate exceeded threshold",
                    body=(
                        f"Current cancellation rate is {kpis.cancellation_rate}% and is above "
                        f"{self.settings.alert_cancellation_rate_threshold}%."
                    ),
                )
            )
        if kpis.average_delivery_minutes > self.settings.alert_delivery_minutes_threshold:
            alerts.append(
                Alert(
                    level="warning",
                    title="Average delivery time is elevated",
                    body=(
                        f"Current average delivery time is {kpis.average_delivery_minutes} minutes, "
                        f"above the threshold of {self.settings.alert_delivery_minutes_threshold}."
                    ),
                )
            )
        if kpis.orders_per_minute > self.settings.alert_orders_per_minute_threshold:
            alerts.append(
                Alert(
                    level="info",
                    title="Demand spike detected",
                    body=f"Orders per minute reached {kpis.orders_per_minute}.",
                )
            )
        if not alerts:
            busiest = max(self._city_metrics(orders), key=lambda item: item.total_orders)
            alerts.append(
                Alert(
                    level="info",
                    title="Network stable",
                    body=f"{busiest.city} currently leads demand with {busiest.total_orders} orders.",
                    city=busiest.city,
                )
            )
        return alerts

