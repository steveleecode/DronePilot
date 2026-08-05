from __future__ import annotations

from pydantic import BaseModel, Field


class Material(BaseModel):
    id: str
    name: str
    density_kg_m3: float
    source_note: str


class PartMassAssignment(BaseModel):
    part_id: str
    material_id: str | None = None
    manufacturer_mass_kg: float | None = None


class MaterialAssignmentProfile(BaseModel):
    profile_id: str
    description: str
    default_material_id: str | None = None
    assignments: list[PartMassAssignment] = Field(default_factory=list)
