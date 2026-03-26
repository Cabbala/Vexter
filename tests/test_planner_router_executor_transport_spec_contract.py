import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from vexter.planner_router.interfaces import ExecutorAdapter, ExecutorRegistry, PlanStore, StatusSink
from vexter.planner_router.models import PlanRequest, Source, SourcePinRegistry
from vexter.planner_router.planner import plan_request


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_ROOT = REPO_ROOT / "config" / "planner_router"
FROZEN_PINS = SourcePinRegistry(
    dexter="ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938",
    mewx="dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a",
)
CREATED_AT = datetime(2026, 3, 26, 3, 42, tzinfo=timezone.utc)


class MemoryPlanStore:
    def __init__(self) -> None:
        self.batches = []

    def put_batch(self, batch) -> None:
        self.batches.append(batch)


def _protocol_methods(protocol) -> set[str]:
    return {
        name
        for name, value in protocol.__dict__.items()
        if callable(value) and not name.startswith("_")
    }


def clone_config_dir(tmp_path: Path) -> Path:
    destination = tmp_path / "planner_router"
    shutil.copytree(CONFIG_ROOT, destination)
    return destination


def enable_mewx_sleeve(config_root: Path) -> None:
    sleeves_path = config_root / "sleeves.json"
    payload = json.loads(sleeves_path.read_text())
    payload[1]["enabled"] = True
    sleeves_path.write_text(json.dumps(payload, indent=2) + "\n")


def test_transport_protocol_surface_remains_bounded() -> None:
    assert _protocol_methods(PlanStore) == {"put_batch"}
    assert _protocol_methods(ExecutorAdapter) == {"prepare", "start", "status", "stop", "snapshot"}
    assert _protocol_methods(ExecutorRegistry) == {"adapter_for"}
    assert _protocol_methods(StatusSink) == {"record"}


def test_transport_contract_preserves_source_faithful_entrypoints_and_plan_identity(tmp_path: Path) -> None:
    config_root = clone_config_dir(tmp_path)
    enable_mewx_sleeve(config_root)
    store = MemoryPlanStore()

    batch = plan_request(
        PlanRequest(plan_request_id="req-transport-contract", objective_profile_id="dexter_with_mewx_overlay"),
        config_root,
        FROZEN_PINS,
        store,
        created_at_utc=CREATED_AT,
    )

    dexter_plan, mewx_plan = batch.plans

    assert len(store.batches) == 1
    assert dexter_plan.plan_batch_id == mewx_plan.plan_batch_id
    assert dexter_plan.plan_id != mewx_plan.plan_id
    assert dexter_plan.route.selected_source is Source.DEXTER
    assert mewx_plan.route.selected_source is Source.MEWX
    assert "monitor_mint_session" in dexter_plan.executor_binding.methods
    assert "start_session" in mewx_plan.executor_binding.methods
    assert "sim_session" in mewx_plan.executor_binding.methods
    assert "trade_session" in mewx_plan.executor_binding.methods
    assert tuple(status.value for status in dexter_plan.executor_binding.normalized_statuses) == (
        "planned",
        "starting",
        "running",
        "quarantined",
        "stopping",
        "stopped",
        "failed",
    )
    assert tuple(status.value for status in mewx_plan.executor_binding.normalized_statuses) == (
        "planned",
        "starting",
        "running",
        "quarantined",
        "stopping",
        "stopped",
        "failed",
    )
    assert dexter_plan.executor_binding.pinned_commit == FROZEN_PINS.dexter
    assert mewx_plan.executor_binding.pinned_commit == FROZEN_PINS.mewx


def test_transport_spec_proof_freezes_handle_based_poll_first_contract() -> None:
    proof = json.loads(
        (REPO_ROOT / "artifacts" / "proofs" / "task-007-planner-router-executor-transport-spec-check.json").read_text()
    )

    assert proof["task_id"] == "TASK-007-PLANNER-ROUTER-EXECUTOR-TRANSPORT-SPEC"
    assert proof["transport_contract"]["ownership"]["plan_store"] == "planner_owned_pre_runtime_batch_persistence"
    assert proof["transport_contract"]["process_boundary"]["planner_router"] == "single_in_process_control_plane"
    assert proof["transport_contract"]["process_boundary"]["cross_source_handoff_forbidden"] is True
    assert proof["transport_contract"]["source_faithful_entrypoints"]["dexter"]["entrypoint"] == "monitor_mint_session"
    assert proof["transport_contract"]["source_faithful_entrypoints"]["mewx"]["safe_entrypoint"] == "sim_session"
    assert proof["transport_contract"]["source_faithful_entrypoints"]["mewx"]["funded_entrypoint_deferred"] == "trade_session"
    assert proof["transport_contract"]["envelope"]["prepare_is_only_full_plan_command"] is True
    assert proof["transport_contract"]["status_model"]["polling_is_authoritative_first_cut"] is True
    assert proof["transport_contract"]["status_model"]["push_optional"] is True
    assert proof["task_result"]["recommended_next_step"] == "planner_router_executor_transport_implementation"
