from fastapi import Request

from backend.services.live_pipeline import LivePipeline


def get_pipeline(request: Request) -> LivePipeline:
    return request.app.state.pipeline

