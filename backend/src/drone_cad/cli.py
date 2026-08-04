from __future__ import annotations

import argparse
import json
from pathlib import Path

from drone_cad.cad import StepImporter
from drone_cad.services.mass_properties import MassPropertyAnalyzer
from drone_cad.services.web_export import WebGeometryExporter


def _write_json(payload: str, output_path: Path | None = None) -> None:
    if output_path is None:
        print(payload)
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(payload + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(prog="drone-cad")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect-step")
    inspect_parser.add_argument("step_path", type=Path)
    inspect_parser.add_argument("--output", type=Path)

    analyze_parser = subparsers.add_parser("analyze")
    analyze_parser.add_argument("step_path", type=Path)
    analyze_parser.add_argument("--default-material", default="carbon-fiber")
    analyze_parser.add_argument("--output", type=Path)

    export_parser = subparsers.add_parser("export-web")
    export_parser.add_argument("step_path", type=Path)
    export_parser.add_argument("--output", type=Path, required=True)
    export_parser.add_argument("--tolerance", type=float, default=0.8)

    args = parser.parse_args()
    if args.command == "inspect-step":
        inspection = StepImporter().inspect(args.step_path)
        _write_json(inspection.model_dump_json(indent=2), args.output)
        return 0

    if args.command == "analyze":
        analysis = MassPropertyAnalyzer().analyze_step(
            args.step_path,
            default_material_id=args.default_material,
        )
        _write_json(analysis.model_dump_json(indent=2), args.output)
        return 0

    if args.command == "export-web":
        WebGeometryExporter().export_glb(
            args.step_path,
            output_path=args.output,
            tolerance=args.tolerance,
        )
        print(json.dumps({"status": "ok", "output": str(args.output)}, indent=2))
        return 0

    print(
        json.dumps(
            {
                "status": "not_implemented",
                "command": args.command,
                "message": "This command is added in a later feature commit.",
            },
            indent=2,
        )
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
