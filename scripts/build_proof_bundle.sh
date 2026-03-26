#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUNDLE_PATH="$ROOT_DIR/artifacts/bundles/task-007-monitor-killswitch-spec.tar.gz"
SAMPLE_PACK_DIR="$ROOT_DIR/artifacts/examples/task-004-sample-comparison"
export COPYFILE_DISABLE=1

mkdir -p "$ROOT_DIR/artifacts/bundles"
mkdir -p "$ROOT_DIR/artifacts/examples"
mkdir -p "$ROOT_DIR/artifacts/reports"
mkdir -p "$ROOT_DIR/artifacts/proofs"

rm -f "$BUNDLE_PATH"
rm -rf "$SAMPLE_PACK_DIR"

python "$ROOT_DIR/scripts/comparison_analysis.py" build-pack \
  --dexter-package "$ROOT_DIR/tests/fixtures/comparison_packages/dexter_fixture" \
  --mewx-package "$ROOT_DIR/tests/fixtures/comparison_packages/mewx_fixture" \
  --output-dir "$SAMPLE_PACK_DIR" \
  --summary-note "Fixture-based sample pack for TASK-004 scaffolding. Live Windows comparison remains pending." \
  --defer-winners

tar -czf "$BUNDLE_PATH" \
  --exclude='__pycache__' \
  --exclude='.pytest_cache' \
  --exclude='*.pyc' \
  --exclude='artifacts/proofs/task-005-live-pass-grade-attempt-results' \
  --exclude='artifacts/proofs/task-005-live-pass-grade-window-results' \
  --exclude='artifacts/reports/task-005-live-pass-grade-attempt-comparison' \
  --exclude='artifacts/reports/task-005-live-pass-grade-window-comparison' \
  -C "$ROOT_DIR" \
  README.md \
  docs \
  specs \
  ops \
  plans \
  config \
  templates \
  vexter \
  manifests \
  scripts \
  .github/workflows \
  tests \
  artifacts/context_pack.json \
  artifacts/summary.md \
  artifacts/proof_bundle_manifest.json \
  artifacts/task_ledger.jsonl \
  artifacts/reports \
  artifacts/proofs \
  artifacts/examples

printf '%s\n' "$BUNDLE_PATH"
