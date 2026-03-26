"""Planner/router transport seams."""

from __future__ import annotations

from typing import Any, Mapping, Protocol

from .models import DispatchHandle, ExecutionPlan, PlanBatch, StatusSnapshot


class PlanStore(Protocol):
    def put_batch(self, batch: PlanBatch) -> None: ...


class ExecutorAdapter(Protocol):
    def prepare(self, plan: ExecutionPlan) -> DispatchHandle: ...

    async def start(self, handle: DispatchHandle) -> None: ...

    async def status(self, handle: DispatchHandle) -> StatusSnapshot: ...

    async def stop(self, handle: DispatchHandle, reason: str) -> None: ...

    async def snapshot(self, handle: DispatchHandle) -> Mapping[str, Any]: ...


class ExecutorRegistry(Protocol):
    def adapter_for(self, plan: ExecutionPlan) -> ExecutorAdapter: ...


class StatusSink(Protocol):
    def record(self, snapshot: StatusSnapshot) -> None: ...
