from common.config import Settings
from analytics.kpi_engine import KpiEngine
from data_generator.generator import QuickDropGenerator


def test_kpi_snapshot_has_expected_fields():
    settings = Settings()
    generator = QuickDropGenerator(settings)
    engine = KpiEngine(settings, generator.customers, generator.agents, generator.products)

    for order in generator.generate_batch(40, backfill=True):
        engine.ingest(order)

    snapshot = engine.snapshot()

    assert snapshot.kpis.total_orders == 40
    assert snapshot.kpis.total_revenue >= 0
    assert 0 <= snapshot.kpis.cancellation_rate <= 100
    assert len(snapshot.hourly_metrics) == 12
    assert len(snapshot.daily_metrics) == 7
