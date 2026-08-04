# Frontend

## Current Status

The frontend scaffold exists under `frontend/` and uses React, TypeScript,
Vite, Three.js, React Three Fiber, and Vitest. The foundation screen is a
placeholder shell for the CAD viewer.

Run it with:

```sh
make dev-frontend
```

## Planned Viewer

The v0.1.0 viewer will:

- Load model metadata and analysis from the FastAPI backend.
- Display `generated/v1-drone.glb`.
- Provide orbit controls and a camera reset.
- Show a grid or reference plane.
- Render a center-of-gravity marker from backend coordinates.
- Toggle the center-of-gravity marker.
- Toggle wireframe or part-boundary display where practical.
- Present engineering properties and warnings in a side panel.
- Handle loading and error states.

## Boundaries

- `src/lib/`: API clients and shared utilities.
- `src/features/`: domain-specific viewer and analysis features.
- `src/components/`: reusable UI components.

The frontend must not hard-code calculated CAD properties. It consumes typed API
responses and generated geometry.

## Visual-Check Requirements

Any real viewer change must be checked in a browser at desktop and narrow
widths. The check should verify model visibility, camera framing, orbit
controls, center-of-gravity marker placement, console errors, and layout.
