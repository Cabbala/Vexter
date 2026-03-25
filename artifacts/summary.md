# TASK-005-GAP-AUDIT Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#16` merge commit `b71b5f744027024e2a04606f6c1aa369d0a6c3e3` on `2026-03-25`.
- The pass-grade pair evidence being audited was originally collected from PR `#15` base `28c15b5c7655fe7647c12774494c80b83c58c04f`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`.
- Frozen `Cabbala/Mew-X` stayed pinned at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.

## What This Audit Revalidated

- Re-ran `validate`, `derive-metrics`, and `build-pack` on the promoted pair `task005-pass-grade-pair-20260325T180027Z`.
- Re-ran `validate`, `derive-metrics`, and `build-pack` on the confirmatory pair `task005-pass-grade-pair-20260325T180604Z`.
- Audited current validator requirements against frozen Dexter and frozen Mew-X source code.
- Audited the copied full-stream collection payloads, source exports, and state exports to distinguish source non-emission from packaging loss.
- Did not perform more live recollection because the copied full-stream evidence plus source audit already closed the collectability question.

## Current Pair Results

### Promoted pair `task005-pass-grade-pair-20260325T180027Z`

- Dexter stayed `partial` at `10 / 12`; missing `entry_rejected`, `run_summary`.
- Mew-X stayed `partial` at `9 / 12`; missing `creator_candidate`, `entry_rejected`, `run_summary`.
- Exact raw overlap remained `162,941 ms`.
- The revalidated package was still built from `full_stream_fallback`, so the missing events are absent from the copied full raw stream, not only from window filtering.

### Confirmatory pair `task005-pass-grade-pair-20260325T180604Z`

- Dexter stayed `partial` at `10 / 12`; missing `entry_rejected`, `run_summary`.
- Mew-X stayed `partial` at `8 / 12`; missing `candidate_rejected`, `creator_candidate`, `entry_rejected`, `run_summary`.
- Exact raw overlap remained `53,315 ms`.
- Extending grace to `60` seconds still did not produce `run_summary`.

## Key Audit Findings

### `run_summary`

- Dexter emits `run_summary` only from `DexLab/instrumentation.py` finalizer.
- Mew-X emits `run_summary` only from `src/mew/instrumentation.rs` finalizer, reached on `ctrl_c`, normal end-of-main, or `Drop`.
- Both 2026-03-25 collection payloads show the current runner requested shutdown with `CTRL_BREAK_EVENT`, and both source processes exited with `3221225786` (`0xC000013A`).
- Both exported state files still showed `status: "running"` and `ended_at_utc: null`, which means the finalizer did not complete.
- Therefore `run_summary` is not collectible under the current matched-pair shutdown flow even though the validator requires it.

### `entry_rejected`

- Dexter emits `entry_rejected` only on buy failure paths such as missing bonding curve, insufficient balance, zero quote, creator vault unavailable, migration, price-too-high, or failed confirmation.
- Mew-X emits `entry_rejected` only when `buy_result.success` is false, recorded as `transport_send_failed`.
- The promoted pair still contained multiple successful fills on both sides with zero `entry_rejected`.
- Requiring `entry_rejected` from both sources in the same healthy matched pair means requiring at least one exceptional failed entry on each source, which is not normal pass-grade coverage.

### `creator_candidate` on Mew-X

- Mew-X emits `creator_candidate` only from `algo_choose_creators_report` output on initial selection or refresh additions.
- In both audited runs, the copied `candidates.initial_selection.json` and `candidates.refresh.json` exports had `observations: []` and `source_counts: {}`.
- The same full streams still produced `mint_observed`, `entry_fill`, `exit_fill`, and `position_closed`, which shows frozen Mew-X can produce rich comparable sessions through non-creator paths while never emitting `creator_candidate`.
- Under the current environment, `creator_candidate` is therefore not a dependable required event for a matched paper/sim pair.

## Decision

- Key finding: `structurally not collectible under current contract`
- Interpretation: with frozen Dexter `ddeb18c` and frozen Mew-X `dba3dc8`, the remaining gaps are not realistically collectible together as one pass-grade matched pair without depending on finalizer-specific shutdown behavior plus exceptional failure-path events.
- TASK-006 readiness: `blocked`
- Recommended next step: validator contract audit / rule exception review, or a frozen-source gap memo, instead of more same-shape recollection.

## Key Paths

- Audit report: `artifacts/reports/task-005-gap-audit.md`
- Readiness report: `artifacts/reports/task-005-gap-audit-readiness.md`
- Audit proof: `artifacts/proofs/task-005-gap-audit-check.json`
- Promoted pair revalidation: `artifacts/proofs/task005-gap-audit-20260325T180027Z-results`
- Confirmatory pair revalidation: `artifacts/proofs/task005-gap-audit-20260325T180604Z-results`
- Collection payload copies:
  - `artifacts/proofs/task005-gap-audit-20260325T180027Z.collection.json`
  - `artifacts/proofs/task005-gap-audit-20260325T180604Z.collection.json`
