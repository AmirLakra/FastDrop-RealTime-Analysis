from common.config import Settings
from common.schemas import Customer, DashboardFilters, DashboardSnapshot, DeliveryAgent, OrderEvent, Product
from analytics.kpi_engine import KpiEngine


class InMemoryAnalyticsRepository:
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
        self.engine = KpiEngine(settings, customers, agents, products)

    def ingest_order(self, order: OrderEvent) -> None:
        self.engine.ingest(order)

    def dashboard_snapshot(self, filters: DashboardFilters | None = None) -> DashboardSnapshot:
        return self.engine.snapshot(filters)

    def list_orders(self, filters: DashboardFilters | None = None) -> list[OrderEvent]:
        return self.engine.filtered_orders(filters)

