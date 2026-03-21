# TASK-005-PAPER-REVALIDATE Summary

## Verified Start

- `Cabbala/Vexter` `origin/main` was re-verified at `3a720a64a5dbbda482513446b3bc47c341dde2ae` after merged PR `#14` on `2026-03-21`.
- `Cabbala/Dexter` `main` was re-verified at `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938` after merged PR `#3` on `2026-03-21`.
- Prior authoritative pre-paper baseline remained `resume-after-pr9-20260321T1737` with Dexter `4 / 12` and Mew-X `8 / 12`.
- Prior paper-validation ceiling remained `task005-paper-validation-20260321T1950` and `task005-paper-validation-20260321T2005`, where Dexter stayed at `1 / 12` despite `paper_live`.

## Execution

- Updated Vexter to pin Dexter `main` at `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938` in the sync script, Windows recovery script, and pinned-source manifests.
- Recovered `win-lan`, verified PostgreSQL `17.9`, and confirmed the Windows Dexter checkout at `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938` plus frozen Mew-X at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.
- Recollected two fresh same-attempt Dexter `paper_live` x Mew-X `sim_live` pairs:
  - `task005-paper-revalidate-20260321T123011Z`
  - `task005-paper-revalidate-20260321T123426Z`
- Reran `validate`, `derive-metrics`, and `build-pack` for both fresh pairs.

## Fresh Results

### Promoted pair: `task005-paper-revalidate-20260321T123011Z`

- Exact event overlap: `117,795 ms`
- Dexter validation: `partial` with `9 / 12`
- Dexter now emitted: `creator_candidate, entry_attempt, entry_fill, entry_signal, exit_fill, exit_signal, mint_observed, position_closed, session_update`
- Dexter still missed: `candidate_rejected, entry_rejected, run_summary`
- Mew-X validation: `partial` with `8 / 12`
- Mew-X still missed: `candidate_rejected, creator_candidate, entry_rejected, run_summary`
- Dexter startup `HTTP 429` count: `1`
- Dexter wsLogs `HTTP 429` count: `0`

### Confirmatory pair: `task005-paper-revalidate-20260321T123426Z`

- Exact event overlap: `108,930 ms`
- Dexter validation: `partial` with `9 / 12`
- Mew-X validation: `partial` with `8 / 12`
- Dexter again reached mint, entry, session, exit, and closeout coverage instead of stopping at creator-only.
- Missing event types stayed the same as the promoted pair, so the confirmatory retry reinforced the improvement but did not reach pass-grade coverage.

## Before / After

- Previous paper-validation ceiling: Dexter `1 / 12` -> fresh revalidation `9 / 12` on both retries.
- Previous authoritative pre-paper baseline: Dexter `4 / 12` -> fresh revalidation `9 / 12` on the promoted pair.
- Mew-X stayed `8 / 12` on both fresh revalidations, so the matched pair still did not cross the validator's pass threshold.
- The creator-only Dexter paper ceiling is resolved, but the validation contract is still not fully satisfied.

## Evidence-Based TASK-006 Readiness

- Decision: `BLOCKED`
- Reason 1: Dexter improved materially beyond the prior paper ceiling, but both source packages still classify as `partial` under the current contract.
- Reason 2: `candidate_rejected`, `entry_rejected`, and `run_summary` remained absent for Dexter; `candidate_rejected`, `creator_candidate`, `entry_rejected`, and `run_summary` remained absent for Mew-X.
- Reason 3: `comparison_pack` winner mode stayed `deferred` on both fresh pairs.
- Next TASK-005 follow-up: `TASK-005-PASS-GRADE-PAIR` to collect a pass-grade matched paper/sim pair without changing source logic or comparison rules.

## Key Paths

- Promoted comparison output:
  - `/Users/cabbala/Documents/worktrees/Vexter-task005-paper-revalidate/artifacts/reports/task005-paper-revalidate-20260321T123011Z-comparison`
- Confirmatory comparison output:
  - `/Users/cabbala/Documents/worktrees/Vexter-task005-paper-revalidate/artifacts/reports/task005-paper-revalidate-20260321T123426Z-comparison`
- Readiness proof:
  - `/Users/cabbala/Documents/worktrees/Vexter-task005-paper-revalidate/artifacts/proofs/task-005-paper-revalidate-check.json`
- Windows recovery proof:
  - `/Users/cabbala/Documents/worktrees/Vexter-task005-paper-revalidate/artifacts/proofs/task-005-windows-runtime-recovery.json`
