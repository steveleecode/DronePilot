# AGENTS.md

This file is the operating guide for coding agents working in this repository.
Follow it before changing code, documentation, CAD assets, or project
configuration.

## Repository Overview

DronePilot is intended to become a CAD-based drone simulation project. The long
term system should import drone CAD assemblies, assign engineering metadata to
parts, calculate mass properties, simulate vehicle dynamics, and visualize the
vehicle in a React and Three.js or React Three Fiber frontend.

Current repository state:

- Implemented: a root `README.md`, this `AGENTS.md`, versioned documentation
  under `docs/`, a local documentation link validator, and one STEP CAD file at
  `cad/V.1 Drone .STEP Export.step`.
- Not yet implemented: Python CAD processing, backend APIs, simulation code,
  frontend visualization, test suites, package manifests, CI, deployment, and a
  C++ Open CASCADE service.
- Git branch observed when this file was created: `main`, tracking
  `origin/main`.
- Recent history observed when this file was created:
  - `776fd3e Create V.1 Drone .STEP Export.step`
  - `d7d946d first commit`

Important paths:

- `cad/`: CAD input fixtures. Currently contains the initial STEP assembly.
- `docs/`: versioned documentation system.
- `docs/versions/v0.1.0/`: initial documentation snapshot for the current
  repository.
- `docs/current.md`: pointer and summary for the current documentation version.
- `docs/changelog.md`: documentation version index and change history.
- `scripts/validate-docs-links.sh`: local Markdown link validator for docs and
  root documentation files.
- `README.md`: short project entry point.

Planned architecture boundaries:

- CAD processing should live behind a replaceable interface so Python
  CadQuery/OCP implementations can later move to a C++ Open CASCADE service
  without forcing frontend rewrites.
- Backend APIs should expose normalized JSON data, not CadQuery or Open CASCADE
  objects.
- Simulation physics should remain independent from rendering logic.
- Frontend rendering should consume simulation and CAD-derived data through
  explicit schemas.

Example target CAD boundary:

```python
class CadProcessor:
    def import_assembly(self, path: str): ...
    def calculate_mass_properties(self, assembly, materials): ...
    def create_render_mesh(self, assembly): ...
```

Example target normalized result:

```json
{
  "parts": [
    {
      "id": "battery",
      "name": "Battery",
      "material_id": null,
      "volume_m3": 0.00012,
      "mass_kg": 0.42,
      "mass_source": "manufacturer_override",
      "center_of_mass_m": [0.0, -0.04, -0.02],
      "transform": []
    }
  ],
  "total_mass_kg": 1.82,
  "center_of_gravity_m": [0.01, -0.004, -0.03],
  "inertia_tensor_kg_m2": []
}
```

Treat these examples as architectural direction until matching code exists.

## Setup And Development Commands

The repository currently has no package manifest, virtual environment config,
frontend app, backend app, simulator, CI config, or test runner. Do not invent
commands in summaries or commits.

Available commands:

```sh
./scripts/validate-docs-links.sh
```

Use the command above to validate local Markdown links in `README.md`,
`AGENTS.md`, and `docs/**/*.md`.

Commands that do not exist yet:

- Install dependencies: no `package.json`, `pyproject.toml`, `requirements.txt`,
  `Cargo.toml`, `CMakeLists.txt`, or equivalent exists.
- Start development services: no service runner exists.
- Run the frontend: no frontend directory or script exists.
- Run the backend: no backend directory or script exists.
- Run CAD-processing workers: no worker code or script exists.
- Run the simulator: no simulator code or script exists.
- Run tests: no test framework is configured.
- Run linters: no linter is configured.
- Run formatters: no formatter is configured.
- Run type checks: no type checker is configured.
- Build production artifacts: no build system is configured.
- Perform visual checks: no frontend or browser target exists.

When adding a toolchain, add the narrowest useful script to the relevant package
configuration and update this file plus the current docs in the same commit.

## Coding Conventions

### Python

- Use Python for initial CAD import and engineering calculations when those
  modules are added.
- Prefer typed data models for CAD metadata, materials, mass properties, and API
  boundaries.
- Keep CadQuery/OCP-specific objects behind CAD adapter interfaces.
- Avoid leaking Open CASCADE handles into simulation, API, or frontend code.
- Use deterministic numerical tests with tolerances for engineering math.

### TypeScript And React

- Use TypeScript for frontend code when a frontend is added.
- Keep React components focused on UI and visualization state.
- Keep physics integration and CAD processing out of React components.
- Prefer explicit API schemas for data crossing from backend to frontend.
- Use Three.js or React Three Fiber for 3D rendering; document the chosen scene
  structure before relying on it across features.

### C++

- No C++ code exists yet.
- If performance-critical CAD operations move to C++, isolate the service behind
  the same normalized CAD-processing contract used by the Python implementation.
- Document compiler, build, test, and Open CASCADE dependency requirements when
  C++ is introduced.

### API Schemas

- Use stable, versioned schemas for backend/frontend boundaries.
- Include units in field names where practical, such as `mass_kg`, `volume_m3`,
  `center_of_mass_m`, and `inertia_tensor_kg_m2`.
- Distinguish derived values from user-provided or manufacturer-provided values.
- Document quaternion ordering wherever quaternions cross a boundary.

### Units And Coordinate Systems

- Use SI units internally unless an external CAD, vendor, or API format requires
  another unit system.
- Convert external units at boundaries and record the source unit.
- Make units explicit in variable names, typed models, and documentation where
  practical.
- Document coordinate-system conventions before adding simulation or rendering
  features.
- Document any conversion between CAD coordinates, physics coordinates, and
  Three.js coordinates.

### CAD Geometry Handling

- Treat CAD files as untrusted inputs.
- Validate file type, size, parse status, unit metadata, body solidity, and
  topology health before using CAD-derived properties.
- Keep invalid or non-solid bodies visible in diagnostics instead of silently
  dropping them.
- Do not assume assembly names, material names, or STEP entity ordering are
  stable.
- Generate render meshes separately from mass-property calculations.

### Materials And Mass Properties

- Keep density-derived mass and manufacturer-provided mass overrides
  distinguishable.
- Record `mass_source` values such as `density_derived`,
  `manufacturer_override`, or `measured_override`.
- Store densities in `kg/m^3`.
- Calculate aggregate center of gravity and inertia tensors from part-level
  properties using documented formulas and tolerances.
- Cover unit conversion, volume-to-mass conversion, center-of-gravity
  aggregation, parallel-axis theorem, and inertia-tensor aggregation in tests
  when implemented.

### Simulation State

- Simulation code should avoid mixing rendering logic with physics logic.
- Use fixed-timestep integration where practical.
- Normalize quaternions after integration.
- Document quaternion ordering, body/world frame conventions, and sign
  conventions for thrust, torque, drag, and angular velocity.
- Add deterministic tests for thrust, reaction torque, drag, quaternion
  normalization, and fixed-timestep integration.

### Error Handling

- Fail loudly on invalid units, missing required mass properties, malformed CAD
  results, and incompatible schema versions.
- Return structured errors from APIs and workers.
- Include actionable context without dumping huge CAD payloads into logs.

### Logging

- Use structured logs when services are added.
- Log CAD file identifiers, processing stage, timing, and high-level validation
  results.
- Do not log proprietary CAD contents, secrets, or large mesh payloads.

### Testing

- Add tests close to the code under test.
- Use tolerances instead of exact floating-point equality for numerical results.
- Add fixtures for valid, invalid, and edge-case CAD bodies when CAD processing
  exists.
- Include API contract tests before depending on backend/frontend schemas.
- Add browser and screenshot checks for frontend and Three.js changes.

### Documentation

- Update documentation in the same commit as behavior changes.
- Distinguish implemented functionality from planned functionality.
- Avoid copying inaccurate architecture forward into later version snapshots.
- Update `docs/current.md` and `docs/changelog.md` for meaningful milestones.

### Dependency Management

- Commit dependency manifest and lock files together.
- Keep Python, Node, and C++ dependencies scoped to the packages that use them.
- Document system dependencies such as Open CASCADE, CadQuery, Node.js, and
  compilers when introduced.
- Separate dependency update commits from feature commits unless the dependency
  is directly required for that feature.

## Git Workflow

Codex is authorized to use Git for this repository, including creating or
switching branches when appropriate, staging files, creating commits, pushing
commits to the current remote branch, and creating multiple commits on the same
feature branch.

Before modifying files:

1. Run `git status --short --branch`.
2. Identify the current branch.
3. Inspect relevant recent commits.
4. Confirm that no unrelated user changes will be overwritten.

Never discard, reset, overwrite, or amend unrelated user work. Do not use
destructive commands such as `git reset --hard`, `git clean -fd`, forced pushes,
or rewriting shared history unless the user explicitly requests them.

If unrelated changes are present, leave them alone. If they overlap with the
task, understand them before editing and work with them.

## Feature Commit And Push Policy

Every distinct feature or logically independent change must be implemented,
validated, committed, and pushed separately.

For each feature:

1. Inspect the relevant code and documentation.
2. Implement only that feature's scoped changes.
3. Run the relevant tests, linting, formatting, type checks, builds, and visual
   checks.
4. Update the documentation for that feature.
5. Review `git diff`.
6. Create one focused commit.
7. Push that commit before beginning the next feature.

Do not combine unrelated features into one commit.

Examples of separate feature boundaries:

- Adding STEP import.
- Adding material assignment.
- Adding mass-property calculations.
- Adding a motor model.
- Adding battery simulation.
- Adding six-degree-of-freedom dynamics.
- Adding the Three.js viewer.
- Adding center-of-gravity overlays.
- Adding thrust-vector visualization.
- Adding WebSocket simulation streaming.
- Updating dependencies.
- Refactoring an API boundary.
- Adding tests.
- Updating documentation infrastructure.

Small fixes directly required by a feature may remain in that feature's commit.
Unrelated fixes must be separated.

Use clear commit messages, for example:

- `feat(cad): add STEP assembly import`
- `feat(materials): add density-based mass calculation`
- `feat(simulation): add rigid-body state integration`
- `feat(viewer): render center-of-gravity overlay`
- `fix(cad): handle invalid solid volume`
- `docs: add CAD processing architecture`
- `chore(deps): update frontend dependencies`

After each successful commit, push using the normal non-force push command for
the current branch.

If pushing fails because of authentication, permissions, branch protection,
remote divergence, or another external issue:

- Preserve the local commit.
- Report the exact failure.
- Do not force-push.
- Continue only when doing so will not create confusing or conflicting history.

## Validation Requirements

Before committing a feature, run the narrowest relevant validation plus any
required repository-wide checks.

Validation may include:

- Unit tests.
- Integration tests.
- Python type checking.
- TypeScript type checking.
- Linting.
- Formatting checks.
- Production builds.
- CAD fixture imports.
- Numerical regression tests.
- API contract tests.
- Browser rendering checks.
- Screenshot or visual checks.

For physics and engineering calculations, add deterministic tests where
possible. Tests should cover tolerances rather than exact floating-point
equality when appropriate.

Important engineering cases:

- Unit conversion.
- Volume-to-mass conversion.
- Center-of-gravity calculation.
- Parallel-axis theorem.
- Inertia-tensor aggregation.
- Thrust and reaction torque.
- Quaternion normalization.
- Fixed-timestep integration.
- Invalid or non-solid CAD bodies.
- Manufacturer mass overrides.
- Missing material assignments.

Current repository-wide validation:

```sh
./scripts/validate-docs-links.sh
```

## Visual-Check Workflow

Any feature that affects the frontend, Three.js scene, simulation animation,
overlays, layout, or user interaction must receive a visual check before
committing.

Visual-check process:

1. Start the required development services.
2. Open the affected interface.
3. Test the changed interaction.
4. Check for browser-console errors.
5. Check relevant responsive sizes.
6. Verify that the 3D model, camera, controls, overlays, and simulation state
   appear correctly.
7. Save a screenshot or other visual artifact when the available environment
   supports it.
8. Record the visual-check result in the feature documentation or commit notes.

Do not claim a visual check succeeded if the environment did not permit one.
State the limitation clearly.

## Documentation Workflow

Documentation lives under `docs/` and supports versioned snapshots:

```text
docs/
├── README.md
├── versions/
│   └── v0.1.0/
│       ├── overview.md
│       ├── architecture.md
│       ├── setup.md
│       ├── cad-processing.md
│       ├── simulation.md
│       ├── frontend.md
│       └── testing.md
├── decisions/
├── templates/
│   └── version-release.md
├── changelog.md
└── current.md
```

For each documentation release:

- Create a semantic version such as `v0.1.0`.
- Preserve prior documentation versions.
- Update `docs/current.md`.
- Update `docs/changelog.md`.
- Record the Git commit associated with the version where practical.
- Distinguish implemented functionality from proposed functionality.
- Avoid copying inaccurate architecture forward into later versions.

Semantic-versioning guidance:

- Patch: documentation corrections, small fixes, or minor non-breaking
  implementation changes.
- Minor: new features or substantial new documented capabilities.
- Major: breaking architectural, API, data-model, or workflow changes.

Do not create a new documentation version for every trivial typo. Do create one
when a meaningful feature changes the documented system.

Each feature commit that changes behavior must update the current documentation.
When the feature constitutes a meaningful product milestone, create or advance
the versioned documentation snapshot in the same feature commit.

## Security Notes

CAD files can be large, proprietary, malformed, or intentionally hostile. Future
CAD-processing services should run with least privilege, validate inputs before
expensive operations, avoid shelling out with unsanitized paths, enforce file
size and runtime limits, and keep generated meshes or logs from exposing more
model detail than intended.
