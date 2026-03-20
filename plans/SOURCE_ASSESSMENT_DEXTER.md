# Dexter Source Assessment

## Detailed Assessment

See `docs/dexter_source_assessment.md` for the file and function level review.

## Current Conclusions

- Dexter is strongest at creator scoring and adaptive exit management.
- Historical replay seeds already exist in PostgreSQL, especially through `stagnant_mints`.
- The main missing piece is a normalized event trail for live session decisions.

## Instrumentation Priority

- leaderboard snapshots and creator score attribution
- session admit or reject reasons
- entry quote, submission, and fill timing
- session checkpoints for MFE, MAE, and ladder state
- exit signal, exit fill, and realized-versus-peak gap

## Next Implementation Link

See `plans/dexter_instrumentation_plan.md`.
