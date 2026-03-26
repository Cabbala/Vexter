import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def pytest_configure(config) -> None:
    config.addinivalue_line(
        "markers",
        "transport_livepaper_observability_watchdog_ci_gate: grouped watchdog CI gate suite that keeps watchdog, watchdog-runtime, and watchdog-regression-pack surfaces green in CI",
    )
    config.addinivalue_line(
        "markers",
        "transport_livepaper_observability_ci_gate: transport live-paper observability gate suite that must stay green in CI",
    )
    config.addinivalue_line(
        "markers",
        "transport_livepaper_observability_watchdog: transport live-paper observability watchdog suite for drift and omission detection",
    )
    config.addinivalue_line(
        "markers",
        "transport_livepaper_observability_watchdog_runtime: transport live-paper observability watchdog runtime suite for runtime-oriented follow-up continuity",
    )
    config.addinivalue_line(
        "markers",
        "transport_livepaper_observability_watchdog_regression_pack: transport live-paper observability watchdog regression-pack suite for durable drift and omission coverage",
    )
