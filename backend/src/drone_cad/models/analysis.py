from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from drone_cad.models.cad import BoundingBox, CadPart, Vector3
from drone_cad.models.materials import Material

MassSource = Literal["density_calculated", "manufacturer_override", "unassigned"]


class AnalyzedPart(CadPart):
    material_id: str | None = None
    density_kg_m3: float | None = None
    mass_kg: float
    mass_source: MassSource
    inertia_tensor_kg_m2: list[list[float]]


class AnalysisMetadata(BaseModel):
    source_step_path: str
    source_length_unit: str
    coordinate_convention: str = "+x right, +y forward, +z up"
    unit_convention: str = "SI units: meters, cubic meters, kilograms, kg/m^3, kg*m^2"
    processing_version: str = "0.1.0"
    default_material_id: str | None = None


class DroneAnalysis(BaseModel):
    model_id: str
    part_count: int
    total_volume_m3: float
    total_mass_kg: float
    center_of_gravity_m: Vector3
    inertia_tensor_kg_m2: list[list[float]]
    principal_moments_kg_m2: list[float]
    bounding_box_m: BoundingBox
    materials: list[Material]
    parts: list[AnalyzedPart]
    warnings: list[str] = Field(default_factory=list)
    metadata: AnalysisMetadata
