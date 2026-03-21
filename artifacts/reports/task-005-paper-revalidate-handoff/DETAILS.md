# TASK-005-PAPER-REVALIDATE Handoff

## Verified Start

- Vexter `origin/main` verified at `3a720a64a5dbbda482513446b3bc47c341dde2ae` after PR `#14`
- Dexter `main` verified at `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938` after PR `#3`
- Previous paper ceiling: Dexter `1 / 12`

## What This Task Did

- Updated Vexter's pinned Dexter SHA to PR `#3` merged `main`
- Recovered the Windows runtime and confirmed both source checkouts
- Recollected two fresh same-attempt Dexter `paper_live` x Mew-X `sim_live` pairs
- Reran `validate`, `derive-metrics`, and `build-pack` for both pairs

## Fresh Results

### Promoted pair

- Label: `task005-paper-revalidate-20260321T123011Z`
- Dexter coverage: `9 / 12`
- Mew-X coverage: `8 / 12`
- Exact event overlap: `117,795 ms`
- Dexter no longer stops at creator-only; it now reaches mint, entry, session, exit, and closeout events.

### Confirmatory pair

- Label: `task005-paper-revalidate-20260321T123426Z`
- Dexter coverage: `9 / 12`
- Mew-X coverage: `8 / 12`
- Exact event overlap: `108,930 ms`
- Improvement reproduced, but the packages still validate only as `partial`.

## TASK-006 Readiness

- STATUS: `BLOCKED`
- Why: both matched packages still miss required event types under the current contract, especially `run_summary`.
- Next task: `TASK-005-PASS-GRADE-PAIR`
