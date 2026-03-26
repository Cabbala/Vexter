# PATTERN-A-DEMO-EXECUTOR-CUTOVER

## 1. Intent
- Stop further observability / handoff / watchdog deepening here.
- Fix the shortest Pattern A route toward demo-account forward testing.

## 2. Fixed Boundary
- Dexter `paper_live` is the first real demo target.
- Frozen Mew-X stays `sim_live` and does not enter the first real demo order path.
- Planner stays on `prepare / start / status / stop / snapshot`.
- Adapter owns demo submit / cancel / status / fill / stop-all.

## 3. Acceptance Slice
- Dexter-only
- one handle
- one open position max
- small lot
- allowlist only
- operator-supervised bounded window
- stop-all and terminal snapshot must remain explicit

## 4. Abort Conditions
- pin or mode mismatch
- ambiguous handle identity
- status/fill reconciliation gap
- unexpected funded-live path
- unconfirmed cancel or stop-all
- quarantine or manual halt trigger

## 5. Next Task
- `demo_executor_adapter_implementation`
