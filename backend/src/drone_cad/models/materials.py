from __future__ import annotations

from pydantic import BaseModel


class Material(BaseModel):
    id: str
    name: str
    density_kg_m3: float
    source_note: str


class PartMassAssignment(BaseModel):
    part_id: str
    material_id: str | None = None
    manufacturer_mass_kg: float | None = None
