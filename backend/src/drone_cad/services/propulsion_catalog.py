from __future__ import annotations

import json
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from drone_cad.models.propulsion import BatterySpec, MotorSpec

MOTOR_SPECS: dict[str, MotorSpec] = {
    "2212-920kv-1045": MotorSpec(
        id="2212-920kv-1045",
        name="2212 920KV class quad motor with 10x4.5 prop",
        kv_rating=920,
        recommended_propeller_in="10x4.5",
        nominal_voltage_v=14.8,
        max_thrust_n=9.8,
        max_current_a=15.0,
        mass_kg=0.055,
        source_note=(
            "Approximate common 2212-class multicopter motor preset for early sizing. "
            "Replace with measured thrust stand data before design decisions."
        ),
    ),
    "2306-2400kv-5045": MotorSpec(
        id="2306-2400kv-5045",
        name="2306 2400KV class FPV motor with 5x4.5 prop",
        kv_rating=2400,
        recommended_propeller_in="5x4.5",
        nominal_voltage_v=14.8,
        max_thrust_n=13.0,
        max_current_a=36.0,
        mass_kg=0.032,
        source_note=(
            "Approximate common 5-inch FPV motor preset. High-current behavior depends "
            "strongly on propeller, ESC, and battery voltage sag."
        ),
    ),
    "3508-700kv-1245": MotorSpec(
        id="3508-700kv-1245",
        name="3508 700KV class aerial-photo motor with 12x4.5 prop",
        kv_rating=700,
        recommended_propeller_in="12x4.5",
        nominal_voltage_v=22.2,
        max_thrust_n=22.0,
        max_current_a=28.0,
        mass_kg=0.095,
        source_note=(
            "Approximate larger multicopter motor preset for heavier camera platforms. "
            "Use manufacturer thrust tables for real sizing."
        ),
    ),
}

BATTERY_SPECS: dict[str, BatterySpec] = {
    "4s-5200mah-35c-lipo": BatterySpec(
        id="4s-5200mah-35c-lipo",
        name="4S 5200mAh 35C LiPo pack",
        cell_count=4,
        capacity_mah=5200.0,
        nominal_voltage_v=14.8,
        max_continuous_current_a=182.0,
        mass_kg=0.48,
        source_note=(
            "Approximate common 4S 5200mAh LiPo class pack. Actual mass and discharge "
            "rating vary by vendor and pack age."
        ),
    ),
    "4s-1500mah-100c-lipo": BatterySpec(
        id="4s-1500mah-100c-lipo",
        name="4S 1500mAh 100C LiPo pack",
        cell_count=4,
        capacity_mah=1500.0,
        nominal_voltage_v=14.8,
        max_continuous_current_a=150.0,
        mass_kg=0.18,
        source_note=(
            "Approximate common 5-inch FPV LiPo class pack. C-ratings are optimistic "
            "and should be validated under load."
        ),
    ),
    "6s-10000mah-25c-lipo": BatterySpec(
        id="6s-10000mah-25c-lipo",
        name="6S 10000mAh 25C LiPo pack",
        cell_count=6,
        capacity_mah=10000.0,
        nominal_voltage_v=22.2,
        max_continuous_current_a=250.0,
        mass_kg=1.35,
        source_note=(
            "Approximate larger 6S aerial-platform pack preset. Confirm pack mass, "
            "connector, and discharge behavior before hardware selection."
        ),
    ),
}

SpecT = TypeVar("SpecT", bound=BaseModel)


class PropulsionSpecError(ValueError):
    """Raised when motor or battery specs cannot be loaded."""


def get_motor_spec(spec_id: str, custom_path: Path | None = None) -> MotorSpec:
    if custom_path is not None:
        return _load_spec(custom_path, MotorSpec)
    try:
        return MOTOR_SPECS[spec_id]
    except KeyError as exc:
        raise PropulsionSpecError(f"Unknown motor spec id: {spec_id}") from exc


def get_battery_spec(spec_id: str, custom_path: Path | None = None) -> BatterySpec:
    if custom_path is not None:
        return _load_spec(custom_path, BatterySpec)
    try:
        return BATTERY_SPECS[spec_id]
    except KeyError as exc:
        raise PropulsionSpecError(f"Unknown battery spec id: {spec_id}") from exc


def _load_spec(path: Path, model_type: type[SpecT]) -> SpecT:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return model_type.model_validate(payload)
    except FileNotFoundError as exc:
        raise PropulsionSpecError(f"Spec file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PropulsionSpecError(f"Invalid JSON in spec file: {path}") from exc
    except ValidationError as exc:
        raise PropulsionSpecError(f"Invalid spec schema: {exc}") from exc
