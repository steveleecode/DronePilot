from __future__ import annotations

from pydantic import BaseModel, Field


class MotorSpec(BaseModel):
    id: str
    name: str
    kv_rating: int
    recommended_propeller_in: str
    nominal_voltage_v: float
    max_thrust_n: float
    max_current_a: float
    mass_kg: float
    source_note: str


class BatterySpec(BaseModel):
    id: str
    name: str
    cell_count: int
    capacity_mah: float
    nominal_voltage_v: float
    max_continuous_current_a: float
    mass_kg: float
    usable_capacity_fraction: float = 0.8
    source_note: str


class HandlingEstimateMetadata(BaseModel):
    model_id: str
    motor_id: str
    battery_id: str
    source_analysis_mass_kg: float
    mass_accounting_note: str
    calculation_note: str = (
        "Static handling estimate only. It does not model aerodynamic drag, propeller curves, "
        "ESC efficiency, voltage sag, attitude dynamics, control loops, or 6DOF motion."
    )


class DroneHandlingEstimate(BaseModel):
    gross_mass_kg: float
    base_airframe_mass_kg: float
    battery_mass_kg: float
    payload_mass_kg: float
    weight_n: float
    motor_count: int
    max_total_thrust_n: float
    thrust_to_weight_ratio: float
    hover_throttle_fraction: float
    estimated_hover_current_a: float
    estimated_hover_power_w: float
    estimated_hover_time_min: float | None
    warnings: list[str] = Field(default_factory=list)
    motor: MotorSpec
    battery: BatterySpec
    metadata: HandlingEstimateMetadata
