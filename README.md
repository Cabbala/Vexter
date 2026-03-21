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

`TASK-005-live-comparison-evidence` remains blocked on `codex/task-005-resume-after-pr9`. The promoted evidence was collected after re-verifying `origin/main` at `20d0eb3d7f6bda11c2526711145c0cd3298e4adf` (PR `#9`, merged on `2026-03-21`), and a closeout-only recheck on post-PR10 `origin/main` `5a352c5fa8773ca336eb593385f53f8ef2ffcb3c` confirmed the same promoted pair `resume-after-pr9-20260321T1737`, the preserved Mew-X `session_summary` pointer, the same partial blocker, and the deferred paper-mode design note only. Dexter still validates `4 / 12` and Mew-X validates `8 / 12`, so `TASK-006` remains blocked and winner/tie decisions stay deferred.

`DEXTER-PAPER-DESIGN` records the completed design-only follow-up from `origin/main` at `0d4ff2e160feecd4313f0d8ff95d2ff084c5a7ee` (PR `#11`, merged on `2026-03-21`). It treats the blocker as Dexter coverage stall rather than repeated retry mechanics and documents a source-faithful minimal paper-mode / paper-equivalent path in `docs/dexter_paper_mode_design.md`. The design conclusion is to implement that minimal Dexter paper-equivalent path next, while keeping Dexter and Mew-X strategy logic, execution decisions, and instrumentation contracts unchanged during this design task and keeping `TASK-006` blocked.

`DEXTER-PAPER-IMPLEMENT` is now complete on `Cabbala/Dexter` `main` at `5dc1036c499af5f14f06d08ad0fa96aa36228c96` (PR `#2`, merged on `2026-03-21`). Dexter keeps `observe_live` as the default, adds an explicit opt-in `paper_live` execution path for comparison-safe entry/session/exit coverage, and leaves strategy semantics, trust logic, entry/exit thresholds, and Mew-X unchanged. Vexter now pins Dexter `main` at that merged commit for future sync/bootstrap work.
