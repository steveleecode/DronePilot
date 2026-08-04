# CAD Processing

## Current Status

The source STEP file is:

```text
cad/v1-drone.step
```

It was renamed through Git from `cad/V.1 Drone .STEP Export.step` so project
commands can use a stable, path-safe filename. The original file content is
unchanged.

The STEP inspection feature implements:

```sh
python -m drone_cad.cli inspect-step cad/v1-drone.step
```

The analyzer and GLB exporter are now implemented in v0.1.0 feature commits.

## Actual Import Results

`cad/v1-drone.step` was imported successfully with CadQuery.

- Detected root shape type: `Compound`.
- Recovered STEPCAF root label: `Drone RCTimer with Realsense Camera`.
- Recovered direct assembly component labels: `24`.
- Recovered total component usages: `71`.
- Detected source length unit: millimeter.
- Length scale to SI meters: `0.001`.
- Usable solids found: `300`.
- Sum of usable solid volumes: `0.0005540579326155427 m^3`.
- Sum of usable solid surface areas: `0.4037010449866602 m^2`.
- Bounding box: `0.4889966331918045 m x 0.49986626311032695 m x
  0.10102408664317991 m`.

Warnings:

- CadQuery imports the file as one compound. STEPCAF recovers component labels,
  but component-to-solid correlation is not yet implemented.
- Stable IDs are generated as `solid-001`, `solid-002`, and so on from the
  imported solid order.

Representative recovered component labels:

- `15. Brazo v1:1`
- `base drone v1:1`
- `Zippy2800 v1:1`
- `18. Motor v1:1`
- `17. Hélice v1:1`
- `Intel Realsense D435 v1:1`
- `CASING BARU RASPI 4 v11:1`
- `Pixhawk 2.4.8 v1:1`
- `SPF455A 4in1 ESC v1:1`

## Planned Pipeline

Implemented:

1. Validate file existence, type, size, and extension.
2. Import the STEP assembly with CadQuery.
3. Detect millimeter source units and convert to SI units.
4. Enumerate positive-volume solids.
5. Generate stable internal part IDs.
6. Calculate volume, surface area, center of mass, bounds, and warnings.
7. Recover STEPCAF root and component labels when available.

Web export:

- `python -m drone_cad.cli export-web cad/v1-drone.step --output generated/v1-drone.glb`
  tessellates each imported solid and writes one GLB scene node per stable part
  ID.
- Vertices are converted to meters before export.
- Meshes are generated for browser display, not mass-property calculation.
- The current export path uses CadQuery tessellation plus `trimesh` GLB export
  because CadQuery does not provide direct GLB export in this environment.
- The real drone export produced `generated/v1-drone.glb`, `11830320` bytes,
  loadable by `trimesh` as a scene with `300` geometries.

Still planned:

1. Correlate STEPCAF component labels and transforms to imported solids.
2. Tune mesh quality after browser visual validation.

## Unit Convention

All normalized outputs use SI units:

- `volume_m3`
- `surface_area_m2`
- `center_of_mass_m`
- `mass_kg`
- `density_kg_m3`
- `inertia_tensor_kg_m2`

## Assembly Metadata

The STEP file came from Autodesk tooling. Assembly names, part names, and STEP
entity ordering should not be assumed stable until recovered and normalized by
the importer.
