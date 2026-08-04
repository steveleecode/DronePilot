# Known Limitations

- STEP inspection imports `cad/v1-drone.step`, but assembly hierarchy,
  component names, and placement transforms are not recovered by the basic
  CadQuery importer.
- STEP units are detected from header unit declarations; unusual STEP files may
  need more robust OCP-level unit handling.
- No material assignment, volume-derived mass, center of gravity, bounding box,
  inertia tensor, or generated GLB exists yet.
- The frontend currently renders only a placeholder shell.
- The API currently exposes only `GET /health`.
- No browser visual validation has been performed for a real drone model yet.
- CAD files are untrusted inputs; parser hardening, file-size limits, topology
  diagnostics, and runtime limits still need implementation.
