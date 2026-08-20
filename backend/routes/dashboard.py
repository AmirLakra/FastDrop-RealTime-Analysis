from fastapi import APIRouter, Depends, Query

from backend.dependencies import get_pipeline
from backend.services.live_pipeline import LivePipeline
from common.schemas import CustomerType, DashboardFilters, OrderStatus, ProductCategory


router = APIRouter(tags=["dashboard"])


@router.get("/dashboard")
def get_dashboard(
    city: str | None = Query(default=None),
    status: OrderStatus | None = Query(default=None),
    category: ProductCategory | None = Query(default=None),
    product_id: str | None = Query(default=None),
    agent_id: str | None = Query(default=None),
    customer_type: CustomerType | None = Query(default=None),
    limit: int = Query(default=25, ge=1, le=200),
    pipeline: LivePipeline = Depends(get_pipeline),
):
    filters = DashboardFilters(
        city=city,
        status=status,
        category=category,
        product_id=product_id,
        agent_id=agent_id,
        customer_type=customer_type,
        limit=limit,
    )
    return pipeline.repository.dashboard_snapshot(filters)

