from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.analytics import router as analytics_router
from backend.routes.dashboard import router as dashboard_router
from backend.routes.entities import router as entities_router
from backend.routes.health import router as health_router
from backend.routes.orders import router as orders_router
from backend.services.live_pipeline import LivePipeline
from common.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    pipeline = LivePipeline(settings)
    app.state.pipeline = pipeline
    await pipeline.start()
    try:
        yield
    finally:
        await pipeline.stop()


settings = get_settings()
app = FastAPI(
    title="QuickDrop Analytics API",
    version="1.0.0",
    description="Real-time delivery analytics backend for QuickDrop.",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")
app.include_router(orders_router, prefix="/api")
app.include_router(entities_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "QuickDrop backend is running."}


@app.websocket("/ws/dashboard")
async def dashboard_socket(websocket: WebSocket) -> None:
    pipeline: LivePipeline = app.state.pipeline
    await pipeline.websockets.connect(websocket)
    try:
        snapshot = pipeline.repository.dashboard_snapshot()
        await pipeline.websockets.send_json(
            websocket,
            {
                "type": "kpi_update",
                "timestamp": snapshot.timestamp.isoformat(),
                "data": snapshot.model_dump(mode="json"),
            },
        )
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pipeline.websockets.disconnect(websocket)
    except Exception:
        pipeline.websockets.disconnect(websocket)

