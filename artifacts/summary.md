# TASK-005 Live Comparison Evidence Summary

## Status

- `TASK-005-live-comparison-evidence` remains blocked in `partial_live_comparison_blocker` state on branch `codex/task-005-resume-after-pr9` as of `2026-03-21T08:32:37Z`.
- Start conditions were re-verified from `Cabbala/Vexter` latest `main` commit `20d0eb3d7f6bda11c2526711145c0cd3298e4adf`; PR `#9` was confirmed merged on `2026-03-21`.
- Dexter and Mew-X strategy, execution, and instrumentation logic remain unchanged.
- Sub-agents `Wegener` and `Schrodinger` were launched for sidecar inspection while the main thread handled the collector fix, same-attempt repackaging, and artifact rebuild.
- A newer `resume-after-pr9-20260321T1726` Windows attempt was observed while this closeout was in progress, but `mew.exe` was still active and the completed raw pair on disk had weaker coverage than the latest completed same-attempt pair, so the promoted evidence set below uses `resume-after-pr8-20260321T0801`.

## Promoted Same-Attempt Result

- Vexter-side packaging was corrected without touching frozen source logic:
  - `scripts/collect_comparison_package.ps1` now copies time-bounded Mew-X `export/sessions/` artifacts into the run package
  - the repaired collector restores the `session_summary` export pointer in `run_metadata.json`
- Promoted same-attempt label: `resume-after-pr8-20260321T0801`
- Promoted matched measurement window:
  - concurrent runtime start: `2026-03-20T22:47:12.105Z`
  - concurrent runtime end: `2026-03-20T22:50:39.892066Z`
  - concurrent runtime duration: `207.787 s`
  - exact event overlap start: `2026-03-20T22:48:39.092958Z`
  - exact event overlap end: `2026-03-20T22:50:35.078Z`
  - exact event overlap duration: `115.985 s`
- Promoted package outputs:
  - Dexter package dir: `artifacts/tmp/winlan-packages-resume-after-pr8-20260321T0801/dexter-resume-after-pr8-20260321T0801`
  - Mew-X package dir: `artifacts/tmp/winlan-packages-resume-after-pr8-20260321T0801/mewx-resume-after-pr8-20260321T0801`
  - comparison output dir: `artifacts/reports/task-005-live-resume-after-pr8-20260321T0801-comparison`
  - comparison pack JSON: `artifacts/proofs/task-005-live-resume-after-pr8-20260321T0801-results/comparison-pack.json`
- Promoted validation coverage:
  - Dexter: `partial`, `4 / 12` required event types, `2384` total events
  - Mew-X: `partial`, `9 / 12` required event types, `44` total events
- `validate`, `derive-metrics`, and `build-pack` were rerun successfully on the promoted same-attempt pair.

## Comparison To Prior Fresh Pair

- Prior promoted same-attempt pair remained:
  - label: `resume-after-pr8-20260321T0743`
  - Dexter: `4 / 12` required event types
  - Mew-X: `8 / 12` required event types
  - Mew-X package was missing a `session_summary` export pointer
- Promoted `0801` pair versus `0743`:
  - Dexter stayed at `4 / 12`, but the same four observed event types were reproduced on a shorter, cleaner stream
  - Mew-X improved from `8 / 12` to `9 / 12`
  - Mew-X regained `candidate_rejected`
  - the `session_summary` export pointer gap is now fixed
  - winner / tie decisions still remain deferred because both packages still validate as `partial`

## Current Blocker

- `TASK-005` is no longer blocked by the Mew-X package export-pointer gap on the promoted same-attempt pair.
- `TASK-005` remains blocked on partial matched-pair coverage:
  - Dexter still lacks `candidate_rejected`, `entry_attempt`, `entry_fill`, `exit_fill`, `exit_signal`, `position_closed`, `run_summary`, and `session_update`
  - Mew-X still lacks `creator_candidate`, `entry_rejected`, and `run_summary`
- Winner / tie decisions remain deferred for candidate sourcing, execution quality, exit quality, and replayability.
- `TASK-006` remains blocked until a matched pair supports non-partial validation or otherwise yields evidence strong enough to move comparison areas out of the current deferred state.
