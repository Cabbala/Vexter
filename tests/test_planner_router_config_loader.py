import json
import shutil
from pathlib import Path

import pytest

from vexter.planner_router.config_loader import load_planner_router_package
from vexter.planner_router.errors import ConfigLoadError, ConfigValidationError
from vexter.planner_router.models import FailureCode, Source, SourcePinRegistry


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_ROOT = REPO_ROOT / "config" / "planner_router"
FROZEN_PINS = SourcePinRegistry(
    dexter="ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
    mewx="dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
)


def clone_config_dir(tmp_path: Path) -> Path:
    destination = tmp_path / "planner_router"
    shutil.copytree(CONFIG_ROOT, destination)
    return destination


def test_load_planner_router_package_uses_repo_config() -> None:
    package = load_planner_router_package(CONFIG_ROOT, FROZEN_PINS)

    assert package.planner.default_execution_anchor is Source.DEXTER
    assert package.planner.default_objective_profile_id == "mixed_default"
    assert tuple(mode.value for mode in package.planner.allowed_route_modes) == (
        "single_sleeve",
        "portfolio_split",
    )
    assert package.sleeves["dexter_default"].executor_profile is not None
    assert package.sleeves["mewx_containment"].enabled is False


def test_load_planner_router_package_rejects_duplicate_ids(tmp_path: Path) -> None:
    config_root = clone_config_dir(tmp_path)
    objective_profiles_path = config_root / "objective_profiles.json"
    payload = json.loads(objective_profiles_path.read_text())
    payload.append(dict(payload[0]))
    objective_profiles_path.write_text(json.dumps(payload, indent=2) + "\n")

    with pytest.raises(ConfigLoadError) as exc_info:
        load_planner_router_package(config_root, FROZEN_PINS)

    assert exc_info.value.failure is not None
    assert exc_info.value.failure.code is FailureCode.DUPLICATE_CONFIG_ID


def test_load_planner_router_package_rejects_pin_mismatch(tmp_path: Path) -> None:
    config_root = clone_config_dir(tmp_path)
    executor_profiles_path = config_root / "executor_profiles.json"
    payload = json.loads(executor_profiles_path.read_text())
    payload[0]["pinned_commit"] = "deadbeef"
    executor_profiles_path.write_text(json.dumps(payload, indent=2) + "\n")

    with pytest.raises(ConfigValidationError) as exc_info:
        load_planner_router_package(config_root, FROZEN_PINS)

    assert exc_info.value.failure is not None
    assert exc_info.value.failure.code is FailureCode.PIN_MISMATCH
