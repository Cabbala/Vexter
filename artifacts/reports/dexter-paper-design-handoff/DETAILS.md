# Dexter Paper-Implement Handoff

## Send this to

- `Vexter` new Codex thread
- mode: `Worktree`
- base branch: `main`

## Why this is the next task

`DEXTER-PAPER-DESIGN` on `Cabbala/Vexter` latest `main` (`0d4ff2e160feecd4313f0d8ff95d2ff084c5a7ee`, PR `#11`) confirmed that:

- repeated `TASK-005` retries are no longer the primary issue
- the promoted same-attempt pair `resume-after-pr9-20260321T1737` still leaves Dexter stalled at `4 / 12`
- Dexter does not have a formal paper mode today
- Dexter does already contain a lower transaction-layer simulation seam
- the smallest worthwhile follow-up is to implement a minimal Dexter paper-equivalent path before any more blind retry-only work

## Hard scope

Implement only the minimal Dexter paper-mode / paper-equivalent path defined in `docs/dexter_paper_mode_design.md`.

- keep Dexter strategy thresholds unchanged
- keep creator scoring unchanged
- keep exit ladder semantics unchanged
- keep Mew-X unchanged
- keep Vexter validator rules unchanged for the first slice
- do not start `TASK-006`

## Required read order

1. `README.md`
2. `artifacts/summary.md`
3. `docs/dexter_paper_mode_design.md`
4. `manifests/reference_repos.json`
5. `docs/dexter_source_assessment.md`
6. `docs/dexter_event_mapping.md`
7. `docs/mewx_source_assessment.md`
8. `docs/mewx_event_mapping.md`

## Required implementation constraints

- implement against the Vexter-pinned Dexter source commit lineage, not upstream Dexter `main`
- add an explicit opt-in Dexter paper execution mode
- never send live buy or sell transactions in that mode
- never depend on `get_swap_tx()` for paper confirmation
- keep default behavior on `observe_live`
- reuse the existing normalized event contract before proposing new event types

## Minimum file touch set

- `sources/Dexter/Dexter.py`
- `sources/Dexter/DexLab/pump_fun/pump_swap.py`
- `sources/Dexter/DexLab/instrumentation.py`
- Dexter source tests

## Proof expectations

- same-window safe paper run should add:
  - `entry_attempt`
  - `entry_fill`
  - `session_update`
  - `exit_signal`
  - `exit_fill`
  - `position_closed`
- `run_summary` should become reliable if closeout is hardened
- paper runs must stamp `mode=paper_live`
- paper runs must remain safe and non-funded

## Completion format

Return only:

- STATUS: PASS/FAIL
- PR: <number or NONE>
- BRANCH: <branch>
- COMMIT: <sha>
- RESULT: IMPLEMENTED or FAILED
- HANDOFF_TARBALL: <path or NONE>
- NEXT_TASK_ID: TASK-005-RESUME or TASK-006-BLOCKED
