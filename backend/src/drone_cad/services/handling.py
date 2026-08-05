from __future__ import annotations

from drone_cad.models.analysis import DroneAnalysis
from drone_cad.models.propulsion import (
    BatterySpec,
    DroneHandlingEstimate,
    HandlingEstimateMetadata,
    MotorSpec,
)

GRAVITY_M_S2 = 9.80665


def estimate_handling(
    analysis: DroneAnalysis,
    motor: MotorSpec,
    battery: BatterySpec,
    motor_count: int = 4,
    payload_mass_kg: float = 0.0,
    include_battery_mass: bool = True,
    base_airframe_mass_kg: float | None = None,
) -> DroneHandlingEstimate:
    if motor_count <= 0:
        raise ValueError("motor_count must be positive")
    if payload_mass_kg < 0:
        raise ValueError("payload_mass_kg cannot be negative")

    base_mass = (
        base_airframe_mass_kg if base_airframe_mass_kg is not None else analysis.total_mass_kg
    )
    battery_mass = battery.mass_kg if include_battery_mass else 0.0
    gross_mass = base_mass + battery_mass + payload_mass_kg
    weight_n = gross_mass * GRAVITY_M_S2
    max_total_thrust_n = motor.max_thrust_n * motor_count
    thrust_to_weight = max_total_thrust_n / weight_n if weight_n > 0 else 0.0
    hover_throttle = weight_n / max_total_thrust_n if max_total_thrust_n > 0 else 1.0
    hover_throttle = max(0.0, hover_throttle)
    estimated_hover_current_a = motor_count * motor.max_current_a * min(hover_throttle, 1.0) ** 1.5
    estimated_hover_power_w = estimated_hover_current_a * battery.nominal_voltage_v
    usable_capacity_ah = battery.capacity_mah / 1000.0 * battery.usable_capacity_fraction
    estimated_hover_time_min = (
        usable_capacity_ah / estimated_hover_current_a * 60.0
        if estimated_hover_current_a > 0
        else None
    )

    warnings = _handling_warnings(
        thrust_to_weight=thrust_to_weight,
        hover_throttle=hover_throttle,
        estimated_hover_current_a=estimated_hover_current_a,
        battery=battery,
        motor=motor,
    )

    return DroneHandlingEstimate(
        gross_mass_kg=gross_mass,
        base_airframe_mass_kg=base_mass,
        battery_mass_kg=battery_mass,
        payload_mass_kg=payload_mass_kg,
        weight_n=weight_n,
        motor_count=motor_count,
        max_total_thrust_n=max_total_thrust_n,
        thrust_to_weight_ratio=thrust_to_weight,
        hover_throttle_fraction=hover_throttle,
        estimated_hover_current_a=estimated_hover_current_a,
        estimated_hover_power_w=estimated_hover_power_w,
        estimated_hover_time_min=estimated_hover_time_min,
        warnings=warnings,
        motor=motor,
        battery=battery,
        metadata=HandlingEstimateMetadata(
            model_id=analysis.model_id,
            motor_id=motor.id,
            battery_id=battery.id,
            source_analysis_mass_kg=analysis.total_mass_kg,
            mass_accounting_note=(
                "Battery mass included as an additional mass term."
                if include_battery_mass
                else "Battery mass excluded; CAD/analysis mass is assumed to include it."
            ),
        ),
    )


def _handling_warnings(
    thrust_to_weight: float,
    hover_throttle: float,
    estimated_hover_current_a: float,
    battery: BatterySpec,
    motor: MotorSpec,
) -> list[str]:
    warnings: list[str] = []
    if thrust_to_weight < 1.0:
        warnings.append("Maximum thrust is below vehicle weight; hover is not possible.")
    elif thrust_to_weight < 1.5:
        warnings.append("Thrust-to-weight ratio is low for multicopter control margin.")
    elif thrust_to_weight < 2.0:
        warnings.append("Thrust-to-weight ratio is flyable only with limited control margin.")

    if hover_throttle > 0.8:
        warnings.append("Estimated hover throttle is high; handling and climb margin are limited.")
    if estimated_hover_current_a > battery.max_continuous_current_a:
        warnings.append("Estimated hover current exceeds battery continuous discharge rating.")
    if abs(motor.nominal_voltage_v - battery.nominal_voltage_v) / battery.nominal_voltage_v > 0.15:
        warnings.append("Motor nominal voltage differs materially from selected battery voltage.")
    return warnings
