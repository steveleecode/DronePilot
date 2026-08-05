from pathlib import Path

import pytest

from drone_cad.services.propulsion_catalog import (
    PropulsionSpecError,
    get_battery_spec,
    get_motor_spec,
)


def test_load_custom_motor_spec(tmp_path: Path) -> None:
    path = tmp_path / "motor.json"
    path.write_text(
        """
        {
          "id": "custom",
          "name": "Custom motor",
          "kv_rating": 1000,
          "recommended_propeller_in": "10x4.5",
          "nominal_voltage_v": 14.8,
          "max_thrust_n": 10.0,
          "max_current_a": 20.0,
          "mass_kg": 0.05,
          "source_note": "test"
        }
        """,
        encoding="utf-8",
    )

    assert get_motor_spec("ignored", path).id == "custom"


def test_load_custom_battery_spec(tmp_path: Path) -> None:
    path = tmp_path / "battery.json"
    path.write_text(
        """
        {
          "id": "custom-pack",
          "name": "Custom pack",
          "cell_count": 4,
          "capacity_mah": 2200,
          "nominal_voltage_v": 14.8,
          "max_continuous_current_a": 80,
          "mass_kg": 0.22,
          "source_note": "test"
        }
        """,
        encoding="utf-8",
    )

    assert get_battery_spec("ignored", path).capacity_mah == 2200


def test_unknown_catalog_id_raises() -> None:
    with pytest.raises(PropulsionSpecError, match="Unknown motor"):
        get_motor_spec("missing")
