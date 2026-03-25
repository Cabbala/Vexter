# TASK-005 Gap Audit Readiness

## Verified State

- Vexter latest merged `main`: PR `#16`, commit `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Prior task base for the audited pass-grade pair: PR `#15`, commit `28c15b5c7655fe7647c12774494c80b83c58c04f`
- Dexter merged `main`: PR `#3`, commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## Audit Result

- Key finding: `structurally not collectible under current contract`
- Fresh recollection required to close the audit: `no`
- TASK-006 ready: `no`

## Evidence Summary

### `run_summary`

- Both promoted and confirmatory runs were revalidated from copied full streams.
- Both sources still missed `run_summary`.
- Both copied state exports remained `running` with `ended_at_utc: null`.
- The current matched-pair helper shuts down with `CTRL_BREAK_EVENT`, while frozen source finalizers emit `run_summary` only on successful finalization paths.

### `entry_rejected`

- Dexter emits `entry_rejected` only on failed buy paths.
- Mew-X emits `entry_rejected` only on `transport_send_failed`.
- Requiring both in the same matched pass-grade pair means requiring failure-path evidence, not just normal profitable/session evidence.

### `creator_candidate` on Mew-X

- Frozen Mew-X emits `creator_candidate` only when Deagle candidate reports contain observations.
- Both audited runs exported empty initial and refresh candidate snapshots while still producing fills and closed sessions.

## Decision

- Comparison contract satisfied: `no`
- Winner mode available: `no`
- TASK-006 readiness: `blocked`
- Recommended next step: validator contract audit / rule exception review before any more same-shape recollection.
