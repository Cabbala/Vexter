#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_PATH="${1:-/Users/cabbala/Downloads/vexter_attestation_refresh_bundle_latest.tar.gz}"
BUNDLE_DIR_NAME="vexter_attestation_refresh_bundle_latest"
export COPYFILE_DISABLE=1

PROOF_BUNDLE_PATH="$("$ROOT_DIR/scripts/build_proof_bundle.sh")"

WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

OUT_DIR="$WORK_DIR/$BUNDLE_DIR_NAME"
mkdir -p "$OUT_DIR"

ROOT_DIR="$ROOT_DIR" \
OUT_DIR="$OUT_DIR" \
PROOF_BUNDLE_PATH="$PROOF_BUNDLE_PATH" \
RESULT_BRANCH="${RESULT_BRANCH:-$(git -C "$ROOT_DIR" branch --show-current)}" \
RESULT_COMMIT_SHA="${RESULT_COMMIT_SHA:-$(git -C "$ROOT_DIR" rev-parse HEAD)}" \
RESULT_PR_URL="${RESULT_PR_URL:-TBD}" \
RESULT_MERGE_COMMIT_SHA="${RESULT_MERGE_COMMIT_SHA:-TBD}" \
RESULT_MERGED_AT="${RESULT_MERGED_AT:-TBD}" \
RESULT_TEST_COMMAND="${RESULT_TEST_COMMAND:-python3.12 -m pytest -q}" \
RESULT_TEST_RESULT="${RESULT_TEST_RESULT:-TBD}" \
RESULT_OUTCOME="${RESULT_OUTCOME:-}" \
RESULT_CURRENT_RECOMMENDED_STEP="${RESULT_CURRENT_RECOMMENDED_STEP:-}" \
RESULT_PASS_SUCCESSOR="${RESULT_PASS_SUCCESSOR:-}" \
ANSCOMBE_SUMMARY="${ANSCOMBE_SUMMARY:-}" \
EULER_SUMMARY="${EULER_SUMMARY:-}" \
PARFIT_SUMMARY="${PARFIT_SUMMARY:-}" \
python3 - <<'PY'
import json
import os
import shutil
from pathlib import Path

root = Path(os.environ["ROOT_DIR"])
out_dir = Path(os.environ["OUT_DIR"])
proof_bundle_path = Path(os.environ["PROOF_BUNDLE_PATH"])

proof = json.loads(
    (root / "artifacts/proofs/demo-forward-supervised-run-retry-gate-attestation-refresh-check.json").read_text()
)
manifest = json.loads((root / "artifacts/proof_bundle_manifest.json").read_text())
preflight = json.loads(
    (root / "artifacts/proofs/demo-forward-supervised-run-retry-gate-evidence-preflight-check.json").read_text()
)

handoff_src = (
    root / "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/HANDOFF.md"
)
subagent_src = (
    root
    / "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/subagent_summary.md"
)
external_contract_src = (
    root / "specs/DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_EXTERNAL_EVIDENCE_CONTRACT.md"
)
external_manifest_src = (
    root / "manifests/demo_forward_supervised_run_retry_gate_external_evidence_manifest.json"
)
external_preflight_report_src = (
    root / "artifacts/reports/demo-forward-supervised-run-retry-gate-evidence-preflight-report.md"
)
external_preflight_proof_src = (
    root / "artifacts/proofs/demo-forward-supervised-run-retry-gate-evidence-preflight-check.json"
)
external_preflight_summary_src = (
    root / "artifacts/proofs/demo-forward-supervised-run-retry-gate-evidence-preflight-summary.md"
)
external_gap_report_src = (
    root / "artifacts/reports/demo-forward-supervised-run-retry-gate-external-evidence-gap-report.md"
)
external_gap_proof_src = (
    root / "artifacts/proofs/demo-forward-supervised-run-retry-gate-external-evidence-gap-check.json"
)
external_gap_summary_src = (
    root / "artifacts/proofs/demo-forward-supervised-run-retry-gate-external-evidence-gap-summary.md"
)

outcome = os.environ["RESULT_OUTCOME"] or proof["task_result"]["outcome"]
recommended_next_step = (
    os.environ["RESULT_CURRENT_RECOMMENDED_STEP"] or proof["task_result"]["recommended_next_step"]
)
pass_successor = os.environ["RESULT_PASS_SUCCESSOR"] or proof["task_result"]["gate_pass_successor"]
readiness = preflight["reopen_readiness"]
next_human_pass = readiness["next_human_pass"]

result_text = "\n".join(
    [
        "# ATTESTATION-REFRESH Result",
        "",
        f"- Result: {outcome}",
        f"- Validation: `{os.environ['RESULT_TEST_COMMAND']}` -> {os.environ['RESULT_TEST_RESULT']}",
        f"- PR: {os.environ['RESULT_PR_URL']}",
        f"- Branch: `{os.environ['RESULT_BRANCH']}`",
        f"- Final pushed commit: `{os.environ['RESULT_COMMIT_SHA']}`",
        f"- Merge commit: `{os.environ['RESULT_MERGE_COMMIT_SHA']}`",
        f"- Merged at: `{os.environ['RESULT_MERGED_AT']}`",
        f"- Current recommended step: `{recommended_next_step}`",
        f"- Gate-pass successor: `{pass_successor}`",
        "- Next human pass: `NEXT_HUMAN_PASS.md`",
    ]
) + "\n"

next_human_pass_lines = [
    "# ATTESTATION-REFRESH Next Human Pass",
    "",
    f"- Reopen false-path: {readiness['template_only_false_path']}",
    f"- Canonical preflight report: `{external_preflight_report_src.name}`",
    f"- Canonical preflight proof: `{external_preflight_proof_src.name}`",
    f"- Compatibility gap report: `{external_gap_report_src.name}`",
    "",
    "## Checklist",
    f"- Keep manifest_role at template: {next_human_pass['hold_manifest_role_until_ready']}",
    f"- Fill bounded-window fields once: `{', '.join(next_human_pass['bounded_window_fields_once'])}`",
]
for face in next_human_pass["faces"]:
    blocker_groups = "; ".join(
        f"{group}={', '.join(reasons)}" for group, reasons in face["blocked_reason_groups"].items()
    )
    next_human_pass_lines.append(
        "- "
        f"`{face['face']}` -> fill `{', '.join(face['manifest_fields_to_fill'])}`; "
        f"blockers `{blocker_groups or 'none'}`; operator input: {face['operator_input_needed']}"
    )
next_human_pass_lines.extend(
    [
        "",
        "## Rerun Order",
        *[f"- `{command}`" for command in next_human_pass["rerun_sequence"]],
        f"- Optional legacy compatibility rerun: `{next_human_pass['legacy_compatibility_command']}`",
        "",
        "## Consistency Checks",
        *[
            f"- `{name}`: `{str(value).lower()}`"
            for name, value in readiness["consistency_checks"].items()
        ],
        "",
    ]
)
next_human_pass_text = "\n".join(next_human_pass_lines)

named_summaries = {
    "Anscombe": os.environ["ANSCOMBE_SUMMARY"].strip(),
    "Euler": os.environ["EULER_SUMMARY"].strip(),
    "Parfit": os.environ["PARFIT_SUMMARY"].strip(),
}

if all(named_summaries.values()):
    lines = ["# ATTESTATION-REFRESH Sub-agent Summaries", ""]
    for name, summary in named_summaries.items():
        lines.append(f"## {name}")
        lines.append(f"- {summary}")
        lines.append("")
    subagent_text = "\n".join(lines).rstrip() + "\n"
else:
    subagent_text = subagent_src.read_text()

shutil.copy2(handoff_src, out_dir / "HANDOFF.md")
shutil.copy2(proof_bundle_path, out_dir / proof_bundle_path.name)
shutil.copy2(external_contract_src, out_dir / external_contract_src.name)
shutil.copy2(external_manifest_src, out_dir / external_manifest_src.name)
shutil.copy2(external_preflight_report_src, out_dir / external_preflight_report_src.name)
shutil.copy2(external_preflight_proof_src, out_dir / external_preflight_proof_src.name)
shutil.copy2(external_preflight_summary_src, out_dir / external_preflight_summary_src.name)
shutil.copy2(external_gap_report_src, out_dir / external_gap_report_src.name)
shutil.copy2(external_gap_proof_src, out_dir / external_gap_proof_src.name)
shutil.copy2(external_gap_summary_src, out_dir / external_gap_summary_src.name)
(out_dir / "RESULT.md").write_text(result_text)
(out_dir / "NEXT_HUMAN_PASS.md").write_text(next_human_pass_text)
(out_dir / "subagent_summary.md").write_text(subagent_text)

(out_dir / "manifest.json").write_text(
    json.dumps(
        {
            "task_id": manifest["task_id"],
            "status": manifest["status"],
            "bundle_path": manifest["bundle_path"],
            "bundle_source": manifest.get("bundle_source"),
            "proof_bundle": proof_bundle_path.name,
            "external_evidence_contract": external_contract_src.name,
            "external_evidence_template": external_manifest_src.name,
            "external_evidence_preflight_report": external_preflight_report_src.name,
            "external_evidence_preflight_proof": external_preflight_proof_src.name,
            "external_evidence_preflight_summary": external_preflight_summary_src.name,
            "external_evidence_gap_report": external_gap_report_src.name,
            "external_evidence_gap_proof": external_gap_proof_src.name,
            "external_evidence_gap_summary": external_gap_summary_src.name,
            "next_human_pass": "NEXT_HUMAN_PASS.md",
            "template_only_false_path": readiness["template_only_false_path"],
            "consistency_checks": readiness["consistency_checks"],
        },
        indent=2,
        sort_keys=False,
    )
    + "\n"
)
PY

mkdir -p "$(dirname "$OUTPUT_PATH")"
rm -f "$OUTPUT_PATH"
tar -czf "$OUTPUT_PATH" -C "$WORK_DIR" "$BUNDLE_DIR_NAME"
printf '%s\n' "$OUTPUT_PATH"
