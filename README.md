# DronePilot

DronePilot is a CAD-based drone analysis and simulation project. The current
milestone establishes the project structure for importing the bundled STEP
drone, calculating preliminary engineering properties, exporting browser
geometry, and viewing the result in a React and Three.js frontend.

The source CAD fixture is tracked as:

```text
cad/v1-drone.step
```

The original uploaded filename was `cad/V.1 Drone .STEP Export.step`. It was
renamed through Git to avoid fragile shell quoting and path handling.

## Prerequisites

- Python 3.11 or 3.12.
- Node.js 20 or another current LTS release.
- npm.

## Commands

Install all dependencies:

```sh
make setup
```

Install only backend dependencies:

```sh
make setup-backend
```

Install only frontend dependencies:

```sh
make setup-frontend
```

Process the STEP file into normalized analysis JSON:

```sh
make process-cad
```

Equivalent direct command:

```sh
.venv/bin/python -m drone_cad.cli analyze cad/v1-drone.step --default-material carbon-fiber --output generated/v1-drone-analysis.json
```

Inspect the STEP file and print normalized geometry JSON:

```sh
.venv/bin/python -m drone_cad.cli inspect-step cad/v1-drone.step
```

Export browser-renderable geometry:

```sh
make export-web
```

Start the API:

```sh
make dev-api
```

Start the frontend:

```sh
make dev-frontend
```

Run tests:

```sh
make test
```

Run linting and documentation-link validation:

```sh
make lint
```

Run type checks:

```sh
make typecheck
```

Build frontend production assets:

```sh
make build
```

Run the practical local validation suite:

```sh
make validate
```

Run the local demo after setup and processing:

```sh
make process-cad
make export-web
make dev-api
make dev-frontend
```

## Documentation

- [AGENTS.md](AGENTS.md) defines repository conventions for coding agents.
- [docs/README.md](docs/README.md) explains the versioned documentation system.
- [docs/current.md](docs/current.md) points to the active documentation snapshot.
