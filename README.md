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

`TASK-005-live-comparison-evidence` remained blocked on the pre-paper promoted pair `resume-after-pr9-20260321T1737`, collected before Dexter `paper_live` validation. That baseline still sits at Dexter `4 / 12` and Mew-X `8 / 12`, so `TASK-006` stayed blocked and winner/tie decisions remained deferred.

`DEXTER-PAPER-DESIGN` records the completed design-only follow-up from `origin/main` at `0d4ff2e160feecd4313f0d8ff95d2ff084c5a7ee` (PR `#11`, merged on `2026-03-21`). It treats the blocker as Dexter coverage stall rather than repeated retry mechanics and documents a source-faithful minimal paper-mode / paper-equivalent path in `docs/dexter_paper_mode_design.md`. The design conclusion is to implement that minimal Dexter paper-equivalent path next, while keeping Dexter and Mew-X strategy logic, execution decisions, and instrumentation contracts unchanged during this design task and keeping `TASK-006` blocked.

`DEXTER-PAPER-IMPLEMENT` is now complete on `Cabbala/Dexter` `main` at `5dc1036c499af5f14f06d08ad0fa96aa36228c96` (PR `#2`, merged on `2026-03-21`). Dexter keeps `observe_live` as the default, adds an explicit opt-in `paper_live` execution path for comparison-safe entry/session/exit coverage, and leaves strategy semantics, trust logic, entry/exit thresholds, and Mew-X unchanged. Vexter now pins Dexter `main` at that merged commit for future sync/bootstrap work.

`TASK-005-PAPER-VALIDATION` re-verified `Cabbala/Vexter` `origin/main` through merged PR `#12` (`4b32053697fc4efddd76e542b3d2a1411b450240`) and PR `#13` (`379f55a50dbfd91968ba643e2fbfe5e73fad8392`), then recollected fresh matched Dexter `paper_live` x Mew-X `sim_live` evidence on `win-lan`. Two fresh same-attempt pairs (`task005-paper-validation-20260321T1950` and `task005-paper-validation-20260321T2005`) were rebuilt end to end. Dexter regressed to `1 / 12` required event types on both retries, emitting only `creator_candidate` despite explicit `paper_live`; Mew-X validated `9 / 12` on the stronger pair and `8 / 12` on the confirmatory retry. The second retry removed Dexter main-runtime startup `HTTP 429` without improving Dexter coverage, so the sharper blocker is now paper-live session conversion rather than generic startup recovery. `TASK-006` remains blocked.
