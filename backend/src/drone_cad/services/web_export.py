from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import trimesh  # type: ignore[import-untyped]

from drone_cad.cad.step_importer import StepImporter


class WebGeometryExporter:
    def export_glb(
        self,
        step_path: Path,
        output_path: Path,
        model_id: str = "v1-drone",
        tolerance: float = 0.8,
    ) -> Path:
        geometry = StepImporter().load(step_path, model_id=model_id)
        scene = trimesh.Scene()
        scene.metadata.update(
            {
                "model_id": model_id,
                "source_step_path": geometry.inspection.source_step_path,
                "source_length_unit": geometry.inspection.source_length_unit,
                "length_unit_scale_to_m": geometry.inspection.length_unit_scale_to_m,
                "coordinate_convention": "+x right, +y forward, +z up",
                "unit_convention": "Scene vertices are meters.",
                "processing_version": "0.1.0",
                "part_count": geometry.inspection.part_count,
                "warnings": geometry.inspection.warnings,
            }
        )

        for part, solid in zip(geometry.inspection.parts, geometry.solids, strict=True):
            mesh = solid_to_trimesh(
                solid,
                length_scale_m=geometry.inspection.length_unit_scale_to_m,
                tolerance=tolerance,
            )
            mesh.metadata["part_id"] = part.id
            mesh.metadata["name"] = part.name
            scene.add_geometry(mesh, geom_name=part.id, node_name=part.id)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        scene.export(output_path)
        return output_path


def solid_to_trimesh(solid: Any, length_scale_m: float, tolerance: float) -> trimesh.Trimesh:
    vertices, faces = solid.tessellate(tolerance)
    vertex_array = np.array(
        [[float(vertex.x), float(vertex.y), float(vertex.z)] for vertex in vertices],
        dtype=float,
    )
    vertex_array *= length_scale_m
    face_array = np.array(faces, dtype=np.int64)
    return trimesh.Trimesh(vertices=vertex_array, faces=face_array, process=False)
