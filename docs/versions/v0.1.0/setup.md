# Setup

## Prerequisites

- Python 3.11 or 3.12.
- Node.js 20 or another current LTS release.
- npm.
- Git and a POSIX-compatible shell.

The backend uses CadQuery and OCP/Open CASCADE through Python dependencies.
Those packages may install platform-specific wheels.

## Install Dependencies

Install all dependencies:

```sh
make setup
```

Backend only:

```sh
make setup-backend
```

Frontend only:

```sh
make setup-frontend
```

## CAD Processing

Analyze the source STEP file:

```sh
make process-cad
```

Export browser geometry:

```sh
make export-web
```

These commands target `cad/v1-drone.step` and write generated artifacts under
`generated/`.

## Development Services

Start the API:

```sh
make dev-api
```

Start the frontend:

```sh
make dev-frontend
```

`make dev` prints the two commands because they are intended to run in separate
terminals.

## Tests, Linters, Type Checks, And Builds

Run tests:

```sh
make test
```

Run linting and Markdown-link validation:

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

Run practical validation:

```sh
make validate
```

## Local Demo

After dependencies are installed, run:

```sh
make process-cad
make export-web
make dev-api
make dev-frontend
```

The processing commands become fully operational in the CAD import and export
feature commits.
