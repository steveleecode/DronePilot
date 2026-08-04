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
- Frontend placeholder render test.
- Documentation local link validation.

## Required Engineering Tests

CAD and analysis feature commits should add deterministic tests for:

- Unit conversion.
- Volume-to-mass conversion.
- Center-of-gravity aggregation.
- Parallel-axis theorem.
- Inertia-tensor aggregation.
- Zero-volume handling.
- Missing-material handling.
- Manufacturer mass overrides.
- Invalid or non-solid CAD bodies.

Use tolerances rather than exact floating-point equality for numerical results.

## Visual Checks

The foundation commit does not render the real CAD model. Browser visual
validation is required when the Three.js viewer is implemented.
