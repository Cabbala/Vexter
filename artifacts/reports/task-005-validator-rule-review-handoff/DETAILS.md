# TASK-005-VALIDATOR-RULE-REVIEW Handoff

## Verified GitHub State

- Vexter latest merged `main`: PR `#18`, `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`
- Supporting Vexter states: PR `#17`, `b09033d6c8ce21510da23025cee935e46f3ef4df`; PR `#16`, `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## What This Task Did

- Rechecked the current validator hard-pass contract against the merged promoted and confirmatory proof set
- Converted the merged contract-audit conclusion into an approval-grade rule review / exception memo
- Kept frozen source logic and validator rules unchanged
- Updated closeout artifacts for the rule-review decision

## Key Finding

- `rule memo ready`

## Recommended Rule Treatment

- `run_summary`: treat as `shutdown_success_dependent`; require it only on proven clean shutdown or later replayability / integration review
- `entry_rejected`: treat as `failure_path_only`; require it only when an entry failure actually occurs
- Mew-X `creator_candidate`: treat as `source_specific_conditional`; require it only when candidate snapshots are non-empty

## Outcome

- Selected outcome: `A`
- Validator rule implementation approved by this task: `no`
- TASK-006 readiness: `BLOCKED`

## Recommended Next Step

- Approval-driven validator rule implementation
- Optional later helper task limited to `run_summary` shutdown hardening

## Key Paths

- Rule review memo:
  - `artifacts/reports/task-005-validator-rule-review.md`
- Readiness report:
  - `artifacts/reports/task-005-validator-rule-review-readiness.md`
- Review proof:
  - `artifacts/proofs/task-005-validator-rule-review-check.json`
- Supporting promoted proof dir:
  - `artifacts/proofs/task005-gap-audit-20260325T180027Z-results`
- Supporting confirmatory proof dir:
  - `artifacts/proofs/task005-gap-audit-20260325T180604Z-results`
