# DEXTER-PAPER-DESIGN Summary

## Status

- `DEXTER-PAPER-DESIGN` completed as a design-only follow-up from `Cabbala/Vexter` latest `origin/main` commit `0d4ff2eca834765f538db2dc1d798e664f786d2d` (PR `#11`, merged on `2026-03-21`).
- The `TASK-005` blocker assumption was re-confirmed as Dexter coverage stall under safe modes, not another repeated retry workflow problem.
- Dexter and Mew-X strategy, execution, and instrumentation logic were not changed during this task.
- Detached source worktrees were inspected at the Vexter-pinned commits:
  - Dexter: `69de8b6ca57ca3d03025d85329c88aa4a167da34`
  - Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Sub-agents `Banach` and `Godel` were launched for sidecar source inspection while the main thread verified the pinned commits, current Vexter evidence, and the design decision locally.

## Current Evidence Baseline

- Promoted same-attempt pair remains `resume-after-pr9-20260321T1737`.
- Promoted exact event overlap remains `167.174 s`, from `2026-03-21T08:39:09.961841Z` to `2026-03-21T08:41:57.136Z`.
- Dexter remains `partial` at `4 / 12` required event types.
- Mew-X remains `partial` at `8 / 12` required event types.
- Dexter still misses:
  - `candidate_rejected`
  - `entry_attempt`
  - `entry_fill`
  - `exit_fill`
  - `exit_signal`
  - `position_closed`
  - `run_summary`
  - `session_update`

## Source Findings

- Dexter does not already expose a formal paper or sim runtime mode.
- `VEXTER_MODE` in `sources/Dexter/DexLab/instrumentation.py` is metadata only; it does not change runtime execution behavior.
- Dexter does contain a lower send-layer simulation seam in `sources/Dexter/DexLab/pump_fun/pump_swap.py` via `pump_buy(..., sim=True)` and `pump_sell(..., sim=True)`.
- Dexter's live controller never uses that seam. `sources/Dexter/Dexter.py` hard-codes live send behavior and then waits for holder-balance or RPC transaction confirmation.
- Mew-X `MODE=sim` remains the correct paper/sim baseline because its frozen sim path already emits simulated `entry_attempt`, `entry_fill`, `session_update`, `exit_signal`, `exit_fill`, and `position_closed`.

## Minimum Slice Worth Doing

- The smallest safe Dexter paper-equivalent path is concentrated in:
  - `sources/Dexter/Dexter.py`
  - `sources/Dexter/DexLab/pump_fun/pump_swap.py`
  - `sources/Dexter/DexLab/instrumentation.py`
  - Dexter source tests
- The mode should keep candidate selection, trust-level projection, live market intake, and exit ladder semantics unchanged.
- The mode should replace only:
  - submission path
  - fill confirmation path
  - wallet and reserve accounting path
  - closeout reliability for `run_summary`
- No new normalized event classes are needed for the first implementation slice.

## Coverage Impact

- A minimal paper-equivalent path should realistically add:
  - `entry_attempt`
  - `entry_fill`
  - `session_update`
  - `exit_signal`
  - `exit_fill`
  - `position_closed`
- `run_summary` should also be recoverable if Dexter closeout is hardened.
- `candidate_rejected` remains conditional and should not be promised on every run.
- Expected Dexter improvement on eventful paper runs:
  - floor: `4 / 12` -> `10 / 12`
  - with reliable finalization: `4 / 12` -> `11 / 12`

## Comparability Limits

- A Dexter paper-equivalent path would make candidate conversion, signal timing, session evolution, exit logic, and replayability more comparable to Mew-X `sim`.
- It would still not make true execution quality, route behavior, real slippage, or transaction failure semantics comparable.
- `TASK-006` remains blocked until that safer paper-equivalent path is implemented and re-measured or until some other explicitly approved evidence path replaces it.

## Recommendation

- Recommendation: `IMPLEMENT`
- Next task ID: `DEXTER-PAPER-IMPLEMENT`
- Keep `TASK-006` blocked.
- Keep retry-only `TASK-005` work deferred unless the paper-equivalent path is explicitly rejected.

## Deliverables

- Design memo: `docs/dexter_paper_mode_design.md`
- Handoff prompt files:
  - `artifacts/reports/dexter-paper-design-handoff/DETAILS.md`
  - `artifacts/reports/dexter-paper-design-handoff/MIN_PROMPT.txt`
- Bundle target: `artifacts/bundles/dexter-paper-design.tar.gz`
