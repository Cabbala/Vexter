# DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_REFRESH

## Goal
Promote a bounded `attestation_refresh` lane as the current source of truth after attestation record-pack regeneration, without fabricating regenerated current records, retry-gate reopen, or retry execution success.

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
- attestation refresh checklist
- attestation refresh decision surface
- next recommended step

## Honest Refresh Model
- `PASS`: every required record face has explicit refresh rules plus one current, fresh-enough regenerated locator sufficient to rerun record-pack regeneration and reopen retry-gate review honestly
- `FAIL/BLOCKED`: one or more record faces remain missing, stale, ambiguous, non-refreshable, or not usable enough for retry-gate review

## Required Refresh Face Detail
Each refresh face must make explicit:
- refresh owner
- refresh trigger
- minimum fresh evidence locator shape
- stale condition
- what makes the refreshed face usable for retry-gate review

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
The promoted lane remains fail-closed until fresh-enough current regenerated locators exist for every required face and the current attestation record-pack regeneration can be rerun honestly for retry-gate review.
