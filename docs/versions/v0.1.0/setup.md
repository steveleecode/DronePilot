# Setup

## Prerequisites

No runtime prerequisites are defined by the repository yet because there is no
application code, package manifest, or build system.

Useful local tools:

- Git.
- A POSIX-compatible shell for `scripts/validate-docs-links.sh`.

Future work may introduce Python, CadQuery, OCP/Open CASCADE, Node.js,
TypeScript, React, Three.js, C++, and Open CASCADE system dependencies.

## Install Dependencies

No install command exists yet.

The repository does not currently include any of these files:

- `package.json`
- `pyproject.toml`
- `requirements.txt`
- `Cargo.toml`
- `CMakeLists.txt`
- Lock files

## Development Services

No development service command exists yet.

## Frontend

No frontend application exists yet. There is no command to start or build a
frontend.

## Backend

No backend application exists yet. There is no command to start a backend API.

## CAD-Processing Workers

No CAD-processing worker exists yet. There is no command to import the STEP file
or calculate mass properties.

## Simulator

No simulator exists yet. There is no command to run dynamics simulation.

## Tests, Linters, Formatters, Type Checks, And Builds

No test, lint, format, type-check, or production-build command exists yet.

## Documentation Validation

Run:

```sh
./scripts/validate-docs-links.sh
```

This checks local Markdown links in root documentation and `docs/**/*.md`.

## Visual Checks

No visual-check workflow can run yet because there is no frontend.

When a frontend is added, visual checks should include running the required
services, opening the changed screen, checking browser-console errors, testing
responsive sizes, verifying Three.js model/camera/control/overlay behavior, and
saving a screenshot when supported by the environment.
