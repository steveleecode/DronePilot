# Testing And Validation

## Current Status

No automated test framework exists in v0.1.0.

The only repository validation command is:

```sh
./scripts/validate-docs-links.sh
```

This command validates local Markdown links in root documentation and
`docs/**/*.md`.

## Required Testing Direction

Future features should add focused tests with the feature code. Validation
should be as narrow as possible while still covering the risk of the change.

Expected validation categories:

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

## Engineering Calculation Cases

Tests for engineering calculations should cover:

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

Use tolerances rather than exact floating-point equality for numerical results
where appropriate.

## CAD Fixtures

The current STEP file may become an integration fixture, but no code imports it
yet. When CAD import is added, include smaller deterministic fixtures where
possible so routine tests do not depend only on a large assembly file.

## Visual Checks

No visual checks can run in v0.1.0 because there is no frontend.

When a frontend exists, any change affecting rendering, overlays, animation,
layout, or interaction must include a visual check and record the result.
