# DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK_REGENERATION

## Goal
Promote a bounded `attestation_record_pack_regeneration` lane as the current source of truth after attestation refresh, without fabricating retry-gate reopen, retry execution success, or any funded-live path.

## Boundary
- Dexter-only real demo slice
- `single_sleeve`
- `dexter_default`
- Dexter `paper_live`
- frozen Mew-X `sim_live`
- max active real demo plans = `1`
- max open positions = `1`
- explicit allowlist required
- small lot required
- bounded supervised window required
- external credential refs remain outside repo
- operator owner explicit
- venue / connectivity confirmation explicit
- bounded start criteria explicit
- allowlist / symbol / lot-size reconfirmation explicit
- `manual_latched_stop_all` visibility reconfirmation explicit
- terminal snapshot readability reconfirmation explicit
- Mew-X unchanged
- funded live forbidden

## Required Current Surfaces
- current status report
- current report
- current summary
- current proof json
- current handoff
- record-pack regeneration checklist
- record-pack regeneration decision surface
- canonical external evidence contract
- canonical external evidence manifest
- canonical external evidence gap proof / gap report / gap summary
- next recommended step

## Honest Regeneration Model
- `PASS`: refreshed locator rules produce a current, reviewable regenerated record pack sufficient to reopen retry-gate review honestly
- `FAIL/BLOCKED`: one or more regenerated faces remain missing, stale, ambiguous, or non-reviewable

## Required Regeneration Face Detail
Each regeneration face must make explicit:
- regeneration owner
- regeneration trigger
- minimum regenerated locator shape
- freshness inheritance or reset rule
- what makes the regenerated face reviewable enough

The lane must derive those fields from the canonical external-evidence validator instead of re-parsing older lane prose.

## Planner Boundary
- `prepare`
- `start`
- `status`
- `stop`
- `snapshot`
- `manual_latched_stop_all` remains planner-owned

## Out Of Scope
- no funded live trading
- no Mew-X real-demo expansion
- no cross-source handoff
- no source logic rewrite in Dexter or Mew-X
- no fake retry execution success
- no secret material committed to repo

## Result Model
The promoted lane remains fail-closed until every required face can inherit freshness from one current, reviewable bounded-window locator and the regenerated record pack can reopen retry-gate review honestly.
