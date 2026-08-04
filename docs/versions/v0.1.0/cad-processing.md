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

The analyzer and exporter are implemented in later v0.1.0 feature commits.

## Actual Import Results

`cad/v1-drone.step` was imported successfully with CadQuery.

- Detected root shape type: `Compound`.
- Detected source length unit: millimeter.
- Length scale to SI meters: `0.001`.
- Usable solids found: `300`.
- Sum of usable solid volumes: `0.0005540579326155427 m^3`.
- Sum of usable solid surface areas: `0.4037010449866602 m^2`.
- Bounding box: `0.4889966331918045 m x 0.49986626311032695 m x
  0.10102408664317991 m`.

Warnings:

- The file imported as one compound. Assembly hierarchy, component names, and
  placement transforms were not recovered by the basic CadQuery importer.
- Stable IDs are generated as `solid-001`, `solid-002`, and so on from the
  imported solid order.

## Planned Pipeline

Implemented:

1. Validate file existence, type, size, and extension.
2. Import the STEP assembly with CadQuery.
3. Detect millimeter source units and convert to SI units.
4. Enumerate positive-volume solids.
5. Generate stable internal part IDs.
6. Calculate volume, surface area, center of mass, bounds, and warnings.

Planned:

1. Recover richer assembly names and transforms through lower-level OCP APIs.
2. Export browser geometry.

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
