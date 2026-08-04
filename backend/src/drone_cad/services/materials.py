from __future__ import annotations

from drone_cad.models.materials import Material

MATERIALS: dict[str, Material] = {
    "carbon-fiber": Material(
        id="carbon-fiber",
        name="Carbon fiber composite",
        density_kg_m3=1600.0,
        source_note="Approximate engineering default; actual layup and resin fraction vary.",
    ),
    "aluminum-6061": Material(
        id="aluminum-6061",
        name="Aluminum 6061",
        density_kg_m3=2700.0,
        source_note="Approximate common reference density for 6061 aluminum.",
    ),
    "pla": Material(
        id="pla",
        name="PLA",
        density_kg_m3=1240.0,
        source_note="Approximate default for common 3D-printing PLA.",
    ),
    "abs": Material(
        id="abs",
        name="ABS",
        density_kg_m3=1040.0,
        source_note="Approximate default for common ABS plastic.",
    ),
    "generic-steel": Material(
        id="generic-steel",
        name="Generic steel",
        density_kg_m3=7850.0,
        source_note="Approximate default for carbon steel.",
    ),
}


def get_material(material_id: str | None) -> Material | None:
    if material_id is None:
        return None
    return MATERIALS.get(material_id)
