# DEMO-FORWARD-SUPERVISED-RUN-RETRY-READINESS

## 1. Intent
- Accept the blocked supervised run as baseline.
- Promote retry readiness to the repo-visible current source of truth.

## 2. Boundary
- Dexter `paper_live` only
- frozen Mew-X `sim_live` only
- `single_sleeve`
- `dexter_default`
- one active real demo plan max
- one open position max
- allowlist only
- small lot only
- bounded supervised window only
- external refs remain outside repo

## 3. Required Current Surfaces
- status
- report
- summary
- proof
- handoff
- checklist
- prerequisite matrix
- sub-agent summary

## 4. Honest Outcome
- `PASS` only if all retry prerequisites are explicitly satisfied enough for the next bounded retry lane.
- `FAIL/BLOCKED` if any external prerequisite remains unresolved.

## 5. Next Task
- `supervised_run_retry_gate`
