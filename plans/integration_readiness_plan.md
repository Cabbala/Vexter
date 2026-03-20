# Integration Readiness Plan

## Goal

Delay bot integration until Dexter and Mew-X have been measured on the same contract and their winning components are attributable, replayable, and operationally safe.

## Stage 1: Contract Compliance

- implement normalized event writers for both source repos
- export masked config snapshots and source commit IDs
- verify Windows runtime paths for raw data, logs, replays, and DB exports
- pass a Vexter-side validation check that required event types exist

Exit criteria:

- both repos emit the required event schema
- both repos can produce metrics from the same catalog

## Stage 2: Source Comparison

- run isolated Dexter observation sessions
- run isolated Mew-X observation sessions
- fill the comparison matrix with the same measurement window
- identify the winning component in each of:
  - candidate sourcing
  - execution
  - exit quality
  - replayability

Exit criteria:

- one evidence-backed winner or tie is recorded for each comparison area

## Stage 3: Replay Validation

- extract raw artifacts from Windows
- reconstruct representative sessions offline
- measure live-versus-replay gap for entries and exits
- reject any component whose replay gap is too large to trust

Exit criteria:

- replayability grade is `full` or an explicitly accepted `partial`

## Stage 4: Integration Gate

Before any combined bot implementation:

- winning components are named and justified
- losing components are not silently carried over
- operational risks are documented
- remaining blind spots have explicit follow-up work

## Immediate Next Tasks

1. Add observational event writers to Dexter.
2. Add observational event writers to Mew-X.
3. Build a Vexter-side validator that checks contract completeness and metrics derivation.
