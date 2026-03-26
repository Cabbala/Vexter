"""Planner/router exception hierarchy."""

from __future__ import annotations

from collections.abc import Sequence

from .models import DispatchHandle, FailureDetail


class PlannerRouterError(Exception):
    """Base planner/router error."""

    def __init__(self, message: str, *, failure: FailureDetail | None = None) -> None:
        super().__init__(message)
        self.failure = failure


class ConfigLoadError(PlannerRouterError):
    """Raised when config files cannot be loaded."""


class ConfigValidationError(PlannerRouterError):
    """Raised when loaded config violates the fixed planner/router contract."""


class UnknownObjectiveProfileError(ConfigValidationError):
    """Raised when an explicit objective profile is unknown."""


class SleeveSelectionError(PlannerRouterError):
    """Raised when sleeve selection fails."""


class BudgetBindingError(PlannerRouterError):
    """Raised when budget binding fails."""


class PlanEmissionError(PlannerRouterError):
    """Raised when immutable plan emission fails."""


class DispatchError(PlannerRouterError):
    """Raised when dispatch orchestration fails."""

    def __init__(
        self,
        message: str,
        *,
        failure: FailureDetail | None = None,
        prepared_handles: Sequence[DispatchHandle] = (),
    ) -> None:
        super().__init__(message, failure=failure)
        self.prepared_handles = tuple(prepared_handles)


class InvalidStatusTransitionError(DispatchError):
    """Raised when an executor reports an illegal normalized transition."""
