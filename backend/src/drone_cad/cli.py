from __future__ import annotations

import argparse
import json
from pathlib import Path

from drone_cad.cad import StepImporter
from drone_cad.models.analysis import DroneAnalysis
from drone_cad.services.handling import estimate_handling
from drone_cad.services.mass_properties import MassPropertyAnalyzer
from drone_cad.services.material_profiles import (
    MaterialProfileError,
    load_material_assignment_profile,
)
from drone_cad.services.propulsion_catalog import (
    BATTERY_SPECS,
    MOTOR_SPECS,
    PropulsionSpecError,
    get_battery_spec,
    get_motor_spec,
)
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
    analyze_parser.add_argument("--assignments", type=Path)
    analyze_parser.add_argument("--output", type=Path)

    export_parser = subparsers.add_parser("export-web")
    export_parser.add_argument("step_path", type=Path)
    export_parser.add_argument("--output", type=Path, required=True)
    export_parser.add_argument("--tolerance", type=float, default=0.8)

    handling_parser = subparsers.add_parser("estimate-handling")
    handling_parser.add_argument(
        "--analysis",
        type=Path,
        default=Path("generated/v1-drone-analysis.json"),
    )
    handling_parser.add_argument("--motor", default="2212-920kv-1045", choices=sorted(MOTOR_SPECS))
    handling_parser.add_argument(
        "--battery",
        default="4s-5200mah-35c-lipo",
        choices=sorted(BATTERY_SPECS),
    )
    handling_parser.add_argument("--motor-spec", type=Path)
    handling_parser.add_argument("--battery-spec", type=Path)
    handling_parser.add_argument("--motor-count", type=int, default=4)
    handling_parser.add_argument("--payload-mass-kg", type=float, default=0.0)
    handling_parser.add_argument("--base-airframe-mass-kg", type=float)
    handling_parser.add_argument("--exclude-battery-mass", action="store_true")
    handling_parser.add_argument("--output", type=Path)

    args = parser.parse_args()
    if args.command == "inspect-step":
        inspection = StepImporter().inspect(args.step_path)
        _write_json(inspection.model_dump_json(indent=2), args.output)
        return 0

    if args.command == "analyze":
        default_material = args.default_material
        assignments = []
        if args.assignments is not None:
            try:
                profile = load_material_assignment_profile(args.assignments)
            except MaterialProfileError as exc:
                parser.error(str(exc))
            default_material = profile.default_material_id or default_material
            assignments = profile.assignments
        analysis = MassPropertyAnalyzer().analyze_step(
            args.step_path,
            default_material_id=default_material,
            assignments=assignments,
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

    if args.command == "estimate-handling":
        try:
            analysis = DroneAnalysis.model_validate_json(args.analysis.read_text(encoding="utf-8"))
            motor = get_motor_spec(args.motor, args.motor_spec)
            battery = get_battery_spec(args.battery, args.battery_spec)
            estimate = estimate_handling(
                analysis=analysis,
                motor=motor,
                battery=battery,
                motor_count=args.motor_count,
                payload_mass_kg=args.payload_mass_kg,
                include_battery_mass=not args.exclude_battery_mass,
                base_airframe_mass_kg=args.base_airframe_mass_kg,
            )
        except FileNotFoundError:
            parser.error(f"Analysis file not found: {args.analysis}")
        except (PropulsionSpecError, ValueError) as exc:
            parser.error(str(exc))
        _write_json(estimate.model_dump_json(indent=2), args.output)
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
