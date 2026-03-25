# TASK-005 Pass Grade Pair Blocker

## Verified Start

- `Cabbala/Vexter` `origin/main` was re-verified at `28c15b5c7655fe7647c12774494c80b83c58c04f` on `2026-03-25` after merged PR `#15`.
- `Cabbala/Dexter` `main` remained re-verified at `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938` (merged PR `#3`) so the fresh recollections used the current merged `paper_live` path.
- Frozen Mew-X remained pinned at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`.
- Previous paper-revalidate promoted pair remained `task005-paper-revalidate-20260321T123011Z` at Dexter `9 / 12` and Mew-X `8 / 12`.

## Fresh Pass Grade Attempts

| Label | Dexter Mode | Mew-X Mode | Exact Overlap | Dexter Coverage | Mew-X Coverage | Note |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `task005-pass-grade-pair-20260325T180027Z` | `paper_live` | `sim_live` | `162,941 ms` | `10 / 12` | `9 / 12` | promoted pair; packaging fallback fix held, Dexter kept `candidate_rejected`, Mew-X kept `candidate_rejected` |
| `task005-pass-grade-pair-20260325T180604Z` | `paper_live` | `sim_live` | `53,315 ms` | `10 / 12` | `8 / 12` | confirmatory retry with `--grace-seconds 60`; `run_summary` still absent |

## What Improved

- Vexter-side packaging is now more robust: `scripts/collect_comparison_package.ps1` no longer crashes when the Mew-X full-stream fallback copies exactly one session export.
- Dexter improved from the prior paper-revalidate ceiling of `9 / 12` to `10 / 12` on both fresh attempts by retaining `candidate_rejected` while still reaching mint, entry, session, exit, and closeout events.
- Mew-X improved from `8 / 12` to `9 / 12` on the promoted fresh pair.
- Both fresh retries cleared Dexter wallet-balance startup `HTTP 429`; remaining rate-limit noise was confined to `wsLogs`.

## What Did Not Improve

- Dexter still missed `entry_rejected` and `run_summary` on both fresh retries.
- Mew-X still missed `creator_candidate`, `entry_rejected`, and `run_summary` on the promoted retry; the confirmatory retry also lost `candidate_rejected`.
- `run_summary` did not appear on either source in either fresh retry, even after the confirmatory attempt extended graceful shutdown to `60 s`.
- Both fresh retries still needed full-stream fallback because the first raw events landed before the post-readiness measurement window.
- No comparison area became non-deferred, so winner and tie decisions stayed blocked.

## Sharpest Remaining Blocker

The blocker is no longer creator-only Dexter paper coverage. The promoted fresh pair now proves Dexter can reach `candidate_rejected`, mint, entry, session, exit, and position-close events without changing source logic.

The blocker is now the remaining validator gap on the matched pair itself:

- Dexter still never emitted `entry_rejected` or `run_summary`.
- Mew-X still never emitted `creator_candidate`, `entry_rejected`, or `run_summary`.
- The stronger fresh pair still validated only as `partial`, and the confirmatory retry with longer grace did not close the gap.

That means the current pass-grade-pair evidence is still insufficient for TASK-006.

## Current State

- Strongest fresh pair:
  - report: `artifacts/reports/task005-pass-grade-pair-20260325T180027Z-comparison`
  - proof pack: `artifacts/proofs/task005-pass-grade-pair-20260325T180027Z-results/comparison-pack.json`
- Confirmatory retry:
  - report: `artifacts/reports/task005-pass-grade-pair-20260325T180604Z-comparison`
  - proof pack: `artifacts/proofs/task005-pass-grade-pair-20260325T180604Z-results/comparison-pack.json`
- `TASK-006` remains blocked.
