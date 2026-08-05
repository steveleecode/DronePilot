# Simulation

## Current Status

The project now includes static handling estimates. Full rigid-body flight
simulation is still not implemented.

Implemented:

- Motor and battery spec models.
- Approximate common motor and battery presets.
- Custom motor and battery spec JSON loading.
- Static estimates for thrust-to-weight ratio, hover throttle, hover current,
  hover power, and hover time.

See [Handling Estimates](handling-estimates.md).

## Planned Model

The simulator should model:

- Rigid-body six-degree-of-freedom vehicle state.
- Motors.
- Propellers.
- Batteries.
- Thrust.
- Reaction torque.
- Drag.
- Gravity.
- Center-of-gravity effects.
- Inertia tensors.

## State Conventions

Before simulation state is shared across packages or APIs, document:

- Position units and frame.
- Velocity units and frame.
- Orientation representation.
- Quaternion ordering.
- Angular velocity units and frame.
- Force and torque sign conventions.
- Fixed timestep.

SI units should be used internally. External data must be converted at
boundaries.

## Separation From Rendering

Simulation code should produce state. Rendering code should display state.
Avoid putting physics integration, force accumulation, or vehicle dynamics
inside React components or Three.js scene objects.

## Deterministic Testing Targets

When implemented, simulation tests should cover:

- Unit conversion.
- Thrust calculation.
- Reaction torque.
- Drag forces.
- Battery state updates.
- Quaternion normalization.
- Fixed-timestep integration.
- Inertia-tensor use.
- Center-of-gravity offsets.
- Numerical tolerances for floating-point calculations.

## Known Limitations In v0.1.0

- No motor model exists.
- No propeller model exists.
- No battery model exists.
- No 6DOF dynamics model exists.
- No simulator API or state schema exists.
