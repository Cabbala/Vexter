# TASK-005-PAPER-VALIDATION Summary

## Verified Start

- `Cabbala/Vexter` `origin/main` was re-verified at `379f55a50dbfd91968ba643e2fbfe5e73fad8392` on 2026-03-21 after merged PR `#12` (`4b32053697fc4efddd76e542b3d2a1411b450240`) and PR `#13` (`379f55a50dbfd91968ba643e2fbfe5e73fad8392`).
- `Cabbala/Dexter` `main` was re-verified at `5dc1036c499af5f14f06d08ad0fa96aa36228c96` on 2026-03-21 after merged PR `#2`, confirming the explicit opt-in `paper_live` path.
- Prior authoritative TASK-005 baseline remained `resume-after-pr9-20260321T1737` with Dexter `4 / 12` required event types and Mew-X `8 / 12`.

## Execution

- Updated Vexter's TASK-005 helper flow so the matched-pair collector can request Dexter `paper_live`, package `paper_live` runs, and load pinned source SHAs from `manifests/reference_repos.json`.
- Recovered `win-lan` with Dexter pinned to merged `main` `5dc1036c499af5f14f06d08ad0fa96aa36228c96` and Mew-X pinned to `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.
- Recollected two fresh same-attempt paper/sim pairs:
  - `task005-paper-validation-20260321T1950`
  - `task005-paper-validation-20260321T2005`
- Rebuilt `validate`, `derive-metrics`, and `build-pack` outputs for both fresh pairs.

## Fresh Results

### Strongest fresh pair: `task005-paper-validation-20260321T1950`

- Dexter mode: `paper_live`
- Mew-X mode: `sim_live`
- Exact event overlap: `141 ms`
- Dexter coverage: `1 / 12`
- Mew-X coverage: `9 / 12`
- Dexter observed only: `creator_candidate`
- Dexter still missed:
  - `candidate_rejected`
  - `mint_observed`
  - `entry_signal`
  - `entry_attempt`
  - `entry_fill`
  - `entry_rejected`
  - `session_update`
  - `exit_signal`
  - `exit_fill`
  - `position_closed`
  - `run_summary`
- Mew-X improved versus the prior `8 / 12` baseline and now emitted:
  - `candidate_rejected`
  - `mint_observed`
  - `entry_signal`
  - `entry_attempt`
  - `entry_fill`
  - `session_update`
  - `exit_signal`
  - `exit_fill`
  - `position_closed`
- Sharp note: Dexter still logged a startup websocket `HTTP 429` in stderr on this retry.

### Confirmatory retry: `task005-paper-validation-20260321T2005`

- Exact event overlap: `137 ms`
- Dexter coverage: `1 / 12`
- Mew-X coverage: `8 / 12`
- Extra startup serialization removed Dexter main-runtime `HTTP 429`, but Dexter still emitted only `creator_candidate`.
- This confirms the poor Dexter paper result was not just a main-runtime startup-429 artifact.

## Before / After

- Prior authoritative baseline: Dexter `4 / 12`, Mew-X `8 / 12`
- Fresh strongest paper/sim pair: Dexter `1 / 12`, Mew-X `9 / 12`
- Net change:
  - Dexter regressed by `3` required event types
  - Mew-X improved by `1` required event type
- `run_summary` did not appear on either fresh pair.
- No comparison area became non-deferred; winner/tie decisions remain blocked.

## Sharpest Remaining Blocker

- Dexter `paper_live` did not progress into mint/session/exit coverage on either fresh same-attempt recollection. The new ceiling observed in these retries was still creator-only coverage, not the expected paper-path entry/session/exit trail.
- Both fresh pairs required full-stream fallback because the first raw events landed before the post-readiness measurement window, which left only subsecond exact overlap.
- `TASK-006` is still blocked.

## Key Paths

- Strongest fresh Dexter package:
  - `/Users/cabbala/Documents/worktrees/Vexter-task005-paper-validation/artifacts/tmp/winlan-packages-task005-paper-validation-20260321T1950/dexter-task005-paper-validation-20260321T1950`
- Strongest fresh Mew-X package:
  - `/Users/cabbala/Documents/worktrees/Vexter-task005-paper-validation/artifacts/tmp/winlan-packages-task005-paper-validation-20260321T1950/mewx-task005-paper-validation-20260321T1950`
- Strongest fresh comparison output:
  - `/Users/cabbala/Documents/worktrees/Vexter-task005-paper-validation/artifacts/reports/task-005-paper-validation-20260321T1950-comparison`
- Confirmatory comparison output:
  - `/Users/cabbala/Documents/worktrees/Vexter-task005-paper-validation/artifacts/reports/task-005-paper-validation-20260321T2005-comparison`
