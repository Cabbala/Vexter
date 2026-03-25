# TASK-005-VALIDATOR-CONTRACT-AUDIT

## Scope

This audit answered one narrower follow-up question on top of merged Vexter `main`: should the current validator contract be relaxed for `run_summary`, `entry_rejected`, and Mew-X `creator_candidate`, or can a minimal shutdown / packaging fix restore collectability without changing frozen source logic or comparison rules?

The audit kept Dexter strategy semantics, Mew-X source logic, and validator rules unchanged. It reused the GitHub-visible promoted and confirmatory full-stream proofs from the merged gap audit, then rechecked those proofs against the latest merged Vexter `main`, the current validator contract, the matched-pair helper, and the frozen source commits.

## Verified GitHub State

- Latest merged Vexter `main`: PR `#17`, merge commit `b09033d6c8ce21510da23025cee935e46f3ef4df`, merged at `2026-03-25T18:40:50Z`
- Prior supporting Vexter `main`: PR `#16`, merge commit `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, reverified on GitHub at `2026-03-20T16:05:19Z`

## Current Contract Boundary

- `vexter/comparison/constants.py` still lists `creator_candidate`, `entry_rejected`, and `run_summary` inside `REQUIRED_EVENT_TYPES`.
- `vexter/comparison/validator.py` still classifies a package as `partial` whenever any required event type is missing.
- `scripts/collect_comparison_package.ps1` already falls back to copying the full raw stream when window filtering returns zero events.
- `scripts/collect_matched_live_pair.py` still requests shutdown with `CTRL_BREAK_EVENT`.

That means this task had to decide whether the remaining gaps are still helper-fixable under those frozen inputs, or whether the current contract itself now overstates what a healthy matched pair should always contain.

## Event Classification

| Event | Frozen-source behavior | Contract class | Minimal helper / packaging fix viable? | Conclusion |
| --- | --- | --- | --- | --- |
| `run_summary` | Finalizer-only on Dexter and Mew-X | `shutdown_success_dependent` | `limited yes` on helper shutdown only | This sits at the shutdown boundary, not the packaging boundary. |
| `entry_rejected` | Buy-failure-only on both sources | `failure_path_only` | `no` | Healthy matched pairs cannot be expected to emit it on demand. |
| `creator_candidate` on Mew-X | Only emitted from non-empty candidate reports | `source_specific_conditional` | `no` | Current frozen environment can still produce comparable fills and closes with zero such events. |

## Evidence

### `run_summary`

- Dexter emits `run_summary` only in `DexLab/instrumentation.py` `finalize()`.
- Dexter reaches that finalizer from `Dexter.close()`.
- Frozen Mew-X emits `run_summary` only in `src/mew/instrumentation.rs` `finalize()`, reached from the `ctrl_c` task, normal end-of-main, or `Drop`.
- Both supporting 2026-03-25 collection payloads show the current helper requested shutdown with `CTRL_BREAK_EVENT`.
- Both payloads recorded source exit code `3221225786` (`0xC000013A`).
- The copied state exports still showed unfinished state with null `ended_at_utc`.
- Both supporting collections were already built from `full_stream_fallback`, so the missing event is absent from the copied raw streams themselves, not only from the PowerShell time filter.

Conclusion: shutdown hardening may recover `run_summary`, but packaging alone is already doing the best available copy. This event is helper-sensitive, not packaging-sensitive.

### `entry_rejected`

- Frozen Dexter records `entry_rejected` only on failed buy paths such as missing bonding curve, insufficient balance, migration, zero quote, creator vault unavailable, price-too-high, or confirmation failure.
- Frozen Mew-X records `entry_rejected` only when `buy_result.success` is false and the event is attributed as `transport_send_failed`.
- The promoted pair still showed Dexter `4` `entry_fill` and Mew-X `6` `entry_fill`, while both sides had `0` `entry_rejected`.

Conclusion: a shutdown or packaging change cannot recover an event that a healthy run never emitted. This is contract-shape, not helper-shape.

### `creator_candidate` on Mew-X

- Frozen Mew-X emits `creator_candidate` only from `algo_choose_creators_report` output on initial selection and refresh additions.
- The supporting `candidates.initial_selection.json` and `candidates.refresh.json` exports still showed `observations: []` and `source_counts: {}`.
- The same runs still produced `mint_observed`, `entry_fill`, `exit_fill`, and `position_closed`.

Conclusion: under the current frozen environment, Mew-X can produce rich comparable sessions through non-creator paths while never emitting `creator_candidate`. Helper-side fixes cannot change that without altering source behavior or market conditions.

## Responsibility Boundary

- Frozen source logic decides whether `entry_rejected` and Mew-X `creator_candidate` ever exist.
- The packager only copies what the raw stream and source exports already contain; `full_stream_fallback` proves it is already not the bottleneck here.
- The shutdown helper can influence only finalizer-bound artifacts such as `run_summary`.
- The validator currently folds all three categories into one always-required pass gate.

## Decision

### Selected outcome

- `A`

### Key finding

- `rule review needed`

### Why this is A, not B

- `run_summary` alone has a plausible helper-side recovery path.
- `entry_rejected` and Mew-X `creator_candidate` do not.
- Therefore a minimal shutdown / packaging fix is insufficient to make all three residual events collectible again under frozen Dexter `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, frozen Mew-X `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, and the current validator contract.

The contract currently requires one matched pair to simultaneously demonstrate:

- healthy entry / session / exit behavior
- graceful finalizer completion
- failure-path entry evidence
- source-specific creator-report evidence

That combination does not match the frozen-source reality captured by the merged proof set.

## TASK-006 Readiness

- Status: `blocked`
- Reason: the contract-level mismatch is still unresolved, and helper hardening alone would not eliminate all current required-event gaps.
- Recommended next step: approved validator rule review / exception memo first
- Optional follow-on after approval: narrow helper shutdown hardening task scoped only to `run_summary`
