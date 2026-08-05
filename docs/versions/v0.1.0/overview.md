# DronePilot v0.1.0 Overview

DronePilot is a CAD-based drone analysis and simulation project. The v0.1.0
milestone is the first end-to-end foundation for importing the bundled STEP
drone, calculating preliminary mass properties, exporting renderable geometry,
and displaying model properties in a browser.

## Implemented In This Snapshot

- Root `Makefile` with setup, processing, development, validation, and build
  commands.
- Python backend package scaffold under `backend/`.
- FastAPI application with `GET /health`.
- React, TypeScript, and Vite frontend scaffold under `frontend/`.
- Generated artifact directory boundary under `generated/`.
- Versioned documentation under `docs/`.
- Local Markdown link validator at `scripts/validate-docs-links.sh`.
- Git-tracked CAD file rename to `cad/v1-drone.step`.
- STEP inspection CLI that imports the provided drone and reports normalized
  part geometry.
- STEPCAF assembly metadata recovery for the root model label and direct
  component labels.
- Material database and mass-property analyzer with density-derived mass,
  manufacturer override support, center-of-gravity aggregation, and inertia
  aggregation.
- Interactive React and Three.js viewer that loads API data and generated GLB
  geometry.
- Static handling estimator with motor and battery presets plus custom JSON
  spec loading.

## Not Yet Implemented

- Rich STEP assembly hierarchy and placement recovery.
- Per-part custom material assignment files.
- GLB or glTF export.
- API endpoints for model metadata and analysis.
- Visual validation of the real viewer in a browser.
- Full flight dynamics, propeller performance curves, battery discharge curves,
  PID control, PX4 or ArduPilot integration, CFD, deployment, or auth.

## Current Repository Layout

```text
.
├── AGENTS.md
├── Makefile
├── README.md
├── backend/
│   ├── pyproject.toml
│   ├── src/drone_cad/
│   └── tests/
├── cad/
│   └── v1-drone.step
├── docs/
├── frontend/
│   ├── package.json
│   └── src/
├── generated/
│   └── .gitkeep
└── scripts/
    └── validate-docs-links.sh
```

## CAD Fixture

The STEP file is `cad/v1-drone.step`. It was originally supplied as
`cad/V.1 Drone .STEP Export.step` and renamed through Git to reduce path-handling
errors.

The STEP header reports:

- Original file name: `V.1 Drone .STEP Export.step`.
- Timestamp: `2026-07-31T10:38:13-04:00`.
- Originating system: `Autodesk Translation Framework v15.8.0.0`.
- STEP schema: `AUTOMOTIVE_DESIGN`.

The foundation commit does not claim the file has been parsed or validated by
project code. The STEP inspection feature imported it as a compound with 300
usable solids, detected millimeter source units, and measured a summed solid
volume of `0.0005540579326155427 m^3`. With the approximate `carbon-fiber`
default material, the density-derived total mass is `0.8864926921848683 kg`.
STEPCAF metadata recovery identifies the root model as `Drone RCTimer with
Realsense Camera`, with `24` direct component labels and `71` total component
usages.

## Product Direction

The system is being introduced in vertical slices:

1. Tooling and project structure.
2. STEP import and inspection.
3. Material and mass-property analysis.
4. Browser geometry export.
5. FastAPI model and analysis endpoints.
6. Interactive React and Three.js viewer.
7. Visual validation and integration polish.
