# Testing And Validation

## Current Commands

Run backend and frontend tests:

```sh
make test
```

Run linting plus Markdown-link validation:

```sh
make lint
```

Run type checks:

```sh
make typecheck
```

Run production build checks:

```sh
make build
```

Run the practical validation suite:

```sh
make validate
```

## Current Coverage

- Backend health endpoint test.
- STEP unit detection test.
- STEP inspection test using a generated box fixture.
- Density-to-mass, mass override, missing material, zero-volume, part inertia,
  parallel-axis, and aggregate inertia tests.
- GLB export test that writes a generated box fixture and verifies `trimesh`
  can load the resulting file as a non-empty scene.
- API tests for model metadata, generated analysis response loading, and GLB
  file serving.
- Frontend tests for API-backed analysis rendering and engineering value
  formatting.
- Frontend placeholder render test.
- Documentation local link validation.

## Required Engineering Tests

CAD and analysis feature commits should add deterministic tests for:

- Unit conversion.
- CAD unit conversion beyond the initial millimeter path.
- Invalid or non-solid CAD bodies.

Use tolerances rather than exact floating-point equality for numerical results.

## Visual Checks

The foundation commit does not render the real CAD model. Browser visual
validation is required when the Three.js viewer is implemented.
