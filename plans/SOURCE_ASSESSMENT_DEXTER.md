# Dexter Source Assessment Seed

## Current reading highlights
- Python bot with PostgreSQL-backed history and live session logic.
- README expects Python 3.8+, PostgreSQL, and `req.txt` install flow.
- `DexAI/trust_factor.py` computes creator-level metrics including trust factor and performance score.
- `Dexter.py` runs subscribe / market handling / leaderboard update loops.
- Session logic appears to combine price trend and tx momentum and uses reserved balance helpers.

## Assessment tasks
- map exact DB bootstrap and schema usage
- isolate event ingestion path from Helius/websocket to tradable mint/session state
- enumerate exit triggers and their precedence
- define what telemetry to add without changing strategy behavior
- define replayable artifacts required for profitability analysis
