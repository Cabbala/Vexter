# Fixed Workflow for Vexter

This workflow is fixed for future tasks unless explicitly changed.

## Source of truth
- GitHub is the source of truth for latest Vexter status.
- ChatGPT will inspect GitHub-visible changes after Codex work completes.

## Control rules
1. Codex starts from Mac local folder `~/Projects/Vexter`.
2. Git operations are always executed from the Mac control plane.
3. Runtime/data/db placement happens on Windows reachable by `ssh win-lan`.
4. Windows path selection must be discovered and created by Codex; target root should prefer `D:\\Quant\\Vexter\\` and fall back to a suitable user-space path.
5. Dexter/Mew-X analysis must remain reproducible and attributable.
6. Every task must end with Git operations completed where possible so GitHub reflects the latest inspectable state:
   - branch created or reused appropriately
   - commits made in logical units
   - push completed
   - PR created or updated if repo/phase is ready
7. If agent or sub-agent capabilities are available and help with repo audit, environment verification, multi-source validation, or implementation, Codex should use them proactively. If they are unavailable, Codex should continue and record that limitation in artifacts.
8. Codex completion output should stay minimal; detailed evidence goes into artifacts/bundles.
9. Future ChatGPT responses should continue using **minimal prompt + detailed tar.gz bundle**.
10. Future analysis and validation should prefer paper or sim-safe collection modes over funded live trading when those modes are available. Mew-X should default to `sim_live`; Dexter should stay on `observe_live` with a zero-balance safety path unless a formal paper mode is explicitly confirmed.

## Branching guidance
- Vexter research/bootstrap work should use feature branches in `Cabbala/Vexter`.
- If instrumentation is added to `Cabbala/Dexter` or `Cabbala/Mew-X`, use isolated feature branches in those repos and keep changes observational unless explicitly approved otherwise.

## End-of-task proof
Each Codex task should emit:
- `artifacts/context_pack.json`
- `artifacts/summary.md`
- `artifacts/proof_bundle_manifest.json`
- optional task-specific logs / metrics / diffs
