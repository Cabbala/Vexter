# TASK-007-LIVEPAPER-OBSERVABILITY-OPERATOR-RUNBOOK

## 1. 目的

固定済み live-paper observability contract を、運用者が bounded に読んで判断できる operator runbook に落とし込む。

## 2. 固定入力

- Latest merged Vexter `main`: PR `#59` commit `4be21e4e52fbe686e585dea6b573efea759e0933`
- Dexter merged `main`: PR `#3` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- Comparison source of truth: `comparison_closed_out`
- Canonical contract: `specs/LIVEPAPER_OBSERVABILITY_CONTRACT.md`

## 3. 必須 runbook 範囲

- status / report / proof の確認順
- watchdog CI gate から入る incident localization 順
- `omission` / `drift` / `partial_visibility` の解釈
- failure surface の優先順位
- ack-history の読み方
- manual stop-all / quarantine / terminal snapshot / normalized failure detail の運用判断
- halt / continue / inspect more deeply の bounded guidance
- next-task recommendation

## 4. 制約

- no source logic changes
- no validator rule changes
- no comparison baseline reopen
- no new evidence collection
- keep source-faithful Dexter `paper_live` / Mew-X `sim_live` seam

## 5. 推奨次タスク

- `livepaper_observability_shift_checklist`
