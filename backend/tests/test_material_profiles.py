from pathlib import Path

import pytest

from drone_cad.services.material_profiles import (
    MaterialProfileError,
    load_material_assignment_profile,
)


def test_load_material_assignment_profile(tmp_path: Path) -> None:
    profile_path = tmp_path / "profile.json"
    profile_path.write_text(
        """
        {
          "profile_id": "test",
          "description": "test profile",
          "default_material_id": "pla",
          "assignments": [
            {"part_id": "solid-001", "material_id": "aluminum-6061"},
            {"part_id": "solid-002", "manufacturer_mass_kg": 0.25}
          ]
        }
        """,
        encoding="utf-8",
    )

    profile = load_material_assignment_profile(profile_path)

    assert profile.default_material_id == "pla"
    assert profile.assignments[0].part_id == "solid-001"
    assert profile.assignments[1].manufacturer_mass_kg == 0.25


def test_load_material_assignment_profile_rejects_unknown_material(tmp_path: Path) -> None:
    profile_path = tmp_path / "profile.json"
    profile_path.write_text(
        """
        {
          "profile_id": "test",
          "description": "test profile",
          "assignments": [{"part_id": "solid-001", "material_id": "mystery"}]
        }
        """,
        encoding="utf-8",
    )

    with pytest.raises(MaterialProfileError, match="Unknown material"):
        load_material_assignment_profile(profile_path)


def test_load_material_assignment_profile_rejects_duplicate_part_ids(tmp_path: Path) -> None:
    profile_path = tmp_path / "profile.json"
    profile_path.write_text(
        """
        {
          "profile_id": "test",
          "description": "test profile",
          "assignments": [
            {"part_id": "solid-001", "material_id": "pla"},
            {"part_id": "solid-001", "material_id": "abs"}
          ]
        }
        """,
        encoding="utf-8",
    )

    with pytest.raises(MaterialProfileError, match="Duplicate part"):
        load_material_assignment_profile(profile_path)
