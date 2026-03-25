# TASK-005-VALIDATOR-RULE-REVIEW

## Scope

This review turns the merged contract-audit conclusion into an approval-grade validator rule review / exception memo. It does not change frozen Dexter or Mew-X source logic, does not change comparison rules in code, and does not recollect the same matched pair again. Instead, it uses the current GitHub-visible promoted and confirmatory proofs to document which validator requirements still mismatch frozen-source reality and what proposal-level rule treatment is evidence-based.

## Verified GitHub State

- Latest merged Vexter `main`: PR `#18`, merge commit `b7c8cb900ced104f4fe76cfd9ca48c2b21b82d81`, merged at `2026-03-25T18:57:55Z`
- Supporting merged Vexter states: PR `#17` `b09033d6c8ce21510da23025cee935e46f3ef4df`, PR `#16` `b71b5f744027024e2a04606f6c1aa369d0a6c3e3`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`, merged at `2026-03-21T11:31:07Z`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`, reverified on GitHub at `2026-03-20T16:05:19Z`

## Current Contract Boundary

- `vexter/comparison/constants.py` still includes `creator_candidate`, `entry_rejected`, and `run_summary` inside `REQUIRED_EVENT_TYPES`.
- `vexter/comparison/validator.py` still marks a run package `partial` whenever any required event type is missing.
- The merged contract audit already proved that packaging is not the main issue here because both supporting collections used `full_stream_fallback`.

This review therefore answers a narrower approval question: under the current frozen-source reality, which of the remaining missing events should stay always-required, which should become conditional, and which should become source-specific exceptions?

## Supporting Evidence

### Promoted pair

- Label: `task005-pass-grade-pair-20260325T180027Z`
- Dexter: `10 / 12`, missing `entry_rejected`, `run_summary`
- Mew-X: `9 / 12`, missing `creator_candidate`, `entry_rejected`, `run_summary`
- Packaging mode: `full_stream_fallback` on both sides
- Shutdown result: both source processes exited with `3221225786` (`0xC000013A`)

### Confirmatory pair

- Label: `task005-pass-grade-pair-20260325T180604Z`
- Dexter: `10 / 12`, missing `entry_rejected`, `run_summary`
- Mew-X: `8 / 12`, missing `candidate_rejected`, `creator_candidate`, `entry_rejected`, `run_summary`
- Packaging mode: `full_stream_fallback` on both sides
- Extended grace: `60` seconds still did not recover `run_summary`

This memo stays scoped to the three residual event classes already isolated by the merged audit: `run_summary`, `entry_rejected`, and Mew-X `creator_candidate`.

## Event Review

| Event | Frozen-source reality | Evidence | Taxonomy | Preferred contract treatment |
| --- | --- | --- | --- | --- |
| `run_summary` | Finalizer-only on Dexter and Mew-X | Both supporting collections ended through `CTRL_BREAK_EVENT`; both copied state exports stayed `running` with `ended_at_utc: null` even though `full_stream_fallback` copied the full raw stream | `shutdown_success_dependent` | Remove from the always-required matched-pair gate; require it only when clean shutdown completion is proven, or reserve it for replayability / integration evidence |
| `entry_rejected` | Failure-path-only on both frozen sources | Promoted pair had Dexter `4` fills and Mew-X `6` fills with zero rejects on both sides | `failure_path_only` | Require only when an entry failure actually occurs; otherwise treat as observed-if-present evidence, not a healthy success-path gate |
| `creator_candidate` on Mew-X | Emitted only from non-empty initial-selection or refresh-addition reports | Promoted initial and refresh candidate snapshots both exported `observations: []` and `source_counts: {}` while the same run still emitted fills and closed positions | `source_specific_conditional` | Require only when Mew-X candidate snapshots are non-empty; otherwise treat as Mew-X-specific optional evidence rather than a source-agnostic hard requirement |

## Source-Level Basis

### `run_summary`

- Dexter emits `run_summary` inside `DexLab/instrumentation.py` `finalize()`, and `Dexter.close()` is the path that calls `self.instrumentation.finalize()`.
- Frozen Mew-X emits `run_summary` inside `src/mew/instrumentation.rs` `finalize()`.
- Frozen Mew-X calls `finalize()` on `ctrl_c` and after the main `join!`, which means the event still depends on orderly finalization rather than ordinary mid-run activity.
- Because the packager already used `full_stream_fallback`, the missing event is absent from the copied raw streams themselves, not merely from the PowerShell window filter.

Conclusion: `run_summary` is not healthy-run business logic evidence. It is shutdown-success evidence.

### `entry_rejected`

- Dexter records `entry_rejected` only on failed buy paths such as missing bonding curve, insufficient balance, migrated curve, zero quote, creator vault unavailable, price-too-high, or confirmation failure.
- Frozen Mew-X records `entry_rejected` only when `buy_result.success` is false, with the current frozen reason path labeled `transport_send_failed`.
- The promoted pair already demonstrated successful fill and close behavior on both sides without any `entry_rejected`.

Conclusion: keeping `entry_rejected` as always-required forces failure-path evidence into healthy matched pairs.

### `creator_candidate` on Mew-X

- Frozen Mew-X builds `CandidateSelectionReport` from creator observations and source counts.
- `src/main.rs` exports an initial candidate snapshot and emits `creator_candidate` only from `candidate_report.observations`.
- `refresh_creators_loop()` exports refresh snapshots and emits additional `creator_candidate` events only for added observation keys.
- The promoted candidate snapshots were empty in both initial and refresh exports, yet the same run still produced `mint_observed`, `entry_fill`, `exit_fill`, and `position_closed`.

Conclusion: for frozen Mew-X, `creator_candidate` is not universally dependable even in otherwise rich comparable runs.

## Rule-Change Candidates

These are proposal-level candidates only. This task does not apply them.

### Candidate set A: preferred

1. Reclassify `run_summary` from always-required to conditional, triggered only by proof of clean shutdown completion, or move it to replayability / integration-ready review instead of comparable-pass review.
2. Reclassify `entry_rejected` from always-required to conditional, triggered only when an `entry_attempt` fails or a source explicitly reports an entry failure outcome.
3. Reclassify Mew-X `creator_candidate` from source-agnostic always-required to source-specific conditional, triggered only when candidate snapshot exports contain observations.

Why this is preferred:

- It matches the frozen-source evidence already captured on GitHub.
- It avoids forcing helper quality, failure paths, and source-specific candidate plumbing into one blanket pass gate.
- It preserves the evidence when present without pretending those events are universally collectible.

### Candidate set B: strict alternative

1. Keep `run_summary` hard-required, but only after helper shutdown success conditions are formalized and validated.
2. Keep `entry_rejected` and Mew-X `creator_candidate` outside the always-required gate for healthy matched-pair validation.

Why this is not enough by itself:

- It still requires a separate helper-hardening task before `run_summary` becomes dependable.
- It does not solve the contract mismatch for the other two events without the same conditional / source-specific treatment described above.

## Decision

### Selected outcome

- `A`

### Key finding

- `rule memo ready`

### What is now ready

- Approval review for validator rule changes
- A narrow implementation task that applies only the approved requirement relaxation / conditional rule / source-specific exception set

### What is not yet ready

- `TASK-006`
- Any unapproved validator rule edits

## Recommended Next Step

- Open approval on this memo.
- If approved, start a dedicated validator rule implementation task without changing source logic.
- Treat any helper-side follow-up as a separate optional task limited to `run_summary` shutdown hygiene.
