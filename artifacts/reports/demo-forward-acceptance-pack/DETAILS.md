# DEMO-FORWARD-ACCEPTANCE-PACK

## 1. Intent
- Fix the bounded forward acceptance, operator, proof, and handoff surfaces after the Dexter demo adapter landed.
- Keep the seam source-faithful and stop before the supervised run itself.

## 2. Acceptance Boundary
- Dexter `paper_live` only
- frozen Mew-X `sim_live` only
- `single_sleeve`
- `dexter_default`
- one active real demo plan max
- one open position max
- allowlist only
- small lot only
- bounded operator-supervised window only

## 3. Required Current Surfaces
- current status
- current report
- current summary
- current proof json
- current handoff
- current operator checklist
- current abort / rollback matrix

## 4. Abort Conditions
- pin mismatch
- mode mismatch
- status/fill reconciliation gap
- duplicate or ambiguous handle
- unexpected funded live path
- cancel or stop-all unconfirmed
- quarantine or manual halt triggered
- terminal snapshot visibility lost

## 5. Next Task
- `demo_forward_supervised_run`
