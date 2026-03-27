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

handoff_src = (
    root / "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/HANDOFF.md"
)
subagent_src = (
    root
    / "artifacts/reports/demo-forward-supervised-run-retry-gate-attestation-refresh/subagent_summary.md"
)

outcome = os.environ["RESULT_OUTCOME"] or proof["task_result"]["outcome"]
recommended_next_step = (
    os.environ["RESULT_CURRENT_RECOMMENDED_STEP"] or proof["task_result"]["recommended_next_step"]
)
pass_successor = os.environ["RESULT_PASS_SUCCESSOR"] or proof["task_result"]["gate_pass_successor"]

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
    ]
) + "\n"

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
(out_dir / "RESULT.md").write_text(result_text)
(out_dir / "subagent_summary.md").write_text(subagent_text)

(out_dir / "manifest.json").write_text(
    json.dumps(
        {
            "task_id": manifest["task_id"],
            "status": manifest["status"],
            "bundle_path": manifest["bundle_path"],
            "bundle_source": manifest.get("bundle_source"),
            "proof_bundle": proof_bundle_path.name,
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
