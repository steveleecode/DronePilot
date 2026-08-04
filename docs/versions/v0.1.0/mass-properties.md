# Mass Properties

Mass-property analysis is planned for v0.1.0 but is not implemented in the
foundation commit.

## Conventions

- Internal units: SI.
- Mass: kilograms.
- Density: kilograms per cubic meter.
- Volume: cubic meters.
- Position and center of gravity: meters.
- Inertia tensor: kilogram-square meters.
- World coordinates: `+x` right, `+y` forward, `+z` up.

## Planned Model

Each part will distinguish its mass source:

- `density_calculated`: mass derived from material density and CAD volume.
- `manufacturer_override`: mass supplied explicitly for the part.
- `unassigned`: no reliable mass can be calculated.

The assembly center of gravity will be the mass-weighted average of part centers
of mass. Inertia tensors will be reported about the combined center of gravity
in the documented world frame and combined with the parallel-axis theorem.

No analysis result should be treated as proof that the CAD model is physically
flight-ready.
