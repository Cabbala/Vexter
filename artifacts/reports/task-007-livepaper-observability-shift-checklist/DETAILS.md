# TASK-007-LIVEPAPER-OBSERVABILITY-SHIFT-CHECKLIST

## 1. 目的

固定済み live-paper observability contract と operator runbook を、運用シフトでそのまま使える bounded checklist に落とし込む。

## 2. 固定入力

- Latest merged Vexter `main`: PR `#60` commit `ec46f051b41c3e140db09e808ef54e4d6e3d33ac`
- Dexter merged `main`: PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Canonical contract: `specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md`
- Canonical runbook: `docs/livepaper_observability_operator_runbook.md`

## 3. 必須 checklist 範囲

- pre-shift の確認順
- during-shift periodic review の確認順
- `omission` / `drift` / `partial_visibility` の即時分岐
- `halt` / `quarantine` / `continue` への action mapping
- manual stop-all / quarantine / terminal snapshot / normalized failure detail の扱い
- end-of-shift の proof trail と handoff 記録
- next-task recommendation

## 4. 制約

- no source logic changes
- no validator rule changes
- no comparison baseline reopen
- no new evidence collection
- keep source-faithful Dexter `paper_live` / Mew-X `sim_live` seam

## 5. 推奨次タスク

- `livepaper_observability_shift_handoff_template`
