# TASK-008 Dexter v3.0.1 Upgrade Audit

## Decision

- Recommended path: selective cherry-pick / partial adoption only.
- Full upstream `FLOCK4H/Dexter` `v3.0.1` is not safe to adopt into the Dexter implementation currently pinned by Vexter.
- The upstream tag and the pinned fork commit have no Git merge-base in the fetched histories, so this audit is tree-to-tree and behavior-to-behavior, not a clean linear upgrade.

## Comparison Basis

- Vexter-pinned Dexter fork: `Cabbala/Dexter` `main` commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Upstream target: `FLOCK4H/Dexter` tag `v3.0.1` commit `1a31624906114150b4f05a0f8103af0ad383ebe7`
- Fork pin commit date: `2026-03-21T20:31:07+09:00`
- Upstream tag commit date: `2026-03-25T02:34:41+01:00`
- Git relation: `NO_MERGE_BASE`
- Direct diff summary: `36 files changed, 16187 insertions(+), 2968 deletions(-)`

## Why Full Adoption Is Unsafe

1. The Vexter seam is fork-specific.
   - The pinned fork explicitly implements `VEXTER_MODE=paper_live`, `VEXTER_OUTPUT_ROOT`, `VEXTER_RUNTIME_ROOT`, `VEXTER_RUN_ID`, and `DexLab/instrumentation.py` NDJSON/replay artifacts.
   - Upstream `v3.0.1` removes that fork-only instrumentation module and the fork tests that freeze it.

2. Upstream 3.0.1 changes control-plane ownership.
   - Upstream moves to a TUI/CLI-first app that edits `.env`, persists operator control state, publishes runtime snapshots, and exposes source-owned operator actions.
   - Vexter's bounded architecture keeps planner/router ownership at `prepare / start / status / stop / snapshot` with planner-owned `manual_latched_stop_all`.

3. Upstream 3.0.1 changes strategy and runtime semantics.
   - `Dexter.py` grows from `1370` to `6521` lines.
   - `DexAI/trust_factor.py` adds new creator-quality inputs such as failure clusters, rug ratios, migration ratios, and wallet reuse ratios.
   - New `dexter_strategy.py` adds profile-driven thresholds that would change candidate admission and exit behavior.

4. Upstream 3.0.1 has no `tests/` tree at the audited tag.
   - The fork pin ships `tests/test_paper_live.py`, `tests/test_vexter_instrumentation.py`, and `tests/test_wslogs.py`.
   - Those fork tests are the only direct regression guards for the Vexter seam in Dexter itself.

## Concrete Upstream-vs-Fork Diff Inventory

| Path | Status | Area | Classification | Adoption note |
| --- | --- | --- | --- | --- |
| `.env` | deleted | env bootstrap | adoptable with adaptation | Safe only if local `.env` materialization stays explicit. |
| `.env.example` | added | env bootstrap | safe to adopt directly | Reference sample only; no runtime effect by itself. |
| `.gitignore` | modified | repo hygiene | safe to adopt directly | No bounded seam effect. |
| `DexAI/trust_factor.py` | modified | creator scoring | unsafe / conflicts with Vexter seam | Changes leaderboard semantics and trust shaping. |
| `DexLab/__init__.py` | modified | package surface | adoptable with adaptation | Mostly export reshaping; still needs fork compatibility review. |
| `DexLab/common_.py` | modified | rpc/env helpers | adoptable with adaptation | Helper drift can be shimmed, but runtime callers changed too. |
| `DexLab/instrumentation.py` | deleted | fork observability contract | unsafe / conflicts with Vexter seam | Removes the fork's NDJSON/config/replay export surface. |
| `DexLab/market.py` | modified | historical ingestion | adoptable with adaptation | New phase2 hooks may help, but DB/export contract differs. |
| `DexLab/pump_fun/pump_swap.py` | modified | execution transport | unknown pending deeper runtime verification | High-risk path-sensitive send/sim behavior changes. |
| `DexLab/pump_swap_executor.py` | added | PumpSwap execution | unknown pending deeper runtime verification | Useful only after live/demo transport validation. |
| `DexLab/pump_swap_market.py` | added | PumpSwap market discovery | adoptable with adaptation | Potentially useful for migration visibility or demo research. |
| `DexLab/swaps.py` | modified | tx confirmation | unknown pending deeper runtime verification | Touches fill and wallet reconciliation assumptions. |
| `DexLab/utils.py` | modified | execution helpers | adoptable with adaptation | Helper changes are portable, but current callers diverge. |
| `DexLab/wsLogs.py` | modified | live log parsing | adoptable with adaptation | Parser/raw-event retention improvements are portable if observability contract stays intact. |
| `Dexter.py` | modified | runtime core | unsafe / conflicts with Vexter seam | Rewrites mode model, config ownership, operator surfaces, and session plumbing. |
| `README.md` | modified | docs | safe to adopt directly | Documentation only. |
| `blacklist.txt` | modified | runtime behavior | unsafe / conflicts with Vexter seam | Changes live candidate gating behavior. |
| `database.py` | modified | DB bootstrap | adoptable with adaptation | Could help phase2 ingestion, but schema expectations diverge. |
| `dexter_alerts.py` | added | alerts / operator controls | unsafe / conflicts with Vexter seam | Introduces source-owned notification and command surfaces. |
| `dexter_cli.py` | added | CLI control plane | unsafe / conflicts with Vexter seam | Source starts owning launch/config workflows. |
| `dexter_config.py` | added | config model | unsafe / conflicts with Vexter seam | Replaces fork `VEXTER_*` mode contract with new runtime model. |
| `dexter_data_store.py` | added | data layer alias | adoptable with adaptation | Thin entrypoint to phase2; useful only with compatible exports. |
| `dexter_logging.py` | added | utility leaf | safe to adopt directly | Standalone helper if kept isolated. |
| `dexter_mev.py` | added | MEV/live routing | unsafe / conflicts with Vexter seam | Extends live-send behavior beyond current bounded seam. |
| `dexter_migration_harness.py` | added | harness / migration | unknown pending deeper runtime verification | Valuable for experiments, not safe for baseline replacement. |
| `dexter_operator.py` | added | operator state | unsafe / conflicts with Vexter seam | Creates source-owned pause/force-sell/control files. |
| `dexter_phase2.py` | added | normalized replay/export layer | adoptable with adaptation | Interesting for research, but not compatible with fork NDJSON contract as-is. |
| `dexter_price.py` | added | utility / pricing | adoptable with adaptation | Portable only if current quote/fill semantics remain unchanged. |
| `dexter_strategy.py` | added | strategy profiles | unsafe / conflicts with Vexter seam | Explicit threshold and scoring drift. |
| `dexter_time.py` | added | utility leaf | safe to adopt directly | Standalone timestamp normalization helper. |
| `install_postgre.sh` | added | install helper | safe to adopt directly | Auxiliary script only. |
| `pyproject.toml` | added | packaging | safe to adopt directly | Packaging metadata only if kept inert in Vexter flow. |
| `settings.py` | modified | runtime thresholds | unsafe / conflicts with Vexter seam | Threshold and policy drift would invalidate frozen comparisons. |
| `tests/test_paper_live.py` | deleted | seam regression guard | unsafe / conflicts with Vexter seam | Removes paper-path guarantees Vexter relies on. |
| `tests/test_vexter_instrumentation.py` | deleted | seam regression guard | unsafe / conflicts with Vexter seam | Removes event/export contract coverage. |
| `tests/test_wslogs.py` | deleted | seam regression guard | unsafe / conflicts with Vexter seam | Removes mint-detection regression coverage used by the fork pin. |

## Area-Level Safe / Unsafe Matrix

| Area | Classification | Reason |
| --- | --- | --- |
| Packaging, install, doc leaf files | safe to adopt directly | `.env.example`, `.gitignore`, `README.md`, `install_postgre.sh`, `pyproject.toml`, and small utility leaves do not change bounded runtime semantics by themselves. |
| Parser, market, and export plumbing | adoptable with adaptation | `DexLab/wsLogs.py`, `DexLab/market.py`, `database.py`, `dexter_phase2.py`, and `dexter_data_store.py` may contain useful observational improvements, but only if the fork's `paper_live` mode, NDJSON contract, and replay surfaces remain intact. |
| Execution transport and swap paths | unknown pending deeper runtime verification | `DexLab/pump_fun/pump_swap.py`, `DexLab/swaps.py`, and PumpSwap executor additions change quote, send, fill, and migration behavior that Vexter currently treats as source-faithful and bounded. |
| Runtime control plane | unsafe / conflicts with Vexter seam | `Dexter.py`, `dexter_cli.py`, `dexter_config.py`, `dexter_operator.py`, and `dexter_alerts.py` move ownership of mode/config/control away from Vexter. |
| Strategy and scoring | unsafe / conflicts with Vexter seam | `DexAI/trust_factor.py`, `dexter_strategy.py`, `settings.py`, and `blacklist.txt` alter decision semantics and would invalidate the frozen comparison basis. |
| Fork-only instrumentation and tests | unsafe / conflicts with Vexter seam | Deleting `DexLab/instrumentation.py` and the fork tests breaks the exact observability contract Vexter uses for matched-pair collection, replay, and watchdog proofs. |

## Exact Vexter Integration Touchpoints

| Vexter touchpoint | Current assumption | Upstream impact |
| --- | --- | --- |
| `manifests/reference_repos.json:8-21` | Dexter source of truth is `Cabbala/Dexter` pinned to `ddeb18c...` | Any upstream move changes the declared frozen source and invalidates current audit references. |
| `manifests/windows_runtime.json:138-163` | Windows runtime points at `sources/Dexter` commit `ddeb18c...` and only requires `PRIVATE_KEY`, `HTTP_URL`, `WS_URL` | Upstream adds a new `.env`/runtime model and more config ownership, so bootstrap assumptions drift. |
| `templates/windows_runtime/dexter.env.example:14-33` | Dexter is driven by `VEXTER_RUNTIME_ROOT`, `VEXTER_OUTPUT_ROOT`, `VEXTER_MODE=paper_live`, `VEXTER_TRANSPORT_MODE` plus bounded demo refs | Upstream `paper`/`simulate`/`live` model does not preserve this exact contract. |
| `scripts/sync_reference_repos.sh:9-28` | Frozen repo sync checks out exact Dexter commit `ddeb18c...` | Full adoption requires pin and sync model rewrite. |
| `scripts/recover_windows_runtime.sh:24-136` | Recovery reinstalls `req.txt`, `database.py`, detached checkout, and current Dexter runtime shape | Upstream packaging and config model diverge; the recovery flow becomes stale. |
| `scripts/collect_matched_live_pair.py:19-30,200-212` | Default Dexter collection mode is `paper_live`, injected through `VEXTER_*` env vars | Upstream removes this exact mode/env handshake. |
| `config/planner_router/executor_profiles.json:3-15` | Vexter trusts pinned Dexter methods `_settings_snapshot`, reserve helpers, `set_trust_level`, `buy`, `sell`, `monitor_mint_session` | Upstream keeps some names but changes surrounding semantics and constructor/config ownership. |
| `vexter/planner_router/interfaces.py:14-23` | Public planner boundary is fixed at `prepare / start / status / stop / snapshot` | Upstream adds source-owned CLI/TUI/operator surfaces that sit outside this boundary. |
| `vexter/planner_router/transport.py:132-146` | Dexter transport spec is `execution_mode="paper_live"` with entrypoint `monitor_mint_session` | Upstream mode names and transport assumptions differ. |
| `config/planner_router/planner.json:8-10` | Global halt ownership is `manual_latched_stop_all` | Upstream operator controls risk creating competing stop/pause owners. |
| `vexter/planner_router/handoff_watchdog.py:392-433,666-685` | Watchdog asserts explicit `paper_live` / `sim_live` seam, exact Dexter commit, and visible `manual_latched_stop_all` fields | Full upstream adoption would immediately trip pin/seam/ownership drift checks. |
| `specs/PATTERN_A_DEMO_EXECUTOR_CUTOVER.md:31-75,106-113` | The first real demo slice is Dexter-only `paper_live`, with planner-owned `manual_latched_stop_all` and bounded adapter lifecycle | Upstream TUI/operator model conflicts with the fixed cutover boundary. |
| `scripts/run_demo_forward_supervised_run.py:141-151,222-225,299-300` | Repo-visible proofs already exercise the bounded `prepare / start / status / stop / snapshot` sequence against Dexter `paper_live` | Any upstream runtime swap must preserve those proof surfaces or Vexter loses its current acceptance evidence. |
| `docs/dexter_source_assessment.md:14-21,71-116` | Vexter's source map and replay interpretation are built around current fork modules and event surface | Upstream v3.0.1 changes the source map enough that the analysis docs become stale. |
| `README.md` task history across `TASK-005` to `TASK-007` | Comparison, replay, and demo planning all cite Dexter PR `#3` commit `ddeb18c...` and `paper_live` event coverage | Full adoption would invalidate the frozen baseline that all later Vexter tasks assume. |

## Planner / Runtime Invariant Check

| Invariant | Current status against upstream full adoption |
| --- | --- |
| Dexter-only `paper_live` bounded seam | fails |
| Frozen Mew-X `sim_live` | unchanged directly, but seam wording drifts |
| Planner boundary `prepare / start / status / stop / snapshot` | fails unless wrapped with a compatibility adapter |
| Planner-owned `manual_latched_stop_all` | high conflict risk from upstream operator controls |
| Fail-closed semantics | unclear under full upstream runtime/control changes |
| Funded-live prohibitions | degraded by upstream live/mainnet gating model unless Vexter wraps it tightly |

## Exact Risks

1. No-merge-base risk.
   - There is no merge-base between the Vexter pin and upstream `v3.0.1`; a straight merge/rebase path is unavailable.

2. Event-contract risk.
   - Vexter collection and replay depend on fork-only NDJSON events such as `creator_candidate`, `entry_signal`, `entry_fill`, `exit_fill`, `position_closed`, and `run_summary`.

3. Control-plane inversion risk.
   - Upstream source code starts owning `.env` edits, runtime snapshots, pause/blacklist/force-sell state, and dashboard surfaces.

4. Strategy drift risk.
   - Upstream creator scoring and strategy profiles change candidate selection and exit logic, which would invalidate Vexter's closed comparison baseline.

5. Test-gap risk.
   - The audited upstream tag has no `tests/` tree, while the Vexter pin has targeted seam tests.

6. Bootstrap drift risk.
   - Vexter's Windows recovery and sync scripts assume current `req.txt`, `database.py`, and current env shape.

## Recommended Upgrade Strategy

- Do not attempt a whole-repo upgrade from `ddeb18c...` to upstream `v3.0.1`.
- If any adoption is desired now, limit it to low-risk, low-value direct cherry-picks:
  - `.env.example`
  - `.gitignore`
  - `README.md`
  - `install_postgre.sh`
  - `pyproject.toml`
  - isolated leaf helpers such as `dexter_logging.py` and `dexter_time.py`
- Treat all runtime, strategy, and control-plane code as incompatible until a separate design decision explicitly reopens the Vexter seam.

## Next-Step Plan For Selective Adoption

1. Start from the current Dexter pin `ddeb18c...`, not from upstream `v3.0.1`.
2. Preserve these fork requirements unchanged:
   - `VEXTER_MODE=paper_live`
   - `DexLab/instrumentation.py`
   - `tests/test_paper_live.py`
   - `tests/test_vexter_instrumentation.py`
   - `tests/test_wslogs.py`
   - method set in `config/planner_router/executor_profiles.json`
3. If the goal is observational improvement only, prototype a compatibility port of:
   - `DexLab/wsLogs.py`
   - `DexLab/market.py`
   - `database.py`
   - selected `dexter_phase2.py` ideas
4. Keep the prototype behind the current fork contract:
   - same `paper_live` mode label
   - same NDJSON event types
   - same replay export roots
   - same planner-owned stop and snapshot behavior
5. Verify on both sides before any re-pin:
   - Dexter source tests
   - Vexter planner/router tests
   - matched-pair collection
   - replay validation / replay deepening
   - handoff watchdog and CI-gate proofs

## Final Recommendation

- Whole upstream `v3.0.1` adoption: `no`
- Small direct cherry-picks of non-runtime leaf files: `yes`
- Runtime or strategy cherry-picks: `not without a dedicated compatibility branch and fresh seam validation`

