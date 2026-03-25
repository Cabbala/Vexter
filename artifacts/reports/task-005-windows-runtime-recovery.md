# TASK-005 Windows Runtime Recovery

## Verified Runtime

- Checked at: `2026-03-25T18:12:38Z`
- Windows host: `DESKTOP-NNC6MPS` via `win-lan`
- Selected root: `C:\Users\bot\quant\Vexter`
- PostgreSQL: `psql (PostgreSQL) 17.9`
- Listener: `127.0.0.1:5432` accepting connections
- Dexter checkout: `C:\Users\bot\quant\Vexter\sources\Dexter` at `ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938`
- Mew-X checkout: `C:\Users\bot\quant\Vexter\sources\Mew-X` at `dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a`
- Dexter virtualenv Python: `Python 3.11.9`
- Cargo: `cargo 1.94.0 (85eff7c80 2026-01-15)`
- Rust: `rustc 1.94.0 (4a4ef493e 2026-03-02)`

## Notes

- Recovery is no longer the sharp blocker for TASK-005.
- The remaining blocker is comparison-readiness evidence: the fresh pass-grade-pair retries still validate only as `partial`.
- TASK-006 remains blocked until a pass-grade matched pair is collected.
