from fastapi import APIRouter, Depends, Query

from backend.dependencies import get_pipeline
from backend.services.live_pipeline import LivePipeline
from common.schemas import DashboardFilters


router = APIRouter(tags=["analytics"])


@router.get("/kpis")
def get_kpis(city: str | None = Query(default=None), pipeline: LivePipeline = Depends(get_pipeline)):
    return pipeline.repository.dashboard_snapshot(DashboardFilters(city=city)).kpis


@router.get("/analytics/hourly")
def hourly_analytics(
    city: str | None = Query(default=None),
    pipeline: LivePipeline = Depends(get_pipeline),
):
    return pipeline.repository.dashboard_snapshot(DashboardFilters(city=city)).hourly_metrics


@router.get("/analytics/daily")
def daily_analytics(
    city: str | None = Query(default=None),
    pipeline: LivePipeline = Depends(get_pipeline),
):
    return pipeline.repository.dashboard_snapshot(DashboardFilters(city=city)).daily_metrics


@router.get("/analytics/delivery")
def delivery_analytics(
    city: str | None = Query(default=None),
    pipeline: LivePipeline = Depends(get_pipeline),
):
    return pipeline.repository.dashboard_snapshot(DashboardFilters(city=city)).delivery_metrics


@router.get("/alerts")
def alerts(city: str | None = Query(default=None), pipeline: LivePipeline = Depends(get_pipeline)):
    return pipeline.repository.dashboard_snapshot(DashboardFilters(city=city)).alerts

