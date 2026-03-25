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

`TASK-005-PAPER-REVALIDATE` re-verified `Cabbala/Vexter` `origin/main` at merged PR `#14` commit `3a720a64a5dbbda482513446b3bc47c341dde2ae` and `Cabbala/Dexter` `main` at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938` on `2026-03-21`. Two fresh same-attempt Dexter `paper_live` x Mew-X `sim_live` recollections (`task005-paper-revalidate-20260321T123011Z` and `task005-paper-revalidate-20260321T123426Z`) showed that Dexter is no longer stuck at creator-only coverage: both runs reached `mint_observed`, `entry_signal`, `entry_attempt`, `entry_fill`, `session_update`, `exit_signal`, `exit_fill`, and `position_closed`, lifting Dexter to `9 / 12`. Mew-X remained at `8 / 12` on both retries, and both comparison packs still validated only as `partial` because `candidate_rejected`, `entry_rejected`, and `run_summary` were still absent from the matched packages. The creator-only paper ceiling is resolved, but `TASK-006` remains blocked until a pass-grade matched pair is collected.

`TASK-005-PASS-GRADE-PAIR` re-verified `Cabbala/Vexter` `origin/main` at merged PR `#15` commit `28c15b5c7655fe7647c12774494c80b83c58c04f` and kept Dexter `main` pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938` with frozen Mew-X `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`. A Vexter-side packaging regression in `scripts/collect_comparison_package.ps1` was fixed so single copied Mew-X session exports no longer crash the full-stream fallback path, then two fresh same-attempt Dexter `paper_live` x Mew-X `sim_live` recollections (`task005-pass-grade-pair-20260325T180027Z` and `task005-pass-grade-pair-20260325T180604Z`) were rebuilt end to end. The promoted pair improved to Dexter `10 / 12` and Mew-X `9 / 12`, but both fresh pairs still validated only as `partial`: Dexter missed `entry_rejected` and `run_summary` on both retries, while Mew-X still missed `creator_candidate`, `entry_rejected`, and `run_summary` on the strongest pair. Even the extended-grace confirmatory retry did not recover `run_summary`, so winner mode stayed deferred and `TASK-006` remains blocked.

`TASK-005-GAP-AUDIT` re-verified latest GitHub-visible Vexter `main` at merged PR `#16` commit `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`, then revalidated the promoted and confirmatory pass-grade-pair packages against the current validator contract and the frozen Dexter / Mew-X sources. The audit closed in favor of a structural contract/source gap rather than a missing recollection recipe: `run_summary` is finalizer-only on both sources and the current matched-pair shutdown leaves both copied state exports in `running` state with no finalizer completion, `entry_rejected` is failure-path-only on both sources, and Mew-X `creator_candidate` depends on non-empty Deagle candidate reports even though both audited full-stream runs exported empty initial and refresh candidate snapshots. `TASK-006` therefore remains blocked, and the next logical step is validator contract audit / rule exception review rather than more same-shape recollection.

`TASK-005-VALIDATOR-CONTRACT-AUDIT` re-verified latest GitHub-visible Vexter `main` at merged PR `#18` commit `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, with supporting prior states PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df` and PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`. It confirmed that helper hardening alone is not a full unblock: `run_summary` sits on the shutdown-success boundary and may be helper-recoverable, but `entry_rejected` remains failure-path-only on both frozen sources and Mew-X `creator_candidate` remains conditional on non-empty candidate reports. The resulting outcome was `rule review needed`, so `TASK-006` stayed blocked and the approval-grade next step became a validator rule review / exception memo.

`TASK-005-VALIDATOR-RULE-REVIEW` rechecked the same GitHub-visible basis on `2026-03-26` without changing frozen source logic or validator rules. The resulting memo classifies `run_summary` as `shutdown_success_dependent`, `entry_rejected` as `failure_path_only`, and Mew-X `creator_candidate` as `source_specific_conditional`, then recommends proposal-level contract treatment for each: make `run_summary` conditional on clean shutdown completion or reserve it for replayability / integration evidence, make `entry_rejected` conditional on observed entry failures rather than healthy success paths, and make Mew-X `creator_candidate` conditional on non-empty candidate snapshots instead of a source-agnostic hard gate. The rule memo is now ready for approval, but `TASK-006` remains blocked until any approved validator rule implementation is actually applied.

`TASK-005-VALIDATOR-RULE-IMPLEMENT` re-verified latest GitHub-visible Vexter `main` at merged PR `#19` commit `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`, then applied the approved conditional validator treatments inside `vexter/comparison/validator.py` without changing Dexter or Mew-X source logic. The promoted pair `task005-pass-grade-pair-20260325T180027Z` reclassified to `pass/pass` with `winner_mode: derived`, while the confirmatory pair narrowed to a single Mew-X `candidate_rejected` residual. `TASK-006` therefore became ready for downstream replay validation.

`TASK-006-REPLAY-VALIDATION` re-verified latest GitHub-visible Vexter `main` at merged PR `#20` commit `6f2f50cc14dddfa52e6632db1dcbb98dbdb8a668` on `2026-03-25T19:47:52Z`, kept Dexter pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, and kept frozen Mew-X at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`. The promoted and confirmatory matched pairs were re-run through `validate`, `derive-metrics`, and `build-pack` on the current comparison layer. The promoted comparable pack remained `pass/pass` with `winner_mode: derived` and was accepted as downstream replay input, while the confirmatory pack stayed `pass/partial` with only a narrow Mew-X `candidate_rejected` residual. Both promoted replayability grades remained `partial`, so TASK-006 is now in progress rather than fully closed: the next step is replay deepening and live-versus-replay gap measurement, not another comparable-pack intake decision.
