import json
import shutil
from pathlib import Path

import pytest

from vexter.comparison import build_comparison_pack, derive_metrics, validate_run_package


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "comparison_packages"
DEXTER_FIXTURE = FIXTURE_ROOT / "dexter_fixture"
MEWX_FIXTURE = FIXTURE_ROOT / "mewx_fixture"


def _load_json(path: Path) -> dict:
    with path.open() as handle:
        return json.load(handle)


def test_validate_run_package_passes_for_fixtures() -> None:
    dexter_result = validate_run_package(DEXTER_FIXTURE)
    mewx_result = validate_run_package(MEWX_FIXTURE)

    assert dexter_result["classification"] == "pass"
    assert mewx_result["classification"] == "pass"
    assert dexter_result["checks"]["source_exports_ok"] is True
    assert mewx_result["checks"]["proof_attribution_ok"] is True
    assert dexter_result["coverage"]["event_completeness_ratio"] == pytest.approx(1.0)
    assert mewx_result["coverage"]["event_completeness_ratio"] == pytest.approx(1.0)


def test_validate_run_package_marks_partial_when_export_missing(tmp_path: Path) -> None:
    target = tmp_path / "dexter_fixture"
    shutil.copytree(DEXTER_FIXTURE, target)
    (target / "exports" / "stagnant_mint_replay.json").unlink()

    result = validate_run_package(target)

    assert result["classification"] == "partial"
    assert any(
        issue["code"] == "missing_source_export_file" for issue in result["issues"]
    )


def test_derive_metrics_returns_expected_subset() -> None:
    dexter_metrics = derive_metrics(DEXTER_FIXTURE)["metrics"]
    mewx_metrics = derive_metrics(MEWX_FIXTURE)["metrics"]

    assert dexter_metrics["candidate_count"]["value"] == 2
    assert dexter_metrics["candidate_precision_proxy"]["value"] == pytest.approx(0.5)
    assert dexter_metrics["fill_success_rate"]["value"] == pytest.approx(0.5)
    assert dexter_metrics["signal_to_attempt_latency_ms"]["value"] == pytest.approx(2000.0)
    assert dexter_metrics["attempt_to_fill_latency_ms"]["value"] == pytest.approx(2000.0)
    assert dexter_metrics["quote_vs_fill_slippage_bps"]["value"] == pytest.approx(294.1176, rel=1e-4)
    assert dexter_metrics["replayability_grade"]["value"] == "full"

    assert mewx_metrics["candidate_count"]["value"] == 3
    assert mewx_metrics["candidate_precision_proxy"]["value"] == pytest.approx(2 / 3)
    assert mewx_metrics["fill_success_rate"]["value"] == pytest.approx(2 / 3)
    assert mewx_metrics["signal_to_attempt_latency_ms"]["value"] == pytest.approx(1000.0)
    assert mewx_metrics["attempt_to_fill_latency_ms"]["value"] == pytest.approx(1000.0)
    assert mewx_metrics["stale_position_ratio"]["value"] == pytest.approx(0.5)


def test_build_comparison_pack_writes_expected_outputs(tmp_path: Path) -> None:
    output_dir = tmp_path / "comparison-pack"
    build_comparison_pack(
        dexter_package_dir=DEXTER_FIXTURE,
        mewx_package_dir=MEWX_FIXTURE,
        output_dir=output_dir,
        summary_note="Fixture-based sample pack. Live Windows comparison remains pending.",
        defer_winners=True,
    )

    assert (output_dir / "summary.md").exists()
    assert (output_dir / "comparison_matrix.md").exists()
    assert (output_dir / "comparison_pack.json").exists()

    pack_manifest = _load_json(output_dir / "pack_manifest.json")
    comparison_pack = _load_json(output_dir / "comparison_pack.json")
    summary = (output_dir / "summary.md").read_text()

    assert pack_manifest["winner_mode"] == "deferred"
    assert comparison_pack["validation"]["dexter"]["classification"] == "pass"
    assert comparison_pack["validation"]["mewx"]["classification"] == "pass"
    first_row = comparison_pack["comparison_matrix"]["candidate_generation"][0]
    assert first_row["winner"] == "pending_live_evidence"
    assert "Live Windows comparison remains pending" in summary
