"""Prepare/start dispatch orchestration."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from typing import Any

from .errors import DispatchError, InvalidStatusTransitionError, PlannerRouterError
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
    return _failure_snapshot_with_detail(plan, failure)


def _failure_snapshot_with_detail(
    plan: ExecutionPlan,
    failure: FailureDetail,
    extra_detail: Mapping[str, Any] | None = None,
) -> StatusSnapshot:
    merged_detail = {
        "failure_code": failure.code.value,
        "stage": failure.stage,
        **dict(failure.detail),
    }
    if extra_detail is not None:
        merged_detail.update(dict(extra_detail))
    return StatusSnapshot(
        plan_id=plan.plan_id,
        status=PlanStatus.FAILED,
        source_reason=failure.source_reason,
        observed_at_utc=_now_utc(),
        detail=freeze_detail(merged_detail),
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


def _failure_from_exception(
    exc: Exception,
    *,
    stage: str,
    plan: ExecutionPlan,
    default_code: FailureCode,
) -> FailureDetail:
    if isinstance(exc, PlannerRouterError) and exc.failure is not None:
        return FailureDetail(
            code=exc.failure.code,
            stage=exc.failure.stage,
            plan_id=exc.failure.plan_id or plan.plan_id,
            source=exc.failure.source or plan.route.selected_source,
            source_reason=exc.failure.source_reason,
            detail=freeze_detail(exc.failure.detail),
        )
    return _failure(
        default_code,
        stage=stage,
        plan=plan,
        source_reason=str(exc),
        detail={"error": str(exc)},
    )


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
                failure=_failure_from_exception(
                    exc,
                    stage="prepare",
                    plan=plan,
                    default_code=FailureCode.PREPARE_FAILED,
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
    ) -> dict[str, Mapping[str, Any]]:
    rollback_results: dict[str, Mapping[str, Any]] = {}
    for handle in reversed(tuple(handles)):
        adapter = _adapter_for_handle(handle, executor_registry)
        plan = handle.plan
        if plan is None:
            rollback_results[handle.plan_id] = freeze_detail(
                {
                    "rollback_attempted": False,
                    "rollback_confirmed": False,
                    "rollback_for": failure.code.value,
                    "rollback_failure_code": FailureCode.SOURCE_STOP_FAILED.value,
                    "rollback_source_reason": "handle_missing_plan",
                }
            )
            continue
        try:
            await adapter.stop(handle, reason=failure.code.value)
        except Exception as exc:
            stop_failure = _failure_from_exception(
                exc,
                stage="rollback_stop",
                plan=plan,
                default_code=FailureCode.SOURCE_STOP_FAILED,
            )
            rollback_results[handle.plan_id] = freeze_detail(
                {
                    "rollback_attempted": True,
                    "rollback_confirmed": False,
                    "rollback_for": failure.code.value,
                    "rollback_failure_code": stop_failure.code.value,
                    "rollback_stage": stop_failure.stage,
                    "rollback_source_reason": stop_failure.source_reason,
                    **dict(stop_failure.detail),
                }
            )
            continue

        rollback_results[handle.plan_id] = await _confirm_rollback_stop(handle, plan, adapter, failure)

    return rollback_results


async def _confirm_rollback_stop(
    handle: DispatchHandle,
    plan: ExecutionPlan,
    adapter,
    failure: FailureDetail,
) -> Mapping[str, Any]:
    try:
        status_snapshot = await adapter.status(handle)
    except Exception as exc:
        status_failure = _failure_from_exception(
            exc,
            stage="rollback_status",
            plan=plan,
            default_code=FailureCode.SHUTDOWN_UNCONFIRMED,
        )
        return freeze_detail(
            {
                "rollback_attempted": True,
                "rollback_confirmed": False,
                "rollback_confirmation_source": "status",
                "rollback_for": failure.code.value,
                "rollback_failure_code": status_failure.code.value,
                "rollback_stage": status_failure.stage,
                "rollback_source_reason": status_failure.source_reason,
                **dict(status_failure.detail),
            }
        )

    if status_snapshot.status in {PlanStatus.STOPPED, PlanStatus.FAILED}:
        return freeze_detail(
            {
                "rollback_attempted": True,
                "rollback_confirmed": True,
                "rollback_confirmation_source": "status",
                "rollback_for": failure.code.value,
                "rollback_observed_status": status_snapshot.status.value,
                "rollback_sequence": status_snapshot.detail.get("sequence"),
                "rollback_status_detail": dict(status_snapshot.detail),
            }
        )

    try:
        snapshot = await adapter.snapshot(handle)
    except Exception as exc:
        snapshot_failure = _failure_from_exception(
            exc,
            stage="rollback_snapshot",
            plan=plan,
            default_code=FailureCode.SHUTDOWN_UNCONFIRMED,
        )
        return freeze_detail(
            {
                "rollback_attempted": True,
                "rollback_confirmed": False,
                "rollback_confirmation_source": "snapshot",
                "rollback_for": failure.code.value,
                "rollback_failure_code": snapshot_failure.code.value,
                "rollback_stage": snapshot_failure.stage,
                "rollback_source_reason": snapshot_failure.source_reason,
                **dict(snapshot_failure.detail),
            }
        )

    executor_status = str(snapshot.get("executor_status", "")).strip().lower()
    if executor_status in {PlanStatus.STOPPED.value, PlanStatus.FAILED.value}:
        return freeze_detail(
            {
                "rollback_attempted": True,
                "rollback_confirmed": True,
                "rollback_confirmation_source": "snapshot",
                "rollback_for": failure.code.value,
                "rollback_observed_status": executor_status,
                "rollback_snapshot": dict(snapshot),
            }
        )

    return freeze_detail(
        {
            "rollback_attempted": True,
            "rollback_confirmed": False,
            "rollback_confirmation_source": "snapshot",
            "rollback_for": failure.code.value,
            "rollback_failure_code": FailureCode.SHUTDOWN_UNCONFIRMED.value,
            "rollback_observed_status": status_snapshot.status.value,
            "rollback_status_detail": dict(status_snapshot.detail),
            "rollback_snapshot": dict(snapshot),
        }
    )


async def _abort_dispatch(
    batch: PlanBatch,
    handles: Sequence[DispatchHandle],
    executor_registry: ExecutorRegistry,
    status_sink: StatusSink,
    snapshots: list[StatusSnapshot],
    failure: FailureDetail,
) -> list[StatusSnapshot]:
    rollback_results = await rollback_prepared_batch(handles, executor_registry, failure)
    for batch_plan in batch.plans:
        snapshot = _failure_snapshot_with_detail(
            batch_plan,
            failure,
            rollback_results.get(
                batch_plan.plan_id,
                freeze_detail(
                    {
                        "rollback_attempted": False,
                        "rollback_confirmed": False,
                        "rollback_for": failure.code.value,
                    }
                ),
            ),
        )
        status_sink.record(snapshot)
        snapshots.append(snapshot)
    return snapshots


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
        return await _abort_dispatch(batch, exc.prepared_handles, executor_registry, status_sink, snapshots, failure)

    handles_by_plan_id = {handle.plan_id: handle for handle in handles}
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
        except Exception as exc:
            failure = _failure_from_exception(
                exc,
                stage="start",
                plan=plan,
                default_code=FailureCode.START_FAILED,
            )
            return await _abort_dispatch(batch, handles, executor_registry, status_sink, snapshots, failure)

        try:
            runtime_snapshot = await adapter.status(handle)
            validate_transition(PlanStatus.STARTING, runtime_snapshot.status)
        except InvalidStatusTransitionError as exc:
            failure = exc.failure or _failure(
                FailureCode.INVALID_STATUS_TRANSITION,
                stage="status",
                plan=plan,
                detail={},
            )
            return await _abort_dispatch(batch, handles, executor_registry, status_sink, snapshots, failure)
        except Exception as exc:
            failure = _failure_from_exception(
                exc,
                stage="status",
                plan=plan,
                default_code=FailureCode.STATUS_TIMEOUT,
            )
            return await _abort_dispatch(batch, handles, executor_registry, status_sink, snapshots, failure)

        status_sink.record(runtime_snapshot)
        snapshots.append(runtime_snapshot)

    return snapshots
