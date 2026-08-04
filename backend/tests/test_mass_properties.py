from __future__ import annotations

import cadquery as cq  # type: ignore[import-untyped]
import pytest

from drone_cad.models.analysis import AnalyzedPart
from drone_cad.models.cad import CadPart, Vector3
from drone_cad.services.mass_properties import (
    MassPropertyAnalyzer,
    aggregate_inertia_tensor,
    part_inertia_tensor,
)


def _cad_part(part_id: str, volume_m3: float, center: Vector3) -> CadPart:
    return CadPart(
        id=part_id,
        name=part_id,
        volume_m3=volume_m3,
        surface_area_m2=None,
        center_of_mass_m=center,
        source_type="solid",
        warnings=[],
    )


def _analyzed_part(
    part_id: str,
    mass_kg: float,
    center: Vector3,
    inertia_tensor_kg_m2: list[list[float]],
) -> AnalyzedPart:
    return AnalyzedPart(
        **_cad_part(part_id, 1.0, center).model_dump(),
        material_id="test",
        density_kg_m3=1.0,
        mass_kg=mass_kg,
        mass_source="density_calculated",
        inertia_tensor_kg_m2=inertia_tensor_kg_m2,
    )


def test_density_to_mass_conversion() -> None:
    solid = cq.Workplane("XY").box(10, 10, 10).val()
    part = _cad_part("solid-001", 0.001, Vector3(x=0.0, y=0.0, z=0.0))

    analyzed_part, warnings = MassPropertyAnalyzer.analyze_part(
        part=part,
        solid=solid,
        length_scale_m=0.1,
        material_id="test",
        density_kg_m3=500.0,
    )

    assert warnings == []
    assert analyzed_part.mass_kg == pytest.approx(0.5)
    assert analyzed_part.mass_source == "density_calculated"


def test_mass_override_behavior() -> None:
    solid = cq.Workplane("XY").box(10, 10, 10).val()
    part = _cad_part("solid-001", 0.001, Vector3(x=0.0, y=0.0, z=0.0))

    analyzed_part, warnings = MassPropertyAnalyzer.analyze_part(
        part=part,
        solid=solid,
        length_scale_m=0.1,
        material_id="test",
        density_kg_m3=500.0,
        manufacturer_mass_kg=2.0,
    )

    assert warnings == []
    assert analyzed_part.mass_kg == pytest.approx(2.0)
    assert analyzed_part.mass_source == "manufacturer_override"


def test_missing_material_handling() -> None:
    solid = cq.Workplane("XY").box(10, 10, 10).val()
    part = _cad_part("solid-001", 0.001, Vector3(x=0.0, y=0.0, z=0.0))

    analyzed_part, warnings = MassPropertyAnalyzer.analyze_part(
        part=part,
        solid=solid,
        length_scale_m=0.1,
        material_id=None,
        density_kg_m3=None,
    )

    assert analyzed_part.mass_kg == 0.0
    assert analyzed_part.mass_source == "unassigned"
    assert "no material assignment" in warnings[0]


def test_zero_volume_handling() -> None:
    solid = cq.Workplane("XY").box(10, 10, 10).val()
    part = _cad_part("solid-001", 0.0, Vector3(x=0.0, y=0.0, z=0.0))

    analyzed_part, warnings = MassPropertyAnalyzer.analyze_part(
        part=part,
        solid=solid,
        length_scale_m=0.1,
        material_id="test",
        density_kg_m3=500.0,
    )

    assert analyzed_part.mass_kg == 0.0
    assert analyzed_part.mass_source == "unassigned"
    assert "zero volume" in warnings[0]


def test_part_inertia_tensor_scales_density_and_units() -> None:
    solid = cq.Workplane("XY").box(10, 20, 30).val()

    inertia = part_inertia_tensor(solid, length_scale_m=0.001, density_kg_m3=1000.0)

    assert inertia[0][0] == pytest.approx(6.5e-7)
    assert inertia[1][1] == pytest.approx(5.0e-7)
    assert inertia[2][2] == pytest.approx(2.5e-7)


def test_parallel_axis_theorem() -> None:
    part = _analyzed_part(
        "solid-001",
        mass_kg=2.0,
        center=Vector3(x=1.0, y=0.0, z=0.0),
        inertia_tensor_kg_m2=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
    )

    aggregate = aggregate_inertia_tensor([part], Vector3(x=0.0, y=0.0, z=0.0))

    assert aggregate.flatten().tolist() == pytest.approx(
        [1.0, 0.0, 0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 3.0]
    )


def test_inertia_tensor_aggregation_and_combined_center() -> None:
    parts = [
        _analyzed_part(
            "solid-001",
            mass_kg=1.0,
            center=Vector3(x=0.0, y=0.0, z=0.0),
            inertia_tensor_kg_m2=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
        ),
        _analyzed_part(
            "solid-002",
            mass_kg=3.0,
            center=Vector3(x=2.0, y=0.0, z=0.0),
            inertia_tensor_kg_m2=[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]],
        ),
    ]
    combined_center = Vector3(x=1.5, y=0.0, z=0.0)

    aggregate = aggregate_inertia_tensor(parts, combined_center)

    assert aggregate.flatten().tolist() == pytest.approx(
        [3.0, 0.0, 0.0, 0.0, 6.0, 0.0, 0.0, 0.0, 6.0]
    )
