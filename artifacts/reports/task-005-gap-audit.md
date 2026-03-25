# TASK-005-GAP-AUDIT

## Scope

This audit answered one narrow question on top of latest GitHub-visible Vexter `main`: are the remaining TASK-005 missing events still collectible under frozen Dexter `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, frozen Mew-X `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, and the current validator contract, or does a structural gap remain?

The audit kept source logic and comparison rules unchanged. It revalidated the strongest two previously collected matched pairs and then compared the validator requirements against source-side emission conditions and copied full-stream evidence.

## Revalidated Inputs

### Promoted pair

- Label: `task005-pass-grade-pair-20260325T180027Z`
- Dexter validation: `10 / 12`, `partial`
- Mew-X validation: `9 / 12`, `partial`
- Full-stream fallback used: `yes`
- Missing events:
  - Dexter: `entry_rejected`, `run_summary`
  - Mew-X: `creator_candidate`, `entry_rejected`, `run_summary`

### Confirmatory pair

- Label: `task005-pass-grade-pair-20260325T180604Z`
- Dexter validation: `10 / 12`, `partial`
- Mew-X validation: `8 / 12`, `partial`
- Full-stream fallback used: `yes`
- Extended grace: `60` seconds
- Missing events:
  - Dexter: `entry_rejected`, `run_summary`
  - Mew-X: `candidate_rejected`, `creator_candidate`, `entry_rejected`, `run_summary`

## Evidence

### `run_summary` is finalizer-only and the current matched-pair shutdown path misses it

Dexter only emits `run_summary` in `DexLab/instrumentation.py` `finalize()`. Mew-X only emits `run_summary` in `src/mew/instrumentation.rs` `finalize()`, reached from `ctrl_c`, normal end-of-main, or `Drop`.

The current Windows matched-pair helper requests shutdown with `CTRL_BREAK_EVENT`, then waits for a grace deadline before killing anything that remains. In both copied collection payloads:

- `process_results` show Dexter and Mew-X exiting with `3221225786` (`0xC000013A`)
- the copied `*.state.json` exports still show `status: "running"`
- `ended_at_utc` stays `null`
- the copied full raw streams still lack `run_summary`

That combination means the raw stream itself ended before source finalization completed. This is not a packaging loss.

### `entry_rejected` is a failure-path event on both frozen sources

Dexter records `entry_rejected` only when a buy path fails: missing bonding curve, insufficient balance, zero quote, creator vault unavailable, migration, price-too-high, or failed confirmation.

Mew-X records `entry_rejected` only when `buy_result.success` is false and the outbound buy path reports `transport_send_failed`.

The promoted pair already contains multiple successful entries and fills on both sides:

- Dexter: `4` `entry_fill`
- Mew-X: `6` `entry_fill`
- Dexter: `0` `entry_rejected`
- Mew-X: `0` `entry_rejected`

So the current contract requires a matched pair to contain at least one exceptional failed entry on each source even when the same pair is otherwise rich enough to compare entry, session, and exit behavior.

### Mew-X `creator_candidate` is conditional on non-empty Deagle candidate reports

Frozen Mew-X emits `creator_candidate` only from `algo_choose_creators_report` output:

- `src/main.rs` emits `initial_selection`
- `src/mew/snipe/handler.rs` emits `refresh_addition` only when `added_keys` is non-empty

In both audited runs, the copied exports show:

- `candidates.initial_selection.json`: `observations: []`, `source_counts: {}`
- `candidates.refresh.json`: `observations: []`, `source_counts: {}`

The same runs still emitted fills and closed sessions. That proves frozen Mew-X can produce rich comparable live/sim evidence without ever producing a `creator_candidate` event in the current environment.

## Conclusion

### Key finding

`structurally not collectible under current contract`

### Why this is B, not A

The remaining gaps are not just "one more retry away" under the current frozen sources and validator contract:

- `run_summary` currently depends on finalizer-specific shutdown behavior that the matched-pair helper does not deliver.
- `entry_rejected` is failure-path-only on both sources and is not dependable healthy-run coverage.
- Mew-X `creator_candidate` depends on non-empty Deagle candidate reports, but the audited full-stream runs exported none.

Taken together, the current contract requires a pass-grade matched pair to contain a mix of healthy execution coverage, graceful finalizer completion, and source-specific failure-path evidence that is not realistically dependable in the current frozen runtime.

## TASK-006 Readiness

- Status: `blocked`
- Reason: the audit closes in favor of a structural contract/source gap, not a missing recollection recipe.
- Recommended next step: validator contract audit / rule exception review, or a frozen-source gap memo.
