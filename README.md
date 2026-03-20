# Vexter

Vexter is the Mac-side control plane for comparative analysis of `Cabbala/Dexter` and `Cabbala/Mew-X`. Git lives here; runtime, databases, logs, and replay data live on Windows via `ssh win-lan`.

## Fixed Environment Split

- Mac control plane: `/Users/cabbala/Projects/Vexter`
- Windows runtime host: `win-lan`
- Windows preferred root: `D:\Quant\Vexter`, with fallback to user space
- VPS: later-stage validation only

## Bootstrap Workflow

1. Run `./scripts/sync_reference_repos.sh` to clone or refresh the frozen Dexter and Mew-X branches into the local ignored `sources/` workspace.
2. Run `./scripts/bootstrap_windows_workspace.sh` from the Mac control plane to discover and prepare the Windows runtime/data layout.
3. Run `./scripts/recover_windows_runtime.sh` to restore PostgreSQL, detached frozen source checkouts, and the Dexter Python runtime on `win-lan`.
4. Run `./scripts/build_proof_bundle.sh` to refresh the task proof artifact bundle.
5. Run `pytest -q` before Git operations.
6. Complete Git operations from the Mac control plane so GitHub remains the source of truth, including branch, commit, push, and PR create/update.

## Operating Rules

- Every Codex task must leave GitHub in a state where ChatGPT can inspect the latest result directly. The minimum closeout path is branch, commit, push, and PR create/update.
- If agent or sub-agent capabilities are available and improve repo audit, environment verification, or implementation accuracy, Codex should use them proactively. If they are unavailable in the current session, proceed normally and record that limitation in artifacts.

## Repository Layout

- `docs/`, `specs/`, `ops/`, `plans/`: fixed guidance imported from the bootstrap bundle
- `manifests/`: committed source repo and environment manifests
- `scripts/`: Mac-side bootstrap and proof automation
- `artifacts/`: context pack, summary, proof manifest, task ledger, and bundles
- `tests/`: bootstrap validation checks

## Current Task

`TASK-001-source-assessment` is complete on `main`. The shared evaluation contract, source assessments, instrumentation plans, and Windows runtime layout are now the source of truth for Vexter.

`TASK-002-dexter-instrumentation` is complete on `main` as of 2026-03-21. The paired Dexter source branch adds observational NDJSON events, masked config export, leaderboard snapshots, and stagnant-mint replay exports without changing strategy logic.

`TASK-003-mewx-instrumentation` is complete on `main` after merging PR #3 on 2026-03-21. The paired Mew-X source branch adds observational NDJSON events, masked config export, candidate refresh snapshots, and session summaries without changing strategy or execution decisions.

`TASK-004-comparison-analysis` adds the first Vexter-side validator, shared metrics derivation layer, side-by-side comparison pack builder, and Windows collection runbook while keeping Dexter and Mew-X instrumentation frozen.

`TASK-005-live-comparison-evidence` is now in `partial_live_comparison_blocker` state on `main` after PR #5. `win-lan` remains recovered to the fixed Windows root, PostgreSQL listener, detached frozen source checkouts, Dexter Python runtime, and Mew-X protobuf build prerequisites. The exact signer / RPC env blocker is resolved, live smoke packages now exist for both Dexter and Mew-X, and `validate`, `derive-metrics`, and `build-pack` complete end-to-end on the Mac control plane. The remaining blocker is evidence quality rather than startup failure: the current smoke packages were not collected from the same live measurement window and both still validate as `partial`, so winner / tie decisions stay deferred and `TASK-006` remains blocked until a matched comparable live window is collected.
