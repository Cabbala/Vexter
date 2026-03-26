"""Bounded executor transport implementations and helpers."""

from __future__ import annotations

from collections.abc import Mapping
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
