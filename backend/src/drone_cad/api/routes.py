from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from drone_cad.models.analysis import DroneAnalysis
from drone_cad.services.mass_properties import MassPropertyAnalyzer
from drone_cad.services.web_export import WebGeometryExporter

router = APIRouter(prefix="/api/v1")


class DroneModelMetadata(BaseModel):
    model_id: str
    source_step_path: str
    analysis_url: str
    geometry_url: str


def model_id() -> str:
    return "v1-drone"


def source_step_path() -> Path:
    return Path("cad/v1-drone.step")


def generated_dir() -> Path:
    return Path("generated")


def analysis_path() -> Path:
    return generated_dir() / "v1-drone-analysis.json"


def geometry_path() -> Path:
    return generated_dir() / "v1-drone.glb"


@router.get("/models/v1-drone", response_model=DroneModelMetadata)
def get_model() -> DroneModelMetadata:
    return DroneModelMetadata(
        model_id=model_id(),
        source_step_path=str(source_step_path()),
        analysis_url="/api/v1/models/v1-drone/analysis",
        geometry_url="/api/v1/models/v1-drone/geometry.glb",
    )


@router.get("/models/v1-drone/analysis", response_model=DroneAnalysis)
def get_analysis() -> DroneAnalysis:
    path = analysis_path()
    if path.exists():
        return DroneAnalysis.model_validate_json(path.read_text(encoding="utf-8"))

    step_path = source_step_path()
    if not step_path.exists():
        raise HTTPException(status_code=404, detail=f"Source STEP file not found: {step_path}")

    analysis = MassPropertyAnalyzer().analyze_step(step_path, default_material_id="carbon-fiber")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(analysis.model_dump_json(indent=2) + "\n", encoding="utf-8")
    return analysis


@router.get("/models/v1-drone/geometry.glb")
def get_geometry() -> FileResponse:
    path = geometry_path()
    if not path.exists():
        step_path = source_step_path()
        if not step_path.exists():
            raise HTTPException(status_code=404, detail=f"Source STEP file not found: {step_path}")
        WebGeometryExporter().export_glb(step_path, path)

    return FileResponse(path, media_type="model/gltf-binary", filename="v1-drone.glb")
