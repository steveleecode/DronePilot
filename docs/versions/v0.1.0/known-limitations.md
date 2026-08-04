# Known Limitations

- STEP inspection imports `cad/v1-drone.step`, but assembly hierarchy,
  component names, and placement transforms are not recovered by the basic
  CadQuery importer.
- STEP units are detected from header unit declarations; unusual STEP files may
  need more robust OCP-level unit handling.
- Mass properties assume each imported solid has uniform density unless a
  manufacturer mass override is supplied programmatically.
- The CLI currently applies one global default material to every part.
- Inertia values are density-derived from CAD geometry and do not include motors,
  electronics, fasteners, batteries, propellers, or manufacturing variation
  unless those are represented as solids with appropriate material assumptions.
- GLB export preserves separate imported solids as scene nodes, but does not yet
  recover semantic assembly component names.
- Mesh quality uses one default tessellation tolerance and has not yet been
  visually tuned for the real drone.
- API endpoints regenerate missing artifacts synchronously, so first request
  latency can be high for the 44 MB STEP file.
- The frontend currently renders only a placeholder shell.
- The API currently exposes only `GET /health`.
- No browser visual validation has been performed for a real drone model yet.
- CAD files are untrusted inputs; parser hardening, file-size limits, topology
  diagnostics, and runtime limits still need implementation.
