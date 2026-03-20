#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUNDLE_PATH="$ROOT_DIR/artifacts/bundles/task-000-bootstrap.tar.gz"

rm -f "$BUNDLE_PATH"

tar -czf "$BUNDLE_PATH" \
  -C "$ROOT_DIR" \
  README.md \
  docs \
  specs \
  ops \
  plans \
  manifests \
  scripts \
  .github/workflows \
  tests \
  artifacts/context_pack.json \
  artifacts/summary.md \
  artifacts/proof_bundle_manifest.json \
  artifacts/task_ledger.jsonl

printf '%s\n' "$BUNDLE_PATH"
