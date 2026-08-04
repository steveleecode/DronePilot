from pathlib import Path

import cadquery as cq  # type: ignore[import-untyped]
import trimesh  # type: ignore[import-untyped]

from drone_cad.services.web_export import WebGeometryExporter


def test_export_web_writes_valid_glb(tmp_path: Path) -> None:
    step_path = tmp_path / "box.step"
    output_path = tmp_path / "box.glb"
    box = cq.Workplane("XY").box(10, 20, 30)
    cq.exporters.export(box, str(step_path))

    WebGeometryExporter().export_glb(step_path, output_path, model_id="box")

    assert output_path.exists()
    assert output_path.stat().st_size > 0
    loaded = trimesh.load(output_path)
    assert isinstance(loaded, trimesh.Scene)
    assert len(loaded.geometry) == 1
