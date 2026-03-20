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


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n")


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


def test_validate_run_package_accepts_windows_relative_paths(tmp_path: Path) -> None:
    target = tmp_path / "mewx_fixture"
    shutil.copytree(MEWX_FIXTURE, target)

    metadata_path = target / "run_metadata.json"
    metadata = _load_json(metadata_path)
    metadata["config_snapshot"] = "config\\config_snapshot.json"
    metadata["source_exports"]["candidate_refresh_snapshot"] = (
        "exports\\candidate_refresh_snapshot.json"
    )
    metadata["source_exports"]["session_summary"] = "exports\\session_summary.json"
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n")

    result = validate_run_package(target)

    assert result["classification"] == "pass"
    assert result["checks"]["source_exports_ok"] is True
    assert result["checks"]["proof_attribution_ok"] is True


def test_validate_run_package_summarizes_repeated_payload_issues(tmp_path: Path) -> None:
    target = tmp_path / "mewx_fixture"
    shutil.copytree(MEWX_FIXTURE, target)

    events_path = target / "events.ndjson"
    events = [json.loads(line) for line in events_path.read_text().splitlines() if line.strip()]
    updated = 0
    duplicate_event = None
    for event in events:
        if event["event_type"] == "entry_fill":
            event["payload"].pop("tx_signature", None)
            updated += 1
            duplicate_event = dict(event)
            duplicate_event["event_id"] = "mew-duplicate"
            break
    assert updated == 1
    assert duplicate_event is not None
    events.append(duplicate_event)
    events_path.write_text("".join(json.dumps(event) + "\n" for event in events))

    result = validate_run_package(target)

    payload_issues = [
        issue for issue in result["issues"] if issue["code"] == "missing_event_payload_fields"
    ]
    assert len(payload_issues) == 1
    assert payload_issues[0]["count"] == 2
    assert len(payload_issues[0]["sample_event_ids"]) == 2


def test_validate_run_package_allows_entry_rejected_without_tx_signature(tmp_path: Path) -> None:
    target = tmp_path / "mewx_fixture"
    shutil.copytree(MEWX_FIXTURE, target)

    events_path = target / "events.ndjson"
    events = [json.loads(line) for line in events_path.read_text().splitlines() if line.strip()]
    updated = 0
    for event in events:
        if event["event_type"] == "entry_rejected":
            event["payload"].pop("tx_signature", None)
            updated += 1
    assert updated == 1
    events_path.write_text("".join(json.dumps(event) + "\n" for event in events))

    result = validate_run_package(target)

    assert result["classification"] == "pass"
    assert result["checks"]["payload_fields_ok"] is True


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
    assert "Resume TASK-005 with a matched comparable live window" in summary


def test_build_comparison_pack_auto_defers_fixture_winners(tmp_path: Path) -> None:
    output_dir = tmp_path / "comparison-pack-auto-deferred"
    build_comparison_pack(
        dexter_package_dir=DEXTER_FIXTURE,
        mewx_package_dir=MEWX_FIXTURE,
        output_dir=output_dir,
    )

    pack_manifest = _load_json(output_dir / "pack_manifest.json")
    comparison_pack = _load_json(output_dir / "comparison_pack.json")

    assert pack_manifest["winner_mode"] == "deferred"
    assert comparison_pack["winner_mode"] == "deferred"
    first_row = comparison_pack["comparison_matrix"]["candidate_generation"][0]
    assert first_row["winner"] == "pending_live_evidence"


def test_build_comparison_pack_auto_defers_unmatched_live_windows(
    tmp_path: Path,
) -> None:
    dexter_live = tmp_path / "dexter-live"
    mewx_live = tmp_path / "mewx-live"
    shutil.copytree(DEXTER_FIXTURE, dexter_live)
    shutil.copytree(MEWX_FIXTURE, mewx_live)

    dexter_metadata = _load_json(dexter_live / "run_metadata.json")
    mewx_metadata = _load_json(mewx_live / "run_metadata.json")
    dexter_metadata["evidence_kind"] = "live"
    mewx_metadata["evidence_kind"] = "live"
    mewx_metadata["started_at_utc"] = "2026-03-21T01:05:00Z"
    mewx_metadata["ended_at_utc"] = "2026-03-21T01:25:00Z"
    _write_json(dexter_live / "run_metadata.json", dexter_metadata)
    _write_json(mewx_live / "run_metadata.json", mewx_metadata)

    output_dir = tmp_path / "comparison-pack-live-unmatched"
    build_comparison_pack(
        dexter_package_dir=dexter_live,
        mewx_package_dir=mewx_live,
        output_dir=output_dir,
    )

    pack_manifest = _load_json(output_dir / "pack_manifest.json")
    comparison_pack = _load_json(output_dir / "comparison_pack.json")
    summary = (output_dir / "summary.md").read_text()

    assert pack_manifest["winner_mode"] == "deferred"
    assert comparison_pack["winner_mode"] == "deferred"
    first_row = comparison_pack["comparison_matrix"]["candidate_generation"][0]
    assert first_row["winner"] == "pending_live_evidence"
    assert "Resume TASK-005 with a matched comparable live window" in summary


def test_build_comparison_pack_matched_partial_live_windows_updates_summary(
    tmp_path: Path,
) -> None:
    dexter_live = tmp_path / "dexter-live"
    mewx_live = tmp_path / "mewx-live"
    shutil.copytree(DEXTER_FIXTURE, dexter_live)
    shutil.copytree(MEWX_FIXTURE, mewx_live)

    for package_dir, run_id in (
        (dexter_live, "dexter-live-001"),
        (mewx_live, "mewx-live-001"),
    ):
        metadata = _load_json(package_dir / "run_metadata.json")
        metadata["evidence_kind"] = "live"
        metadata["run_id"] = run_id
        metadata["started_at_utc"] = "2026-03-21T01:00:00Z"
        metadata["ended_at_utc"] = "2026-03-21T01:20:00Z"
        _write_json(package_dir / "run_metadata.json", metadata)

        events_path = package_dir / "events.ndjson"
        events = [json.loads(line) for line in events_path.read_text().splitlines() if line.strip()]
        for event in events:
            event["run_id"] = run_id
        if package_dir == dexter_live:
            events = [event for event in events if event["event_type"] != "run_summary"]
        events_path.write_text("".join(json.dumps(event) + "\n" for event in events))

    output_dir = tmp_path / "comparison-pack-live-matched-partial"
    build_comparison_pack(
        dexter_package_dir=dexter_live,
        mewx_package_dir=mewx_live,
        output_dir=output_dir,
    )

    summary = (output_dir / "summary.md").read_text()

    assert "matched-window packages validate beyond `partial`" in summary
    assert "TASK-006 remains blocked" in summary
