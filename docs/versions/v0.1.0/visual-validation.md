# Visual Validation

Visual validation was performed on 2026-08-04 against the real local vertical
slice.

## Commands

Generated analysis:

```sh
make process-cad
```

Generated GLB:

```sh
make export-web
```

Started API:

```sh
make dev-api
```

Started frontend:

```sh
make dev-frontend
```

Ran validation:

```sh
make validate
```

## Results

- Backend started successfully at `http://127.0.0.1:8000`.
- Frontend started successfully at `http://127.0.0.1:5173`.
- STEP processing completed for `cad/v1-drone.step`.
- GLB export completed as `generated/v1-drone.glb`.
- GLB loaded in the browser through the API.
- Drone geometry was visible.
- Camera framing was adjusted until the drone was visible with the grid.
- Orbit controls were present.
- Center-of-gravity marker was visible and plausibly positioned on the drone.
- Analysis properties loaded from the API.
- COG and wireframe toggles responded.
- Reset-camera control responded.
- No critical browser-console warnings or errors were reported.
- No critical backend errors were reported.
- Desktop and narrow responsive layouts were checked.

Screenshots:

- [Desktop viewer](artifacts/viewer-desktop.png)
- [Narrow viewer](artifacts/viewer-mobile.png)

## Notes

- The model is rendered with a neutral unlit material because the tessellated
  GLB normals/materials did not produce useful lit shading in the browser.
- The browser uses the documented z-up convention so backend coordinates and the
  center-of-gravity marker can be used directly.
- Full physical flight simulation, controls, propulsion, and battery modeling
  are not implemented in v0.1.0.
