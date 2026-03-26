"""Deterministic planner/router config loading."""

from __future__ import annotations

import json
from dataclasses import replace
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable, TypeVar

from .errors import ConfigLoadError, ConfigValidationError
from .models import (
    DEFAULT_CONFIG_PACKAGE_ORDER,
    DEFAULT_OBJECTIVE_PROFILE_ID,
    BudgetPolicyConfig,
    ExecutorProfileConfig,
    FailureCode,
    GlobalHaltPolicy,
    MonitorProfileConfig,
    ObjectiveProfileConfig,
    PlanStatus,
    PlannerConfig,
    PlannerRouterPackage,
    RouteMode,
    SleeveConfig,
    Source,
    SourcePinRegistry,
    freeze_mapping,
)


JSONValue = dict[str, Any] | list[Any] | str | int | float | bool | None
T = TypeVar("T")


def _object_pairs_no_duplicates(pairs: list[tuple[str, JSONValue]]) -> dict[str, JSONValue]:
    payload: dict[str, JSONValue] = {}
    for key, value in pairs:
        if key in payload:
            raise ConfigLoadError(
                f"duplicate key {key!r}",
                failure=_failure(
                    FailureCode.DUPLICATE_CONFIG_ID,
                    stage="load",
                    detail={"duplicate_key": key},
                ),
            )
        payload[key] = value
    return payload


def _load_json(path: Path) -> JSONValue:
    try:
        with path.open() as handle:
            return json.load(handle, object_pairs_hook=_object_pairs_no_duplicates)
    except FileNotFoundError as exc:
        raise ConfigLoadError(
            f"missing config file: {path}",
            failure=_failure(
                FailureCode.CONFIG_MISSING,
                stage="load",
                detail={"path": str(path)},
            ),
        ) from exc
    except json.JSONDecodeError as exc:
        raise ConfigLoadError(
            f"invalid json at {path}: {exc}",
            failure=_failure(
                FailureCode.CONFIG_MISSING,
                stage="load",
                detail={"path": str(path), "error": str(exc)},
            ),
        ) from exc


def _expect_object(payload: JSONValue, *, path: Path) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ConfigLoadError(
            f"expected object JSON at {path}",
            failure=_failure(
                FailureCode.CONFIG_MISSING,
                stage="load",
                detail={"path": str(path), "expected": "object"},
            ),
        )
    return payload


def _expect_list(payload: JSONValue, *, path: Path) -> list[dict[str, Any]]:
    if not isinstance(payload, list):
        raise ConfigLoadError(
            f"expected array JSON at {path}",
            failure=_failure(
                FailureCode.CONFIG_MISSING,
                stage="load",
                detail={"path": str(path), "expected": "array"},
            ),
        )
    items: list[dict[str, Any]] = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise ConfigLoadError(
                f"expected object item at {path}:{index}",
                failure=_failure(
                    FailureCode.CONFIG_MISSING,
                    stage="load",
                    detail={"path": str(path), "index": index},
                ),
            )
        items.append(item)
    return items


def _as_string(raw: Any, *, path: Path, field: str) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise ConfigValidationError(
            f"invalid {field!r} at {path}",
            failure=_failure(
                FailureCode.CONFIG_MISSING,
                stage="validate",
                detail={"path": str(path), "field": field},
            ),
        )
    return raw.strip()


def _as_bool(raw: Any, *, path: Path, field: str) -> bool:
    if not isinstance(raw, bool):
        raise ConfigValidationError(
            f"invalid boolean {field!r} at {path}",
            failure=_failure(
                FailureCode.CONFIG_MISSING,
                stage="validate",
                detail={"path": str(path), "field": field},
            ),
        )
    return raw


def _parse_source(raw: Any, *, path: Path, field: str) -> Source:
    value = _as_string(raw, path=path, field=field).lower()
    try:
        return Source(value)
    except ValueError as exc:
        raise ConfigValidationError(
            f"invalid source {raw!r} at {path}",
            failure=_failure(
                FailureCode.ROUTE_MODE_INVALID,
                stage="validate",
                detail={"path": str(path), "field": field, "value": raw},
            ),
        ) from exc


def _parse_route_mode(raw: Any, *, path: Path, field: str) -> RouteMode:
    value = _as_string(raw, path=path, field=field).lower()
    try:
        return RouteMode(value)
    except ValueError as exc:
        raise ConfigValidationError(
            f"invalid route mode {raw!r} at {path}",
            failure=_failure(
                FailureCode.ROUTE_MODE_INVALID,
                stage="validate",
                detail={"path": str(path), "field": field, "value": raw},
            ),
        ) from exc


def _parse_share(raw: Any, *, path: Path, sleeve_id: str) -> Decimal:
    if isinstance(raw, (int, float)):
        return Decimal(str(raw))
    if isinstance(raw, str):
        normalized = raw.strip()
        if normalized.endswith("%"):
            normalized = normalized[:-1].strip()
        try:
            return Decimal(normalized)
        except Exception as exc:  # pragma: no cover - Decimal can raise multiple types
            raise ConfigValidationError(
                f"invalid sleeve share for {sleeve_id!r} at {path}",
                failure=_failure(
                    FailureCode.CONFIG_MISSING,
                    stage="validate",
                    detail={"path": str(path), "sleeve_id": sleeve_id, "value": raw},
                ),
            ) from exc
    raise ConfigValidationError(
        f"invalid sleeve share for {sleeve_id!r} at {path}",
        failure=_failure(
            FailureCode.CONFIG_MISSING,
            stage="validate",
            detail={"path": str(path), "sleeve_id": sleeve_id, "value": raw},
        ),
    )


def _load_registry(
    path: Path,
    id_field: str,
    loader: Callable[[dict[str, Any], Path], T],
) -> dict[str, T]:
    items = _expect_list(_load_json(path), path=path)
    registry: dict[str, T] = {}
    for item in items:
        config = loader(item, path)
        identifier = getattr(config, id_field)
        if identifier in registry:
            raise ConfigLoadError(
                f"duplicate config id {identifier!r} in {path}",
                failure=_failure(
                    FailureCode.DUPLICATE_CONFIG_ID,
                    stage="load",
                    detail={"path": str(path), "id": identifier},
                ),
            )
        registry[identifier] = config
    return registry


def _failure(
    code: FailureCode,
    *,
    stage: str,
    detail: dict[str, Any],
) -> Any:
    from .models import FailureDetail

    return FailureDetail(code=code, stage=stage, plan_id=None, source=None, source_reason=None, detail=detail)


def load_planner_config(path: Path) -> PlannerConfig:
    payload = _expect_object(_load_json(path), path=path)
    halt = payload.get("global_halt_policy")
    if not isinstance(halt, dict):
        raise ConfigValidationError(
            f"planner global_halt_policy missing at {path}",
            failure=_failure(
                FailureCode.CONFIG_MISSING,
                stage="validate",
                detail={"path": str(path), "field": "global_halt_policy"},
            ),
        )
    config_package_order = tuple(payload.get("config_package_order", DEFAULT_CONFIG_PACKAGE_ORDER))
    return PlannerConfig(
        default_objective_profile_id=_as_string(
            payload.get("default_objective_profile_id", DEFAULT_OBJECTIVE_PROFILE_ID),
            path=path,
            field="default_objective_profile_id",
        ),
        default_execution_anchor=_parse_source(
            payload.get("default_execution_anchor"),
            path=path,
            field="default_execution_anchor",
        ),
        allowed_route_modes=tuple(
            _parse_route_mode(value, path=path, field="allowed_route_modes")
            for value in payload.get("allowed_route_modes", [])
        ),
        global_halt_policy=GlobalHaltPolicy(
            mode=_as_string(halt.get("mode"), path=path, field="global_halt_policy.mode"),
            active=_as_bool(halt.get("active"), path=path, field="global_halt_policy.active"),
        ),
        config_package_order=config_package_order,
    )


def load_objective_profiles(path: Path) -> dict[str, ObjectiveProfileConfig]:
    return _load_registry(path, "objective_profile_id", _load_objective_profile)


def _load_objective_profile(item: dict[str, Any], path: Path) -> ObjectiveProfileConfig:
    overlay_ids = item.get("overlay_sleeve_ids", [])
    if overlay_ids is None:
        overlay_ids = []
    if not isinstance(overlay_ids, list):
        raise ConfigValidationError(
            f"overlay_sleeve_ids must be a list at {path}",
            failure=_failure(
                FailureCode.CONFIG_MISSING,
                stage="validate",
                detail={"path": str(path), "field": "overlay_sleeve_ids"},
            ),
        )
    return ObjectiveProfileConfig(
        objective_profile_id=_as_string(item.get("objective_profile_id"), path=path, field="objective_profile_id"),
        preferred_source=_parse_source(item.get("preferred_source"), path=path, field="preferred_source"),
        route_mode=_parse_route_mode(item.get("route_mode"), path=path, field="route_mode"),
        primary_sleeve_id=_as_string(item.get("primary_sleeve_id"), path=path, field="primary_sleeve_id"),
        overlay_sleeve_ids=tuple(
            _as_string(value, path=path, field="overlay_sleeve_ids") for value in overlay_ids
        ),
        budget_policy_id=_as_string(item.get("budget_policy_id"), path=path, field="budget_policy_id"),
        monitor_profile_id=_as_string(item.get("monitor_profile_id"), path=path, field="monitor_profile_id"),
        executor_profile_id=_as_string(item.get("executor_profile_id"), path=path, field="executor_profile_id"),
    )


def load_sleeves(path: Path) -> dict[str, SleeveConfig]:
    return _load_registry(path, "sleeve_id", _load_sleeve)


def _load_sleeve(item: dict[str, Any], path: Path) -> SleeveConfig:
    return SleeveConfig(
        sleeve_id=_as_string(item.get("sleeve_id"), path=path, field="sleeve_id"),
        source=_parse_source(item.get("source"), path=path, field="source"),
        enabled=_as_bool(item.get("enabled"), path=path, field="enabled"),
        budget_mode=_as_string(item.get("budget_mode"), path=path, field="budget_mode"),
        executor_profile_id=_as_string(item.get("executor_profile_id"), path=path, field="executor_profile_id"),
    )


def load_budget_policies(path: Path) -> dict[str, BudgetPolicyConfig]:
    return _load_registry(path, "budget_policy_id", _load_budget_policy)


def _load_budget_policy(item: dict[str, Any], path: Path) -> BudgetPolicyConfig:
    shares_raw = item.get("sleeve_shares")
    caps_raw = item.get("cap_reference_by_sleeve", {})
    if not isinstance(shares_raw, dict):
        raise ConfigValidationError(
            f"sleeve_shares must be an object at {path}",
            failure=_failure(
                FailureCode.CONFIG_MISSING,
                stage="validate",
                detail={"path": str(path), "field": "sleeve_shares"},
            ),
        )
    if not isinstance(caps_raw, dict):
        raise ConfigValidationError(
            f"cap_reference_by_sleeve must be an object at {path}",
            failure=_failure(
                FailureCode.CONFIG_MISSING,
                stage="validate",
                detail={"path": str(path), "field": "cap_reference_by_sleeve"},
            ),
        )
    shares = {
        _as_string(sleeve_id, path=path, field="sleeve_shares"): _parse_share(raw_share, path=path, sleeve_id=sleeve_id)
        for sleeve_id, raw_share in shares_raw.items()
    }
    caps = {
        _as_string(sleeve_id, path=path, field="cap_reference_by_sleeve"): _as_string(
            cap_reference,
            path=path,
            field=f"cap_reference_by_sleeve.{sleeve_id}",
        )
        for sleeve_id, cap_reference in caps_raw.items()
    }
    return BudgetPolicyConfig(
        budget_policy_id=_as_string(item.get("budget_policy_id"), path=path, field="budget_policy_id"),
        sleeve_shares=freeze_mapping(shares),
        explicit_cap_required=_as_bool(
            item.get("explicit_cap_required"),
            path=path,
            field="explicit_cap_required",
        ),
        cap_reference_by_sleeve=freeze_mapping(caps),
    )


def load_monitor_profiles(path: Path) -> dict[str, MonitorProfileConfig]:
    return _load_registry(path, "monitor_profile_id", _load_monitor_profile)


def _load_monitor_profile(item: dict[str, Any], path: Path) -> MonitorProfileConfig:
    return MonitorProfileConfig(
        monitor_profile_id=_as_string(item.get("monitor_profile_id"), path=path, field="monitor_profile_id"),
        admission_gate_class=_as_string(
            item.get("admission_gate_class"),
            path=path,
            field="admission_gate_class",
        ),
        timeout_envelope_class=_as_string(
            item.get("timeout_envelope_class"),
            path=path,
            field="timeout_envelope_class",
        ),
        quarantine_scope=_as_string(item.get("quarantine_scope"), path=path, field="quarantine_scope"),
        global_halt_participation=_as_bool(
            item.get("global_halt_participation"),
            path=path,
            field="global_halt_participation",
        ),
    )


def load_executor_profiles(path: Path) -> dict[str, ExecutorProfileConfig]:
    return _load_registry(path, "executor_profile_id", _load_executor_profile)


def _load_executor_profile(item: dict[str, Any], path: Path) -> ExecutorProfileConfig:
    methods_raw = item.get("methods", [])
    statuses_raw = item.get("normalized_statuses", [])
    if not isinstance(methods_raw, list) or not isinstance(statuses_raw, list):
        raise ConfigValidationError(
            f"methods and normalized_statuses must be arrays at {path}",
            failure=_failure(
                FailureCode.CONFIG_MISSING,
                stage="validate",
                detail={"path": str(path)},
            ),
        )
    return ExecutorProfileConfig(
        executor_profile_id=_as_string(item.get("executor_profile_id"), path=path, field="executor_profile_id"),
        source=_parse_source(item.get("source"), path=path, field="source"),
        pinned_commit=_as_string(item.get("pinned_commit"), path=path, field="pinned_commit"),
        methods=tuple(_as_string(method, path=path, field="methods") for method in methods_raw),
        normalized_statuses=tuple(
            PlanStatus(_as_string(status, path=path, field="normalized_statuses")) for status in statuses_raw
        ),
    )


def validate_package_references(
    package: PlannerRouterPackage,
    frozen_pins: SourcePinRegistry,
) -> None:
    if tuple(package.planner.config_package_order) != tuple(DEFAULT_CONFIG_PACKAGE_ORDER):
        raise ConfigValidationError(
            "planner config_package_order must remain source-faithful",
            failure=_failure(
                FailureCode.CONFIG_MISSING,
                stage="validate",
                detail={"config_package_order": list(package.planner.config_package_order)},
            ),
        )
    if package.planner.default_objective_profile_id not in package.objective_profiles:
        raise ConfigValidationError(
            "default objective profile is missing",
            failure=_failure(
                FailureCode.UNKNOWN_OBJECTIVE_PROFILE,
                stage="validate",
                detail={"objective_profile_id": package.planner.default_objective_profile_id},
            ),
        )
    if package.planner.default_execution_anchor is not Source.DEXTER:
        raise ConfigValidationError(
            "Dexter must remain the default execution anchor",
            failure=_failure(
                FailureCode.ROUTE_MODE_INVALID,
                stage="validate",
                detail={"default_execution_anchor": package.planner.default_execution_anchor.value},
            ),
        )
    if tuple(package.planner.allowed_route_modes) != (RouteMode.SINGLE_SLEEVE, RouteMode.PORTFOLIO_SPLIT):
        raise ConfigValidationError(
            "allowed_route_modes must remain single_sleeve then portfolio_split",
            failure=_failure(
                FailureCode.ROUTE_MODE_INVALID,
                stage="validate",
                detail={"allowed_route_modes": [mode.value for mode in package.planner.allowed_route_modes]},
            ),
        )

    for executor_profile in package.executor_profiles.values():
        expected_pin = frozen_pins.pinned_commit_for(executor_profile.source)
        if executor_profile.pinned_commit != expected_pin:
            raise ConfigValidationError(
                f"executor profile pin mismatch for {executor_profile.executor_profile_id}",
                failure=_failure(
                    FailureCode.PIN_MISMATCH,
                    stage="validate",
                    detail={
                        "executor_profile_id": executor_profile.executor_profile_id,
                        "expected": expected_pin,
                        "actual": executor_profile.pinned_commit,
                    },
                ),
            )

    for sleeve in package.sleeves.values():
        executor_profile = package.executor_profiles.get(sleeve.executor_profile_id)
        if executor_profile is None:
            raise ConfigValidationError(
                f"missing executor profile for sleeve {sleeve.sleeve_id}",
                failure=_failure(
                    FailureCode.EXECUTOR_SOURCE_MISMATCH,
                    stage="validate",
                    detail={"sleeve_id": sleeve.sleeve_id, "executor_profile_id": sleeve.executor_profile_id},
                ),
            )
        if executor_profile.source is not sleeve.source:
            raise ConfigValidationError(
                f"executor profile source mismatch for sleeve {sleeve.sleeve_id}",
                failure=_failure(
                    FailureCode.EXECUTOR_SOURCE_MISMATCH,
                    stage="validate",
                    detail={
                        "sleeve_id": sleeve.sleeve_id,
                        "sleeve_source": sleeve.source.value,
                        "executor_source": executor_profile.source.value,
                    },
                ),
            )

    for objective_profile in package.objective_profiles.values():
        if objective_profile.route_mode not in package.planner.allowed_route_modes:
            raise ConfigValidationError(
                f"unsupported route mode for {objective_profile.objective_profile_id}",
                failure=_failure(
                    FailureCode.ROUTE_MODE_INVALID,
                    stage="validate",
                    detail={
                        "objective_profile_id": objective_profile.objective_profile_id,
                        "route_mode": objective_profile.route_mode.value,
                    },
                ),
            )
        if objective_profile.primary_sleeve_id not in package.sleeves:
            raise ConfigValidationError(
                f"missing primary sleeve for {objective_profile.objective_profile_id}",
                failure=_failure(
                    FailureCode.CONFIG_MISSING,
                    stage="validate",
                    detail={
                        "objective_profile_id": objective_profile.objective_profile_id,
                        "primary_sleeve_id": objective_profile.primary_sleeve_id,
                    },
                ),
            )
        for overlay_sleeve_id in objective_profile.overlay_sleeve_ids:
            if overlay_sleeve_id not in package.sleeves:
                raise ConfigValidationError(
                    f"missing overlay sleeve for {objective_profile.objective_profile_id}",
                    failure=_failure(
                        FailureCode.CONFIG_MISSING,
                        stage="validate",
                        detail={
                            "objective_profile_id": objective_profile.objective_profile_id,
                            "overlay_sleeve_id": overlay_sleeve_id,
                        },
                    ),
                )
        if objective_profile.budget_policy_id not in package.budget_policies:
            raise ConfigValidationError(
                f"unknown budget policy for {objective_profile.objective_profile_id}",
                failure=_failure(
                    FailureCode.UNKNOWN_BUDGET_POLICY,
                    stage="validate",
                    detail={
                        "objective_profile_id": objective_profile.objective_profile_id,
                        "budget_policy_id": objective_profile.budget_policy_id,
                    },
                ),
            )
        if objective_profile.monitor_profile_id not in package.monitor_profiles:
            raise ConfigValidationError(
                f"unknown monitor profile for {objective_profile.objective_profile_id}",
                failure=_failure(
                    FailureCode.CONFIG_MISSING,
                    stage="validate",
                    detail={
                        "objective_profile_id": objective_profile.objective_profile_id,
                        "monitor_profile_id": objective_profile.monitor_profile_id,
                    },
                ),
            )
        objective_executor = package.executor_profiles.get(objective_profile.executor_profile_id)
        if objective_executor is None:
            raise ConfigValidationError(
                f"unknown executor profile for {objective_profile.objective_profile_id}",
                failure=_failure(
                    FailureCode.EXECUTOR_SOURCE_MISMATCH,
                    stage="validate",
                    detail={
                        "objective_profile_id": objective_profile.objective_profile_id,
                        "executor_profile_id": objective_profile.executor_profile_id,
                    },
                ),
            )
        if objective_executor.source is not objective_profile.preferred_source:
            raise ConfigValidationError(
                f"executor profile source mismatch for {objective_profile.objective_profile_id}",
                failure=_failure(
                    FailureCode.EXECUTOR_SOURCE_MISMATCH,
                    stage="validate",
                    detail={
                        "objective_profile_id": objective_profile.objective_profile_id,
                        "preferred_source": objective_profile.preferred_source.value,
                        "executor_profile_source": objective_executor.source.value,
                    },
                ),
            )
        expected_sleeves = (objective_profile.primary_sleeve_id, *objective_profile.overlay_sleeve_ids)
        budget_policy = package.budget_policies[objective_profile.budget_policy_id]
        for sleeve_id in expected_sleeves:
            if sleeve_id not in budget_policy.sleeve_shares:
                raise ConfigValidationError(
                    f"budget policy {budget_policy.budget_policy_id} missing sleeve {sleeve_id}",
                    failure=_failure(
                        FailureCode.UNKNOWN_BUDGET_POLICY,
                        stage="validate",
                        detail={
                            "budget_policy_id": budget_policy.budget_policy_id,
                            "sleeve_id": sleeve_id,
                        },
                    ),
                )


def load_planner_router_package(
    config_root: Path,
    frozen_pins: SourcePinRegistry,
) -> PlannerRouterPackage:
    config_root = Path(config_root).resolve()
    planner = load_planner_config(config_root / "planner.json")
    objective_profiles = freeze_mapping(load_objective_profiles(config_root / "objective_profiles.json"))
    raw_sleeves = load_sleeves(config_root / "sleeves.json")
    budget_policies = freeze_mapping(load_budget_policies(config_root / "budget_policies.json"))
    monitor_profiles = freeze_mapping(load_monitor_profiles(config_root / "monitor_profiles.json"))
    executor_profiles = load_executor_profiles(config_root / "executor_profiles.json")
    resolved_sleeves = {
        sleeve_id: replace(
            sleeve,
            executor_profile=executor_profiles.get(sleeve.executor_profile_id),
        )
        for sleeve_id, sleeve in raw_sleeves.items()
    }
    package = PlannerRouterPackage(
        planner=planner,
        objective_profiles=objective_profiles,
        sleeves=freeze_mapping(resolved_sleeves),
        budget_policies=budget_policies,
        monitor_profiles=monitor_profiles,
        executor_profiles=freeze_mapping(executor_profiles),
        source_pins=frozen_pins,
    )
    validate_package_references(package, frozen_pins)
    return package
