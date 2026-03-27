# Demo Forward Abort And Rollback Matrix

| Condition | Detection surface | Required operator action | Expected proof surface |
| --- | --- | --- | --- |
| `pin_mismatch` | `prepare` rejection, current status, proof json | Abort immediately. Do not start the supervised window. | status report, report, proof json |
| `mode_mismatch` | `prepare` rejection or runtime detail drift | Abort immediately and confirm the route is still Dexter `paper_live` / Mew-X `sim_live`. | status report, report, handoff |
| `status_or_fill_reconciliation_gap` | `status` failure detail, runtime proof, current report | Abort the window, stop the handle, and preserve normalized failure detail. | report, proof json, handoff |
| `duplicate_or_ambiguous_handle` | handle identity chain, status detail, handoff continuity | Abort the window and quarantine the run context until the handle chain is unambiguous. | current report, handoff |
| `unexpected_funded_live_path` | route or runtime detail | Abort immediately. Treat as out-of-scope and do not continue. | status report, report, proof json |
| `cancel_or_stop_all_unconfirmed` | `stop_all_state`, snapshot detail | Continue rollback until cancel or flatten confirmation is visible. If still unconfirmed, abort and hand off. | current report, handoff, proof json |
| `quarantine_or_manual_halt_triggered` | `status`, watchdog-facing status fields, handoff | Stop the supervised window, preserve the reason, and carry it forward in the handoff. | current status, current handoff |
| `terminal_snapshot_visibility_lost` | missing `snapshot` detail, missing rollback detail | Abort and do not claim supervised-run readiness until terminal detail is restored. | current report, proof json, handoff |

## Rollback Notes

- `manual_latched_stop_all` remains planner-owned.
- Cancel or flatten stays adapter-owned inside Dexter demo runtime.
- The rollback proof is incomplete until terminal snapshot visibility is restored.
