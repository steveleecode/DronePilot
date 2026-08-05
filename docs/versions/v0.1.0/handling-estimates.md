# Handling Estimates

The next simulation step is a static handling and energy estimate. It uses the
current CAD-derived mass analysis plus a motor and battery specification to
estimate whether a multicopter configuration has enough thrust and energy
margin to hover.

This is not a full flight simulator. It does not model aerodynamic drag,
propeller performance curves, ESC efficiency, voltage sag, wind, attitude
dynamics, control loops, or six-degree-of-freedom motion.

## Built-In Presets

Motor presets:

- `2212-920kv-1045`: common 2212-class motor with 10x4.5 prop.
- `2306-2400kv-5045`: common 5-inch FPV class motor with 5x4.5 prop.
- `3508-700kv-1245`: larger aerial-photo class motor with 12x4.5 prop.

Battery presets:

- `4s-5200mah-35c-lipo`
- `4s-1500mah-100c-lipo`
- `6s-10000mah-25c-lipo`

These presets are approximate sizing defaults. Real hardware selection should
use measured thrust tables, battery mass, discharge tests, ESC limits, propeller
choice, and environmental conditions.

## CLI

Generate analysis first:

```sh
make process-cad
```

Estimate handling:

```sh
python -m drone_cad.cli estimate-handling \
  --analysis generated/v1-drone-analysis.json \
  --motor 2212-920kv-1045 \
  --battery 4s-5200mah-35c-lipo \
  --motor-count 4
```

Use custom motor and battery specs:

```sh
python -m drone_cad.cli estimate-handling \
  --analysis generated/v1-drone-analysis.json \
  --motor-spec config/propulsion/motor.custom.example.json \
  --battery-spec config/propulsion/battery.custom.example.json
```

Options:

- `--payload-mass-kg`: adds payload mass.
- `--base-airframe-mass-kg`: overrides the CAD-derived base mass.
- `--exclude-battery-mass`: assumes the analysis mass already includes battery
  mass.

## API

The API exposes:

```text
GET /api/v1/models/v1-drone/handling
```

Query parameters:

- `motor`
- `battery`
- `motor_count`
- `payload_mass_kg`
- `include_battery_mass`

## Output

The estimate includes:

- Gross mass.
- Vehicle weight.
- Maximum total thrust.
- Thrust-to-weight ratio.
- Estimated hover throttle.
- Estimated hover current.
- Estimated hover power.
- Estimated hover time.
- Warnings for low thrust margin, high hover throttle, current limit issues, or
  voltage mismatch.

## Current Default Estimate

Using `generated/v1-drone-analysis.json`, `2212-920kv-1045`, four motors, and
`4s-5200mah-35c-lipo`:

- Gross mass: `1.3664926921848681 kg`.
- Weight: `13.400715559814737 N`.
- Maximum total thrust: `39.2 N`.
- Thrust-to-weight ratio: `2.9252169277848576`.
- Estimated hover throttle: `0.3418549887707841`.
- Estimated hover current: `11.992621675435261 A`.
- Estimated hover power: `177.49080079644187 W`.
- Estimated hover time: `20.812796964258528 min`.
- Warnings: none.

This result is optimistic because it uses simplified current scaling and an
approximate battery usable-capacity assumption.
