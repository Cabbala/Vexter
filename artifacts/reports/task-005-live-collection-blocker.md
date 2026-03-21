# TASK-005 Live Collection Blocker

## Checked Scope

- checked at `2026-03-21T08:46:35Z`
- target host: `win-lan` (`DESKTOP-NNC6MPS`)
- fixed runtime root: `C:\Users\bot\quant\Vexter`
- verified latest start point: `origin/main` commit `20d0eb3d7f6bda11c2526711145c0cd3298e4adf`
- verified PR state: PR `#9` merged on `2026-03-21`
- required result: one fresh Dexter package and one fresh Mew-X package from the same attempt, followed by `validate`, `derive-metrics`, and `build-pack`

## What Advanced

- A fresh PR9 recollection was completed end-to-end without touching frozen Dexter or Mew-X logic.
- The Mew-X package export-pointer gap stays resolved on fresh PR9 runs:
  - `scripts/collect_comparison_package.ps1` preserves time-bounded `runtime\mewx\export\sessions\` files inside the package `exports/` bucket
  - the packaged `run_metadata.json` now restores the `session_summary` pointer for Mew-X on the promoted PR9 pair
- Two fresh PR9 same-attempt retries were collected:
  - `resume-after-pr9-20260321T1729` cleared Dexter startup 429 but over-serialized startup enough to lose exact event overlap
  - `resume-after-pr9-20260321T1737` restored exact overlap and was promoted through `validate`, `derive-metrics`, and `build-pack`

## Promoted Same-Attempt Outputs

- Promoted matched measurement window:
  - concurrent runtime start: `2026-03-21T08:39:25.571218Z`
  - concurrent runtime end: `2026-03-21T08:42:25.644005Z`
  - concurrent runtime duration: `180.073 s`
  - exact event overlap start: `2026-03-21T08:39:09.961841Z`
  - exact event overlap end: `2026-03-21T08:41:57.136Z`
  - exact event overlap duration: `167.174 s`
- Promoted package paths:
  - Dexter package dir: `artifacts/tmp/winlan-packages-resume-after-pr9-20260321T1737/dexter-resume-after-pr9-20260321T1737`
  - Mew-X package dir: `artifacts/tmp/winlan-packages-resume-after-pr9-20260321T1737/mewx-resume-after-pr9-20260321T1737`
  - Dexter validation JSON: `artifacts/proofs/task-005-live-resume-after-pr9-20260321T1737-results/dexter.validate.json`
  - Mew-X validation JSON: `artifacts/proofs/task-005-live-resume-after-pr9-20260321T1737-results/mewx.validate.json`
  - promoted comparison output dir: `artifacts/reports/task-005-live-resume-after-pr9-20260321T1737-comparison`
  - promoted comparison pack JSON: `artifacts/proofs/task-005-live-resume-after-pr9-20260321T1737-results/comparison-pack.json`
- Promoted validation results:
  - Dexter: `partial`, `4 / 12` required event types, `113868` total events
    - observed: `creator_candidate`, `entry_rejected`, `entry_signal`, `mint_observed`
  - Mew-X: `partial`, `8 / 12` required event types, `54` total events
    - observed: `entry_attempt`, `entry_fill`, `entry_signal`, `exit_fill`, `exit_signal`, `mint_observed`, `position_closed`, `session_update`
    - fixed: `session_summary` export pointer is now present in `run_metadata.json`

## Comparison To Prior Fresh Pair

- Prior same-attempt promotion remained:
  - label: `resume-after-pr8-20260321T0801`
  - Dexter validation: `partial`, `4 / 12`
  - Mew-X validation: `partial`, `9 / 12`
  - comparison output dir: `artifacts/reports/task-005-live-resume-after-pr8-20260321T0801-comparison`
- Discarded fresh PR9 retry:
  - label: `resume-after-pr9-20260321T1729`
  - exact event overlap: none; Dexter first raw event landed `24.242 s` after the Mew-X stream had already ended
  - note: startup serialization avoided wallet-balance HTTP 429, but the resulting pair was not comparable enough to promote
- Promoted `1737` pair versus `0801`:
  - Dexter coverage stayed flat at `4 / 12`
  - Mew-X regressed from `9 / 12` to `8 / 12`
  - exact event overlap improved from `115.985 s` to `167.174 s`
  - the `session_summary` export pointer remains present on the promoted PR9 pair
  - comparison winners / ties still remain deferred

## Current Blocker

- The task is no longer blocked by the Mew-X `session_summary` package pointer gap.
- The current blocker remains partial matched-pair coverage on the promoted same-attempt package:
  - Dexter still lacks `candidate_rejected`, `entry_attempt`, `entry_fill`, `exit_fill`, `exit_signal`, `position_closed`, `run_summary`, and `session_update`
  - Mew-X still lacks `candidate_rejected`, `creator_candidate`, `entry_rejected`, and `run_summary`
- The sharper blocker on fresh PR9 evidence is the safe-mode coverage ceiling:
  - Dexter `observe_live` on the zero-balance safety path still emitted no attempt/fill/exit/run-summary classes on the promoted retry
  - Mew-X `sim_live` still did not emit `creator_candidate`, `entry_rejected`, or `run_summary`, and `candidate_rejected` did not recur on the promoted retry
- Because the promoted pair remains partial, no comparison area becomes decisive enough to advance replay validation or TASK-006.

## Result

- latest promoted Dexter package: `artifacts/proofs/task-005-live-resume-after-pr9-20260321T1737-results/dexter.validate.json`
- latest promoted Mew-X package: `artifacts/proofs/task-005-live-resume-after-pr9-20260321T1737-results/mewx.validate.json`
- latest promoted comparison output: `artifacts/reports/task-005-live-resume-after-pr9-20260321T1737-comparison`
- winner / tie decisions: deferred
- blocker state: `partial_live_comparison_blocker`
- `TASK-006` readiness: `blocked`
