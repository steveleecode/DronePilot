# Frontend

## Current Status

No frontend code exists in v0.1.0.

## Planned Frontend

The planned frontend should use React with Three.js or React Three Fiber to show
the imported drone and its simulated movement.

Expected capabilities:

- Load normalized assembly data.
- Render drone geometry from generated meshes.
- Show camera controls.
- Display center-of-gravity overlays.
- Display thrust vectors and motor state.
- Animate simulation state.
- Surface CAD-processing and simulation errors clearly.

## Scene Data Boundaries

The frontend should consume normalized data from a backend or static fixture.
It should not depend on CadQuery, OCP, or Open CASCADE objects.

Rendering data and physics data should stay separate:

- Render meshes describe visual geometry.
- Simulation state describes time, position, orientation, velocity, and control
  state.
- Engineering overlays describe centers of gravity, inertia, thrust, and part
  metadata.

## Coordinate Systems

The project has not selected final coordinate conventions yet. When a frontend
is introduced, document:

- CAD source coordinate system.
- Simulation world coordinate system.
- Three.js coordinate system.
- Unit scale used by the scene.
- Quaternion ordering at API boundaries.

## Visual-Check Requirements

Any frontend, Three.js scene, overlay, animation, layout, or interaction change
must receive a visual check before commit:

1. Start required services.
2. Open the affected interface.
3. Exercise the changed interaction.
4. Check browser-console errors.
5. Check relevant responsive sizes.
6. Verify model, camera, controls, overlays, and simulation state.
7. Save a screenshot or visual artifact when supported.
8. Record the result in docs or commit notes.

Do not claim visual validation when no frontend or browser target exists.

## Known Limitations In v0.1.0

- No React app exists.
- No Three.js scene exists.
- No visual-check target exists.
- No generated render meshes exist.
