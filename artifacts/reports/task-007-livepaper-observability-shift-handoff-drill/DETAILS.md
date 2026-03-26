# TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-HANDOFF-DRILL

## 1. 目的

固定済み live-paper observability handoff template を、実際の outgoing / incoming handoff drill として再現し、sample handoff が追加推論なしで読めることを確認する。

## 2. 固定入力

- Latest merged Vexter `main`: PR `#63` commit `9c00b7917f80bfbc4c7a0334625dddc09d903aca`
- Latest merged checklist lane: PR `#61` commit `991efd2566dc0a51121c5c36e806fd0a215bcea6`
- Dexter merged `main`: PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Canonical contract: `specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md`
- Canonical runbook: `docs/livepaper_observability_operator_runbook.md`
- Canonical checklist: `docs/livepaper_observability_shift_checklist.md`
- Canonical handoff template: `docs/livepaper_observability_shift_handoff_template.md`

## 3. ドリルで確認すること

- current status が explicit か
- proof / report pointers が explicit か
- `omission` / `drift` / `partial_visibility` が explicit か
- manual stop-all / quarantine 状態が explicit か
- terminal snapshot 状態が explicit か
- normalized failure detail 状態が explicit か
- open questions が explicit か
- next-shift priority checks が explicit か
- absence が `false` / `none` で明示されているか

## 4. 制約

- no source logic changes
- no validator rule changes
- no comparison baseline reopen
- no new evidence collection
- keep source-faithful Dexter `paper_live` / Mew-X `sim_live` seam

## 5. 推奨次タスク

- `livepaper_observability_shift_handoff_ci_check`

