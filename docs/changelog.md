# Documentation Changelog

## v0.1.0 - 2026-08-04

Associated Git commit: recorded per feature commit during the vertical-slice
implementation.

Milestone target:

> The repository can import the provided drone STEP file, calculate preliminary
> mass properties, export renderable geometry, and display the model and its
> properties in a browser.

Foundation changes:

- Renamed the provided STEP file from `cad/V.1 Drone .STEP Export.step` to
  `cad/v1-drone.step` through Git.
- Added Python backend package scaffolding with FastAPI, CadQuery, Pydantic,
  pytest, Ruff, and mypy configuration.
- Added React, TypeScript, Vite, Three.js, React Three Fiber, ESLint, Prettier,
  and Vitest frontend scaffolding.
- Added root `Makefile` commands for setup, CAD processing, web export,
  development servers, tests, linting, type checks, builds, and validation.
- Added generated-artifact boundaries under `generated/`.
- Updated versioned documentation to describe the implemented foundation and
  planned CAD analysis steps.

STEP inspection changes:

- Added typed CAD inspection models.
- Added a CadQuery STEP importer that validates paths, detects millimeter units,
  enumerates positive-volume solids, and converts geometry properties to SI
  units.
- Added STEPCAF metadata recovery for root and component labels.
- Added `python -m drone_cad.cli inspect-step cad/v1-drone.step`.
- Recorded actual import results for the provided drone: `300` usable solids and
  `0.0005540579326155427 m^3` summed solid volume.
- Recorded recovered assembly metadata: root label `Drone RCTimer with Realsense
  Camera`, `24` direct components, and `71` total component usages.

Mass analysis changes:

- Added material and part mass assignment models.
- Added an initial approximate material database.
- Added density-derived mass, manufacturer mass override behavior, combined
  center-of-gravity calculation, and inertia aggregation with the parallel-axis
  theorem.
- Added `python -m drone_cad.cli analyze cad/v1-drone.step --default-material
  carbon-fiber --output generated/v1-drone-analysis.json`.
- Recorded the preliminary carbon-fiber default analysis result:
  `0.8864926921848683 kg` total mass.
- Added JSON material assignment profiles for per-solid material and
  manufacturer-mass overrides.

Web export changes:

- Added a CadQuery tessellation to `trimesh` GLB export pipeline.
- Added `python -m drone_cad.cli export-web cad/v1-drone.step --output
  generated/v1-drone.glb`.
- Preserved separate imported solids as GLB scene geometry named by stable part
  IDs where possible.
- Verified the generated drone GLB is `11830320` bytes and loads as a scene with
  `300` geometries.

API changes:

- Added FastAPI routes for model metadata, analysis JSON, and GLB serving.
- Added narrow development CORS for the local Vite frontend.
- Added API tests using generated temporary artifacts.

Viewer changes:

- Added an interactive React Three Fiber viewer that loads API-served GLB
  geometry.
- Added center-of-gravity and wireframe toggles, orbit controls, camera reset,
  z-up grid, and engineering-property panel.
- Added frontend tests for API-loaded properties and engineering-value
  formatting.

Integration validation:

- Recorded the end-to-end browser validation result with desktop and narrow
  screenshots.
- Confirmed the API and frontend run together against generated analysis and
  GLB artifacts.

Handling estimate changes:

- Added motor and battery spec models with approximate common presets.
- Added custom motor and battery JSON spec loading.
- Added static handling estimates for thrust-to-weight ratio, hover throttle,
  hover current, hover power, and hover time.
- Added `GET /api/v1/models/v1-drone/handling`.
- Added `python -m drone_cad.cli estimate-handling`.
- Recorded the current default estimate: `2.9252169277848576`
  thrust-to-weight and `20.812796964258528 min` idealized hover time.
