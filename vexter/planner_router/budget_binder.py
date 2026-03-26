"""Sleeve-scoped budget binding."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from decimal import Decimal

from .errors import BudgetBindingError, ConfigValidationError
from .models import (
    DEFAULT_PORTFOLIO_BUDGET_ID,
    BudgetBinding,
    BudgetPolicyConfig,
    FailureCode,
    PlanRequest,
    ResolvedObjectiveProfile,
    SelectedSleeve,
    Source,
)


def _failure(code: FailureCode, *, detail: dict[str, object]) -> object:
    from .models import FailureDetail

    return FailureDetail(code=code, stage="bind", plan_id=None, source=None, source_reason=None, detail=detail)


def bind_budgets(
    request: PlanRequest,
    objective: ResolvedObjectiveProfile,
    selected_sleeves: Sequence[SelectedSleeve],
    budget_policies: Mapping[str, BudgetPolicyConfig],
) -> tuple[BudgetBinding, ...]:
    budget_policy = budget_policies.get(objective.budget_policy.budget_policy_id)
    if budget_policy is None:
        raise ConfigValidationError(
            f"unknown budget policy {objective.budget_policy.budget_policy_id!r}",
            failure=_failure(
                FailureCode.UNKNOWN_BUDGET_POLICY,
                detail={"budget_policy_id": objective.budget_policy.budget_policy_id},
            ),
        )

    portfolio_budget_id = request.portfolio_budget_id or DEFAULT_PORTFOLIO_BUDGET_ID
    bindings: list[BudgetBinding] = []
    total_share = Decimal("0")
    for sleeve in selected_sleeves:
        if sleeve.sleeve_id not in budget_policy.sleeve_shares:
            raise ConfigValidationError(
                f"budget policy {budget_policy.budget_policy_id!r} missing sleeve {sleeve.sleeve_id!r}",
                failure=_failure(
                    FailureCode.UNKNOWN_BUDGET_POLICY,
                    detail={
                        "budget_policy_id": budget_policy.budget_policy_id,
                        "sleeve_id": sleeve.sleeve_id,
                    },
                ),
            )
        share = budget_policy.sleeve_shares[sleeve.sleeve_id]
        total_share += share
        cap_reference = budget_policy.cap_reference_by_sleeve.get(sleeve.sleeve_id)
        explicit_cap_required = sleeve.source is Source.MEWX and share > 0

        if explicit_cap_required and (not budget_policy.explicit_cap_required or not cap_reference):
            raise BudgetBindingError(
                "nonzero Mew-X allocation requires an explicit cap reference",
                failure=_failure(
                    FailureCode.MEWX_CAP_REQUIRED,
                    detail={
                        "budget_policy_id": budget_policy.budget_policy_id,
                        "sleeve_id": sleeve.sleeve_id,
                        "share": str(share),
                    },
                ),
            )

        bindings.append(
            BudgetBinding(
                portfolio_budget_id=portfolio_budget_id,
                policy_id=budget_policy.budget_policy_id,
                sleeve_id=sleeve.sleeve_id,
                sleeve_share=share,
                explicit_cap_required=explicit_cap_required,
                cap_reference=cap_reference,
            )
        )

    if total_share > Decimal("100"):
        raise BudgetBindingError(
            "aggregate sleeve share exceeds 100%",
            failure=_failure(
                FailureCode.BUDGET_SHARE_OVERFLOW,
                detail={"total_share": str(total_share)},
            ),
        )

    return tuple(bindings)
