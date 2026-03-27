# DEMO_FORWARD_SUPERVISED_RUN_RETRY_GATE_ATTESTATION_RECORD_PACK

## Goal
Promote a bounded `attestation_record_pack` lane as the current source of truth after retry-gate attestation audit, without fabricating retry-gate reopen or retry execution success.

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
- attestation record checklist
- attestation record pack decision surface
- next recommended step

## Honest Record-Pack Model
- `PASS`: every required record face is explicit enough and current enough to reopen retry-gate review honestly
- `FAIL/BLOCKED`: one or more record faces remain missing, stale, ambiguous, or not reviewable enough

## Required Record Face Detail
Each record face must make explicit:
- who owns the record
- what the record covers
- minimum evidence locator shape
- freshness requirement
- stale condition
- what makes the record reviewable enough

## Planner Boundary
- `prepare`
- `start`
- `status`
- `stop`
- `snapshot`

## Out Of Scope
- no funded live trading
- no Mew-X real-demo expansion
- no cross-source handoff
- no source logic rewrite in Dexter or Mew-X
- no fake retry execution success
- no secret material committed to repo

## Result Model
The promoted lane remains fail-closed until current record locators exist for every required face and retry-gate review can honestly reopen.
