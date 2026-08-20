from fastapi import APIRouter, Depends, Query

from backend.dependencies import get_pipeline
from backend.services.live_pipeline import LivePipeline
from common.schemas import CustomerType, DashboardFilters, OrderStatus, ProductCategory


router = APIRouter(tags=["orders"])


@router.get("/orders")
def list_orders(
    city: str | None = Query(default=None),
    status: OrderStatus | None = Query(default=None),
    category: ProductCategory | None = Query(default=None),
    product_id: str | None = Query(default=None),
    agent_id: str | None = Query(default=None),
    customer_type: CustomerType | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
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
    return pipeline.repository.list_orders(filters)[:limit]


@router.get("/orders/recent")
def recent_orders(
    limit: int = Query(default=25, ge=1, le=200),
    pipeline: LivePipeline = Depends(get_pipeline),
):
    return pipeline.repository.dashboard_snapshot(DashboardFilters(limit=limit)).recent_orders

