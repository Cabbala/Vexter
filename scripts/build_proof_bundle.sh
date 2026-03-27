#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUNDLE_PATH="$ROOT_DIR/artifacts/bundles/demo-forward-supervised-run.tar.gz"
export COPYFILE_DISABLE=1

mkdir -p "$ROOT_DIR/artifacts/bundles"
mkdir -p "$ROOT_DIR/artifacts/examples"
mkdir -p "$ROOT_DIR/artifacts/reports"
mkdir -p "$ROOT_DIR/artifacts/proofs"

rm -f "$BUNDLE_PATH"

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
  pytest.ini \
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
