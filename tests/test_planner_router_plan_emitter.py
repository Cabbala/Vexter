import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pytest

from vexter.planner_router.budget_binder import bind_budgets
from vexter.planner_router.config_loader import load_planner_router_package
from vexter.planner_router.errors import PlanEmissionError
from vexter.planner_router.models import PlanRequest, ResolvedPlanningContext, Source, SourcePinRegistry
from vexter.planner_router.objective_resolver import resolve_objective_profile
from vexter.planner_router.plan_emitter import build_execution_plans, emit_plan_batch
from vexter.planner_router.sleeve_selector import select_sleeves


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_ROOT = REPO_ROOT / "config" / "planner_router"
FROZEN_PINS = SourcePinRegistry(
    dexter="ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
    mewx="dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
)


class MemoryPlanStore:
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.batches = []

    def put_batch(self, batch) -> None:
        if self.fail:
            raise RuntimeError("store unavailable")
        self.batches.append(batch)


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


def test_build_execution_plans_for_overlay_batch(tmp_path: Path) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    context = build_context(
        config_root,
        PlanRequest(plan_request_id="req-4", objective_profile_id="dexter_with_mewx_overlay"),
    )

    plans = build_execution_plans(context, datetime(2026, 3, 26, 2, 0, tzinfo=timezone.utc))

    assert len(plans) == 2
    assert plans[0].plan_batch_id == plans[1].plan_batch_id
    assert plans[0].route.selected_source is Source.DEXTER
    assert plans[0].budget_binding.sleeve_share == 80
    assert plans[1].route.selected_source is Source.MEWX
    assert plans[1].monitor_binding.monitor_profile_id == "mewx_timeout_guard"
    assert plans[1].budget_binding.explicit_cap_required is True


def test_emit_plan_batch_is_atomic_at_store_boundary() -> None:
    context = build_context(CONFIG_ROOT, PlanRequest(plan_request_id="req-5"))
    plans = build_execution_plans(context, datetime(2026, 3, 26, 2, 5, tzinfo=timezone.utc))

    with pytest.raises(PlanEmissionError):
        emit_plan_batch(plans, context.request, MemoryPlanStore(fail=True))
