# TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-TEMPLATE

## 1. 目的

固定済み live-paper observability contract / operator runbook / shift checklist を、シフト交代でそのまま引き継げる bounded handoff template に落とし込む。

## 2. 固定入力

- Latest merged Vexter `main`: PR `#62` commit `3b595faacf316aca89655b6e1ffcf7568478763e`
- Latest merged checklist lane: PR `#61` commit `991efd2566dc0a51121c5c36e806fd0a215bcea6`
- Dexter merged `main`: PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Canonical contract: `specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md`
- Canonical runbook: `docs/livepaper_observability_operator_runbook.md`
- Canonical checklist: `docs/livepaper_observability_shift_checklist.md`

## 3. 必須 handoff 面

- current status
- proof / report / proof-summary / proof-json pointers
- `omission` / `drift` / `partial_visibility` の有無と要約
- manual stop-all / quarantine 状態
- terminal snapshot の有無
- normalized failure detail の有無
- open questions
- next-shift priority checks
- bounded handoff completeness criteria

## 4. 制約

- no source logic changes
- no validator rule changes
- no comparison baseline reopen
- no new evidence collection
- keep source-faithful Dexter `paper_live` / Mew-X `sim_live` seam

## 5. 推奨次タスク

- `livepaper_observability_shift_handoff_drill`
