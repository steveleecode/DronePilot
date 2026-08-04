from __future__ import annotations

import argparse
import json
from pathlib import Path


def _not_implemented(command: str) -> int:
    print(
        json.dumps(
            {
                "status": "not_implemented",
                "command": command,
                "message": "CAD processing is added in the next feature commit.",
            },
            indent=2,
        )
    )
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(prog="drone-cad")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect-step")
    inspect_parser.add_argument("step_path", type=Path)

    analyze_parser = subparsers.add_parser("analyze")
    analyze_parser.add_argument("step_path", type=Path)
    analyze_parser.add_argument("--default-material", default="carbon-fiber")
    analyze_parser.add_argument("--output", type=Path)

    export_parser = subparsers.add_parser("export-web")
    export_parser.add_argument("step_path", type=Path)
    export_parser.add_argument("--output", type=Path, required=True)

    args = parser.parse_args()
    return _not_implemented(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
