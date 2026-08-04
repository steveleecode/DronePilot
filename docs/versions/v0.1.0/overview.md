# DronePilot v0.1.0 Overview

DronePilot is an early CAD-based drone simulation project. The intended product
will import drone CAD assemblies, assign materials and measured engineering
metadata, calculate mass properties, simulate six-degree-of-freedom dynamics,
and display the drone in a React and Three.js or React Three Fiber frontend.

## Implemented In This Snapshot

- Root project README.
- One STEP CAD assembly fixture:
  `cad/V.1 Drone .STEP Export.step`.
- Versioned documentation under `docs/`.
- Root `AGENTS.md` workflow instructions.
- Local Markdown link validator at `scripts/validate-docs-links.sh`.

## Not Yet Implemented

- Python CAD importer.
- CadQuery or OCP/Open CASCADE integration.
- Material assignment model.
- Volume, mass, center-of-gravity, or inertia calculations.
- Motor, propeller, battery, drag, torque, or dynamics models.
- Backend API.
- React frontend.
- Three.js or React Three Fiber scene.
- Test suites, linters, type checks, builds, CI, or deployment.
- C++ Open CASCADE service.

## Current Repository Layout

```text
.
├── AGENTS.md
├── README.md
├── cad/
│   └── V.1 Drone .STEP Export.step
├── docs/
│   ├── README.md
│   ├── changelog.md
│   ├── current.md
│   ├── decisions/
│   ├── templates/
│   │   └── version-release.md
│   └── versions/
│       └── v0.1.0/
│           ├── architecture.md
│           ├── cad-processing.md
│           ├── frontend.md
│           ├── overview.md
│           ├── setup.md
│           ├── simulation.md
│           └── testing.md
└── scripts/
    └── validate-docs-links.sh
```

## Current CAD Fixture

The STEP file header reports:

- File name: `V.1 Drone .STEP Export.step`.
- Timestamp: `2026-07-31T10:38:13-04:00`.
- Originating system: `Autodesk Translation Framework v15.8.0.0`.
- STEP schema: `AUTOMOTIVE_DESIGN`.

The documentation does not assume this file has already been parsed or
validated by project code.

## Product Direction

The planned system should support these stages:

1. Import a CAD assembly.
2. Normalize part identities, transforms, units, and metadata.
3. Assign materials, densities, measured masses, manufacturer masses, and other
   engineering metadata.
4. Calculate part and assembly mass properties.
5. Build simulation-ready drone models.
6. Run deterministic physics simulation.
7. Stream or load state into a frontend viewer.
8. Render geometry, center of gravity, thrust vectors, and simulation movement.

All planned stages must be introduced incrementally with tests and
documentation.
