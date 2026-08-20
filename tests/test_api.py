from fastapi.testclient import TestClient

from backend.main import app


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_dashboard_endpoint():
    client = TestClient(app)
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    assert "kpis" in response.json()
