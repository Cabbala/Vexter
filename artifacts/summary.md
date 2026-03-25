# TASK-005-VALIDATOR-RULE-REVIEW Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#18` merge commit `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81` on `2026-03-25T18:57:55Z`.
- Supporting merged Vexter states remained PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df` and PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938` on `2026-03-21T11:31:07Z`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, reverified on GitHub at `2026-03-20T16:05:19Z`.

## What This Review Did

- Reconfirmed that `vexter/comparison/constants.py` and `vexter/comparison/validator.py` still treat all `REQUIRED_EVENT_TYPES` as one hard pass gate.
- Reused the GitHub-visible promoted and confirmatory pass-grade proofs plus the merged contract audit instead of recollecting the same frozen-source shape again.
- Kept Dexter strategy semantics, Mew-X source logic, and validator rules unchanged while translating the audit result into an approval-grade rule review / exception memo.

## Rule Review Result

### `run_summary`

- Frozen Dexter and frozen Mew-X both emit `run_summary` only from finalizers.
- Both 2026-03-25 supporting collections ended through `CTRL_BREAK_EVENT` with exit code `3221225786` (`0xC000013A`), and both copied state exports still showed `status: running` with `ended_at_utc: null`.
- Recommended treatment: stop treating `run_summary` as source-agnostic always-required evidence; make it conditional on clean shutdown completion or reserve it for replayability / integration evidence.

### `entry_rejected`

- Frozen Dexter records `entry_rejected` only on failed buy paths such as missing bonding curve, insufficient balance, migration, zero quote, creator vault unavailable, price-too-high, or confirmation failure.
- Frozen Mew-X records `entry_rejected` only when `buy_result.success` is false and the rejection is attributed as `transport_send_failed`.
- Recommended treatment: make `entry_rejected` conditional on observed entry failure rather than a healthy success-path pass gate; otherwise keep it as observed-if-present evidence.

### `creator_candidate` on Mew-X

- Frozen Mew-X emits `creator_candidate` only from non-empty initial-selection or refresh-addition reports.
- The promoted pair still exported `observations: []` and `source_counts: {}` in both initial and refresh candidate snapshots while also producing `mint_observed`, `entry_fill`, `exit_fill`, and `position_closed`.
- Recommended treatment: keep it source-specific and conditional for Mew-X when candidate snapshots are non-empty; otherwise treat it as optional rather than a source-agnostic hard requirement.

## Decision

- Outcome: `A`
- Key finding: `rule memo ready`
- Rule implementation approved by this task: `no`
- TASK-006 readiness: `blocked`
- Recommended next step: approval-driven validator rule implementation, with optional later helper hardening scoped only to `run_summary`

## Key Paths

- Rule review memo: `artifacts/reports/task-005-validator-rule-review.md`
- Readiness report: `artifacts/reports/task-005-validator-rule-review-readiness.md`
- Review proof: `artifacts/proofs/task-005-validator-rule-review-check.json`
- Supporting promoted proof dir: `artifacts/proofs/task005-gap-audit-20260325T180027Z-results`
- Supporting confirmatory proof dir: `artifacts/proofs/task005-gap-audit-20260325T180604Z-results`
- Supporting collection payloads:
  - `artifacts/proofs/task005-gap-audit-20260325T180027Z.collection.json`
  - `artifacts/proofs/task005-gap-audit-20260325T180604Z.collection.json`
