# TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-WATCHDOG

## 1. 目的
最新 GitHub-visible `main` では `TASK-007-TRANSPORT-LIVEPAPER-OBSERVABILITY-CI-GATE` まで完了し、
その結論は
- `executor_transport_livepaper_observability_ci_gate_passed`
- `transport_livepaper_observability_ci_gate_bounded`
- `recommended next step: transport_livepaper_observability_watchdog`
で確定している。

したがって次は、新証拠の収集や comparison baseline の再評価ではなく、
**CI で守られる回帰面に加えて、運用寄りの partial visibility / drift / omission を早期検知する watchdog surface を追加すること**
が正しい次段。

## 2. 現在の source-of-truth
- Latest merged Vexter task: PR `#53`
- Dexter main pinned: `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938` (PR `#3`)
- Frozen Mew-X: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`

## 3. 固定前提
- promoted baseline: `task005-pass-grade-pair-20260325T180027Z`
- comparison source of truth: `comparison_closed_out`
- Dexter replay coverage / gap: `100.00%` / `0.0000`
- Mew-X replay coverage / gap: `100.00%` / `0.0000`
- confirmatory residual overturns promoted baseline: `no`

### 固定 CI-gate conclusion
- immutable handoff metadata continuity is CI-guarded
- handle lifecycle continuity in status sink is CI-guarded
- ack-history retention is CI-guarded
- quarantine reason completeness is CI-guarded
- reverse-order `manual_latched_stop_all` propagation is CI-guarded
- snapshot-backed terminal detail completeness is CI-guarded
- normalized failure detail passthrough is CI-guarded
- remaining risk is operational drift or partial visibility that may not present as a simple regression at code-review time

## 4. このタスクでやること
1. GitHub 上の最新 merged state を確認
2. CI-gate outputs を formal baseline として再確認
3. watchdog surface を追加 / 実行
4. 少なくとも以下を監視・検知対象として設計または実装
   - required observability field omission
   - partial status-sink fan-in
   - ack-history truncation or collapse
   - missing quarantine reason / stop reason / terminal snapshot detail
   - drift between planned metadata and runtime-visible metadata
5. tests / summary / context_pack / proof manifest / task ledger / report / handoff bundle を更新
6. 次タスクを
   - `livepaper_observability_spec`
   - `executor_boundary_code_spec`
   - `transport_livepaper_observability_watchdog_runtime`
   のどれに切るべきか evidence ベースで提案
7. branch → commit(s) → push → PR作成/更新 → 可能なら merge

## 5. 実務上の狙い
このタスクのゴールは、
**“壊れたら落ちるCI”に加えて、“壊れかけや見えなくなりかけ”を先に検知できる watchdog 面を整備すること**。

## 6. 不変条件
- Dexter strategy semantics / trust logic / thresholds は変更しない
- Mew-X source logic は変更しない
- validator rules の再変更はしない
- current frozen source pins は維持
- funded live trading はしない
- comparison baseline は reopen しない
- 新 evidence collection は行わない
- GitHub visible artifacts を source of truth にする
