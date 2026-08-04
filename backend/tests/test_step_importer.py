from pathlib import Path

import cadquery as cq  # type: ignore[import-untyped]

from drone_cad.cad.step_importer import StepImporter, detect_step_length_unit


def test_detect_step_length_unit_reads_millimeters(tmp_path: Path) -> None:
    step_path = tmp_path / "unit.step"
    step_path.write_text(
        """
        #1=(
        LENGTH_UNIT()
        NAMED_UNIT(*)
        SI_UNIT(.MILLI.,.METRE.)
        );
        """,
        encoding="utf-8",
    )

    unit_name, scale = detect_step_length_unit(step_path)

    assert unit_name == "millimeter"
    assert scale == 0.001


def test_importer_inspects_generated_box_in_si_units(tmp_path: Path) -> None:
    step_path = tmp_path / "box.step"
    box = cq.Workplane("XY").box(10, 20, 30)
    cq.exporters.export(box, str(step_path))

    inspection = StepImporter().inspect(step_path, model_id="box")

    assert inspection.model_id == "box"
    assert inspection.part_count == 1
    assert inspection.detected_shape_type
    assert inspection.parts[0].id == "solid-001"
    assert inspection.parts[0].volume_m3 == 0.000006
    assert inspection.bounding_box_m.x == 0.01
    assert inspection.bounding_box_m.y == 0.02
    assert inspection.bounding_box_m.z == 0.03
