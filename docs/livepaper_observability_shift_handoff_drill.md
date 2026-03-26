# Live-Paper Observability Shift Handoff Drill

## Purpose

This drill exercises the fixed live-paper observability shift handoff template as one bounded outgoing and incoming operator workflow for the source-faithful Dexter `paper_live` and frozen Mew-X `sim_live` seam.
It does not authorize source changes, new evidence collection, comparison-baseline reopen, or funded live trading.

## Fixed Inputs

- Vexter merged `main`: PR `#63`, merge commit `9c00b7917f80bfbc4c7a0334625dddc09d903aca`
- Latest merged checklist lane: PR `#61`, merge commit `991efd2566dc0a51121c5c36e806fd0a215bcea6`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Canonical contract: `specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md`
- Canonical runbook: `docs/livepaper_observability_operator_runbook.md`
- Canonical checklist: `docs/livepaper_observability_shift_checklist.md`
- Canonical handoff template: `docs/livepaper_observability_shift_handoff_template.md`

## Drill Goal

Prove that the incoming operator can read the sample handoff without adding inference for:

- current status
- proof and report pointers
- `omission`, `drift`, and `partial_visibility`
- manual stop-all and quarantine state
- terminal snapshot state
- normalized failure detail state
- open questions
- next-shift priority checks

## Drill Shape

1. Read the fixed contract, runbook, checklist, and handoff template.
2. Read the drill report, status, proof summary, proof JSON, and sample handoff.
3. Confirm every required handoff face is explicit or marked `none`.
4. Confirm the sample handoff encodes absence as `false` or `none` instead of leaving fields implied.
5. Confirm the first deep proof remains the watchdog CI gate.

## Acceptance

- Every required handoff face is present.
- No face relies on "same as before" or other unstated carryover.
- `omission`, `drift`, and `partial_visibility` are each explicit.
- Manual stop-all, quarantine, terminal snapshot, and normalized failure detail are each explicit, using source-backed positive-case values where the fixed regression/runtime tests already preserve them.
- The next recommended step is `livepaper_observability_shift_handoff_ci_check`.
