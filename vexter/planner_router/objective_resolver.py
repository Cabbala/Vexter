"""Objective-profile resolution."""

from __future__ import annotations

from .errors import ConfigValidationError, UnknownObjectiveProfileError
from .models import (
    DEFAULT_OBJECTIVE_PROFILE_ID,
    FailureCode,
    MonitorProfileConfig,
    PlanRequest,
    PlannerRouterPackage,
    ResolvedObjectiveProfile,
    RouteMode,
    Source,
)


def _failure(code: FailureCode, *, detail: dict[str, object]) -> object:
    from .models import FailureDetail

    return FailureDetail(code=code, stage="resolve", plan_id=None, source=None, source_reason=None, detail=detail)


def _is_timeout_tolerant(monitor_profile: MonitorProfileConfig) -> bool:
    timeout_class = monitor_profile.timeout_envelope_class.lower()
    return "timeout" in timeout_class or "tolerant" in timeout_class


def _is_explicitly_containment_first(objective_profile_id: str) -> bool:
    return "containment" in objective_profile_id.lower()


def resolve_objective_profile(
    request: PlanRequest,
    package: PlannerRouterPackage,
) -> ResolvedObjectiveProfile:
    if package.planner.global_halt_policy.active:
        raise ConfigValidationError(
            "global halt is active",
            failure=_failure(FailureCode.GLOBAL_HALT_ACTIVE, detail={"plan_request_id": request.plan_request_id}),
        )

    objective_profile_id = request.objective_profile_id or package.planner.default_objective_profile_id or DEFAULT_OBJECTIVE_PROFILE_ID
    config = package.objective_profiles.get(objective_profile_id)
    if config is None:
        raise UnknownObjectiveProfileError(
            f"unknown objective profile {objective_profile_id!r}",
            failure=_failure(
                FailureCode.UNKNOWN_OBJECTIVE_PROFILE,
                detail={"objective_profile_id": objective_profile_id},
            ),
        )

    if config.route_mode not in package.planner.allowed_route_modes:
        raise ConfigValidationError(
            f"unsupported route mode {config.route_mode.value!r}",
            failure=_failure(
                FailureCode.ROUTE_MODE_INVALID,
                detail={
                    "objective_profile_id": config.objective_profile_id,
                    "route_mode": config.route_mode.value,
                },
            ),
        )

    if config.route_mode is RouteMode.SINGLE_SLEEVE and not config.primary_sleeve_id:
        raise ConfigValidationError(
            "single_sleeve profiles require a primary sleeve",
            failure=_failure(
                FailureCode.ROUTE_MODE_INVALID,
                detail={"objective_profile_id": config.objective_profile_id},
            ),
        )

    if config.route_mode is RouteMode.PORTFOLIO_SPLIT:
        if config.preferred_source is not Source.DEXTER:
            raise ConfigValidationError(
                "portfolio_split requires Dexter as the preferred source",
                failure=_failure(
                    FailureCode.ROUTE_MODE_INVALID,
                    detail={"objective_profile_id": config.objective_profile_id},
                ),
            )
        if config.primary_sleeve_id != "dexter_default":
            raise ConfigValidationError(
                "portfolio_split requires dexter_default as the primary sleeve",
                failure=_failure(
                    FailureCode.ROUTE_MODE_INVALID,
                    detail={
                        "objective_profile_id": config.objective_profile_id,
                        "primary_sleeve_id": config.primary_sleeve_id,
                    },
                ),
            )
        if not config.overlay_sleeve_ids:
            raise ConfigValidationError(
                "portfolio_split requires explicit overlay sleeves",
                failure=_failure(
                    FailureCode.ROUTE_MODE_INVALID,
                    detail={"objective_profile_id": config.objective_profile_id},
                ),
            )

    budget_policy = package.budget_policies[config.budget_policy_id]
    monitor_profile = package.monitor_profiles[config.monitor_profile_id]
    executor_profile = package.executor_profiles[config.executor_profile_id]

    if config.preferred_source is Source.MEWX:
        if not _is_explicitly_containment_first(config.objective_profile_id):
            raise ConfigValidationError(
                "Mew-X routing requires an explicit containment-first objective",
                failure=_failure(
                    FailureCode.ROUTE_MODE_INVALID,
                    detail={"objective_profile_id": config.objective_profile_id},
                ),
            )
        if not _is_timeout_tolerant(monitor_profile):
            raise ConfigValidationError(
                "Mew-X routing requires a timeout-tolerant monitor profile",
                failure=_failure(
                    FailureCode.ROUTE_MODE_INVALID,
                    detail={
                        "objective_profile_id": config.objective_profile_id,
                        "monitor_profile_id": monitor_profile.monitor_profile_id,
                    },
                ),
            )

    return ResolvedObjectiveProfile(
        objective_profile_id=config.objective_profile_id,
        preferred_source=config.preferred_source,
        route_mode=config.route_mode,
        primary_sleeve_id=config.primary_sleeve_id,
        overlay_sleeve_ids=config.overlay_sleeve_ids,
        budget_policy=budget_policy,
        monitor_profile=monitor_profile,
        executor_profile=executor_profile,
    )
