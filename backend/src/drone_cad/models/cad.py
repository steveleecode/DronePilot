from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Vector3(BaseModel):
    x: float
    y: float
    z: float


class BoundingBox(BaseModel):
    x: float
    y: float
    z: float


class CadPart(BaseModel):
    id: str
    name: str
    volume_m3: float
    surface_area_m2: float | None
    center_of_mass_m: Vector3
    source_type: Literal["solid", "compound", "assembly_component"]
    warnings: list[str] = Field(default_factory=list)


class CadInspection(BaseModel):
    model_id: str
    source_step_path: str
    source_step_size_bytes: int
    source_length_unit: str
    length_unit_scale_to_m: float
    detected_shape_type: str
    part_count: int
    total_volume_m3: float
    total_surface_area_m2: float | None
    bounding_box_m: BoundingBox
    parts: list[CadPart]
    warnings: list[str] = Field(default_factory=list)
