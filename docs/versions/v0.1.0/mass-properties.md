# Mass Properties

Mass-property analysis is implemented for preliminary density-derived CAD
analysis.

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

## Material Database

The initial material database contains approximate defaults:

- `carbon-fiber`: Carbon fiber composite, `1600 kg/m^3`.
- `aluminum-6061`: Aluminum 6061, `2700 kg/m^3`.
- `pla`: PLA, `1240 kg/m^3`.
- `abs`: ABS, `1040 kg/m^3`.
- `generic-steel`: Generic steel, `7850 kg/m^3`.

Each density is an approximate engineering default. Real drone parts need
material-specific, manufacturing-specific, measured, or manufacturer-supplied
mass data before engineering conclusions are made.

## Actual Analysis Result

Command:

```sh
python -m drone_cad.cli analyze cad/v1-drone.step --default-material carbon-fiber --output generated/v1-drone-analysis.json
```

Result using the approximate `carbon-fiber` default for every imported solid:

- Part count: `300`.
- Total CAD volume: `0.0005540579326155427 m^3`.
- Density-derived total mass: `0.8864926921848683 kg`.
- Center of gravity: `x=-0.22902988883221 m`,
  `y=0.005018542802884506 m`, `z=0.033072371107097966 m`.
- Bounding box: `0.4889966331918045 m x 0.49986626311032695 m x
  0.10102408664317991 m`.
- Principal moments:
  `[0.005870994775351748, 0.011903012589879696, 0.01708921788910604] kg*m^2`.

Inertia tensor about the combined center of gravity:

```text
[
  [0.0058721272217846015, 0.00002428454440922621, 0.0001077315359459865],
  [0.00002428454440922621, 0.01190291482590322, -0.00000009208994624403452],
  [0.0001077315359459865, -0.00000009208994624403452, 0.017088183206649656]
]
```

Warnings:

- The STEP file imports as one compound, so assembly hierarchy, component names,
  and placements are not recovered by the basic CadQuery importer.

## Material Assignment Profiles

Analysis can read a JSON material assignment profile:

```sh
python -m drone_cad.cli analyze cad/v1-drone.step \
  --assignments config/material-assignments/v1-drone.example.json \
  --output generated/v1-drone-analysis.json
```

Profile fields:

- `profile_id`: stable identifier for the assignment set.
- `description`: human-readable note about the profile.
- `default_material_id`: optional default material for all unassigned solids.
- `assignments`: per-solid overrides keyed by stable IDs such as `solid-001`.

Each assignment may specify:

- `material_id`: one of the known material database IDs.
- `manufacturer_mass_kg`: an explicit mass override. When present, this mass
  takes precedence over density-derived mass for that solid.

The example profile is illustrative and is not manufacturer-validated data.
Component labels recovered from STEPCAF are not yet correlated one-to-one with
the stable `solid-###` IDs, so assignment profiles currently target solid IDs.
