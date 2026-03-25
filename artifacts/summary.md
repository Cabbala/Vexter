# TASK-005-PASS-GRADE-PAIR Summary

## Verified Start

- `Cabbala/Vexter` `origin/main` was re-verified at `28c15b5c7655fe7647c12774494c80b83c58c04f` after merged PR `#15` on `2026-03-21`.
- `Cabbala/Dexter` `main` was re-verified at `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938` after merged PR `#3` on `2026-03-21`.
- Prior paper-revalidate promoted pair remained `task005-paper-revalidate-20260321T123011Z` with Dexter `9 / 12` and Mew-X `8 / 12`.
- Frozen Mew-X source stayed pinned at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## Execution

- Rechecked `win-lan`, verified PostgreSQL `17.9`, and confirmed the Windows Dexter checkout at `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938` plus frozen Mew-X at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.
- Fixed a Vexter-side packaging regression in `scripts/collect_comparison_package.ps1` so the Mew-X full-stream fallback no longer fails when exactly one copied `session_summary` export is present.
- Recollected two fresh same-attempt Dexter `paper_live` x Mew-X `sim_live` pairs:
  - `task005-pass-grade-pair-20260325T180027Z`
  - `task005-pass-grade-pair-20260325T180604Z`
- Reran `validate`, `derive-metrics`, and `build-pack` for both fresh pairs.

## Fresh Results

### Promoted pair: `task005-pass-grade-pair-20260325T180027Z`

- Exact event overlap: `162,941 ms`
- Dexter validation: `partial` with `10 / 12`
- Dexter now emitted: `candidate_rejected, creator_candidate, entry_attempt, entry_fill, entry_signal, exit_fill, exit_signal, mint_observed, position_closed, session_update`
- Dexter still missed: `entry_rejected, run_summary`
- Mew-X validation: `partial` with `9 / 12`
- Mew-X now emitted: `candidate_rejected, entry_attempt, entry_fill, entry_signal, exit_fill, exit_signal, mint_observed, position_closed, session_update`
- Mew-X still missed: `creator_candidate, entry_rejected, run_summary`
- Dexter startup wallet-balance `HTTP 429` count: `0`
- Dexter wsLogs `HTTP 429` count: `10`

### Confirmatory pair: `task005-pass-grade-pair-20260325T180604Z`

- Exact event overlap: `53,315 ms`
- Dexter validation: `partial` with `10 / 12`
- Mew-X validation: `partial` with `8 / 12`
- A longer `--grace-seconds 60` did not recover `run_summary` for either source.
- Dexter held the same missing-event pattern as the promoted pair; Mew-X regressed by losing `candidate_rejected`.

## Before / After

- Previous paper-revalidate promoted pair: Dexter `9 / 12` -> fresh pass-grade pair `10 / 12` on both retries.
- Previous paper-revalidate promoted pair: Mew-X `8 / 12` -> fresh promoted pass-grade pair `9 / 12`.
- The promoted pair is the strongest matched paper/sim evidence so far on merged PR `#15` main, but it still does not cross the validator's pass threshold.
- The best remaining gaps are now narrower and more specific than before: `run_summary` on both sources, `entry_rejected` on Dexter and Mew-X, and `creator_candidate` on Mew-X.

## Evidence-Based TASK-006 Readiness

- Decision: `BLOCKED`
- Reason 1: the promoted fresh pair still classifies as `partial` under the current contract at Dexter `10 / 12` and Mew-X `9 / 12`.
- Reason 2: `run_summary` stayed absent on both sources across both fresh attempts, even after the confirmatory retry extended graceful shutdown.
- Reason 3: Dexter still never emitted `entry_rejected`, while Mew-X still never emitted `creator_candidate` or `entry_rejected`.
- Reason 4: `comparison_pack` winner mode stayed `deferred` on both fresh pairs.
- Next state: `BLOCKED` until another approved TASK-005 follow-up can prove a true pass-grade matched pair or explain why the remaining frozen-source gaps are not collectible under the current contract.

## Key Paths

- Promoted comparison output:
  - `/Users/cabbala/Documents/worktrees/Vexter-task005-pass-grade-pair-20260326/artifacts/reports/task005-pass-grade-pair-20260325T180027Z-comparison`
- Confirmatory comparison output:
  - `/Users/cabbala/Documents/worktrees/Vexter-task005-pass-grade-pair-20260326/artifacts/reports/task005-pass-grade-pair-20260325T180604Z-comparison`
- Readiness proof:
  - `/Users/cabbala/Documents/worktrees/Vexter-task005-pass-grade-pair-20260326/artifacts/proofs/task-005-pass-grade-pair-check.json`
- Windows recovery proof:
  - `/Users/cabbala/Documents/worktrees/Vexter-task005-pass-grade-pair-20260326/artifacts/proofs/task-005-windows-runtime-recovery.json`
