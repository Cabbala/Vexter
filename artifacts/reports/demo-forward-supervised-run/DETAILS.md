# DEMO-FORWARD-SUPERVISED-RUN

## 1. Intent
- Promote the bounded supervised run lane to the repo-visible current source of truth.
- Fail closed if the repo cannot honestly claim a real-demo completion.

## 2. Boundary
- Dexter `paper_live` only
- frozen Mew-X `sim_live` only
- `single_sleeve`
- `dexter_default`
- one active real demo plan max
- one open position max
- allowlist only
- small lot only
- bounded operator-supervised window only

## 3. Sequence
- `prepare`
- `start`
- entry visibility
- order status / fill reconciliation
- stop-all visibility
- terminal snapshot
- normalized failure continuity

## 4. Outcome
- `FAIL/BLOCKED` is acceptable if external refs, operator ownership, or connectivity remain unresolved outside the repo.

## 5. Next Task
- `supervised_run_retry_readiness`
