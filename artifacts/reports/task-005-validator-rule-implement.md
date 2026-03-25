# TASK-005-VALIDATOR-RULE-IMPLEMENT

## Scope

This task applies the approved validator contract change from the merged rule-review memo. The change stays inside the Vexter comparison layer, does not modify Dexter or Mew-X source logic, and reuses the existing promoted and confirmatory matched-pair evidence rather than recollecting frozen-source runtime data.

## Verified GitHub State

- Latest merged Vexter `main`: PR `#19`, merge commit `db59c2edc099c4e794d8e0ac177cedb6f6d57d2d`, merged at `2026-03-25T19:18:46Z`
- Supporting merged Vexter states: PR `#18` `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`, PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, reverified on GitHub at `2026-03-20T16:05:19Z`

## Implemented Rule Treatment

### `run_summary`

- The validator now requires `run_summary` only when exported run-state evidence proves a clean shutdown.
- Clean shutdown proof is recognized from exported `*.state.json` files when `ended_at_utc` is populated or `status` enters a completed/finalized state.
- On the promoted and confirmatory packages, no such clean shutdown proof exists, so `run_summary` no longer blocks healthy matched-pair validation.

### `entry_rejected`

- The validator now requires `entry_rejected` only when a package shows an `entry_attempt` without a matching `entry_fill`.
- The promoted and confirmatory packages both show fully matched attempts and fills, so `entry_rejected` becomes observed-if-present evidence rather than a hard pass gate.

### Mew-X `creator_candidate`

- The validator now requires Mew-X `creator_candidate` only when exported candidate snapshots contain observations, added keys, or non-zero source counts.
- The promoted and confirmatory Mew-X candidate snapshot exports remained empty, so `creator_candidate` is now waived for those exact frozen-source runs.

## Code Changes

- `vexter/comparison/validator.py`
  - added conditional requirement resolution from package evidence
  - kept the event catalog intact while computing an active required set per run package
  - surfaced `active_required_event_types`, `waived_event_types`, and conditional rule reasons in validation output
- `tests/test_comparison_analysis.py`
  - added regression coverage for all three approved conditional rule treatments

No changes were made to:

- Dexter source logic
- Mew-X source logic
- comparison metrics derivation
- comparison winner logic beyond the validator-driven readiness state

## Revalidation Result

### Promoted pair `task005-pass-grade-pair-20260325T180027Z`

| Source | Old result | New result | Active required event types | Waived event types |
| --- | --- | --- | --- | --- |
| Dexter | `partial` (`10 / 12`) | `pass` (`10 / 10`) | `creator_candidate`, `candidate_rejected`, `mint_observed`, `entry_signal`, `entry_attempt`, `entry_fill`, `session_update`, `exit_signal`, `exit_fill`, `position_closed` | `entry_rejected`, `run_summary` |
| Mew-X | `partial` (`9 / 12`) | `pass` (`9 / 9`) | `candidate_rejected`, `mint_observed`, `entry_signal`, `entry_attempt`, `entry_fill`, `session_update`, `exit_signal`, `exit_fill`, `position_closed` | `creator_candidate`, `entry_rejected`, `run_summary` |

- The promoted comparison pack now reports `winner_mode: derived`.
- The pack summary explicitly advances to the downstream replay-validation gate instead of keeping TASK-005 blocked.

### Confirmatory pair `task005-pass-grade-pair-20260325T180604Z`

| Source | Old result | New result | Residual |
| --- | --- | --- | --- |
| Dexter | `partial` (`10 / 12`) | `pass` | none |
| Mew-X | `partial` (`8 / 12`) | `partial` (`8 / 9`) | `candidate_rejected` only |

- The confirmatory comparison pack remains `winner_mode: deferred`.
- That residual miss is narrower than the approved implementation scope and does not reopen the three rule treatments that were explicitly approved for this task.

## TASK-006 Readiness

- Promoted evidence now satisfies a comparable matched pair under the approved validator contract.
- The promoted comparison pack no longer defers winners and points directly to the replay-validation gate.
- The confirmatory retry is weaker but not contradictory: it leaves only Mew-X `candidate_rejected` as a residual gap.

Decision:

- `TASK-006 ready: yes`

Rationale:

- The approved validator rule implementation resolved the audited contract mismatch without changing frozen source behavior.
- A promoted comparable pack now exists on current Vexter `main`.
- The remaining confirmatory miss is narrow enough to carry forward as context rather than to block replay-validation startup.
