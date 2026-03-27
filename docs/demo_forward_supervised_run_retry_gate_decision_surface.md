# Demo Forward Supervised Run Retry Gate Decision Surface

This decision surface is the current source of truth for `supervised_run_retry_gate`.

| Gate input | Repo-visible face | Current observation | Gate passes when |
| --- | --- | --- | --- |
| `external_credential_source_face` | `external_reference` | A reference name is visible in repo, but the external credential resolution is not observed in repo. | the named operator explicitly attests that the reference resolves to the intended Dexter paper-live credential source for the bounded retry window |
| `venue_ref_face` | `dexter_paper_live_demo_venue` | A venue reference is visible in repo, but the active venue mapping for the retry window is not observed in repo. | the venue reference is explicitly matched to the intended Dexter demo venue for the bounded retry window |
| `account_ref_face` | `dexter_paper_live_demo_account` | An account reference is visible in repo, but the retry-window account binding is not observed in repo. | the account reference is explicitly matched to the intended Dexter paper-live account for the retry window |
| `connectivity_profile_face` | `dexter_paper_live_demo_connectivity` | A connectivity profile marker is visible in repo, but the live retry-path reachability is not observed in repo. | the connectivity profile is explicitly confirmed to reach the intended venue and account during the bounded retry window |
| `operator_owner_face` | `unconfirmed_outside_repo` | The repo does not identify one retry owner for the full supervised window. | one explicit operator owner is named for the full retry gate and supervised window |
| `bounded_start_criteria_face` | `{"bounded_window_minutes": 15, "halt_mode": "manual_latched_stop_all", "status_delivery": "poll_first"}` | The bounded window and stop model are fixed in repo, but the actual retry start time, go/no-go owner, and abort owner are not observed in repo. | the retry start time, bounded window, abort owner, and go/no-go criteria are explicitly agreed before entry |
| `allowlist_symbol_lot_reconfirmed` | `{"allowed_symbols": ["BONK/USDC"], "bounded_window_minutes": 15, "default_symbol": "BONK/USDC", "max_open_positions": 1, "max_order_size_lots": "0.05", "order_size_lots": "0.05"}` | The bounded symbol, lot-size, window, and one-position guardrails parse cleanly from repo, but retry-time reconfirmation is not observed in repo. | the operator explicitly reconfirms allowlist, default symbol, lot size, bounded window, and one-position cap immediately before retry |
| `manual_latched_stop_all_visibility_reconfirmed` | `baseline_stop_all_state=flatten_confirmed` | The blocked supervised baseline preserved `manual_latched_stop_all`, but retry-path visibility is not yet re-observed for the next gate window. | `manual_latched_stop_all` visibility is explicitly reconfirmed on the bounded retry path before entry |
| `terminal_snapshot_readability_reconfirmed` | `baseline_terminal_snapshot_readable=true` | The baseline handoff shows terminal snapshot detail, but retry-path terminal snapshot readability is not yet re-observed for the next gate window. | terminal snapshot readability is explicitly reconfirmed on the retry path before entry |

## Current Decision

- Gate outcome: `FAIL/BLOCKED`
- Key finding: `supervised_run_retry_gate_blocked_on_unresolved_gate_inputs`
- Claim boundary: `supervised_run_retry_gate_bounded`
- Current task state: `supervised_run_retry_gate_blocked`
- Recommended next step while blocked: `supervised_run_retry_gate`
- Gate-pass successor: `supervised_run_retry_execution`
- Retry execution allowed now: `false`

Retry execution does not begin unless every gate-input row is explicit enough to permit it.
