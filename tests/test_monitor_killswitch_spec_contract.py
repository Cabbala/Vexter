import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pytest

from vexter.planner_router.budget_binder import bind_budgets
from vexter.planner_router.config_loader import load_planner_router_package
from vexter.planner_router.errors import ConfigValidationError
from vexter.planner_router.models import (
    FailureCode,
    PlanRequest,
    ResolvedPlanningContext,
    Source,
    SourcePinRegistry,
)
from vexter.planner_router.objective_resolver import resolve_objective_profile
from vexter.planner_router.plan_emitter import build_execution_plans
from vexter.planner_router.sleeve_selector import select_sleeves


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_ROOT = REPO_ROOT / "config" / "planner_router"
FROZEN_PINS = SourcePinRegistry(
    dexter="ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
    mewx="dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
)
CREATED_AT = datetime(2026, 3, 26, 3, 0, tzinfo=timezone.utc)


def clone_config_dir(tmp_path: Path) -> Path:
    destination = tmp_path / "planner_router"
    shutil.copytree(CONFIG_ROOT, destination)
    return destination


def enable_mewx_sleeve(config_root: Path) -> None:
    sleeves_path = config_root / "sleeves.json"
    payload = json.loads(sleeves_path.read_text())
    payload[1]["enabled"] = True
    sleeves_path.write_text(json.dumps(payload, indent=2) + "\n")


def build_context(config_root: Path, request: PlanRequest) -> ResolvedPlanningContext:
    package = load_planner_router_package(config_root, FROZEN_PINS)
    resolved_objective = resolve_objective_profile(request, package)
    selected_sleeves = select_sleeves(resolved_objective, package.sleeves)
    budget_bindings = bind_budgets(request, resolved_objective, selected_sleeves, package.budget_policies)
    return ResolvedPlanningContext(
        request=request,
        package=package,
        resolved_objective=resolved_objective,
        selected_sleeves=selected_sleeves,
        budget_bindings=budget_bindings,
    )


def test_monitor_profiles_bind_expected_classes_and_scope() -> None:
    package = load_planner_router_package(CONFIG_ROOT, FROZEN_PINS)

    dexter_profile = package.monitor_profiles["dexter_default"]
    mewx_profile = package.monitor_profiles["mewx_timeout_guard"]

    assert (
        dexter_profile.admission_gate_class,
        dexter_profile.timeout_envelope_class,
        dexter_profile.quarantine_scope,
        dexter_profile.global_halt_participation,
    ) == ("lifecycle_control", "dexter_lifecycle_control", "sleeve", True)
    assert (
        mewx_profile.admission_gate_class,
        mewx_profile.timeout_envelope_class,
        mewx_profile.quarantine_scope,
        mewx_profile.global_halt_participation,
    ) == ("timeout_aware", "mewx_timeout_tolerant", "sleeve", True)


def test_resolve_objective_profile_rejects_active_global_halt(tmp_path: Path) -> None:
    config_root = clone_config_dir(tmp_path)
    planner_path = config_root / "planner.json"
    payload = json.loads(planner_path.read_text())
    payload["global_halt_policy"]["active"] = True
    planner_path.write_text(json.dumps(payload, indent=2) + "\n")
    package = load_planner_router_package(config_root, FROZEN_PINS)

    with pytest.raises(ConfigValidationError) as exc_info:
        resolve_objective_profile(PlanRequest(plan_request_id="req-monitor-halt"), package)

    assert exc_info.value.failure is not None
    assert exc_info.value.failure.code is FailureCode.GLOBAL_HALT_ACTIVE


def test_resolve_objective_profile_requires_timeout_tolerant_monitor_for_mewx(tmp_path: Path) -> None:
    config_root = clone_config_dir(tmp_path)
    monitor_profiles_path = config_root / "monitor_profiles.json"
    payload = json.loads(monitor_profiles_path.read_text())
    payload[1]["timeout_envelope_class"] = "mewx_lifecycle_control"
    monitor_profiles_path.write_text(json.dumps(payload, indent=2) + "\n")
    package = load_planner_router_package(config_root, FROZEN_PINS)

    with pytest.raises(ConfigValidationError) as exc_info:
        resolve_objective_profile(
            PlanRequest(plan_request_id="req-monitor-timeout", objective_profile_id="containment_first"),
            package,
        )

    assert exc_info.value.failure is not None
    assert exc_info.value.failure.code is FailureCode.ROUTE_MODE_INVALID


def test_build_execution_plans_preserve_monitor_binding_per_sleeve(tmp_path: Path) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    context = build_context(
        config_root,
        PlanRequest(plan_request_id="req-monitor-overlay", objective_profile_id="dexter_with_mewx_overlay"),
    )

    dexter_plan, mewx_plan = build_execution_plans(context, CREATED_AT)

    assert dexter_plan.route.selected_source is Source.DEXTER
    assert dexter_plan.monitor_binding.monitor_profile_id == "dexter_default"
    assert dexter_plan.monitor_binding.admission_gate_class == "lifecycle_control"
    assert dexter_plan.monitor_binding.timeout_envelope_class == "dexter_lifecycle_control"
    assert dexter_plan.monitor_binding.quarantine_scope == "sleeve"
    assert dexter_plan.monitor_binding.global_halt_participation is True

    assert mewx_plan.route.selected_source is Source.MEWX
    assert mewx_plan.monitor_binding.monitor_profile_id == "mewx_timeout_guard"
    assert mewx_plan.monitor_binding.admission_gate_class == "timeout_aware"
    assert mewx_plan.monitor_binding.timeout_envelope_class == "mewx_timeout_tolerant"
    assert mewx_plan.monitor_binding.quarantine_scope == "sleeve"
    assert mewx_plan.monitor_binding.global_halt_participation is True


def test_failure_codes_cover_monitor_killswitch_escalation_surface() -> None:
    codes = {code.value for code in FailureCode}

    assert {
        "global_halt_active",
        "prepare_failed",
        "start_failed",
        "status_timeout",
        "shutdown_unconfirmed",
        "invalid_status_transition",
        "source_stop_failed",
    }.issubset(codes)
