# Demo Forward Supervised Run Retry Prerequisite Matrix

This matrix bounds the external prerequisite gap for `supervised_run_retry_readiness`.

| Prerequisite | Current bounded fact | Who confirms | Retry allowed when |
| --- | --- | --- | --- |
| `DEXTER_DEMO_CREDENTIAL_SOURCE` | Repo documents a reference name only; no live credential attestation is stored in repo. | Named demo operator outside the repo. | The operator attests that the reference resolves to the intended Dexter `paper_live` credential source for the bounded retry window. |
| `DEXTER_DEMO_VENUE_REF` | Repo documents a venue reference only; the active venue target is not confirmed in repo. | Named demo operator plus venue owner outside the repo. | The venue reference is mapped to the intended Dexter demo venue and that mapping is explicitly confirmed for the retry window. |
| `DEXTER_DEMO_ACCOUNT_REF` | Repo documents an account reference only; the live paper account binding is not confirmed in repo. | Named demo operator outside the repo. | The account reference is matched to the intended Dexter `paper_live` account and explicitly confirmed for the retry window. |
| `DEXTER_DEMO_CONNECTIVITY_PROFILE` | Repo documents a connectivity profile name only; the actual connectivity path remains external and unverified. | Named demo operator plus connectivity owner outside the repo. | The connectivity profile is confirmed to reach the intended venue and account for the bounded retry window. |
| operator owner | The repo does not currently name a single retry owner. | Demo operator lead outside the repo. | One explicit operator owner is named for the retry gate and supervised window. |
| bounded supervised-window start criteria | The repo keeps the need explicit, but start timing and go/no-go criteria remain outside the repo. | Named demo operator outside the repo. | The retry window start time, duration, and stop conditions are explicitly agreed before retry. |
| allowlist / symbol / lot-size reconfirmation | Repo documents `DEXTER_DEMO_ALLOWED_SYMBOLS`, `DEXTER_DEMO_DEFAULT_SYMBOL`, `DEXTER_DEMO_ORDER_SIZE_LOTS`, `DEXTER_DEMO_MAX_ORDER_SIZE_LOTS`, `DEXTER_DEMO_WINDOW_MINUTES`, and `DEXTER_DEMO_MAX_OPEN_POSITIONS=1`, but retry-time reconfirmation is still pending. | Named demo operator outside the repo. | The operator reconfirms the allowlist, symbol, lot size, window, and one-position cap immediately before retry. |
| venue / connectivity confirmation | The blocked supervised-run baseline shows this as unresolved. | Named demo operator plus venue or connectivity owner outside the repo. | Venue reachability and connectivity health are explicitly confirmed for the bounded retry window. |
| stop-all visibility reconfirmation | The blocked supervised-run baseline preserved `manual_latched_stop_all`, but retry-time reconfirmation is still pending. | Named demo operator outside the repo. | The operator reconfirms `manual_latched_stop_all` visibility and terminal snapshot readability on the retry path. |

## Result Model

- PASS: every row is explicitly satisfied enough to attempt the next bounded retry lane.
- FAIL/BLOCKED: one or more rows remain unresolved, so the next lane stays a retry gate rather than retry execution.
