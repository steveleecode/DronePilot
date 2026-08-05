from drone_cad.models.analysis import AnalysisMetadata, DroneAnalysis
from drone_cad.models.cad import BoundingBox, Vector3
from drone_cad.services.handling import estimate_handling
from drone_cad.services.propulsion_catalog import get_battery_spec, get_motor_spec


def _analysis(mass_kg: float = 1.0) -> DroneAnalysis:
    return DroneAnalysis(
        model_id="test-drone",
        part_count=0,
        total_volume_m3=0.0,
        total_mass_kg=mass_kg,
        center_of_gravity_m=Vector3(x=0.0, y=0.0, z=0.0),
        inertia_tensor_kg_m2=[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        principal_moments_kg_m2=[0.0, 0.0, 0.0],
        bounding_box_m=BoundingBox(x=0.0, y=0.0, z=0.0),
        materials=[],
        parts=[],
        warnings=[],
        metadata=AnalysisMetadata(source_step_path="test.step", source_length_unit="millimeter"),
    )


def test_estimate_handling_calculates_hover_metrics() -> None:
    estimate = estimate_handling(
        analysis=_analysis(1.0),
        motor=get_motor_spec("2212-920kv-1045"),
        battery=get_battery_spec("4s-5200mah-35c-lipo"),
        motor_count=4,
        include_battery_mass=True,
    )

    assert estimate.gross_mass_kg == 1.48
    assert estimate.thrust_to_weight_ratio > 2.0
    assert 0.0 < estimate.hover_throttle_fraction < 1.0
    assert estimate.estimated_hover_time_min is not None
    assert (
        estimate.metadata.mass_accounting_note
        == "Battery mass included as an additional mass term."
    )


def test_estimate_handling_warns_when_underpowered() -> None:
    estimate = estimate_handling(
        analysis=_analysis(5.0),
        motor=get_motor_spec("2212-920kv-1045"),
        battery=get_battery_spec("4s-5200mah-35c-lipo"),
        motor_count=4,
    )

    assert any("below vehicle weight" in warning for warning in estimate.warnings)


def test_estimate_handling_can_exclude_battery_mass() -> None:
    estimate = estimate_handling(
        analysis=_analysis(1.0),
        motor=get_motor_spec("2212-920kv-1045"),
        battery=get_battery_spec("4s-5200mah-35c-lipo"),
        motor_count=4,
        include_battery_mass=False,
    )

    assert estimate.gross_mass_kg == 1.0
    assert estimate.battery_mass_kg == 0.0
