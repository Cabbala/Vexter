# TASK-005 Paper Validation Blocker

## Verified Start

- `Cabbala/Vexter` `origin/main` was re-verified at `379f55a50dbfd91968ba643e2fbfe5e73fad8392` on 2026-03-21.
- Merged Vexter PR `#12` (`4b32053697fc4efddd76e542b3d2a1411b450240`) and PR `#13` (`379f55a50dbfd91968ba643e2fbfe5e73fad8392`) were explicitly confirmed.
- `Cabbala/Dexter` `main` was re-verified at `5dc1036c499af5f14f06d08ad0fa96aa36228c96` (merged PR `#2`) so the fresh recollection used the real merged `paper_live` path.
- Prior authoritative TASK-005 baseline remained `resume-after-pr9-20260321T1737` at Dexter `4 / 12` and Mew-X `8 / 12`.

## Fresh Paper / Sim Attempts

| Label | Dexter Mode | Mew-X Mode | Exact Overlap | Dexter Coverage | Mew-X Coverage | Note |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `task005-paper-validation-20260321T1950` | `paper_live` | `sim_live` | `141 ms` | `1 / 12` | `9 / 12` | strongest Mew-X fresh pair; Dexter still logged startup websocket `HTTP 429` |
| `task005-paper-validation-20260321T2005` | `paper_live` | `sim_live` | `137 ms` | `1 / 12` | `8 / 12` | confirmatory retry; Dexter main-runtime `HTTP 429` cleared, result unchanged |

## What Improved

- Vexter now launches Dexter with explicit `paper_live` for TASK-005 recollection.
- Windows recovery now pins Dexter to merged `main` `5dc1036c499af5f14f06d08ad0fa96aa36228c96`.
- Mew-X still behaves as the stronger paper/sim surface and reached `9 / 12` required event types on the strongest fresh pair.
- The second retry showed Dexter's failure to progress was not just a main-runtime startup-429 artifact.

## What Did Not Improve

- Dexter did **not** improve from the prior `4 / 12` baseline. It regressed to `1 / 12` on both fresh `paper_live` retries.
- On both fresh retries Dexter emitted only:
  - `creator_candidate`
- Dexter still missed all of:
  - `candidate_rejected`
  - `mint_observed`
  - `entry_signal`
  - `entry_attempt`
  - `entry_fill`
  - `entry_rejected`
  - `session_update`
  - `exit_signal`
  - `exit_fill`
  - `position_closed`
  - `run_summary`
- `run_summary` did not appear on either fresh pair.
- No comparison area became non-deferred, so winner/tie decisions stayed blocked.

## Sharpest Remaining Blocker

The blocker is no longer "Dexter has no paper mode." The merged `paper_live` path was used directly.

The blocker is now sharper:

- Dexter `paper_live` still did not progress from creator admission into mint/session/exit coverage on two fresh same-attempt recollections.
- Both fresh retries also needed full-stream fallback because the first raw events landed before the post-readiness measurement window, leaving only subsecond exact overlap.

That means the observed paper-validation ceiling on these fresh pairs is still insufficient for TASK-006.

## Current State

- Strongest fresh pair:
  - report: `artifacts/reports/task-005-paper-validation-20260321T1950-comparison`
  - proof pack: `artifacts/proofs/task-005-paper-validation-20260321T1950-results/comparison-pack.json`
- Confirmatory retry:
  - report: `artifacts/reports/task-005-paper-validation-20260321T2005-comparison`
  - proof pack: `artifacts/proofs/task-005-paper-validation-20260321T2005-results/comparison-pack.json`
- `TASK-006` remains blocked.
