from fastapi import APIRouter, Depends, Query

from backend.dependencies import get_pipeline
from backend.services.live_pipeline import LivePipeline
from common.schemas import CustomerType, ProductCategory


router = APIRouter(tags=["entities"])


@router.get("/agents")
def list_agents(
    city: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    pipeline: LivePipeline = Depends(get_pipeline),
):
    agents = list(pipeline.repository.agents.values())
    if city:
        agents = [agent for agent in agents if agent.city == city]
    return agents[:limit]


@router.get("/products")
def list_products(
    category: ProductCategory | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    pipeline: LivePipeline = Depends(get_pipeline),
):
    products = list(pipeline.repository.products.values())
    if category:
        products = [product for product in products if product.category == category]
    return products[:limit]


@router.get("/customers")
def list_customers(
    city: str | None = Query(default=None),
    customer_type: CustomerType | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    pipeline: LivePipeline = Depends(get_pipeline),
):
    customers = list(pipeline.repository.customers.values())
    if city:
        customers = [customer for customer in customers if customer.city == city]
    if customer_type:
        customers = [customer for customer in customers if customer.customer_type == customer_type]
    return customers[:limit]


@router.get("/cities")
def list_cities(pipeline: LivePipeline = Depends(get_pipeline)):
    return pipeline.settings.supported_city_list

