# TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-HARDENING

## 1. 目的
最新 GitHub-visible `main` では `TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-RUNTIME` まで完了し、
その結論は
- `executor_transport_livepaper_observability_runtime_passed`
- `transport_livepaper_observability_runtime_bounded`
- `recommended next step: transport_livepaper_observability_hardening`
で確定している。

したがって次は、新証拠の収集や comparison baseline の再評価ではなく、
**live-paper seam で観測できている transport metadata / status / failure / stop information を、runtime-oriented path でも安定して欠落なく保持すること**
が正しい次段。

## 2. 現在の source-of-truth
- Latest merged Vexter task: PR `#49`
- Supporting merged Vexter states:
  - PR `#48`: transport_livepaper_observability_smoke alignment
  - PR `#47`: transport_livepaper_observability_smoke
  - PR `#46`: transport_livepaper_smoke
  - PR `#45`: transport_runtime_smoke
  - PR `#44`: planner_router_executor_transport_implementation
  - PR `#43`: planner_router_executor_transport_spec
  - PR `#42`: planner_router_livepaper_smoke
  - earlier task chain through PR `#17`
- Dexter main pinned: `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938` (PR `#3`)
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## 3. 固定前提
- promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- comparison source of truth: `comparison_closed_out`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- confirmatory residual overturns promoted baseline: `no`

### 固定 observability conclusion
- immutable handoff metadata is already traceable from planner-owned `planned` storage into prepared handles, runtime follow-up snapshots, and snapshot-backed terminal detail
- status sink fans in Dexter and Mew-X runtime progression while preserving quarantine reason, manual stop propagation, and failure passthrough
- remaining risk is not basic observability presence but observability stability / completeness across follow-up branches and duplicate/reconciled paths

## 4. このタスクでやること
1. GitHub 上の最新 merged state を確認
2. runtime observability outputs を formal baseline として再確認
3. observability hardening を bounded に追加 / 実行
4. 少なくとも以下を補強
   - immutable handoff metadata continuity が prepared handle / status / snapshot / failure detail で欠落しない
   - handle lifecycle / status sink snapshots の field completeness が維持される
   - first-vs-duplicate ack visibility が follow-up transitions 後も崩れない
   - quarantine reason / manual stop-all propagation / snapshot terminal detail が後段 state でも観測可能
   - normalized failure detail と rejection detail の source-faithful passthrough が hardening 後も維持される
5. tests / summary / context_pack / proof manifest / task ledger / report / handoff bundle を更新
6. 次タスクを
   - `livepaper_observability_spec`
   - `executor_boundary_code_spec`
   - `transport_livepaper_observability_regression_pack`
   のどれに切るべきか evidence ベースで提案
7. branch → commit(s) → push → PR作成/更新 → 可能なら merge

## 5. 実務上の狙い
このタスクのゴールは、
**見えている observability surface を “ある” 状態から “欠落しない” 状態へ進めること**。

## 6. 不変条件
- Dexter strategy semantics / trust logic / thresholds は変更しない
- Mew-X source logic は変更しない
- validator rules の再変更はしない
- current frozen source pins は維持
- funded live trading はしない
- comparison baseline は reopen しない
- 新 evidence collection は行わない
- GitHub visible artifacts を source of truth にする
