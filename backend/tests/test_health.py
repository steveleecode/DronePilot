from fastapi.testclient import TestClient

from drone_cad.main import app


def test_health_endpoint() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_model_metadata_endpoint() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/models/v1-drone")

    assert response.status_code == 200
    assert response.json() == {
        "model_id": "v1-drone",
        "source_step_path": "cad/v1-drone.step",
        "analysis_url": "/api/v1/models/v1-drone/analysis",
        "geometry_url": "/api/v1/models/v1-drone/geometry.glb",
    }
