"""Typed planner/router records."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping, TypeVar


DEFAULT_CONFIG_PACKAGE_ORDER = (
    "planner",
    "objective_profiles",
    "sleeves",
    "budget_policies",
    "monitor_profiles",
    "executor_profiles",
)
DEFAULT_OBJECTIVE_PROFILE_ID = "mixed_default"
DEFAULT_PORTFOLIO_BUDGET_ID = "main"


class Source(str, Enum):
    DEXTER = "dexter"
    MEWX = "mewx"


class RouteMode(str, Enum):
    SINGLE_SLEEVE = "single_sleeve"
    PORTFOLIO_SPLIT = "portfolio_split"


class PlanStatus(str, Enum):
    PLANNED = "planned"
    STARTING = "starting"
    RUNNING = "running"
    QUARANTINED = "quarantined"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"


class FailureCode(str, Enum):
    CONFIG_MISSING = "config_missing"
    DUPLICATE_CONFIG_ID = "duplicate_config_id"
    UNKNOWN_OBJECTIVE_PROFILE = "unknown_objective_profile"
    ROUTE_MODE_INVALID = "route_mode_invalid"
    SLEEVE_DISABLED = "sleeve_disabled"
    EXECUTOR_SOURCE_MISMATCH = "executor_source_mismatch"
    PIN_MISMATCH = "pin_mismatch"
    UNKNOWN_BUDGET_POLICY = "unknown_budget_policy"
    MEWX_CAP_REQUIRED = "mewx_cap_required"
    BUDGET_SHARE_OVERFLOW = "budget_share_overflow"
    GLOBAL_HALT_ACTIVE = "global_halt_active"
    PREPARE_FAILED = "prepare_failed"
    START_FAILED = "start_failed"
    STATUS_TIMEOUT = "status_timeout"
    RECONCILIATION_GAP = "reconciliation_gap"
    SHUTDOWN_UNCONFIRMED = "shutdown_unconfirmed"
    INVALID_STATUS_TRANSITION = "invalid_status_transition"
    SOURCE_STOP_FAILED = "source_stop_failed"


T = TypeVar("T")


def freeze_mapping(mapping: Mapping[str, T] | None = None) -> Mapping[str, T]:
    return MappingProxyType(dict(mapping or {}))


def freeze_detail(mapping: Mapping[str, Any] | None = None) -> Mapping[str, Any]:
    return MappingProxyType(dict(mapping or {}))


def ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


@dataclass(frozen=True, slots=True)
class GlobalHaltPolicy:
    mode: str
    active: bool


@dataclass(frozen=True, slots=True)
class PlannerConfig:
    default_objective_profile_id: str
    default_execution_anchor: Source
    allowed_route_modes: tuple[RouteMode, ...]
    global_halt_policy: GlobalHaltPolicy
    config_package_order: tuple[str, ...] = DEFAULT_CONFIG_PACKAGE_ORDER


@dataclass(frozen=True, slots=True)
class ObjectiveProfileConfig:
    objective_profile_id: str
    preferred_source: Source
    route_mode: RouteMode
    primary_sleeve_id: str
    overlay_sleeve_ids: tuple[str, ...]
    budget_policy_id: str
    monitor_profile_id: str
    executor_profile_id: str


@dataclass(frozen=True, slots=True)
class SleeveConfig:
    sleeve_id: str
    source: Source
    enabled: bool
    budget_mode: str
    executor_profile_id: str
    executor_profile: "ExecutorProfileConfig | None" = None


@dataclass(frozen=True, slots=True)
class BudgetPolicyConfig:
    budget_policy_id: str
    sleeve_shares: Mapping[str, Decimal]
    explicit_cap_required: bool
    cap_reference_by_sleeve: Mapping[str, str]


@dataclass(frozen=True, slots=True)
class MonitorProfileConfig:
    monitor_profile_id: str
    admission_gate_class: str
    timeout_envelope_class: str
    quarantine_scope: str
    global_halt_participation: bool


@dataclass(frozen=True, slots=True)
class ExecutorProfileConfig:
    executor_profile_id: str
    source: Source
    pinned_commit: str
    methods: tuple[str, ...]
    normalized_statuses: tuple[PlanStatus, ...]


@dataclass(frozen=True, slots=True)
class SourcePinRegistry:
    dexter: str
    mewx: str

    def pinned_commit_for(self, source: Source) -> str:
        if source is Source.DEXTER:
            return self.dexter
        return self.mewx


@dataclass(frozen=True, slots=True)
class PlanRequest:
    plan_request_id: str
    objective_profile_id: str | None = None
    portfolio_budget_id: str | None = None


@dataclass(frozen=True, slots=True)
class PlannerRouterPackage:
    planner: PlannerConfig
    objective_profiles: Mapping[str, ObjectiveProfileConfig]
    sleeves: Mapping[str, SleeveConfig]
    budget_policies: Mapping[str, BudgetPolicyConfig]
    monitor_profiles: Mapping[str, MonitorProfileConfig]
    executor_profiles: Mapping[str, ExecutorProfileConfig]
    source_pins: SourcePinRegistry


@dataclass(frozen=True, slots=True)
class ResolvedObjectiveProfile:
    objective_profile_id: str
    preferred_source: Source
    route_mode: RouteMode
    primary_sleeve_id: str
    overlay_sleeve_ids: tuple[str, ...]
    budget_policy: BudgetPolicyConfig
    monitor_profile: MonitorProfileConfig
    executor_profile: ExecutorProfileConfig


@dataclass(frozen=True, slots=True)
class SelectedSleeve:
    sleeve_id: str
    source: Source
    executor_profile: ExecutorProfileConfig
    declaration_order: int


@dataclass(frozen=True, slots=True)
class BudgetBinding:
    portfolio_budget_id: str
    policy_id: str
    sleeve_id: str
    sleeve_share: Decimal
    explicit_cap_required: bool
    cap_reference: str | None


@dataclass(frozen=True, slots=True)
class ResolvedPlanningContext:
    request: PlanRequest
    package: PlannerRouterPackage
    resolved_objective: ResolvedObjectiveProfile
    selected_sleeves: tuple[SelectedSleeve, ...]
    budget_bindings: tuple[BudgetBinding, ...]


@dataclass(frozen=True, slots=True)
class RouteBinding:
    mode: RouteMode
    selected_sleeve_id: str
    selected_source: Source


@dataclass(frozen=True, slots=True)
class SleeveBinding:
    sleeve_id: str
    source: Source
    budget_mode: str


@dataclass(frozen=True, slots=True)
class MonitorBinding:
    monitor_profile_id: str
    admission_gate_class: str
    timeout_envelope_class: str
    quarantine_scope: str
    global_halt_participation: bool


@dataclass(frozen=True, slots=True)
class ExecutorBinding:
    executor_profile_id: str
    source: Source
    pinned_commit: str
    methods: tuple[str, ...]
    normalized_statuses: tuple[PlanStatus, ...]


@dataclass(frozen=True, slots=True)
class ExecutionPlan:
    plan_id: str
    plan_batch_id: str
    created_at_utc: datetime
    objective_profile_id: str
    route: RouteBinding
    sleeve_binding: SleeveBinding
    budget_binding: BudgetBinding
    monitor_binding: MonitorBinding
    executor_binding: ExecutorBinding
    source_pin: SourcePinRegistry
    invariants: tuple[str, ...]
    status: PlanStatus


@dataclass(frozen=True, slots=True)
class PlanBatch:
    plan_batch_id: str
    plans: tuple[ExecutionPlan, ...]
    request_id: str
    portfolio_budget_id: str


@dataclass(frozen=True, slots=True)
class DispatchHandle:
    plan_id: str
    source: Source
    native_handle: Any
    plan: ExecutionPlan | None = None

    @property
    def handle_id(self) -> str | None:
        if isinstance(self.native_handle, Mapping):
            value = self.native_handle.get("handle_id")
            if value is None:
                return None
            return str(value)
        return None


@dataclass(frozen=True, slots=True)
class StatusSnapshot:
    plan_id: str
    status: PlanStatus
    source_reason: str | None
    observed_at_utc: datetime
    detail: Mapping[str, Any] = field(default_factory=freeze_detail)


@dataclass(frozen=True, slots=True)
class FailureDetail:
    code: FailureCode
    stage: str
    plan_id: str | None
    source: Source | None
    source_reason: str | None
    detail: Mapping[str, Any] = field(default_factory=freeze_detail)
