"""Prepare/start dispatch orchestration."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from typing import Any

from .errors import DispatchError, InvalidStatusTransitionError
from .interfaces import ExecutorRegistry, StatusSink
from .models import (
    DispatchHandle,
    ExecutionPlan,
    FailureCode,
    FailureDetail,
    PlanBatch,
    PlanStatus,
    StatusSnapshot,
    freeze_detail,
)


ALLOWED_TRANSITIONS = {
    (PlanStatus.PLANNED, PlanStatus.STARTING),
    (PlanStatus.PLANNED, PlanStatus.FAILED),
    (PlanStatus.STARTING, PlanStatus.RUNNING),
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


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _failure(
    code: FailureCode,
    *,
    stage: str,
    plan: ExecutionPlan | None = None,
    source_reason: str | None = None,
    detail: Mapping[str, Any] | None = None,
) -> FailureDetail:
    return FailureDetail(
        code=code,
        stage=stage,
        plan_id=plan.plan_id if plan else None,
        source=plan.route.selected_source if plan else None,
        source_reason=source_reason,
        detail=freeze_detail(detail),
    )


def _failure_snapshot(plan: ExecutionPlan, failure: FailureDetail) -> StatusSnapshot:
    return StatusSnapshot(
        plan_id=plan.plan_id,
        status=PlanStatus.FAILED,
        source_reason=failure.source_reason,
        observed_at_utc=_now_utc(),
        detail=freeze_detail(
            {
                "failure_code": failure.code.value,
                "stage": failure.stage,
                **dict(failure.detail),
            }
        ),
    )


def _adapter_for_handle(handle: DispatchHandle, executor_registry: ExecutorRegistry):
    if handle.plan is None:
        raise DispatchError(
            "dispatch handle is missing plan context",
            failure=FailureDetail(
                code=FailureCode.SOURCE_STOP_FAILED,
                stage="rollback",
                plan_id=handle.plan_id,
                source=handle.source,
                source_reason=None,
                detail=freeze_detail({"reason": "handle_missing_plan"}),
            ),
        )
    return executor_registry.adapter_for(handle.plan)


def validate_transition(previous: PlanStatus, next_status: PlanStatus) -> None:
    if previous == next_status:
        return
    if (previous, next_status) not in ALLOWED_TRANSITIONS:
        raise InvalidStatusTransitionError(
            f"invalid transition {previous.value}->{next_status.value}",
            failure=FailureDetail(
                code=FailureCode.INVALID_STATUS_TRANSITION,
                stage="status",
                plan_id=None,
                source=None,
                source_reason=None,
                detail=freeze_detail({"previous": previous.value, "next_status": next_status.value}),
            ),
        )


def normalize_status_update(
    plan: ExecutionPlan,
    raw_status: str,
    *,
    source_reason: str | None = None,
    detail: Mapping[str, Any] | None = None,
) -> StatusSnapshot:
    normalized = PlanStatus(raw_status.strip().lower())
    return StatusSnapshot(
        plan_id=plan.plan_id,
        status=normalized,
        source_reason=source_reason,
        observed_at_utc=_now_utc(),
        detail=freeze_detail(detail),
    )


async def prepare_batch(
    batch: PlanBatch,
    executor_registry: ExecutorRegistry,
) -> tuple[DispatchHandle, ...]:
    handles: list[DispatchHandle] = []
    for plan in batch.plans:
        adapter = executor_registry.adapter_for(plan)
        try:
            handle = adapter.prepare(plan)
        except Exception as exc:
            raise DispatchError(
                f"prepare failed for {plan.plan_id}",
                failure=_failure(
                    FailureCode.PREPARE_FAILED,
                    stage="prepare",
                    plan=plan,
                    source_reason=str(exc),
                    detail={"error": str(exc)},
                ),
                prepared_handles=handles,
            ) from exc
        if handle.plan is None:
            handle = DispatchHandle(
                plan_id=handle.plan_id,
                source=handle.source,
                native_handle=handle.native_handle,
                plan=plan,
            )
        handles.append(handle)
    return tuple(handles)


async def rollback_prepared_batch(
    handles: Sequence[DispatchHandle],
    executor_registry: ExecutorRegistry,
    failure: FailureDetail,
    status_sink: StatusSink,
) -> None:
    for handle in reversed(tuple(handles)):
        adapter = _adapter_for_handle(handle, executor_registry)
        try:
            await adapter.stop(handle, reason=failure.code.value)
        except Exception as exc:
            status_sink.record(
                StatusSnapshot(
                    plan_id=handle.plan_id,
                    status=PlanStatus.FAILED,
                    source_reason=str(exc),
                    observed_at_utc=_now_utc(),
                    detail=freeze_detail(
                        {
                            "failure_code": FailureCode.SOURCE_STOP_FAILED.value,
                            "rollback_for": failure.code.value,
                        }
                    ),
                )
            )


async def dispatch_plan_batch(
    batch: PlanBatch,
    executor_registry: ExecutorRegistry,
    status_sink: StatusSink,
) -> list[StatusSnapshot]:
    snapshots: list[StatusSnapshot] = []
    try:
        handles = await prepare_batch(batch, executor_registry)
    except DispatchError as exc:
        failure = exc.failure or FailureDetail(
            code=FailureCode.PREPARE_FAILED,
            stage="prepare",
            plan_id=None,
            source=None,
            source_reason=None,
            detail=freeze_detail({}),
        )
        await rollback_prepared_batch(exc.prepared_handles, executor_registry, failure, status_sink)
        for plan in batch.plans:
            snapshot = _failure_snapshot(plan, failure)
            status_sink.record(snapshot)
            snapshots.append(snapshot)
        return snapshots

    handles_by_plan_id = {handle.plan_id: handle for handle in handles}
    started_handles: list[DispatchHandle] = []
    for plan in batch.plans:
        handle = handles_by_plan_id[plan.plan_id]
        adapter = _adapter_for_handle(handle, executor_registry)
        starting_snapshot = StatusSnapshot(
            plan_id=plan.plan_id,
            status=PlanStatus.STARTING,
            source_reason=None,
            observed_at_utc=_now_utc(),
            detail=freeze_detail({"stage": "start"}),
        )
        validate_transition(plan.status, PlanStatus.STARTING)
        status_sink.record(starting_snapshot)
        snapshots.append(starting_snapshot)

        try:
            await adapter.start(handle)
            started_handles.append(handle)
            runtime_snapshot = await adapter.status(handle)
            validate_transition(PlanStatus.STARTING, runtime_snapshot.status)
        except InvalidStatusTransitionError as exc:
            failure = exc.failure or _failure(
                FailureCode.INVALID_STATUS_TRANSITION,
                stage="status",
                plan=plan,
                detail={},
            )
            await rollback_prepared_batch(handles, executor_registry, failure, status_sink)
            for batch_plan in batch.plans:
                snapshot = _failure_snapshot(batch_plan, failure)
                status_sink.record(snapshot)
                snapshots.append(snapshot)
            return snapshots
        except Exception as exc:
            failure = _failure(
                FailureCode.START_FAILED,
                stage="start",
                plan=plan,
                source_reason=str(exc),
                detail={"error": str(exc)},
            )
            await rollback_prepared_batch(handles, executor_registry, failure, status_sink)
            for batch_plan in batch.plans:
                snapshot = _failure_snapshot(batch_plan, failure)
                status_sink.record(snapshot)
                snapshots.append(snapshot)
            return snapshots

        status_sink.record(runtime_snapshot)
        snapshots.append(runtime_snapshot)

    return snapshots
