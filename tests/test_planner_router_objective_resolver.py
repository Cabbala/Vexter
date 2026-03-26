import json
import shutil
from pathlib import Path

import pytest

from vexter.planner_router.config_loader import load_planner_router_package
from vexter.planner_router.errors import ConfigValidationError, UnknownObjectiveProfileError
from vexter.planner_router.models import PlanRequest, RouteMode, Source, SourcePinRegistry
from vexter.planner_router.objective_resolver import resolve_objective_profile


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


def test_resolve_objective_profile_defaults_to_mixed_default() -> None:
    package = load_planner_router_package(CONFIG_ROOT, FROZEN_PINS)

    objective = resolve_objective_profile(PlanRequest(plan_request_id="req-1"), package)

    assert objective.objective_profile_id == "mixed_default"
    assert objective.preferred_source is Source.DEXTER
    assert objective.route_mode is RouteMode.SINGLE_SLEEVE
    assert objective.primary_sleeve_id == "dexter_default"


def test_resolve_objective_profile_rejects_unknown_explicit_profile() -> None:
    package = load_planner_router_package(CONFIG_ROOT, FROZEN_PINS)

    with pytest.raises(UnknownObjectiveProfileError):
        resolve_objective_profile(
            PlanRequest(plan_request_id="req-2", objective_profile_id="unknown_profile"),
            package,
        )


def test_resolve_objective_profile_requires_explicit_containment_for_mewx(tmp_path: Path) -> None:
    config_root = clone_config_dir(tmp_path)
    objective_profiles_path = config_root / "objective_profiles.json"
    payload = json.loads(objective_profiles_path.read_text())
    payload[1]["objective_profile_id"] = "mewx_timeout_only"
    objective_profiles_path.write_text(json.dumps(payload, indent=2) + "\n")
    package = load_planner_router_package(config_root, FROZEN_PINS)

    with pytest.raises(ConfigValidationError):
        resolve_objective_profile(
            PlanRequest(plan_request_id="req-3", objective_profile_id="mewx_timeout_only"),
            package,
        )
