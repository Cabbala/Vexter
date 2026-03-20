# TASK-000-bootstrap

## Objective
Bootstrap `Cabbala/Vexter` as the control-plane repository and prepare a seamless workflow that can:
- analyze Dexter and Mew-X individually
- store shared specs and tooling in Vexter
- place runtime workspaces on Windows via `ssh win-lan`
- keep Git operations on Mac
- make future task follow-up possible from GitHub-visible state

## Scope
- Create/init `~/Projects/Vexter` if needed.
- Create/init Git repo and connect it to `Cabbala/Vexter` if the repo exists.
- Scaffold Vexter repository structure.
- Add fixed workflow/spec docs from this bundle.
- Add Windows environment discovery/bootstrap scripts.
- Add source assessment placeholders for Dexter and Mew-X.
- Add a task ledger / artifact manifest pattern.
- Perform Git operations at the end.

## Deliverables
- committed scaffold in Vexter
- docs/specs/plans/scripts/artifacts layout
- Windows bootstrap/discovery script(s)
- source assessment docs for Dexter and Mew-X seeded with current findings
- PR or pushed branch visible on GitHub
- final artifact bundle path noted in repo artifacts

## Constraints
- Do not perform invasive rewrites of Dexter/Mew-X yet.
- Do not make Windows the Git source of truth.
- Do not use VPS as primary dev environment.
- Prefer observational/setup work only.
