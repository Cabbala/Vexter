import json
import shutil
from pathlib import Path

import pytest

from vexter.comparison import (
    build_comparison_pack,
    derive_metrics,
    run_replay_validation,
    validate_run_package,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "comparison_packages"
DEXTER_FIXTURE = FIXTURE_ROOT / "dexter_fixture"
MEWX_FIXTURE = FIXTURE_ROOT / "mewx_fixture"


def _load_json(path: Path) -> dict:
    with path.open() as handle:
        return json.load(handle)


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n")


def _make_live_package(
    fixture_dir: Path,
    target_dir: Path,
    *,
    run_id: str,
    started_at_utc: str,
    ended_at_utc: str,
) -> None:
    shutil.copytree(fixture_dir, target_dir)

    metadata = _load_json(target_dir / "run_metadata.json")
    metadata["evidence_kind"] = "live"
    metadata["run_id"] = run_id
    metadata["started_at_utc"] = started_at_utc
    metadata["ended_at_utc"] = ended_at_utc
    _write_json(target_dir / "run_metadata.json", metadata)

    events_path = target_dir / "events.ndjson"
    events = [json.loads(line) for line in events_path.read_text().splitlines() if line.strip()]
    for event in events:
        event["run_id"] = run_id
    events_path.write_text("".join(json.dumps(event) + "\n" for event in events))


def _remove_event_type(target_dir: Path, event_type: str) -> None:
    events_path = target_dir / "events.ndjson"
    events = [json.loads(line) for line in events_path.read_text().splitlines() if line.strip()]
    filtered = [event for event in events if event["event_type"] != event_type]
    events_path.write_text("".join(json.dumps(event) + "\n" for event in filtered))


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


def test_validate_run_package_allows_missing_run_summary_without_clean_shutdown_proof(
    tmp_path: Path,
) -> None:
    target = tmp_path / "dexter_fixture"
    shutil.copytree(DEXTER_FIXTURE, target)

    events_path = target / "events.ndjson"
    events = [json.loads(line) for line in events_path.read_text().splitlines() if line.strip()]
    events = [event for event in events if event["event_type"] != "run_summary"]
    events_path.write_text("".join(json.dumps(event) + "\n" for event in events))

    result = validate_run_package(target)

    assert result["classification"] == "pass"
    assert "run_summary" in result["contract"]["waived_event_types"]
    assert "run_summary" not in result["contract"]["active_required_event_types"]


def test_validate_run_package_requires_run_summary_when_clean_shutdown_is_proven(
    tmp_path: Path,
) -> None:
    target = tmp_path / "dexter_fixture"
    shutil.copytree(DEXTER_FIXTURE, target)

    state_export = target / "exports" / "dexter-fixture-001.state.json"
    _write_json(
        state_export,
        {
            "run_id": "dexter-fixture-001",
            "status": "completed",
            "ended_at_utc": "2026-03-21T01:20:00Z",
        },
    )

    events_path = target / "events.ndjson"
    events = [json.loads(line) for line in events_path.read_text().splitlines() if line.strip()]
    events = [event for event in events if event["event_type"] != "run_summary"]
    events_path.write_text("".join(json.dumps(event) + "\n" for event in events))

    result = validate_run_package(target)

    assert result["classification"] == "partial"
    assert "run_summary" in result["contract"]["active_required_event_types"]
    assert any(issue["code"] == "missing_required_event_types" for issue in result["issues"])


def test_validate_run_package_requires_entry_rejected_when_attempt_has_no_fill(
    tmp_path: Path,
) -> None:
    target = tmp_path / "dexter_fixture"
    shutil.copytree(DEXTER_FIXTURE, target)

    events_path = target / "events.ndjson"
    events = [json.loads(line) for line in events_path.read_text().splitlines() if line.strip()]
    events = [event for event in events if event["event_type"] != "entry_rejected"]
    events_path.write_text("".join(json.dumps(event) + "\n" for event in events))

    result = validate_run_package(target)

    assert result["classification"] == "partial"
    assert "entry_rejected" in result["contract"]["active_required_event_types"]
    assert "entry_rejected" in result["coverage"]["missing_event_types"]


def test_validate_run_package_allows_missing_entry_rejected_when_all_attempts_fill(
    tmp_path: Path,
) -> None:
    target = tmp_path / "dexter_fixture"
    shutil.copytree(DEXTER_FIXTURE, target)

    events_path = target / "events.ndjson"
    events = [json.loads(line) for line in events_path.read_text().splitlines() if line.strip()]

    rejected_event = next(event for event in events if event["event_type"] == "entry_rejected")
    replacement_fill = next(event for event in events if event["event_type"] == "entry_fill")
    replacement_fill = json.loads(json.dumps(replacement_fill))
    replacement_fill["event_id"] = "dex-added-fill"
    replacement_fill["ts_utc"] = rejected_event["ts_utc"]
    replacement_fill["session_id"] = rejected_event["session_id"]
    replacement_fill["creator"] = rejected_event["creator"]
    replacement_fill["mint"] = rejected_event["mint"]
    replacement_fill["payload"]["attempt_index"] = rejected_event["payload"]["attempt_index"]

    events = [event for event in events if event["event_type"] != "entry_rejected"]
    events.append(replacement_fill)
    events_path.write_text("".join(json.dumps(event) + "\n" for event in events))

    result = validate_run_package(target)

    assert result["classification"] == "pass"
    assert "entry_rejected" in result["contract"]["waived_event_types"]
    assert "entry_rejected" not in result["coverage"]["missing_event_types"]


def test_validate_run_package_allows_mewx_missing_creator_candidate_when_snapshots_empty(
    tmp_path: Path,
) -> None:
    target = tmp_path / "mewx_fixture"
    shutil.copytree(MEWX_FIXTURE, target)

    _write_json(
        target / "exports" / "candidate_refresh_snapshot.json",
        {
            "captured_at_utc": "2026-03-21T01:00:00Z",
            "observations": [],
            "added_keys": [],
            "source_counts": {},
        },
    )

    events_path = target / "events.ndjson"
    events = [json.loads(line) for line in events_path.read_text().splitlines() if line.strip()]
    events = [event for event in events if event["event_type"] != "creator_candidate"]
    events_path.write_text("".join(json.dumps(event) + "\n" for event in events))

    result = validate_run_package(target)

    assert result["classification"] == "pass"
    assert "creator_candidate" in result["contract"]["waived_event_types"]
    assert "creator_candidate" not in result["contract"]["active_required_event_types"]


def test_validate_run_package_requires_mewx_creator_candidate_when_snapshots_non_empty(
    tmp_path: Path,
) -> None:
    target = tmp_path / "mewx_fixture"
    shutil.copytree(MEWX_FIXTURE, target)

    events_path = target / "events.ndjson"
    events = [json.loads(line) for line in events_path.read_text().splitlines() if line.strip()]
    events = [event for event in events if event["event_type"] != "creator_candidate"]
    events_path.write_text("".join(json.dumps(event) + "\n" for event in events))

    result = validate_run_package(target)

    assert result["classification"] == "partial"
    assert "creator_candidate" in result["contract"]["active_required_event_types"]
    assert "creator_candidate" in result["coverage"]["missing_event_types"]


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
            _write_json(
                package_dir / "exports" / f"{run_id}.state.json",
                {
                    "run_id": run_id,
                    "status": "completed",
                    "ended_at_utc": "2026-03-21T01:20:00Z",
                },
            )
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


def test_run_replay_validation_accepts_promoted_pack_and_keeps_residual_note(
    tmp_path: Path,
) -> None:
    promoted_dexter = tmp_path / "promoted-dexter"
    promoted_mewx = tmp_path / "promoted-mewx"
    confirmatory_dexter = tmp_path / "confirmatory-dexter"
    confirmatory_mewx = tmp_path / "confirmatory-mewx"

    _make_live_package(
        DEXTER_FIXTURE,
        promoted_dexter,
        run_id="dexter-promoted-live",
        started_at_utc="2026-03-25T18:02:11Z",
        ended_at_utc="2026-03-25T18:05:11Z",
    )
    _make_live_package(
        MEWX_FIXTURE,
        promoted_mewx,
        run_id="mewx-promoted-live",
        started_at_utc="2026-03-25T18:02:11Z",
        ended_at_utc="2026-03-25T18:05:11Z",
    )
    _make_live_package(
        DEXTER_FIXTURE,
        confirmatory_dexter,
        run_id="dexter-confirmatory-live",
        started_at_utc="2026-03-25T18:07:10Z",
        ended_at_utc="2026-03-25T18:10:10Z",
    )
    _make_live_package(
        MEWX_FIXTURE,
        confirmatory_mewx,
        run_id="mewx-confirmatory-live",
        started_at_utc="2026-03-25T18:07:10Z",
        ended_at_utc="2026-03-25T18:10:10Z",
    )
    _remove_event_type(confirmatory_mewx, "candidate_rejected")

    report, summary = run_replay_validation(
        promoted_dexter_package_dir=promoted_dexter,
        promoted_mewx_package_dir=promoted_mewx,
        promoted_output_dir=tmp_path / "promoted-results",
        confirmatory_dexter_package_dir=confirmatory_dexter,
        confirmatory_mewx_package_dir=confirmatory_mewx,
        confirmatory_output_dir=tmp_path / "confirmatory-results",
        promoted_summary_note="Promoted baseline.",
        confirmatory_summary_note="Confirmatory residual note.",
    )

    assert report["decision"]["key_finding"] == "replay_input_accepted"
    assert report["decision"]["task_state"] == "in_progress"
    assert report["promoted"]["accepted_as_replay_input"] is True
    assert report["promoted"]["comparison_pack"]["winner_mode"] == "derived"
    assert report["confirmatory"]["comparison_pack"]["winner_mode"] == "deferred"
    assert report["confirmatory"]["residual"]["mewx_missing_event_types"] == [
        "candidate_rejected"
    ]
    assert report["confirmatory"]["residual"]["narrow_note_only"] is True
    assert (tmp_path / "promoted-results" / "comparison_pack.json").exists()
    assert "Input accepted: `yes`" in summary


def test_run_replay_validation_blocks_when_promoted_pack_is_not_derived(
    tmp_path: Path,
) -> None:
    promoted_dexter = tmp_path / "promoted-dexter"
    promoted_mewx = tmp_path / "promoted-mewx"
    confirmatory_dexter = tmp_path / "confirmatory-dexter"
    confirmatory_mewx = tmp_path / "confirmatory-mewx"

    _make_live_package(
        DEXTER_FIXTURE,
        promoted_dexter,
        run_id="dexter-promoted-live",
        started_at_utc="2026-03-25T18:02:11Z",
        ended_at_utc="2026-03-25T18:05:11Z",
    )
    _make_live_package(
        MEWX_FIXTURE,
        promoted_mewx,
        run_id="mewx-promoted-live",
        started_at_utc="2026-03-25T18:02:12Z",
        ended_at_utc="2026-03-25T18:05:12Z",
    )
    _make_live_package(
        DEXTER_FIXTURE,
        confirmatory_dexter,
        run_id="dexter-confirmatory-live",
        started_at_utc="2026-03-25T18:07:10Z",
        ended_at_utc="2026-03-25T18:10:10Z",
    )
    _make_live_package(
        MEWX_FIXTURE,
        confirmatory_mewx,
        run_id="mewx-confirmatory-live",
        started_at_utc="2026-03-25T18:07:10Z",
        ended_at_utc="2026-03-25T18:10:10Z",
    )

    report, summary = run_replay_validation(
        promoted_dexter_package_dir=promoted_dexter,
        promoted_mewx_package_dir=promoted_mewx,
        promoted_output_dir=tmp_path / "promoted-results",
        confirmatory_dexter_package_dir=confirmatory_dexter,
        confirmatory_mewx_package_dir=confirmatory_mewx,
        confirmatory_output_dir=tmp_path / "confirmatory-results",
    )

    assert report["decision"]["key_finding"] == "replay_blocker_found"
    assert report["decision"]["task_state"] == "blocked"
    assert report["promoted"]["accepted_as_replay_input"] is False
    assert "TASK-006 state: `blocked`" in summary
