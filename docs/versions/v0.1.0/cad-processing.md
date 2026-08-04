# CAD Processing

## Current Status

The source STEP file is:

```text
cad/v1-drone.step
```

It was renamed through Git from `cad/V.1 Drone .STEP Export.step` so project
commands can use a stable, path-safe filename. The original file content is
unchanged.

The foundation commit includes CLI command placeholders for:

```sh
python -m drone_cad.cli inspect-step cad/v1-drone.step
python -m drone_cad.cli analyze cad/v1-drone.step --default-material carbon-fiber
python -m drone_cad.cli export-web cad/v1-drone.step --output generated/v1-drone.glb
```

The importer, analyzer, and exporter are implemented in later v0.1.0 feature
commits.

## Planned Pipeline

1. Validate file existence, type, size, and extension.
2. Import the STEP assembly with CadQuery and OCP/Open CASCADE where needed.
3. Detect or document source units and convert to SI units.
4. Enumerate usable solids or components.
5. Generate stable internal part IDs.
6. Capture names and transforms when available.
7. Calculate volume, surface area, center of mass, bounds, and warnings.
8. Apply material assignments and mass overrides.
9. Calculate assembly mass, center of gravity, and inertia.
10. Export browser geometry.

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
