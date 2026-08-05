from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from drone_cad.models.materials import MaterialAssignmentProfile
from drone_cad.services.materials import MATERIALS


class MaterialProfileError(ValueError):
    """Raised when a material assignment profile is invalid."""


def load_material_assignment_profile(path: Path) -> MaterialAssignmentProfile:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        profile = MaterialAssignmentProfile.model_validate(payload)
    except FileNotFoundError as exc:
        raise MaterialProfileError(f"Material assignment profile not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise MaterialProfileError(f"Invalid JSON in material assignment profile: {path}") from exc
    except ValidationError as exc:
        raise MaterialProfileError(f"Invalid material assignment profile schema: {exc}") from exc

    material_ids = {assignment.material_id for assignment in profile.assignments}
    if profile.default_material_id is not None:
        material_ids.add(profile.default_material_id)

    unknown_materials = sorted(
        material_id
        for material_id in material_ids
        if material_id is not None and material_id not in MATERIALS
    )
    if unknown_materials:
        joined = ", ".join(unknown_materials)
        raise MaterialProfileError(f"Unknown material id(s) in assignment profile: {joined}")

    duplicate_part_ids = sorted(
        {
            assignment.part_id
            for assignment in profile.assignments
            if sum(other.part_id == assignment.part_id for other in profile.assignments) > 1
        }
    )
    if duplicate_part_ids:
        joined = ", ".join(duplicate_part_ids)
        raise MaterialProfileError(f"Duplicate part assignment(s): {joined}")

    return profile
