# CAD Processing

## Current Status

The repository contains one STEP file at:

```text
cad/V.1 Drone .STEP Export.step
```

No CAD-processing code exists in v0.1.0. The STEP fixture has not been imported,
validated, meshed, or measured by project code.

## Planned Pipeline

The initial CAD pipeline should use Python with CadQuery and lower-level
OCP/Open CASCADE bindings:

1. Accept a CAD file path.
2. Validate file existence, type, size, and extension.
3. Import the STEP assembly.
4. Detect source units and convert to SI units.
5. Normalize parts, names, transforms, and identifiers.
6. Validate solids and report invalid or non-solid bodies.
7. Assign materials, densities, measured masses, and manufacturer mass
   overrides.
8. Calculate part volumes, masses, centers of mass, and inertia tensors.
9. Aggregate total mass, center of gravity, and assembly inertia tensor.
10. Create render meshes for the frontend.
11. Emit normalized JSON or typed models for downstream use.

## Replaceable Interface

CAD-specific objects should stay behind a replaceable interface:

```python
class CadProcessor:
    def import_assembly(self, path: str): ...
    def calculate_mass_properties(self, assembly, materials): ...
    def create_render_mesh(self, assembly): ...
```

The rest of the application should consume normalized assembly data. This keeps
the door open for migrating performance-critical operations to a separate C++
Open CASCADE service later.

## Materials And Mass Sources

Planned material metadata should include:

- Material identifier.
- Display name.
- Density in `kg/m^3`.
- Source and confidence.
- Optional notes for manufacturer or measured data.

Mass values should retain source information:

- `density_derived`: calculated from volume and density.
- `manufacturer_override`: specified by vendor data.
- `measured_override`: measured directly.

Derived mass and overrides must remain distinguishable because they have
different uncertainty and validation meaning.

## Mass Properties

Mass-property code should calculate:

- `volume_m3`
- `mass_kg`
- `center_of_mass_m`
- `center_of_gravity_m`
- `inertia_tensor_kg_m2`

Use the parallel-axis theorem for assembly-level inertia aggregation. Tests
should use tolerances rather than exact floating-point equality.

## CAD Security

Treat CAD files as untrusted input. Future processing should enforce size and
runtime limits, validate topology, avoid logging proprietary geometry, and avoid
using unsanitized file names in shell commands.

## Known Limitations In v0.1.0

- No importer exists.
- No material system exists.
- No mass-property calculation exists.
- No render mesh generation exists.
- No CAD fixture regression tests exist.
