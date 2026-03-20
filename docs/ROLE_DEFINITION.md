# Vexter Role Definition

## Purpose
Vexter is the control-plane repository for:
- comparative analysis of `Cabbala/Dexter` and `Cabbala/Mew-X`
- shared evaluation contracts and normalized artifacts
- research tooling and replay / profitability analysis
- minimal, evidence-based integration of winning components into a new unified bot

## Non-goals in the first phase
- Do not collapse Dexter and Mew-X into Vexter immediately.
- Do not rewrite both systems before measurement.
- Do not use the VPS as the primary development environment.
- Do not run Git operations from Windows.

## Fixed Environment Split
- **Mac (`~/Projects/Vexter`)**: Git control plane, Codex worktree, source-of-truth repo, docs, scripts, manifests.
- **Windows via `ssh win-lan`**: runtime workspace, Docker compose, PostgreSQL, collectors, replay data, long-running experiments.
- **VPS**: later-stage isolated validation only, not phase-0/1 main development.

## Repository Strategy
- Preserve `Cabbala/Dexter` and `Cabbala/Mew-X` as independent source repos.
- Create new repo `Cabbala/Vexter` as the analysis/integration mothership.
- Any extraction or instrumentation must remain attributable to the original repo during comparison phases.
