# TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-CI-GATE

## 1. 目的
最新 GitHub-visible `main` では `TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-REGRESSION-PACK` まで完了し、
その結論は
- `executor_transport_livepaper_observability_regression_pack_passed`
- `transport_livepaper_observability_regression_pack_bounded`
- `recommended next step: transport_livepaper_observability_ci_gate`
で確定している。

したがって次は、新証拠の収集や comparison baseline の再評価ではなく、
**回帰検知対象として固定した live-paper observability surface を CI で常時守る gate に昇格させること**
が正しい次段。

## 2. 現在の source-of-truth
- Latest merged Vexter task: PR `#52`
- Dexter main pinned: `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938` (PR `#3`)
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## 3. 固定前提
- promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- comparison source of truth: `comparison_closed_out`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- confirmatory residual overturns promoted baseline: `no`

### 固定 regression conclusion
- immutable handoff metadata continuity is locked
- handle lifecycle continuity in status sink is locked
- ack-history retention is locked
- quarantine reason completeness is locked
- reverse-order `manual_latched_stop_all` propagation is locked
- snapshot-backed terminal detail completeness is locked
- normalized failure detail passthrough is locked
- remaining risk is no longer missing assertions, but making sure these checks are always enforced in CI

## 4. このタスクでやること
1. GitHub 上の最新 merged state を確認
2. regression-pack outputs を formal baseline として再確認
3. observability CI gate を追加 / 実行
4. 少なくとも以下を整備
   - regression-pack tests を明示的な CI gate / test grouping に固定
   - proof/report output が CI gate 実行時にも分かるように整理
   - failure時にどの observability surface が壊れたか即分かる構造にする
   - bootstrap / local CI / handoff bundle 側でも gate の存在が分かるように更新
5. tests / summary / context_pack / proof manifest / task ledger / report / handoff bundle を更新
6. 次タスクを
   - `livepaper_observability_spec`
   - `executor_boundary_code_spec`
   - `transport_livepaper_observability_watchdog`
   のどれに切るべきか evidence ベースで提案
7. branch → commit(s) → push → PR作成/更新 → 可能なら merge

## 5. 実務上の狙い
このタスクのゴールは、
**今の回帰検知面を“任意で回せるテスト群”から“標準で守られるCI品質ゲート”へ昇格させること**。

## 6. 不変条件
- Dexter strategy semantics / trust logic / thresholds は変更しない
- Mew-X source logic は変更しない
- validator rules の再変更はしない
- current frozen source pins は維持
- funded live trading はしない
- comparison baseline は reopen しない
- 新 evidence collection は行わない
- GitHub visible artifacts を source of truth にする
