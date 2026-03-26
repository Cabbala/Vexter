# TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-REGRESSION-PACK

## 1. 目的
最新 GitHub-visible `main` では `TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-HARDENING` まで完了し、
その結論は
- `executor_transport_livepaper_observability_hardening_passed`
- `transport_livepaper_observability_hardening_bounded`
- `recommended next step: transport_livepaper_observability_regression_pack`
で確定している。

したがって次は、新証拠の収集や comparison baseline の再評価ではなく、
**hardening まで到達した live-paper observability surface を今後の transport 変更から守る regression pack を整備すること**
が正しい次段。

## 2. 現在の source-of-truth
- Latest merged Vexter task: PR `#51`
- Supporting merged Vexter states:
  - PR `#49`: transport_livepaper_observability_runtime
  - PR `#48`: transport_livepaper_observability_smoke alignment
  - PR `#47`: transport_livepaper_observability_smoke
  - PR `#46`: transport_livepaper_smoke
  - PR `#45`: transport_runtime_smoke
  - PR `#44`: planner_router_executor_transport_implementation
  - PR `#43`: planner_router_executor_transport_spec
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
- immutable handoff metadata is traceable from planner-owned `planned` storage into prepared handles, runtime status, reconciled push promotions, terminal snapshots, and rejection detail
- ack-history retention is now explicit and must stay observable after duplicate prepare/start/stop follow-up
- quarantine completeness, reverse-order manual stop-all propagation, snapshot-backed terminal detail, and normalized failure detail now survive runtime-oriented follow-up
- remaining risk is regression, not missing capability

## 4. このタスクでやること
1. GitHub 上の最新 merged state を確認
2. hardening outputs を formal baseline として再確認
3. regression pack を追加 / 実行
4. 少なくとも以下を回帰検知対象として固定
   - immutable handoff metadata continuity
   - handle lifecycle continuity in status sink
   - first-vs-duplicate ack-history retention
   - quarantine reason completeness
   - reverse-order `manual_latched_stop_all` propagation
   - snapshot-backed terminal detail completeness
   - normalized failure detail passthrough
5. tests / summary / context_pack / proof manifest / task ledger / report / handoff bundle を更新
6. 次タスクを
   - `livepaper_observability_spec`
   - `executor_boundary_code_spec`
   - `transport_livepaper_observability_ci_gate`
   のどれに切るべきか evidence ベースで提案
7. branch → commit(s) → push → PR作成/更新 → 可能なら merge

## 5. 実務上の狙い
このタスクのゴールは、
**今見えている observability surface を将来の transport 変更で壊さないための回帰防止壁を作ること**。

## 6. 不変条件
- Dexter strategy semantics / trust logic / thresholds は変更しない
- Mew-X source logic は変更しない
- validator rules の再変更はしない
- current frozen source pins は維持
- funded live trading はしない
- comparison baseline は reopen しない
- 新 evidence collection は行わない
- GitHub visible artifacts を source of truth にする
