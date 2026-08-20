from __future__ import annotations

import asyncio
import contextlib
from datetime import UTC, datetime

from backend.websocket.manager import WebSocketManager
from common.config import Settings
from common.schemas import DashboardFilters, DashboardSocketMessage
from data_generator.generator import QuickDropGenerator
from database.repository import InMemoryAnalyticsRepository


class LivePipeline:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.generator = QuickDropGenerator(settings)
        self.repository = InMemoryAnalyticsRepository(
            settings=settings,
            customers=self.generator.customers,
            agents=self.generator.agents,
            products=self.generator.products,
        )
        self.websockets = WebSocketManager()
        self._task: asyncio.Task | None = None
        self._running = False

    async def start(self) -> None:
        if self._running:
            return
        self._running = True
        for order in self.generator.generate_batch(self.settings.seed_history_count, backfill=True):
            self.repository.ingest_order(order)
        self._task = asyncio.create_task(self._run(), name="quickdrop-live-pipeline")

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
            self._task = None

    async def _run(self) -> None:
        delay = 1 / max(self.settings.orders_per_second, 1)
        while self._running:
            order = self.generator.generate_order()
            self.repository.ingest_order(order)
            await self.broadcast_snapshot()
            await asyncio.sleep(delay)

    async def broadcast_snapshot(self, filters: DashboardFilters | None = None) -> None:
        snapshot = self.repository.dashboard_snapshot(filters)
        message = DashboardSocketMessage(
            type="kpi_update",
            timestamp=datetime.now(UTC),
            data=snapshot,
        )
        await self.websockets.broadcast(message.model_dump(mode="json"))

