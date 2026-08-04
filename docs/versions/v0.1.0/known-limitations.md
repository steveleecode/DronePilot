# Known Limitations

- The foundation commit has not yet parsed `cad/v1-drone.step`.
- STEP units and assembly metadata are not yet recovered by project code.
- No material assignment, volume-derived mass, center of gravity, bounding box,
  inertia tensor, or generated GLB exists yet.
- The frontend currently renders only a placeholder shell.
- The API currently exposes only `GET /health`.
- No browser visual validation has been performed for a real drone model yet.
- CAD files are untrusted inputs; parser hardening, file-size limits, topology
  diagnostics, and runtime limits still need implementation.
