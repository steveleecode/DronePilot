from pathlib import Path

from fastapi.testclient import TestClient

from drone_cad.api import routes
from drone_cad.main import app
from drone_cad.models.analysis import AnalysisMetadata, DroneAnalysis
from drone_cad.models.cad import BoundingBox, Vector3


def _sample_analysis() -> DroneAnalysis:
    return DroneAnalysis(
        model_id="v1-drone",
        part_count=0,
        total_volume_m3=0.0,
        total_mass_kg=0.0,
        center_of_gravity_m=Vector3(x=0.0, y=0.0, z=0.0),
        inertia_tensor_kg_m2=[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        principal_moments_kg_m2=[0.0, 0.0, 0.0],
        bounding_box_m=BoundingBox(x=0.0, y=0.0, z=0.0),
        materials=[],
        parts=[],
        warnings=[],
        metadata=AnalysisMetadata(
            source_step_path="cad/v1-drone.step",
            source_length_unit="millimeter",
            default_material_id="carbon-fiber",
        ),
    )


def test_analysis_endpoint_returns_generated_json(
    tmp_path: Path,
    monkeypatch,
) -> None:
    generated_analysis = tmp_path / "analysis.json"
    generated_analysis.write_text(_sample_analysis().model_dump_json(), encoding="utf-8")
    monkeypatch.setattr(routes, "analysis_path", lambda: generated_analysis)

    response = TestClient(app).get("/api/v1/models/v1-drone/analysis")

    assert response.status_code == 200
    assert response.json()["model_id"] == "v1-drone"
    assert response.json()["metadata"]["source_length_unit"] == "millimeter"


def test_geometry_endpoint_returns_generated_glb(tmp_path: Path, monkeypatch) -> None:
    generated_geometry = tmp_path / "model.glb"
    generated_geometry.write_bytes(b"glTF test")
    monkeypatch.setattr(routes, "geometry_path", lambda: generated_geometry)

    response = TestClient(app).get("/api/v1/models/v1-drone/geometry.glb")

    assert response.status_code == 200
    assert response.headers["content-type"] == "model/gltf-binary"
    assert response.content == b"glTF test"
