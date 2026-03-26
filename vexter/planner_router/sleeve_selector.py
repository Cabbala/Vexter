"""Sleeve selection for immutable plans."""

from __future__ import annotations

from collections.abc import Mapping

from .errors import ConfigValidationError, SleeveSelectionError
from .models import FailureCode, ResolvedObjectiveProfile, RouteMode, SelectedSleeve, SleeveConfig, Source


def _failure(code: FailureCode, *, detail: dict[str, object]) -> object:
    from .models import FailureDetail

    return FailureDetail(code=code, stage="select", plan_id=None, source=None, source_reason=None, detail=detail)


def select_sleeves(
    objective: ResolvedObjectiveProfile,
    sleeves: Mapping[str, SleeveConfig],
) -> tuple[SelectedSleeve, ...]:
    candidate_ids: tuple[str, ...]
    if objective.route_mode is RouteMode.SINGLE_SLEEVE:
        candidate_ids = (objective.primary_sleeve_id,)
    else:
        candidate_ids = (objective.primary_sleeve_id, *objective.overlay_sleeve_ids)

    selected: list[SelectedSleeve] = []
    for index, sleeve_id in enumerate(candidate_ids):
        sleeve = sleeves.get(sleeve_id)
        if sleeve is None:
            raise ConfigValidationError(
                f"unknown sleeve {sleeve_id!r}",
                failure=_failure(
                    FailureCode.CONFIG_MISSING,
                    detail={"sleeve_id": sleeve_id},
                ),
            )
        if not sleeve.enabled:
            raise SleeveSelectionError(
                f"sleeve {sleeve_id!r} is disabled",
                failure=_failure(
                    FailureCode.SLEEVE_DISABLED,
                    detail={"sleeve_id": sleeve_id},
                ),
            )
        if sleeve.executor_profile.source is not sleeve.source:
            raise SleeveSelectionError(
                f"sleeve {sleeve_id!r} executor source mismatch",
                failure=_failure(
                    FailureCode.EXECUTOR_SOURCE_MISMATCH,
                    detail={"sleeve_id": sleeve_id},
                ),
            )

        if objective.route_mode is RouteMode.SINGLE_SLEEVE and sleeve.source is not objective.preferred_source:
            raise SleeveSelectionError(
                f"sleeve {sleeve_id!r} does not match preferred source",
                failure=_failure(
                    FailureCode.EXECUTOR_SOURCE_MISMATCH,
                    detail={
                        "sleeve_id": sleeve_id,
                        "preferred_source": objective.preferred_source.value,
                        "sleeve_source": sleeve.source.value,
                    },
                ),
            )

        if objective.route_mode is RouteMode.PORTFOLIO_SPLIT:
            expected_source = Source.DEXTER if index == 0 else Source.MEWX
            if sleeve.source is not expected_source:
                raise SleeveSelectionError(
                    f"sleeve {sleeve_id!r} violates split ordering",
                    failure=_failure(
                        FailureCode.EXECUTOR_SOURCE_MISMATCH,
                        detail={
                            "sleeve_id": sleeve_id,
                            "expected_source": expected_source.value,
                            "actual_source": sleeve.source.value,
                        },
                    ),
                )

        selected.append(
            SelectedSleeve(
                sleeve_id=sleeve.sleeve_id,
                source=sleeve.source,
                executor_profile=sleeve.executor_profile,
                declaration_order=index,
            )
        )

    return tuple(selected)
