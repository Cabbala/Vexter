# TASK-005-VALIDATOR-CONTRACT-AUDIT Summary

## Verified GitHub State

- `Cabbala/Vexter` latest merged `main` was reverified at PR `#17` merge commit `b09033d6c8ce21510da23025cee935e46f3ef4df` on `2026-03-25T18:40:50Z`.
- The supporting gap-audit evidence was the prior merged Vexter `main` at PR `#16` merge commit `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`.
- `Cabbala/Dexter` `main` stayed pinned at merged PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938` on `2026-03-21T11:31:07Z`.
- Frozen `Cabbala/Mew-X` stayed pinned at commit `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, reverified on GitHub at `2026-03-20T16:05:19Z`.

## What This Audit Did

- Reconfirmed that the current validator contract still treats every entry in `REQUIRED_EVENT_TYPES` as a hard pass gate.
- Reused the GitHub-visible promoted and confirmatory full-stream proofs from the merged gap audit instead of recollecting the same shape again.
- Audited frozen Dexter, frozen Mew-X, the matched-pair shutdown helper, and the packaging fallback path to separate source non-emission from helper loss.
- Kept source logic, source thresholds, and validator rules unchanged.

## Contract-Level Classification

### `run_summary`

- Both frozen sources emit `run_summary` only from finalizers.
- The current helper still shuts down with `CTRL_BREAK_EVENT`, and both 2026-03-25 collection payloads ended with process exit code `3221225786` (`0xC000013A`) while copied state remained unfinished.
- The packager already used `full_stream_fallback`, so this is not a packaging-only loss.
- Minimal helper hardening is plausible for `run_summary`, but only in the shutdown-success path.

### `entry_rejected`

- Dexter and Mew-X both emit `entry_rejected` only on failed entry paths.
- The promoted pair still showed successful fills on both sides with zero rejects.
- Shutdown or packaging cannot recover an event that a healthy run never emitted.

### `creator_candidate` on Mew-X

- Frozen Mew-X emits `creator_candidate` only from non-empty initial-selection or refresh-addition reports.
- The copied candidate snapshots for the audited runs still had `observations: []` and `source_counts: {}` while the same runs produced fills and closed positions.
- Shutdown or packaging cannot synthesize this event without changing source behavior or forcing different market conditions.

## Decision

- Outcome: `A`
- Key finding: `rule review needed`
- Interpretation: helper-side shutdown hardening may recover `run_summary`, but it cannot make `entry_rejected` or Mew-X `creator_candidate` dependable in healthy frozen-source matched pairs.
- TASK-006 readiness: `blocked`
- Recommended next step: approved validator rule review / exception memo first, with optional follow-on helper hardening scoped only to `run_summary`.

## Key Paths

- Contract audit report: `artifacts/reports/task-005-validator-contract-audit.md`
- Readiness report: `artifacts/reports/task-005-validator-contract-audit-readiness.md`
- Audit proof: `artifacts/proofs/task-005-validator-contract-audit-check.json`
- Supporting promoted proof dir: `artifacts/proofs/task005-gap-audit-20260325T180027Z-results`
- Supporting confirmatory proof dir: `artifacts/proofs/task005-gap-audit-20260325T180604Z-results`
- Supporting collection payloads:
  - `artifacts/proofs/task005-gap-audit-20260325T180027Z.collection.json`
  - `artifacts/proofs/task005-gap-audit-20260325T180604Z.collection.json`
