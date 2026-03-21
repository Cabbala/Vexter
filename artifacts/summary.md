# TASK-005 Live Comparison Evidence Summary

## Status

- `TASK-005-live-comparison-evidence` remains blocked in `partial_live_comparison_blocker` state on branch `codex/task-005-resume-after-pr9` as of `2026-03-21T08:46:35Z`.
- Start conditions were re-verified from `Cabbala/Vexter` latest `main` commit `20d0eb3d7f6bda11c2526711145c0cd3298e4adf`; PR `#9` was confirmed merged on `2026-03-21`.
- Post-PR10 closeout was rechecked on `2026-03-21T09:10:02Z` against `origin/main` `5a352c5fa8773ca336eb593385f53f8ef2ffcb3c`; the promoted same-attempt pair `resume-after-pr9-20260321T1737`, the restored Mew-X `session_summary` pointer, the current partial blocker, and the paper/sim-first deferred follow-up note all stayed unchanged.
- Dexter and Mew-X strategy, execution, and instrumentation logic remain unchanged.
- Sub-agents `Wegener` and `Schrodinger` were launched for sidecar inspection while the main thread handled the fresh PR9 recollection, validation rebuild, and artifact closeout.
- Two fresh PR9 same-attempt retries were collected:
  - `resume-after-pr9-20260321T1729` cleared startup 429 but over-serialized Dexter enough to lose exact event overlap, so it was not promoted.
  - `resume-after-pr9-20260321T1737` shortened the Dexter quiet/settle gap, restored exact event overlap, and became the promoted fresh pair.

## Fresh Same-Attempt Result

- Vexter-side packaging remains corrected without touching frozen source logic:
  - `scripts/collect_comparison_package.ps1` preserves time-bounded Mew-X `export/sessions/` artifacts inside the run package
  - the packaged `run_metadata.json` for Mew-X now keeps the `session_summary` pointer present on fresh PR9 runs
- Promoted same-attempt label: `resume-after-pr9-20260321T1737`
- Promoted matched measurement window:
  - concurrent runtime start: `2026-03-21T08:39:25.571218Z`
  - concurrent runtime end: `2026-03-21T08:42:25.644005Z`
  - concurrent runtime duration: `180.073 s`
  - exact event overlap start: `2026-03-21T08:39:09.961841Z`
  - exact event overlap end: `2026-03-21T08:41:57.136Z`
  - exact event overlap duration: `167.174 s`
- Promoted startup and retry evidence:
  - `resume-after-pr9-20260321T1729` used a `60 s` Dexter quiet period and produced no Dexter startup HTTP 429, but Dexter first raw event landed `24.242 s` after the Mew-X stream had already ended
  - `resume-after-pr9-20260321T1737` reduced the quiet/settle gap to `20 s` / `10 s`, took `2` Dexter startup attempts, and recovered exact event overlap after one initial wallet-balance HTTP 429
  - `wsLogs` subscribed successfully on the promoted run, but still recorded `2` websocket-side `HTTP 429` lines before the stream stabilized
- Promoted package outputs:
  - Dexter package dir: `artifacts/tmp/winlan-packages-resume-after-pr9-20260321T1737/dexter-resume-after-pr9-20260321T1737`
  - Mew-X package dir: `artifacts/tmp/winlan-packages-resume-after-pr9-20260321T1737/mewx-resume-after-pr9-20260321T1737`
  - comparison output dir: `artifacts/reports/task-005-live-resume-after-pr9-20260321T1737-comparison`
  - comparison pack JSON: `artifacts/proofs/task-005-live-resume-after-pr9-20260321T1737-results/comparison-pack.json`
- Promoted validation coverage:
  - Dexter: `partial`, `4 / 12` required event types, `113868` total events
  - Mew-X: `partial`, `8 / 12` required event types, `54` total events
- `validate`, `derive-metrics`, and `build-pack` were rerun successfully on the promoted same-attempt pair.

## Comparison To Prior Fresh Pair

- Prior promoted same-attempt pair remained:
  - label: `resume-after-pr8-20260321T0801`
  - Dexter: `4 / 12` required event types
  - Mew-X: `9 / 12` required event types
  - exact event overlap duration: `115.985 s`
- Promoted `1737` pair versus `0801`:
  - Dexter stayed flat at `4 / 12`, even after a fresh PR9 recollection with a longer `167.174 s` exact overlap
  - Mew-X kept the restored `session_summary` export pointer, but event coverage regressed from `9 / 12` to `8 / 12`
  - the promoted PR9 pair still provides the GitHub-visible fresh same-attempt baseline after PR `#10` merged into `main`
  - winner / tie decisions still remain deferred because both packages still validate as `partial`

## Current Blocker

- `TASK-005` is no longer blocked by the Mew-X package export-pointer gap on the promoted same-attempt pair.
- `TASK-005` remains blocked on partial matched-pair coverage:
  - Dexter still lacks `candidate_rejected`, `entry_attempt`, `entry_fill`, `exit_fill`, `exit_signal`, `position_closed`, `run_summary`, and `session_update`
  - Mew-X still lacks `candidate_rejected`, `creator_candidate`, `entry_rejected`, and `run_summary`
- The sharper blocker on the fresh PR9 pair is evidence quality under safe modes:
  - Dexter `observe_live` with the zero-balance safety path still did not emit any attempt/fill/exit/run-summary classes on the promoted retry
  - Mew-X `sim_live` still did not emit `creator_candidate`, `entry_rejected`, or `run_summary`, and `candidate_rejected` dropped out again on the promoted retry
- Winner / tie decisions remain deferred for candidate sourcing, execution quality, exit quality, and replayability.
- `TASK-006` remains blocked until a matched pair supports non-partial validation or an explicitly approved safer Dexter paper-equivalent path can produce the missing execution/exit classes.
- Deferred next-task candidate only: if repeated `TASK-005` resume retries keep stalling on Dexter coverage, document and review a minimal Dexter paper-mode or paper-equivalent path before any `TASK-006` work. Keep analysis paper/sim-first, prefer Mew-X `sim` / `sim_live`, and keep Dexter on the observe-only / zero-balance safety path until a formal paper mode is confirmed.
