# Demo Forward Supervised Run Retry Gate Decision Surface

- Outcome: `FAIL/BLOCKED`
- Current recommended step: `supervised_run_retry_gate`
- Pass target: `supervised_run_retry_execution`
- Observed repo marker only: `true` means the repo shows a marker, not external confirmation.

| Gate input face | Repo-visible marker | Observed repo marker only | Resolved outside repo | Gate pass when |
| --- | --- | --- | --- | --- |
| external credential source face | external_reference | true | false | the operator explicitly attests that the credential source resolves to the intended Dexter paper_live source for this bounded retry window |
| venue ref face | dexter_paper_live_demo_venue | true | false | the venue reference is explicitly mapped to the intended reachable Dexter paper_live venue for this bounded retry window |
| account ref face | dexter_paper_live_demo_account | true | false | the account reference is explicitly matched to the intended Dexter paper_live account for this bounded retry window |
| connectivity profile face | dexter_paper_live_demo_connectivity | true | false | the connectivity profile is explicitly confirmed to reach the intended venue and account for this bounded retry window |
| operator owner face | unconfirmed_outside_repo | false | false | one operator owner is explicitly named for the full supervised window |
| bounded start criteria face | bounded_window_minutes=15 | true | false | the retry start time, retry end time, abort owner, and stop conditions are explicitly named before retry |
| allowlist symbol lot reconfirmation face | {"allowed_symbols": ["BONK/USDC"], "bounded_window_minutes": 15, "default_symbol": "BONK/USDC", "max_open_positions": 1, "max_order_size_lots": "0.05", "order_size_lots": "0.05"} | true | false | the operator reconfirms allowlist, symbol, lot size, bounded window, and one-position cap immediately before retry |
| manual latched stop all visibility face | {"baseline_halt_mode": "manual_latched_stop_all", "baseline_stop_all_state": "flatten_confirmed"} | true | false | manual_latched_stop_all visibility is explicitly reconfirmed on the retry path |
| terminal snapshot readability face | {"baseline_snapshot_executor_status": "stopped", "baseline_snapshot_fill_count": 2, "baseline_snapshot_order_count": 2} | true | false | terminal snapshot readability is explicitly reconfirmed on the retry path |

## Decision

- `supervised_run_retry_execution` remains blocked.
- The current lane stays `supervised_run_retry_gate` until every face above is explicit enough to pass.
- Repo-visible names such as venue, account, and connectivity references remain observed repo markers only and are not external confirmation.
