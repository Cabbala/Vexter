"""Bounded executor transport implementations and helpers."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from .errors import PlannerRouterError
from .interfaces import ExecutorAdapter, ExecutorRegistry, PlanStore, StatusSink
from .models import (
    DispatchHandle,
    ExecutionPlan,
    FailureCode,
    FailureDetail,
    PlanBatch,
    PlanStatus,
    Source,
    SourcePinRegistry,
    StatusSnapshot,
    ensure_utc,
    freeze_detail,
)

TRANSPORT_VERSION = "v1"
STATUS_DELIVERY_POLL = "poll_first"

_TRANSPORT_RANK = {
    PlanStatus.PLANNED: 0,
    PlanStatus.STARTING: 1,
    PlanStatus.RUNNING: 2,
    PlanStatus.QUARANTINED: 3,
    PlanStatus.STOPPING: 4,
    PlanStatus.STOPPED: 5,
    PlanStatus.FAILED: 5,
}
_TERMINAL_STATUSES = frozenset({PlanStatus.STOPPED, PlanStatus.FAILED})
_VALID_STATUS_TRANSITIONS = frozenset(
    {
        (PlanStatus.PLANNED, PlanStatus.STARTING),
        (PlanStatus.PLANNED, PlanStatus.STOPPING),
        (PlanStatus.PLANNED, PlanStatus.FAILED),
        (PlanStatus.STARTING, PlanStatus.RUNNING),
        (PlanStatus.STARTING, PlanStatus.STOPPING),
        (PlanStatus.STARTING, PlanStatus.FAILED),
        (PlanStatus.RUNNING, PlanStatus.QUARANTINED),
        (PlanStatus.RUNNING, PlanStatus.STOPPING),
        (PlanStatus.RUNNING, PlanStatus.STOPPED),
        (PlanStatus.RUNNING, PlanStatus.FAILED),
        (PlanStatus.QUARANTINED, PlanStatus.STOPPING),
        (PlanStatus.QUARANTINED, PlanStatus.FAILED),
        (PlanStatus.STOPPING, PlanStatus.STOPPED),
        (PlanStatus.STOPPING, PlanStatus.FAILED),
    }
)


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _message_id() -> str:
    return uuid4().hex


def _freeze_payload(payload: Mapping[str, Any] | None = None) -> Mapping[str, Any]:
    return freeze_detail(payload)


class TransportMessageType(str, Enum):
    PREPARE = "prepare"
    START = "start"
    STATUS = "status"
    STOP = "stop"
    SNAPSHOT = "snapshot"


class TransportAckState(str, Enum):
    ACCEPTED = "accepted"
    DUPLICATE = "duplicate"
    REJECTED = "rejected"
    TERMINAL = "terminal"


class TransportRejectionClass(str, Enum):
    PIN_MISMATCH = "pin_mismatch"
    UNSUPPORTED_TRANSPORT_VERSION = "unsupported_transport_version"
    UNKNOWN_HANDLE = "unknown_handle"
    INVALID_PLAN_STATE = "invalid_plan_state"
    SOURCE_MISMATCH = "source_mismatch"
    EXECUTOR_PROFILE_MISMATCH = "executor_profile_mismatch"
    TRANSPORT_UNAVAILABLE = "transport_unavailable"
    NATIVE_PREPARE_REJECTED = "native_prepare_rejected"
    NATIVE_START_REJECTED = "native_start_rejected"
    NATIVE_STOP_REJECTED = "native_stop_rejected"


@dataclass(frozen=True, slots=True)
class TransportEnvelope:
    transport_version: str
    message_type: TransportMessageType
    message_id: str
    sent_at_utc: datetime
    plan_id: str
    plan_batch_id: str
    source: Source
    executor_profile_id: str
    idempotency_key: str
    payload: Mapping[str, Any] = field(default_factory=freeze_detail)


@dataclass(frozen=True, slots=True)
class QueuedPushSnapshot:
    status: PlanStatus
    source_reason: str | None
    detail: Mapping[str, Any] = field(default_factory=freeze_detail)


@dataclass(frozen=True, slots=True)
class SourceTransportSpec:
    source: Source
    execution_mode: str
    entrypoint: str
    startup_method: str | None

    @classmethod
    def for_plan(cls, plan: ExecutionPlan) -> "SourceTransportSpec":
        if plan.route.selected_source is Source.DEXTER:
            return cls(
                source=Source.DEXTER,
                execution_mode="paper_live",
                entrypoint="monitor_mint_session",
                startup_method=None,
            )
        return cls(
            source=Source.MEWX,
            execution_mode="sim_live",
            entrypoint="sim_session",
            startup_method="start_session",
        )


@dataclass(frozen=True, slots=True)
class TransportFailureMode:
    prepare_rejection: TransportRejectionClass | None = None
    start_rejection: TransportRejectionClass | None = None
    stop_rejection: TransportRejectionClass | None = None
    status_timeout: bool = False
    stop_requires_snapshot_confirmation: bool = True
    stop_confirmation_suppressed: bool = False


@dataclass(slots=True)
class _TransportSession:
    plan: ExecutionPlan
    spec: SourceTransportSpec
    handle_id: str
    native_session_id: str
    prepared_at_utc: datetime
    status_delivery: str = STATUS_DELIVERY_POLL
    prepare_request_count: int = 1
    start_request_count: int = 0
    stop_request_count: int = 0
    last_sequence: int = 0
    poll_counter: int = 0
    snapshot_counter: int = 0
    started: bool = False
    stop_requested: bool = False
    stop_confirmed: bool = False
    stop_status_polled: bool = False
    last_stop_reason: str | None = None
    executor_status: PlanStatus = PlanStatus.PLANNED
    last_reported_status: PlanStatus = PlanStatus.PLANNED
    last_prepare_ack_state: TransportAckState = TransportAckState.ACCEPTED
    last_start_ack_state: TransportAckState = TransportAckState.ACCEPTED
    last_stop_ack_state: TransportAckState | None = None
    prepare_accepted_once: bool = True
    prepare_duplicate_seen: bool = False
    start_accepted_once: bool = False
    start_duplicate_seen: bool = False
    start_terminal_seen: bool = False
    stop_accepted_once: bool = False
    stop_duplicate_seen: bool = False
    stop_terminal_seen: bool = False
    queued_push: QueuedPushSnapshot | None = None


class TransportCommandError(PlannerRouterError):
    """Transport-layer error that keeps ack and rejection detail attached."""

    def __init__(
        self,
        message: str,
        *,
        stage: str,
        failure_code: FailureCode,
        ack_state: TransportAckState,
        plan: ExecutionPlan | None = None,
        rejection_class: TransportRejectionClass | None = None,
        source_reason: str | None = None,
        detail: Mapping[str, Any] | None = None,
    ) -> None:
        self.stage = stage
        self.failure_code = failure_code
        self.ack_state = ack_state
        self.rejection_class = rejection_class
        self.source_reason = source_reason
        self.detail = _freeze_payload(detail)
        super().__init__(
            message,
            failure=FailureDetail(
                code=failure_code,
                stage=stage,
                plan_id=plan.plan_id if plan else None,
                source=plan.route.selected_source if plan else None,
                source_reason=source_reason,
                detail=self.detail,
            ),
        )


def prepare_idempotency_key(plan_id: str) -> str:
    return f"{plan_id}:prepare:{TRANSPORT_VERSION}"


def start_idempotency_key(plan_id: str) -> str:
    return f"{plan_id}:start:{TRANSPORT_VERSION}"


def stop_idempotency_key(plan_id: str, reason: str) -> str:
    return f"{plan_id}:stop:{normalize_stop_reason(reason)}:{TRANSPORT_VERSION}"


def status_idempotency_key(plan_id: str, poll_counter: int) -> str:
    return f"{plan_id}:status:{poll_counter}"


def snapshot_idempotency_key(plan_id: str, request_counter: int) -> str:
    return f"{plan_id}:snapshot:{request_counter}"


def normalize_stop_reason(reason: str) -> str:
    return "_".join(reason.strip().lower().split()) or "unspecified_stop"


def build_transport_envelope(
    message_type: TransportMessageType,
    *,
    plan: ExecutionPlan,
    idempotency_key: str,
    payload: Mapping[str, Any] | None = None,
    sent_at_utc: datetime | None = None,
) -> TransportEnvelope:
    return TransportEnvelope(
        transport_version=TRANSPORT_VERSION,
        message_type=message_type,
        message_id=_message_id(),
        sent_at_utc=ensure_utc(sent_at_utc or _now_utc()),
        plan_id=plan.plan_id,
        plan_batch_id=plan.plan_batch_id,
        source=plan.route.selected_source,
        executor_profile_id=plan.executor_binding.executor_profile_id,
        idempotency_key=idempotency_key,
        payload=_freeze_payload(payload),
    )


def serialize_execution_plan(plan: ExecutionPlan) -> Mapping[str, Any]:
    return freeze_detail(
        {
            "plan_id": plan.plan_id,
            "plan_batch_id": plan.plan_batch_id,
            "objective_profile_id": plan.objective_profile_id,
            "created_at_utc": ensure_utc(plan.created_at_utc).isoformat(),
            "source": plan.route.selected_source.value,
            "route_mode": plan.route.mode.value,
            "selected_sleeve_id": plan.route.selected_sleeve_id,
            "monitor_profile_id": plan.monitor_binding.monitor_profile_id,
            "timeout_envelope_class": plan.monitor_binding.timeout_envelope_class,
            "quarantine_scope": plan.monitor_binding.quarantine_scope,
            "global_halt_participation": plan.monitor_binding.global_halt_participation,
            "executor_profile_id": plan.executor_binding.executor_profile_id,
            "pinned_commit": plan.executor_binding.pinned_commit,
            "methods": list(plan.executor_binding.methods),
            "normalized_statuses": [status.value for status in plan.executor_binding.normalized_statuses],
            "invariants": list(plan.invariants),
        }
    )


def is_valid_status_transition(previous: PlanStatus, next_status: PlanStatus) -> bool:
    return previous == next_status or (previous, next_status) in _VALID_STATUS_TRANSITIONS


def reconcile_status_snapshot(
    previous_status: PlanStatus,
    polled_snapshot: StatusSnapshot,
    pushed_snapshot: StatusSnapshot | None = None,
) -> StatusSnapshot:
    if pushed_snapshot is None:
        return StatusSnapshot(
            plan_id=polled_snapshot.plan_id,
            status=polled_snapshot.status,
            source_reason=polled_snapshot.source_reason,
            observed_at_utc=polled_snapshot.observed_at_utc,
            detail=_freeze_payload(
                {
                    **dict(polled_snapshot.detail),
                    "reconciliation_mode": STATUS_DELIVERY_POLL,
                    "reconciliation_decision": "poll_only",
                }
            ),
        )

    polled_valid = is_valid_status_transition(previous_status, polled_snapshot.status)
    pushed_valid = is_valid_status_transition(previous_status, pushed_snapshot.status)
    if pushed_snapshot.status == polled_snapshot.status:
        merged_detail = {
            **dict(polled_snapshot.detail),
            "reconciliation_mode": STATUS_DELIVERY_POLL,
            "reconciliation_decision": "poll_confirmed_by_push",
            "poll_status": polled_snapshot.status.value,
            "poll_detail": dict(polled_snapshot.detail),
            "push_status": pushed_snapshot.status.value,
            "poll_valid": polled_valid,
            "push_valid": pushed_valid,
            "push_source_reason": pushed_snapshot.source_reason,
            "push_detail": dict(pushed_snapshot.detail),
        }
        for key, value in dict(pushed_snapshot.detail).items():
            if key not in merged_detail:
                merged_detail[key] = value
        if "signal" not in merged_detail:
            merged_detail["signal"] = "status_poll"
        return StatusSnapshot(
            plan_id=polled_snapshot.plan_id,
            status=polled_snapshot.status,
            source_reason=pushed_snapshot.source_reason or polled_snapshot.source_reason,
            observed_at_utc=polled_snapshot.observed_at_utc,
            detail=_freeze_payload(merged_detail),
        )

    chosen = polled_snapshot
    decision = "poll_retained"

    if pushed_valid and (
        not polled_valid or _TRANSPORT_RANK[pushed_snapshot.status] > _TRANSPORT_RANK[polled_snapshot.status]
    ):
        chosen = pushed_snapshot
        decision = "push_promoted"

    merged_detail = {
        **dict(chosen.detail),
        "reconciliation_mode": STATUS_DELIVERY_POLL,
        "reconciliation_decision": decision,
        "poll_status": polled_snapshot.status.value,
        "poll_detail": dict(polled_snapshot.detail),
        "push_status": pushed_snapshot.status.value,
        "poll_valid": polled_valid,
        "push_valid": pushed_valid,
        "push_source_reason": pushed_snapshot.source_reason,
        "push_detail": dict(pushed_snapshot.detail),
    }
    if "signal" not in merged_detail:
        merged_detail["signal"] = "status_poll"

    return StatusSnapshot(
        plan_id=chosen.plan_id,
        status=chosen.status,
        source_reason=chosen.source_reason,
        observed_at_utc=chosen.observed_at_utc,
        detail=_freeze_payload(merged_detail),
    )


@dataclass(frozen=True, slots=True)
class LivepaperObservabilityWatchdogFinding:
    surface: str
    severity: str
    message: str
    plan_id: str | None = None
    detail: Mapping[str, Any] = field(default_factory=freeze_detail)


@dataclass(frozen=True, slots=True)
class LivepaperObservabilityWatchdogReport:
    checked_plan_ids: tuple[str, ...]
    findings: tuple[LivepaperObservabilityWatchdogFinding, ...]

    @property
    def passed(self) -> bool:
        return not self.findings

    @property
    def surface_status(self) -> Mapping[str, bool]:
        surfaced = {finding.surface for finding in self.findings}
        return freeze_detail(
            {surface: surface not in surfaced for surface in _LIVEPAPER_WATCHDOG_SURFACES}
        )


_LIVEPAPER_WATCHDOG_SURFACES = (
    "required_observability_field_omission",
    "handle_lifecycle_continuity",
    "planned_runtime_metadata_drift",
    "partial_status_sink_fan_in",
    "ack_history_retention",
    "quarantine_reason_completeness",
    "manual_stop_all_propagation",
    "snapshot_backed_terminal_detail",
    "normalized_failure_detail_passthrough",
)
_WATCHDOG_ACK_DUPLICATE_FLAGS = {
    "prepare_request_count": ("prepare_duplicate_seen",),
    "start_request_count": ("start_duplicate_seen", "start_terminal_seen"),
    "stop_request_count": ("stop_duplicate_seen", "stop_terminal_seen"),
}
_WATCHDOG_FAILED_SNAPSHOT_REQUIRED_KEYS = (
    "failure_code",
    "stage",
    "rollback_confirmed",
    "rollback_confirmation_source",
    "rollback_snapshot",
)
_WATCHDOG_LIFECYCLE_KEYS = (
    "handle_id",
    "native_session_id",
)
_WATCHDOG_ROLLBACK_REQUIRED_KEYS = (
    "execution_mode",
    "monitor_profile_id",
    "executor_profile_id",
    "pinned_commit",
    "stop_reason",
)


_WATCHDOG_HANDLE_REQUIRED_KEYS = (
    "transport_version",
    "handle_id",
    "ack_state",
    "entrypoint",
    "executor_profile_id",
    "pinned_commit",
    "status_delivery",
    "prepared_at_utc",
    "native_session_id",
    "execution_mode",
    "startup_method",
    "plan_batch_id",
    "objective_profile_id",
    "source",
    "selected_sleeve_id",
    "monitor_profile_id",
    "timeout_envelope_class",
    "quarantine_scope",
    "global_halt_participation",
    "prepare_ack_state",
    "prepare_accepted_once",
    "prepare_duplicate_seen",
    "prepare_request_count",
    "start_ack_state",
    "start_accepted_once",
    "start_duplicate_seen",
    "start_terminal_seen",
    "start_request_count",
    "stop_ack_state",
    "stop_accepted_once",
    "stop_duplicate_seen",
    "stop_terminal_seen",
    "stop_request_count",
    "last_reported_status",
)

_WATCHDOG_RUNTIME_REQUIRED_KEYS = (
    "handle_id",
    "native_session_id",
    "transport_version",
    "signal",
    "prepared_at_utc",
    "entrypoint",
    "execution_mode",
    "startup_method",
    "status_delivery",
    "ack_state",
    "plan_batch_id",
    "objective_profile_id",
    "source",
    "selected_sleeve_id",
    "monitor_profile_id",
    "timeout_envelope_class",
    "quarantine_scope",
    "global_halt_participation",
    "executor_profile_id",
    "pinned_commit",
    "prepare_ack_state",
    "prepare_accepted_once",
    "prepare_duplicate_seen",
    "prepare_request_count",
    "start_ack_state",
    "start_accepted_once",
    "start_duplicate_seen",
    "start_terminal_seen",
    "start_request_count",
    "stop_ack_state",
    "stop_accepted_once",
    "stop_duplicate_seen",
    "stop_terminal_seen",
    "stop_request_count",
    "last_reported_status",
)

_WATCHDOG_FAILURE_REQUIRED_KEYS = (
    "code",
    "stage",
    "plan_id",
    "source",
    "source_reason",
    "detail",
)

_WATCHDOG_FAILURE_DETAIL_REQUIRED_KEYS = (
    "plan_id",
    "plan_batch_id",
    "objective_profile_id",
    "source",
    "selected_sleeve_id",
    "monitor_profile_id",
    "timeout_envelope_class",
    "quarantine_scope",
    "global_halt_participation",
    "executor_profile_id",
    "pinned_commit",
    "entrypoint",
    "execution_mode",
    "startup_method",
    "handle_id",
    "transport_version",
)
_WATCHDOG_ACK_RETENTION_KEYS = (
    "prepare_ack_state",
    "prepare_accepted_once",
    "prepare_duplicate_seen",
    "prepare_request_count",
    "start_ack_state",
    "start_accepted_once",
    "start_duplicate_seen",
    "start_terminal_seen",
    "start_request_count",
    "stop_ack_state",
    "stop_accepted_once",
    "stop_duplicate_seen",
    "stop_terminal_seen",
    "stop_request_count",
)
_WATCHDOG_ACK_COUNT_KEYS = (
    "prepare_request_count",
    "start_request_count",
    "stop_request_count",
)
_WATCHDOG_ACK_STICKY_KEYS = (
    "prepare_accepted_once",
    "prepare_duplicate_seen",
    "start_accepted_once",
    "start_duplicate_seen",
    "start_terminal_seen",
    "stop_accepted_once",
    "stop_duplicate_seen",
    "stop_terminal_seen",
)


def _watchdog_issue(
    surface: str,
    severity: str,
    message: str,
    *,
    plan_id: str | None = None,
    detail: Mapping[str, Any] | None = None,
) -> LivepaperObservabilityWatchdogFinding:
    return LivepaperObservabilityWatchdogFinding(
        surface=surface,
        severity=severity,
        message=message,
        plan_id=plan_id,
        detail=_freeze_payload(detail),
    )


def _missing_required_keys(observed: Mapping[str, Any], required_keys: Sequence[str]) -> tuple[str, ...]:
    return tuple(key for key in required_keys if key not in observed)


def _mismatched_required_keys(
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
    required_keys: Sequence[str],
) -> dict[str, dict[str, Any]]:
    mismatched: dict[str, dict[str, Any]] = {}
    for key in required_keys:
        if key in expected and key in observed and observed[key] != expected[key]:
            mismatched[key] = {"expected": expected[key], "observed": observed[key]}
    return mismatched


def _snapshot_detail_matches(
    plan: ExecutionPlan,
    snapshot: StatusSnapshot,
    *,
    required_runtime_detail_keys: Sequence[str] = _WATCHDOG_RUNTIME_REQUIRED_KEYS,
) -> tuple[tuple[str, ...], dict[str, dict[str, Any]]]:
    spec = SourceTransportSpec.for_plan(plan)
    expected = {
        **dict(serialize_execution_plan(plan)),
        "transport_version": TRANSPORT_VERSION,
        "entrypoint": spec.entrypoint,
        "execution_mode": spec.execution_mode,
        "startup_method": spec.startup_method,
        "status_delivery": STATUS_DELIVERY_POLL,
    }
    observed = dict(snapshot.detail)
    missing = _missing_required_keys(observed, required_runtime_detail_keys)
    mismatched = _mismatched_required_keys(expected, observed, required_runtime_detail_keys)
    return missing, mismatched


def _ack_detail_sequence(
    handle: DispatchHandle | None,
    runtime_snapshots: Sequence[StatusSnapshot],
    terminal_snapshot: Mapping[str, Any] | None,
) -> list[Mapping[str, Any]]:
    details: list[Mapping[str, Any]] = []
    if handle is not None and isinstance(handle.native_handle, Mapping):
        details.append(dict(handle.native_handle))
    details.extend(dict(snapshot.detail) for snapshot in runtime_snapshots)
    if terminal_snapshot is not None:
        details.append(dict(terminal_snapshot))
    return details


def _failed_snapshot_detail_missing(detail: Mapping[str, Any]) -> tuple[str, ...]:
    missing = list(_missing_required_keys(detail, _WATCHDOG_FAILED_SNAPSHOT_REQUIRED_KEYS))
    rollback_snapshot = detail.get("rollback_snapshot")
    if not isinstance(rollback_snapshot, Mapping):
        missing.append("rollback_snapshot")
    return tuple(dict.fromkeys(missing))


def evaluate_livepaper_observability_watchdog(
    plans: Sequence[ExecutionPlan],
    handles_by_plan_id: Mapping[str, DispatchHandle],
    *,
    runtime_snapshots: Sequence[StatusSnapshot] = (),
    sink_snapshots: Sequence[StatusSnapshot] = (),
    terminal_snapshots: Mapping[str, Mapping[str, Any]] | None = None,
    failure_details_by_plan_id: Mapping[str, Mapping[str, Any]] | None = None,
) -> LivepaperObservabilityWatchdogReport:
    findings: list[LivepaperObservabilityWatchdogFinding] = []
    terminal_snapshots = terminal_snapshots or {}
    failure_details_by_plan_id = failure_details_by_plan_id or {}
    runtime_by_plan_id: dict[str, list[StatusSnapshot]] = {}
    sink_by_plan_id: dict[str, list[StatusSnapshot]] = {}
    manual_stop_visible_plan_ids: set[str] = set()

    for snapshot in runtime_snapshots:
        runtime_by_plan_id.setdefault(snapshot.plan_id, []).append(snapshot)
    for snapshot in sink_snapshots:
        sink_by_plan_id.setdefault(snapshot.plan_id, []).append(snapshot)

    for plan in plans:
        plan_id = plan.plan_id
        handle = handles_by_plan_id.get(plan_id)
        observed_handle: dict[str, Any] = {}
        failure_detail = failure_details_by_plan_id.get(plan_id)
        expected_handle = {
            **dict(serialize_execution_plan(plan)),
            "transport_version": TRANSPORT_VERSION,
            "handle_id": f"{plan.executor_binding.executor_profile_id}:{plan.plan_id}",
            "ack_state": None,
            "entrypoint": "monitor_mint_session" if plan.route.selected_source is Source.DEXTER else "sim_session",
            "startup_method": None if plan.route.selected_source is Source.DEXTER else "start_session",
            "status_delivery": STATUS_DELIVERY_POLL,
            "native_session_id": (
                f"paper_live:{plan.plan_id}" if plan.route.selected_source is Source.DEXTER else f"sim_live:{plan.plan_id}"
            ),
        }

        if handle is None:
            findings.append(
                _watchdog_issue(
                    "required_observability_field_omission",
                    "omission",
                    "handle missing for planned transport surface",
                    plan_id=plan_id,
                    detail={"missing_field": "handle", "source": plan.route.selected_source.value},
                )
            )
            continue

        if not isinstance(handle.native_handle, Mapping):
            findings.append(
                _watchdog_issue(
                    "required_observability_field_omission",
                    "omission",
                    "native handle is not mapping-like",
                    plan_id=plan_id,
                    detail={"observed_type": type(handle.native_handle).__name__},
                )
            )
        else:
            observed_handle = dict(handle.native_handle)
            missing = _missing_required_keys(observed_handle, _WATCHDOG_HANDLE_REQUIRED_KEYS)
            mismatched = _mismatched_required_keys(
                expected_handle,
                observed_handle,
                (
                    "transport_version",
                    "handle_id",
                    "entrypoint",
                    "executor_profile_id",
                    "pinned_commit",
                    "status_delivery",
                    "prepared_at_utc",
                    "native_session_id",
                    "execution_mode",
                    "startup_method",
                    "plan_batch_id",
                    "objective_profile_id",
                    "source",
                    "selected_sleeve_id",
                    "monitor_profile_id",
                    "timeout_envelope_class",
                    "quarantine_scope",
                    "global_halt_participation",
                ),
            )
            if missing:
                findings.append(
                    _watchdog_issue(
                        "required_observability_field_omission",
                        "omission",
                        "handle metadata omitted required observability fields",
                        plan_id=plan_id,
                        detail={"missing_fields": missing},
                    )
                )
            if mismatched:
                findings.append(
                    _watchdog_issue(
                        "planned_runtime_metadata_drift",
                        "drift",
                        "handle metadata drifted from the planned source-faithful envelope",
                        plan_id=plan_id,
                        detail=mismatched,
                )
            )

        runtime = runtime_by_plan_id.get(plan_id, [])
        sink_runtime = sink_by_plan_id.get(plan_id, [])
        terminal_snapshot = terminal_snapshots.get(plan_id)
        if not runtime:
            findings.append(
                _watchdog_issue(
                    "partial_status_sink_fan_in",
                    "partial_visibility",
                    "no runtime status snapshots were observed for the plan",
                    plan_id=plan_id,
                    detail={"observed_runtime_snapshots": 0},
                )
            )

        lifecycle_values: dict[str, set[str]] = {key: set() for key in _WATCHDOG_LIFECYCLE_KEYS}
        lifecycle_sources: dict[str, list[str]] = {key: [] for key in _WATCHDOG_LIFECYCLE_KEYS}

        def record_lifecycle(detail: Mapping[str, Any], label: str) -> None:
            for key in _WATCHDOG_LIFECYCLE_KEYS:
                value = detail.get(key)
                if value is None:
                    continue
                lifecycle_values[key].add(str(value))
                lifecycle_sources[key].append(label)

        if observed_handle:
            record_lifecycle(observed_handle, "handle")
        for index, snapshot in enumerate(runtime):
            record_lifecycle(dict(snapshot.detail), f"runtime[{index}]")
        for index, snapshot in enumerate(sink_runtime):
            record_lifecycle(dict(snapshot.detail), f"sink[{index}]")
        if isinstance(terminal_snapshot, Mapping):
            record_lifecycle(dict(terminal_snapshot), "terminal_snapshot")
        if isinstance(failure_detail, Mapping):
            nested_detail = failure_detail.get("detail", {})
            if isinstance(nested_detail, Mapping):
                record_lifecycle(dict(nested_detail), "failure_detail")
                rollback_snapshot = nested_detail.get("rollback_snapshot", {})
                if isinstance(rollback_snapshot, Mapping):
                    record_lifecycle(dict(rollback_snapshot), "rollback_snapshot")

        for key, values in lifecycle_values.items():
            if len(values) <= 1:
                continue
            findings.append(
                _watchdog_issue(
                    "handle_lifecycle_continuity",
                    "drift",
                    "handle lifecycle identifiers drifted across runtime-visible surfaces",
                    plan_id=plan_id,
                    detail={
                        "field": key,
                        "observed_values": tuple(sorted(values)),
                        "detail_sources": tuple(lifecycle_sources[key]),
                    },
                )
            )

        for snapshot in runtime:
            missing, mismatched = _snapshot_detail_matches(plan, snapshot)
            if missing:
                findings.append(
                    _watchdog_issue(
                        "required_observability_field_omission",
                        "omission",
                        "runtime snapshot omitted required observability fields",
                        plan_id=plan_id,
                        detail={"missing_fields": missing, "status": snapshot.status.value},
                    )
                )
            if mismatched:
                findings.append(
                    _watchdog_issue(
                        "planned_runtime_metadata_drift",
                        "drift",
                        "runtime snapshot drifted from the planned metadata envelope",
                        plan_id=plan_id,
                        detail=mismatched,
                    )
                )

            detail = dict(snapshot.detail)
            if snapshot.status in {PlanStatus.RUNNING, PlanStatus.QUARANTINED, PlanStatus.STOPPING, PlanStatus.STOPPED, PlanStatus.FAILED}:
                lifecycle_missing = _missing_required_keys(
                    detail,
                    (
                        "sequence",
                        "poll_counter",
                        "snapshot_counter",
                        "executor_status",
                        "started",
                        "stop_requested",
                        "stop_confirmed",
                        "duplicate",
                    ),
                )
                if lifecycle_missing:
                    findings.append(
                        _watchdog_issue(
                            "required_observability_field_omission",
                            "omission",
                            "runtime snapshot omitted lifecycle visibility fields",
                            plan_id=plan_id,
                            detail={"missing_fields": lifecycle_missing, "status": snapshot.status.value},
                        )
                    )

            push_detail = detail.get("push_detail")
            push_quarantine_reason = (
                push_detail.get("quarantine_reason") if isinstance(push_detail, Mapping) else None
            )
            if snapshot.status is PlanStatus.QUARANTINED and not (
                detail.get("quarantine_reason") or push_quarantine_reason
            ):
                findings.append(
                    _watchdog_issue(
                        "quarantine_reason_completeness",
                        "omission",
                        "quarantine snapshot did not retain a visible quarantine reason",
                        plan_id=plan_id,
                        detail=detail,
                    )
                )

            if snapshot.detail.get("signal") == "halt_latched":
                manual_stop_visible_plan_ids.add(plan_id)
                if not detail.get("stop_reason"):
                    findings.append(
                        _watchdog_issue(
                            "manual_stop_all_propagation",
                            "omission",
                            "manual stop-all propagation lost the stop reason",
                            plan_id=plan_id,
                            detail=detail,
                        )
                    )
                if detail.get("halt_mode") != "manual_latched_stop_all":
                    findings.append(
                        _watchdog_issue(
                            "manual_stop_all_propagation",
                            "drift",
                            "manual stop-all propagation drifted from the normalized halt mode",
                            plan_id=plan_id,
                            detail={"halt_mode": detail.get("halt_mode")},
                        )
                    )
                if not detail.get("trigger_plan_id"):
                    findings.append(
                        _watchdog_issue(
                            "manual_stop_all_propagation",
                            "partial_visibility",
                            "manual stop-all propagation did not surface the trigger plan id",
                            plan_id=plan_id,
                            detail=detail,
                        )
                    )

            if snapshot.status is PlanStatus.FAILED:
                missing_failure_detail = _failed_snapshot_detail_missing(detail)
                if missing_failure_detail:
                    findings.append(
                        _watchdog_issue(
                            "normalized_failure_detail_passthrough",
                            "omission",
                            "failed runtime snapshot did not retain normalized failure passthrough detail",
                            plan_id=plan_id,
                            detail={"missing_fields": missing_failure_detail},
                        )
                    )
                if not detail.get("stop_confirmed") or not detail.get("stop_requested"):
                    findings.append(
                        _watchdog_issue(
                            "manual_stop_all_propagation",
                            "partial_visibility",
                            "manual stop-all propagation did not surface the stop lifecycle flags",
                            plan_id=plan_id,
                            detail=detail,
                        )
                    )

        terminal_snapshot = terminal_snapshots.get(plan_id)
        if terminal_snapshot is not None:
            terminal_snapshot = dict(terminal_snapshot)
            missing = _missing_required_keys(terminal_snapshot, _WATCHDOG_RUNTIME_REQUIRED_KEYS)
            if missing:
                findings.append(
                    _watchdog_issue(
                        "snapshot_backed_terminal_detail",
                        "omission",
                        "terminal snapshot omitted required observability fields",
                        plan_id=plan_id,
                        detail={"missing_fields": missing},
                    )
                )
            if terminal_snapshot.get("signal") != "snapshot":
                findings.append(
                    _watchdog_issue(
                        "snapshot_backed_terminal_detail",
                        "partial_visibility",
                        "terminal detail was not backed by a snapshot signal",
                        plan_id=plan_id,
                        detail=terminal_snapshot,
                    )
                )
            if not terminal_snapshot.get("stop_reason"):
                findings.append(
                    _watchdog_issue(
                        "snapshot_backed_terminal_detail",
                        "omission",
                        "terminal snapshot did not retain the stop reason",
                        plan_id=plan_id,
                        detail=terminal_snapshot,
                    )
                )
        elif runtime:
            findings.append(
                _watchdog_issue(
                    "snapshot_backed_terminal_detail",
                    "partial_visibility",
                    "terminal snapshot was not provided for a plan with runtime observations",
                    plan_id=plan_id,
                    detail={"runtime_snapshot_count": len(runtime)},
                )
            )

        failure_detail = failure_details_by_plan_id.get(plan_id)
        if failure_detail is not None:
            observed_failure = dict(failure_detail)
            missing = _missing_required_keys(observed_failure, _WATCHDOG_FAILURE_REQUIRED_KEYS)
            nested_detail = dict(observed_failure.get("detail", {})) if isinstance(observed_failure.get("detail"), Mapping) else {}
            nested_missing = _missing_required_keys(nested_detail, _WATCHDOG_FAILURE_DETAIL_REQUIRED_KEYS)
            if missing or nested_missing:
                findings.append(
                    _watchdog_issue(
                        "normalized_failure_detail_passthrough",
                        "omission",
                        "normalized failure detail did not retain the expected passthrough metadata",
                        plan_id=plan_id,
                        detail={
                            "missing_fields": missing,
                            "nested_missing_fields": nested_missing,
                        },
                    )
                )
            if nested_detail.get("rollback_confirmed"):
                rollback_snapshot = nested_detail.get("rollback_snapshot", {})
                if not isinstance(rollback_snapshot, Mapping):
                    findings.append(
                        _watchdog_issue(
                            "normalized_failure_detail_passthrough",
                            "partial_visibility",
                            "rollback-confirmed failure detail did not surface a rollback snapshot",
                            plan_id=plan_id,
                            detail=nested_detail,
                        )
                    )
                else:
                    rollback_missing = _missing_required_keys(dict(rollback_snapshot), _WATCHDOG_ROLLBACK_REQUIRED_KEYS)
                    if rollback_missing:
                        findings.append(
                            _watchdog_issue(
                                "normalized_failure_detail_passthrough",
                                "omission",
                                "rollback snapshot omitted required source-faithful passthrough fields",
                                plan_id=plan_id,
                                detail={"missing_fields": rollback_missing},
                            )
                        )

        visible_details = _ack_detail_sequence(handle, runtime, terminal_snapshot)
        if failure_detail is not None and isinstance(failure_detail.get("detail"), Mapping):
            visible_details.append(dict(failure_detail["detail"]))

        if visible_details:
            latest_visible_detail = visible_details[-1]
            missing_ack = _missing_required_keys(latest_visible_detail, _WATCHDOG_ACK_RETENTION_KEYS)
            if missing_ack:
                findings.append(
                    _watchdog_issue(
                        "ack_history_retention",
                        "omission",
                        "latest visible transport detail dropped ack-history metadata",
                        plan_id=plan_id,
                        detail={"missing_fields": missing_ack},
                    )
                )

            for key in _WATCHDOG_ACK_COUNT_KEYS:
                previous = None
                for index, detail in enumerate(visible_details):
                    if key not in detail:
                        continue
                    current = int(detail[key])
                    if previous is not None and current < previous:
                        findings.append(
                            _watchdog_issue(
                                "ack_history_retention",
                                "drift",
                                "ack-history request counts regressed instead of staying monotonic",
                                plan_id=plan_id,
                                detail={
                                    "field": key,
                                    "previous": previous,
                                    "observed": current,
                                    "detail_index": index,
                                },
                            )
                        )
                        break
                    previous = current

            for key in _WATCHDOG_ACK_STICKY_KEYS:
                seen_true = False
                for index, detail in enumerate(visible_details):
                    if key not in detail:
                        continue
                    current = bool(detail[key])
                    if seen_true and not current:
                        findings.append(
                            _watchdog_issue(
                                "ack_history_retention",
                                "partial_visibility",
                                "ack-history visibility collapsed after the flag was already observed",
                                plan_id=plan_id,
                                detail={
                                    "field": key,
                                    "detail_index": index,
                                },
                            )
                        )
                        break
                    seen_true = seen_true or current

            for count_key, duplicate_flags in _WATCHDOG_ACK_DUPLICATE_FLAGS.items():
                for index, detail in enumerate(visible_details):
                    if count_key not in detail:
                        continue
                    if int(detail[count_key]) <= 1:
                        continue
                    if any(bool(detail.get(flag)) for flag in duplicate_flags):
                        continue
                    findings.append(
                        _watchdog_issue(
                            "ack_history_retention",
                            "partial_visibility",
                            "ack-history request counts increased without retaining duplicate-or-terminal visibility",
                            plan_id=plan_id,
                            detail={
                                "field": count_key,
                                "detail_index": index,
                                "required_flags": duplicate_flags,
                            },
                        )
                    )
                    break

    if runtime_snapshots or sink_snapshots:
        runtime_sequence = [
            (snapshot.plan_id, snapshot.status.value, snapshot.source_reason, dict(snapshot.detail).get("signal"))
            for snapshot in runtime_snapshots
        ]
        sink_sequence = [
            (snapshot.plan_id, snapshot.status.value, snapshot.source_reason, dict(snapshot.detail).get("signal"))
            for snapshot in sink_snapshots
        ]
        if runtime_sequence != sink_sequence:
            findings.append(
                _watchdog_issue(
                    "partial_status_sink_fan_in",
                    "partial_visibility",
                    "status sink fan-in diverged from the runtime snapshot stream",
                    detail={
                        "runtime_snapshot_count": len(runtime_sequence),
                        "sink_snapshot_count": len(sink_sequence),
                        "runtime_sequence": runtime_sequence,
                        "sink_sequence": sink_sequence,
                    },
                )
            )

    if manual_stop_visible_plan_ids:
        expected_manual_stop_plan_ids = {plan.plan_id for plan in plans}
        for missing_plan_id in sorted(expected_manual_stop_plan_ids - manual_stop_visible_plan_ids):
            findings.append(
                _watchdog_issue(
                    "manual_stop_all_propagation",
                    "partial_visibility",
                    "manual stop-all became visible for peer plans but not for this plan",
                    plan_id=missing_plan_id,
                    detail={"visible_plan_ids": sorted(manual_stop_visible_plan_ids)},
                )
            )

    return LivepaperObservabilityWatchdogReport(
        checked_plan_ids=tuple(plan.plan_id for plan in plans),
        findings=tuple(findings),
    )


class InMemoryPlanStore(PlanStore):
    """Planner-owned immutable batch persistence with no runtime fan-in."""

    def __init__(self) -> None:
        self.batches: list[PlanBatch] = []

    def put_batch(self, batch: PlanBatch) -> None:
        self.batches.append(batch)


class RecordingStatusSink(StatusSink):
    """Normalized runtime fan-in that stays separate from plan storage."""

    def __init__(self) -> None:
        self.snapshots: list[StatusSnapshot] = []
        self.latest_by_plan_id: dict[str, StatusSnapshot] = {}

    def record(self, snapshot: StatusSnapshot) -> None:
        self.snapshots.append(snapshot)
        self.latest_by_plan_id[snapshot.plan_id] = snapshot


class HandleExecutorRegistry(ExecutorRegistry):
    """In-process adapter lookup keyed by executor profile id."""

    def __init__(self, adapters_by_profile_id: Mapping[str, ExecutorAdapter]) -> None:
        self._adapters_by_profile_id = dict(adapters_by_profile_id)

    def adapter_for(self, plan: ExecutionPlan) -> ExecutorAdapter:
        return self._adapters_by_profile_id[plan.executor_binding.executor_profile_id]


class TransportExecutorAdapter(ExecutorAdapter):
    """Source-faithful bounded transport adapter with handle-based idempotency."""

    def __init__(
        self,
        *,
        source: Source,
        executor_profile_id: str,
        pinned_commit: str,
        failure_mode: TransportFailureMode | None = None,
    ) -> None:
        self.source = source
        self.executor_profile_id = executor_profile_id
        self.pinned_commit = pinned_commit
        self.failure_mode = failure_mode or TransportFailureMode()
        self._sessions_by_plan_id: dict[str, _TransportSession] = {}
        self._sessions_by_handle_id: dict[str, _TransportSession] = {}

    def queue_push_snapshot(
        self,
        handle_or_plan_id: DispatchHandle | str,
        status: PlanStatus,
        *,
        source_reason: str | None = None,
        detail: Mapping[str, Any] | None = None,
    ) -> None:
        session = self._session_for_identifier(handle_or_plan_id)
        session.queued_push = QueuedPushSnapshot(status=status, source_reason=source_reason, detail=_freeze_payload(detail))

    def prepare(self, plan: ExecutionPlan) -> DispatchHandle:
        self._validate_plan(plan)
        build_transport_envelope(
            TransportMessageType.PREPARE,
            plan=plan,
            idempotency_key=prepare_idempotency_key(plan.plan_id),
            payload={"plan": serialize_execution_plan(plan)},
        )
        existing = self._sessions_by_plan_id.get(plan.plan_id)
        if existing is not None:
            existing.last_prepare_ack_state = TransportAckState.DUPLICATE
            existing.prepare_duplicate_seen = True
            existing.prepare_request_count += 1
            return self._build_handle(existing, ack_state=TransportAckState.DUPLICATE)

        if self.failure_mode.prepare_rejection is not None:
            raise self._rejection_error(plan, stage="prepare", rejection_class=self.failure_mode.prepare_rejection)

        spec = SourceTransportSpec.for_plan(plan)
        prepared_at_utc = _now_utc()
        handle_id = f"{plan.executor_binding.executor_profile_id}:{plan.plan_id}"
        session = _TransportSession(
            plan=plan,
            spec=spec,
            handle_id=handle_id,
            native_session_id=f"{spec.execution_mode}:{plan.plan_id}",
            prepared_at_utc=prepared_at_utc,
        )
        self._sessions_by_plan_id[plan.plan_id] = session
        self._sessions_by_handle_id[handle_id] = session
        return self._build_handle(session, ack_state=TransportAckState.ACCEPTED)

    async def start(self, handle: DispatchHandle) -> None:
        session = self._session_for_handle(handle)
        session.start_request_count += 1
        build_transport_envelope(
            TransportMessageType.START,
            plan=session.plan,
            idempotency_key=start_idempotency_key(session.plan.plan_id),
            payload={"handle_id": session.handle_id},
        )

        if session.executor_status in _TERMINAL_STATUSES or session.stop_confirmed:
            session.last_start_ack_state = TransportAckState.TERMINAL
            session.start_terminal_seen = True
            return
        if session.started:
            session.last_start_ack_state = TransportAckState.DUPLICATE
            session.start_duplicate_seen = True
            return
        if self.failure_mode.start_rejection is not None:
            raise self._rejection_error(session.plan, stage="start", rejection_class=self.failure_mode.start_rejection)

        session.started = True
        session.executor_status = PlanStatus.STARTING
        session.last_start_ack_state = TransportAckState.ACCEPTED
        session.start_accepted_once = True

    async def status(self, handle: DispatchHandle) -> StatusSnapshot:
        session = self._session_for_handle(handle)
        session.poll_counter += 1
        build_transport_envelope(
            TransportMessageType.STATUS,
            plan=session.plan,
            idempotency_key=status_idempotency_key(session.plan.plan_id, session.poll_counter),
            payload={"handle_id": session.handle_id, "poll_counter": session.poll_counter},
        )

        if self.failure_mode.status_timeout and not session.stop_requested:
            raise TransportCommandError(
                f"status timeout for {session.plan.plan_id}",
                stage="status",
                failure_code=FailureCode.STATUS_TIMEOUT,
                ack_state=TransportAckState.ACCEPTED,
                plan=session.plan,
                source_reason="status timeout",
                detail=self._observability_detail(session, signal="status_poll"),
            )

        polled_status = self._polled_status_for_session(session)
        session.last_sequence += 1
        observed_at_utc = _now_utc()
        polled_snapshot = StatusSnapshot(
            plan_id=session.plan.plan_id,
            status=polled_status,
            source_reason=None,
            observed_at_utc=observed_at_utc,
            detail=_freeze_payload(
                self._observability_detail(session, signal="status_poll")
            ),
        )

        pushed_snapshot = None
        if session.queued_push is not None:
            pushed_snapshot = StatusSnapshot(
                plan_id=session.plan.plan_id,
                status=session.queued_push.status,
                source_reason=session.queued_push.source_reason,
                observed_at_utc=observed_at_utc,
                detail=_freeze_payload(
                    self._observability_detail(
                        session,
                        signal="push_event",
                        extra_detail=session.queued_push.detail,
                    )
                ),
            )
            session.queued_push = None

        reconciled = reconcile_status_snapshot(session.last_reported_status, polled_snapshot, pushed_snapshot)
        session.last_reported_status = reconciled.status
        session.executor_status = reconciled.status
        if reconciled.status in _TERMINAL_STATUSES:
            session.stop_confirmed = True
        return reconciled

    async def stop(self, handle: DispatchHandle, reason: str) -> None:
        session = self._session_for_handle(handle)
        normalized_reason = normalize_stop_reason(reason)
        session.stop_request_count += 1
        build_transport_envelope(
            TransportMessageType.STOP,
            plan=session.plan,
            idempotency_key=stop_idempotency_key(session.plan.plan_id, reason),
            payload={
                "handle_id": session.handle_id,
                "stop_reason": reason,
                "requested_by": "planner_router",
                "requested_at_utc": _now_utc().isoformat(),
            },
        )

        if session.stop_confirmed:
            session.last_stop_ack_state = TransportAckState.TERMINAL
            session.last_stop_reason = normalized_reason
            session.stop_terminal_seen = True
            return
        if session.stop_requested and session.last_stop_reason == normalized_reason:
            session.last_stop_ack_state = TransportAckState.DUPLICATE
            session.stop_duplicate_seen = True
            return
        if self.failure_mode.stop_rejection is not None:
            raise self._rejection_error(
                session.plan,
                stage="stop",
                rejection_class=self.failure_mode.stop_rejection,
                failure_code=FailureCode.SOURCE_STOP_FAILED,
            )

        session.stop_requested = True
        session.stop_status_polled = False
        session.last_stop_reason = normalized_reason
        session.last_stop_ack_state = TransportAckState.ACCEPTED
        session.stop_accepted_once = True
        session.executor_status = PlanStatus.STOPPING

    async def snapshot(self, handle: DispatchHandle) -> Mapping[str, Any]:
        session = self._session_for_handle(handle)
        session.snapshot_counter += 1
        build_transport_envelope(
            TransportMessageType.SNAPSHOT,
            plan=session.plan,
            idempotency_key=snapshot_idempotency_key(session.plan.plan_id, session.snapshot_counter),
            payload={"handle_id": session.handle_id, "request_counter": session.snapshot_counter},
        )

        executor_status = session.executor_status
        if session.stop_requested and not self.failure_mode.stop_confirmation_suppressed:
            executor_status = PlanStatus.STOPPED
            session.executor_status = executor_status
            session.stop_confirmed = True

        return freeze_detail(
            self._observability_detail(
                session,
                signal="snapshot",
                extra_detail={
                    "executor_status": executor_status.value,
                    "stop_reason": session.last_stop_reason,
                },
            )
        )

    def _build_handle(self, session: _TransportSession, *, ack_state: TransportAckState) -> DispatchHandle:
        return DispatchHandle(
            plan_id=session.plan.plan_id,
            source=session.plan.route.selected_source,
            native_handle={
                "transport_version": TRANSPORT_VERSION,
                "handle_id": session.handle_id,
                "ack_state": ack_state.value,
                "entrypoint": session.spec.entrypoint,
                "executor_profile_id": session.plan.executor_binding.executor_profile_id,
                "pinned_commit": session.plan.executor_binding.pinned_commit,
                "status_delivery": session.status_delivery,
                "prepared_at_utc": ensure_utc(session.prepared_at_utc).isoformat(),
                "native_session_id": session.native_session_id,
                "execution_mode": session.spec.execution_mode,
                "startup_method": session.spec.startup_method,
                **dict(self._plan_observability_detail(session.plan)),
                **dict(self._ack_visibility_detail(session)),
            },
            plan=session.plan,
        )

    def _polled_status_for_session(self, session: _TransportSession) -> PlanStatus:
        if session.stop_requested:
            if self.failure_mode.stop_confirmation_suppressed:
                return PlanStatus.STOPPING
            if self.failure_mode.stop_requires_snapshot_confirmation and not session.stop_status_polled:
                session.stop_status_polled = True
                return PlanStatus.STOPPING
            return PlanStatus.STOPPED
        if session.started:
            return PlanStatus.RUNNING
        return PlanStatus.PLANNED

    def _status_ack_state(self, session: _TransportSession) -> TransportAckState:
        if session.stop_requested and session.last_stop_ack_state is not None:
            return session.last_stop_ack_state
        if session.started:
            return session.last_start_ack_state
        return session.last_prepare_ack_state

    def _session_for_identifier(self, handle_or_plan_id: DispatchHandle | str) -> _TransportSession:
        if isinstance(handle_or_plan_id, DispatchHandle):
            return self._session_for_handle(handle_or_plan_id)
        session = self._sessions_by_handle_id.get(handle_or_plan_id)
        if session is not None:
            return session
        return self._sessions_by_plan_id[handle_or_plan_id]

    def _session_for_handle(self, handle: DispatchHandle) -> _TransportSession:
        handle_id = None
        if isinstance(handle.native_handle, Mapping):
            handle_id = handle.native_handle.get("handle_id")
        session = self._sessions_by_handle_id.get(str(handle_id)) if handle_id else None
        if session is None:
            session = self._sessions_by_plan_id.get(handle.plan_id)
        if session is None:
            raise TransportCommandError(
                f"unknown handle for {handle.plan_id}",
                stage="status",
                failure_code=FailureCode.STATUS_TIMEOUT,
                ack_state=TransportAckState.REJECTED,
                plan=handle.plan,
                rejection_class=TransportRejectionClass.UNKNOWN_HANDLE,
                source_reason="unknown handle",
                detail={"plan_id": handle.plan_id, "handle_id": handle_id},
            )
        return session

    def _validate_plan(self, plan: ExecutionPlan) -> None:
        if plan.route.selected_source is not self.source:
            raise self._rejection_error(
                plan,
                stage="prepare",
                rejection_class=TransportRejectionClass.SOURCE_MISMATCH,
            )
        if plan.executor_binding.executor_profile_id != self.executor_profile_id:
            raise self._rejection_error(
                plan,
                stage="prepare",
                rejection_class=TransportRejectionClass.EXECUTOR_PROFILE_MISMATCH,
            )
        if plan.executor_binding.pinned_commit != self.pinned_commit:
            raise self._rejection_error(
                plan,
                stage="prepare",
                rejection_class=TransportRejectionClass.PIN_MISMATCH,
                failure_code=FailureCode.PIN_MISMATCH,
            )

    def _rejection_error(
        self,
        plan: ExecutionPlan,
        *,
        stage: str,
        rejection_class: TransportRejectionClass,
        failure_code: FailureCode | None = None,
    ) -> TransportCommandError:
        if failure_code is None:
            if stage == "prepare":
                failure_code = FailureCode.PREPARE_FAILED
            elif stage == "start":
                failure_code = FailureCode.START_FAILED
            elif stage == "stop":
                failure_code = FailureCode.SOURCE_STOP_FAILED
            else:
                failure_code = FailureCode.STATUS_TIMEOUT
        source_reason = rejection_class.value
        spec = SourceTransportSpec.for_plan(plan)
        return TransportCommandError(
            f"{stage} rejected for {plan.plan_id}",
            stage=stage,
            failure_code=failure_code,
            ack_state=TransportAckState.REJECTED,
            plan=plan,
            rejection_class=rejection_class,
            source_reason=source_reason,
            detail={
                "plan_id": plan.plan_id,
                **dict(self._plan_observability_detail(plan)),
                "entrypoint": spec.entrypoint,
                "execution_mode": spec.execution_mode,
                "startup_method": spec.startup_method,
                "rejection_class": rejection_class.value,
            },
        )

    def _plan_observability_detail(self, plan: ExecutionPlan) -> Mapping[str, Any]:
        return freeze_detail(
            {
                "plan_batch_id": plan.plan_batch_id,
                "objective_profile_id": plan.objective_profile_id,
                "source": plan.route.selected_source.value,
                "selected_sleeve_id": plan.route.selected_sleeve_id,
                "monitor_profile_id": plan.monitor_binding.monitor_profile_id,
                "timeout_envelope_class": plan.monitor_binding.timeout_envelope_class,
                "quarantine_scope": plan.monitor_binding.quarantine_scope,
                "global_halt_participation": plan.monitor_binding.global_halt_participation,
                "executor_profile_id": plan.executor_binding.executor_profile_id,
                "pinned_commit": plan.executor_binding.pinned_commit,
            }
        )

    def _ack_visibility_detail(self, session: _TransportSession) -> Mapping[str, Any]:
        return freeze_detail(
            {
                "prepare_ack_state": session.last_prepare_ack_state.value,
                "prepare_accepted_once": session.prepare_accepted_once,
                "prepare_duplicate_seen": session.prepare_duplicate_seen,
                "prepare_request_count": session.prepare_request_count,
                "start_ack_state": session.last_start_ack_state.value,
                "start_accepted_once": session.start_accepted_once,
                "start_duplicate_seen": session.start_duplicate_seen,
                "start_terminal_seen": session.start_terminal_seen,
                "start_request_count": session.start_request_count,
                "stop_ack_state": session.last_stop_ack_state.value if session.last_stop_ack_state is not None else None,
                "stop_accepted_once": session.stop_accepted_once,
                "stop_duplicate_seen": session.stop_duplicate_seen,
                "stop_terminal_seen": session.stop_terminal_seen,
                "stop_request_count": session.stop_request_count,
                "last_reported_status": session.last_reported_status.value,
            }
        )

    def _observability_detail(
        self,
        session: _TransportSession,
        *,
        signal: str,
        extra_detail: Mapping[str, Any] | None = None,
    ) -> Mapping[str, Any]:
        ack_state = self._status_ack_state(session)
        detail: dict[str, Any] = {
            "handle_id": session.handle_id,
            "native_session_id": session.native_session_id,
            "transport_version": TRANSPORT_VERSION,
            "signal": signal,
            "sequence": session.last_sequence,
            "poll_counter": session.poll_counter,
            "snapshot_counter": session.snapshot_counter,
            "prepared_at_utc": ensure_utc(session.prepared_at_utc).isoformat(),
            "entrypoint": session.spec.entrypoint,
            "execution_mode": session.spec.execution_mode,
            "startup_method": session.spec.startup_method,
            "status_delivery": session.status_delivery,
            "executor_status": session.executor_status.value,
            "stop_reason": session.last_stop_reason,
            "started": session.started,
            "stop_requested": session.stop_requested,
            "stop_confirmed": session.stop_confirmed,
            "ack_state": ack_state.value,
            "duplicate": ack_state is TransportAckState.DUPLICATE,
        }
        detail.update(dict(self._plan_observability_detail(session.plan)))
        detail.update(dict(self._ack_visibility_detail(session)))
        if extra_detail is not None:
            detail.update(dict(extra_detail))
        return freeze_detail(detail)


ReconcilingStatusSink = RecordingStatusSink
TransportExecutorRegistry = HandleExecutorRegistry
SourceFaithfulTransportAdapter = TransportExecutorAdapter
AckState = TransportAckState


def build_source_faithful_transport_registry(
    frozen_pins: SourcePinRegistry,
    *,
    dexter_executor_profile_id: str = "dexter_main_pinned",
    mewx_executor_profile_id: str = "mewx_frozen_pinned",
    dexter_failure_mode: TransportFailureMode | None = None,
    mewx_failure_mode: TransportFailureMode | None = None,
) -> TransportExecutorRegistry:
    return TransportExecutorRegistry(
        {
            dexter_executor_profile_id: SourceFaithfulTransportAdapter(
                source=Source.DEXTER,
                executor_profile_id=dexter_executor_profile_id,
                pinned_commit=frozen_pins.dexter,
                failure_mode=dexter_failure_mode,
            ),
            mewx_executor_profile_id: SourceFaithfulTransportAdapter(
                source=Source.MEWX,
                executor_profile_id=mewx_executor_profile_id,
                pinned_commit=frozen_pins.mewx,
                failure_mode=mewx_failure_mode,
            ),
        }
    )
