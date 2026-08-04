# Frontend

## Current Status

The frontend exists under `frontend/` and uses React, TypeScript, Vite,
Three.js, React Three Fiber, `@react-three/drei`, and Vitest.

Run it with:

```sh
make dev-frontend
```

## Implemented Viewer

The viewer:

- Loads model metadata and analysis from the FastAPI backend.
- Displays the API-served GLB through React Three Fiber.
- Provides orbit controls and a camera reset control.
- Shows a z-up reference grid and axes.
- Renders a center-of-gravity marker from backend coordinates.
- Includes toggles for center-of-gravity visibility and wireframe display.
- Presents mass, volume, part count, bounding dimensions, center of gravity,
  inertia tensor, material assumption, and warnings in a side panel.
- Handles loading and error states.

## Boundaries

- `src/lib/`: API clients and shared utilities.
- `src/features/`: domain-specific viewer and analysis features.
- `src/components/`: reusable UI components.

The frontend must not hard-code calculated CAD properties. It consumes typed API
responses and generated geometry.

The scene uses the documented world convention: `+x` right, `+y` forward, and
`+z` up. The camera and grid are configured for z-up display so exported CAD
coordinates and center-of-gravity coordinates can be used directly.

## Visual-Check Requirements

Any real viewer change must be checked in a browser at desktop and narrow
widths. The check should verify model visibility, camera framing, orbit
controls, center-of-gravity marker placement, console errors, and layout.

## Viewer Visual Check

Initial browser validation was performed against the real API and GLB output on
2026-08-04.

- Backend started at `http://127.0.0.1:8000`.
- Frontend started at `http://127.0.0.1:5173`.
- The GLB loaded in the browser.
- Drone geometry, z-up grid, and center-of-gravity marker were visible.
- Engineering properties loaded from the API.
- COG and wireframe toggles responded.
- Reset-camera control responded.
- No browser console warnings or errors were reported during the check.
- Desktop screenshot: [viewer-desktop.png](artifacts/viewer-desktop.png).
- Narrow screenshot: [viewer-mobile.png](artifacts/viewer-mobile.png).

See [Visual Validation](visual-validation.md) for the full integration record.
