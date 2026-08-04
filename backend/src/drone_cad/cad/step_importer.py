from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

os.environ.setdefault("XDG_CACHE_HOME", str(Path.cwd() / ".cache"))

import cadquery as cq  # type: ignore[import-untyped]

from drone_cad.cad.assembly_metadata import read_step_assembly_metadata
from drone_cad.models.cad import BoundingBox, CadInspection, CadPart, Vector3


class StepImportError(ValueError):
    """Raised when a STEP file cannot be imported as usable CAD geometry."""


@dataclass(frozen=True)
class ImportedCadGeometry:
    inspection: CadInspection
    solids: list[Any]


class StepImporter:
    def inspect(self, step_path: Path, model_id: str = "v1-drone") -> CadInspection:
        return self.load(step_path, model_id=model_id).inspection

    def load(self, step_path: Path, model_id: str = "v1-drone") -> ImportedCadGeometry:
        resolved_path = step_path.expanduser().resolve()
        self._validate_path(resolved_path)

        unit_name, length_scale_m = detect_step_length_unit(resolved_path)
        workplane = cq.importers.importStep(str(resolved_path))
        values = workplane.vals()
        if not values:
            raise StepImportError(f"No shapes were imported from {resolved_path}")

        root_shape: Any = workplane.val()
        solids = list(workplane.solids().vals())
        assembly_metadata = read_step_assembly_metadata(resolved_path)
        warnings: list[str] = []
        if len(values) == 1 and len(solids) > 1:
            if assembly_metadata.components:
                warnings.append(
                    "CadQuery imported one compound; STEPCAF recovered component labels, but "
                    "component-to-solid correlation is not yet implemented."
                )
            else:
                warnings.append(
                    "Imported as one compound; assembly hierarchy, component names, and "
                    "placements were not recovered."
                )
        elif len(solids) == 1:
            warnings.append("Imported as a single solid.")

        part_solid_pairs = [
            (self._solid_to_part(solid=solid, index=index, length_scale_m=length_scale_m), solid)
            for index, solid in enumerate(solids, start=1)
        ]
        usable_pairs = [(part, solid) for part, solid in part_solid_pairs if part.volume_m3 > 0]
        usable_parts = [part for part, _solid in usable_pairs]
        if not usable_parts:
            raise StepImportError(f"No positive-volume solids were imported from {resolved_path}")

        total_surface_area = sum(
            part.surface_area_m2 for part in usable_parts if part.surface_area_m2 is not None
        )
        return ImportedCadGeometry(
            inspection=CadInspection(
                model_id=model_id,
                source_step_path=str(resolved_path),
                source_step_size_bytes=resolved_path.stat().st_size,
                source_length_unit=unit_name,
                length_unit_scale_to_m=length_scale_m,
                detected_shape_type=str(root_shape.ShapeType()),
                part_count=len(usable_parts),
                total_volume_m3=sum(part.volume_m3 for part in usable_parts),
                total_surface_area_m2=total_surface_area,
                bounding_box_m=self._bounding_box(root_shape, length_scale_m),
                parts=usable_parts,
                assembly_metadata=assembly_metadata,
                warnings=warnings,
            ),
            solids=[solid for _part, solid in usable_pairs],
        )

    @staticmethod
    def _validate_path(step_path: Path) -> None:
        if not step_path.exists():
            raise StepImportError(f"STEP file does not exist: {step_path}")
        if not step_path.is_file():
            raise StepImportError(f"STEP path is not a file: {step_path}")
        if step_path.suffix.lower() not in {".step", ".stp"}:
            raise StepImportError(f"Unsupported CAD extension for STEP import: {step_path.suffix}")
        if step_path.stat().st_size <= 0:
            raise StepImportError(f"STEP file is empty: {step_path}")

    @staticmethod
    def _solid_to_part(solid: Any, index: int, length_scale_m: float) -> CadPart:
        warnings: list[str] = []
        raw_volume = float(solid.Volume())
        raw_area = float(solid.Area())
        if raw_volume <= 0:
            warnings.append("Solid has zero or negative volume and was excluded from totals.")

        center = solid.Center()
        return CadPart(
            id=f"solid-{index:03d}",
            name=f"Solid {index:03d}",
            volume_m3=raw_volume * length_scale_m**3,
            surface_area_m2=raw_area * length_scale_m**2 if raw_area > 0 else None,
            center_of_mass_m=Vector3(
                x=float(center.x) * length_scale_m,
                y=float(center.y) * length_scale_m,
                z=float(center.z) * length_scale_m,
            ),
            source_type="solid",
            warnings=warnings
            + ["No STEP component name or placement transform recovered for this solid."],
        )

    @staticmethod
    def _bounding_box(shape: Any, length_scale_m: float) -> BoundingBox:
        bounds = shape.BoundingBox()
        return BoundingBox(
            x=float(bounds.xlen) * length_scale_m,
            y=float(bounds.ylen) * length_scale_m,
            z=float(bounds.zlen) * length_scale_m,
        )


def detect_step_length_unit(step_path: Path) -> tuple[str, float]:
    text = step_path.read_text(encoding="utf-8", errors="ignore")
    unit_blocks = re.findall(
        r"LENGTH_UNIT\(\)\s*NAMED_UNIT\([^)]*\)\s*SI_UNIT\(([^)]*)\)",
        text,
        flags=re.IGNORECASE | re.MULTILINE,
    )
    if not unit_blocks:
        return "unknown_assumed_millimeter", 0.001

    first_unit = unit_blocks[0].replace(" ", "").upper()
    if ".MILLI." in first_unit and ".METRE." in first_unit:
        return "millimeter", 0.001
    if "$,.METRE." in first_unit or ".METRE." in first_unit:
        return "meter", 1.0

    return "unknown_assumed_millimeter", 0.001
