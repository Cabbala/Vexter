# Demo Forward Acceptance Pack

This document fixes the bounded forward-acceptance surface for the first supervised Dexter-only real-demo slice after `DexterDemoExecutorAdapter` landed on GitHub-visible `main`.

## Verified Base

- Latest merged Vexter `main`: PR `#71`, merge commit `5c1feb2561da7b16a17c5d03b71ff2bf895e20e4`, merged at `2026-03-27T00:09:27Z`
- Dexter merged `main`: PR `#3`, merge commit `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Frozen Mew-X commit: `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Demo adapter source of truth: `vexter/planner_router/transport.py`
- Demo adapter proof of implementation: `artifacts/proofs/demo-executor-adapter-implementation-check.json`

## Purpose

The concrete Dexter demo adapter now exists. The next shortest lane is therefore not more adapter expansion. It is fixing the bounded acceptance, operator, proof, and handoff surfaces required before a supervised forward demo run can begin.

## Planner Boundary Remains Fixed

The public planner surface remains:

- `prepare`
- `start`
- `status`
- `stop`
- `snapshot`

Planner ownership remains unchanged:

- immutable plan emission
- `poll_first` reconciliation
- `manual_latched_stop_all`
- quarantine classification
- normalized failure detail fan-in

Adapter-owned runtime detail remains unchanged:

- source-native demo submit
- source-native cancel
- order status polling
- fill collection
- stop-all fanout and terminal snapshot detail

## Acceptance Boundary

The first supervised forward slice remains narrowly bounded:

- Dexter-only real demo slice
- Dexter `paper_live` only
- frozen Mew-X `sim_live` only
- `single_sleeve` route only
- `dexter_default` sleeve only
- max active real demo plans = `1`
- max open positions = `1`
- explicit allowlist required
- small lot required
- bounded operator-supervised window required
- Mew-X overlay disabled / unchanged
- funded live forbidden

## Required Current Surfaces

The repo must expose the following as current source of truth:

- current status report
- current report
- current summary
- current proof json
- current handoff
- current operator checklist
- current abort / rollback matrix
- next recommended step

## Acceptance Sequence

The required sequence is:

1. `prepare`
2. `start`
3. entry visibility
4. order status / fill reconciliation
5. cancel or stop-all visibility
6. terminal snapshot
7. normalized failure detail and handoff continuity

## Required Proof Faces

The bounded proof surface must show:

- verified merged base on Vexter `main`
- unchanged Dexter pin and frozen Mew-X pin
- planner boundary preserved at `prepare / start / status / stop / snapshot`
- Dexter-only demo route and unchanged Mew-X seam
- explicit operator checklist pointer
- explicit abort / rollback matrix pointer
- explicit current report / status / proof / handoff pointers
- next task recommendation advanced to `demo_forward_supervised_run`

## Abort Conditions

Abort or rollback remains mandatory on:

- pin mismatch
- mode mismatch
- status or fill reconciliation gap
- duplicate or ambiguous handle
- unexpected funded live path
- cancel or stop-all unconfirmed
- quarantine or manual halt triggered
- terminal snapshot visibility lost

## Out Of Scope

- no funded live trading
- no Mew-X real-demo expansion
- no cross-source handoff
- no portfolio split
- no new comparison investigation
- no source logic rewrite in Dexter or Mew-X

## Recommended Next Task

`demo_forward_supervised_run`

This acceptance pack does not execute the supervised run. It fixes the bounded operator and proof surfaces required before that lane can start.
