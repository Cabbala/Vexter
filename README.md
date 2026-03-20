# Vexter

Vexter is the Mac-side control plane for comparative analysis of `Cabbala/Dexter` and `Cabbala/Mew-X`. Git lives here; runtime, databases, logs, and replay data live on Windows via `ssh win-lan`.

## Fixed Environment Split

- Mac control plane: `/Users/cabbala/Projects/Vexter`
- Windows runtime host: `win-lan`
- Windows preferred root: `D:\Quant\Vexter`, with fallback to user space
- VPS: later-stage validation only

## Bootstrap Workflow

1. Run `./scripts/sync_reference_repos.sh` to clone or refresh the source repos into the local ignored `sources/` workspace.
2. Run `./scripts/bootstrap_windows_workspace.sh` from the Mac control plane to discover and prepare the Windows runtime/data layout.
3. Run `./scripts/build_proof_bundle.sh` to refresh the task proof artifact bundle.
4. Run `pytest -q` before Git operations.
5. Complete Git operations from the Mac control plane so GitHub remains the source of truth.

## Repository Layout

- `docs/`, `specs/`, `ops/`, `plans/`: fixed guidance imported from the bootstrap bundle
- `manifests/`: committed source repo and environment manifests
- `scripts/`: Mac-side bootstrap and proof automation
- `artifacts/`: context pack, summary, proof manifest, task ledger, and bundles
- `tests/`: bootstrap validation checks

## Current Task

This repo is now in `TASK-001-source-assessment`, which freezes the shared evaluation contract, source assessments, instrumentation plans, and Windows runtime layout needed before any bot integration work.
