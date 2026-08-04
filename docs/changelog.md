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
