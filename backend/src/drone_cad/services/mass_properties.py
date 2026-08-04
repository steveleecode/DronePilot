from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

import cadquery as cq  # type: ignore[import-untyped]
import numpy as np

from drone_cad.cad.step_importer import StepImporter
from drone_cad.models.analysis import AnalysisMetadata, AnalyzedPart, DroneAnalysis
from drone_cad.models.cad import CadPart, Vector3
from drone_cad.models.materials import PartMassAssignment
from drone_cad.services.materials import MATERIALS, get_material


class MassPropertyAnalyzer:
    def analyze_step(
        self,
        step_path: Path,
        default_material_id: str | None = "carbon-fiber",
        assignments: Sequence[PartMassAssignment] = (),
        model_id: str = "v1-drone",
    ) -> DroneAnalysis:
        geometry = StepImporter().load(step_path, model_id=model_id)
        assignment_by_part = {assignment.part_id: assignment for assignment in assignments}

        analyzed_parts: list[AnalyzedPart] = []
        warnings = list(geometry.inspection.warnings)
        for part, solid in zip(geometry.inspection.parts, geometry.solids, strict=True):
            assignment = assignment_by_part.get(part.id, PartMassAssignment(part_id=part.id))
            material_id = assignment.material_id or default_material_id
            material = get_material(material_id)
            analyzed_part, part_warnings = self.analyze_part(
                part=part,
                solid=solid,
                length_scale_m=geometry.inspection.length_unit_scale_to_m,
                material_id=material.id if material else None,
                density_kg_m3=material.density_kg_m3 if material else None,
                manufacturer_mass_kg=assignment.manufacturer_mass_kg,
            )
            analyzed_parts.append(analyzed_part)
            warnings.extend(part_warnings)

        total_mass = sum(part.mass_kg for part in analyzed_parts)
        if total_mass <= 0:
            center_of_gravity = Vector3(x=0.0, y=0.0, z=0.0)
            warnings.append("Total mass is zero; center of gravity defaults to the origin.")
        else:
            center_of_gravity = Vector3(
                x=sum(part.mass_kg * part.center_of_mass_m.x for part in analyzed_parts)
                / total_mass,
                y=sum(part.mass_kg * part.center_of_mass_m.y for part in analyzed_parts)
                / total_mass,
                z=sum(part.mass_kg * part.center_of_mass_m.z for part in analyzed_parts)
                / total_mass,
            )

        aggregate_inertia = aggregate_inertia_tensor(analyzed_parts, center_of_gravity)
        principal_moments = sorted(float(value) for value in np.linalg.eigvalsh(aggregate_inertia))

        return DroneAnalysis(
            model_id=model_id,
            part_count=len(analyzed_parts),
            total_volume_m3=geometry.inspection.total_volume_m3,
            total_mass_kg=total_mass,
            center_of_gravity_m=center_of_gravity,
            inertia_tensor_kg_m2=ndarray_to_tensor(aggregate_inertia),
            principal_moments_kg_m2=principal_moments,
            bounding_box_m=geometry.inspection.bounding_box_m,
            materials=list(MATERIALS.values()),
            parts=analyzed_parts,
            warnings=warnings,
            metadata=AnalysisMetadata(
                source_step_path=geometry.inspection.source_step_path,
                source_length_unit=geometry.inspection.source_length_unit,
                default_material_id=default_material_id,
            ),
        )

    @staticmethod
    def analyze_part(
        part: CadPart,
        solid: Any,
        length_scale_m: float,
        material_id: str | None,
        density_kg_m3: float | None,
        manufacturer_mass_kg: float | None = None,
    ) -> tuple[AnalyzedPart, list[str]]:
        warnings: list[str] = []
        mass_source = "unassigned"
        mass_kg = 0.0
        inertia_density_kg_m3 = 0.0

        if manufacturer_mass_kg is not None:
            mass_kg = manufacturer_mass_kg
            mass_source = "manufacturer_override"
            if part.volume_m3 > 0:
                inertia_density_kg_m3 = manufacturer_mass_kg / part.volume_m3
            else:
                warnings.append(f"{part.id} has a mass override but zero volume.")
        elif density_kg_m3 is not None and part.volume_m3 > 0:
            mass_kg = density_kg_m3 * part.volume_m3
            inertia_density_kg_m3 = density_kg_m3
            mass_source = "density_calculated"
        elif part.volume_m3 <= 0:
            warnings.append(f"{part.id} has zero volume; mass is unassigned.")
        else:
            warnings.append(f"{part.id} has no material assignment; mass is unassigned.")

        inertia_tensor = part_inertia_tensor(solid, length_scale_m, inertia_density_kg_m3)

        return (
            AnalyzedPart(
                **part.model_dump(),
                material_id=material_id,
                density_kg_m3=density_kg_m3,
                mass_kg=mass_kg,
                mass_source=mass_source,  # type: ignore[arg-type]
                inertia_tensor_kg_m2=ndarray_to_tensor(inertia_tensor),
            ),
            warnings,
        )


def part_inertia_tensor(solid: Any, length_scale_m: float, density_kg_m3: float) -> np.ndarray:
    raw_inertia = np.array(cq.Shape.matrixOfInertia(solid), dtype=float)
    return raw_inertia * density_kg_m3 * length_scale_m**5


def ndarray_to_tensor(matrix: np.ndarray) -> list[list[float]]:
    return [[float(value) for value in row] for row in matrix.tolist()]


def aggregate_inertia_tensor(parts: Sequence[AnalyzedPart], origin_m: Vector3) -> np.ndarray:
    aggregate = np.zeros((3, 3), dtype=float)
    origin = np.array([origin_m.x, origin_m.y, origin_m.z], dtype=float)
    identity = np.identity(3)
    for part in parts:
        part_inertia = np.array(part.inertia_tensor_kg_m2, dtype=float)
        center = np.array(
            [part.center_of_mass_m.x, part.center_of_mass_m.y, part.center_of_mass_m.z],
            dtype=float,
        )
        offset = center - origin
        parallel_axis = part.mass_kg * (
            float(np.dot(offset, offset)) * identity - np.outer(offset, offset)
        )
        aggregate += part_inertia + parallel_axis
    return aggregate
