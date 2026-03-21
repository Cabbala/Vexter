# Comparison Collection Runbook

## Goal

Collect one Dexter run package and one Mew-X run package from the fixed Windows layout, then build the first Vexter-side comparison pack without modifying either source instrumentation.

Before launching either source on `win-lan`, populate the repo-root `.env` files described in [docs/windows_runtime_recovery.md](/Users/cabbala/Documents/vexter/task005-live-comparison-evidence/docs/windows_runtime_recovery.md). The fixed-root overrides below keep both frozen sources writing into `C:\Users\bot\quant\Vexter`.

Preflight the user-owned `.env` files before launch:

- `PRIVATE_KEY` must be a valid base58 Solana signing key, not the Helius URL `api-key` value.
- Mew-X must have `RPC_URL` populated explicitly; `HTTP_URL` alone is not consumed by the frozen runtime.

## Fixed Windows Roots

- `C:\Users\bot\quant\Vexter\data\raw\dexter`
- `C:\Users\bot\quant\Vexter\data\raw\mewx`
- `C:\Users\bot\quant\Vexter\runtime\dexter\config`
- `C:\Users\bot\quant\Vexter\runtime\dexter\export`
- `C:\Users\bot\quant\Vexter\runtime\mewx\config`
- `C:\Users\bot\quant\Vexter\runtime\mewx\export`
- `C:\Users\bot\quant\Vexter\data\replays\dexter`
- `C:\Users\bot\quant\Vexter\data\replays\mewx`
- `C:\Users\bot\quant\Vexter\data\logs\dexter`
- `C:\Users\bot\quant\Vexter\data\logs\mewx`

## Windows Packaging

Run the collector once per source. Provide the concrete event file and the run identity values you want frozen into the package metadata.

```powershell
powershell -ExecutionPolicy Bypass -File scripts\collect_comparison_package.ps1 `
  -Source dexter `
  -RunId dexter-20260321-window-a `
  -SourceCommit ddeb18c0dd21fa3a15d4a6a85573428f7d7ae938 `
  -Mode paper_live `
  -TransportMode ws `
  -StartedAtUtc 2026-03-21T01:00:00Z `
  -EndedAtUtc 2026-03-21T01:20:00Z `
  -EventFile C:\Users\bot\quant\Vexter\data\raw\dexter\dexter-20260321-window-a.ndjson
```

```powershell
powershell -ExecutionPolicy Bypass -File scripts\collect_comparison_package.ps1 `
  -Source mewx `
  -RunId mewx-20260321-window-a `
  -SourceCommit dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a `
  -Mode sim_live `
  -TransportMode grpc `
  -StartedAtUtc 2026-03-21T01:00:00Z `
  -EndedAtUtc 2026-03-21T01:20:00Z `
  -EventFile C:\Users\bot\quant\Vexter\data\raw\mewx\mewx-20260321-window-a.ndjson
```

The script creates a normalized run package under:

- `C:\Users\bot\quant\Vexter\artifacts\unified\comparison_inputs\dexter\<run-id>`
- `C:\Users\bot\quant\Vexter\artifacts\unified\comparison_inputs\mewx\<run-id>`

Each package contains:

- `run_metadata.json`
- `events.ndjson`
- `proof_manifest.json`
- copied `config/`, `exports/`, `replays/`, and `logs/` artifacts

## Fixed-Root Launch Overrides

Use these environment overrides when launching the frozen source checkouts so their observational artifacts land in the fixed Vexter root:

```powershell
$env:VEXTER_RUNTIME_ROOT = 'C:\Users\bot\quant\Vexter'
$env:VEXTER_OUTPUT_ROOT = 'C:\Users\bot\quant\Vexter'
```

## Mac-Side Validation And Pack Build

For a same-window retry from the Mac control plane, you can orchestrate the Windows launch and package copy in one step:

```bash
python scripts/collect_matched_live_pair.py \
  --duration-seconds 120 \
  --dexter-mode paper_live \
  --mewx-mode sim \
  --startup-delay-seconds 5 \
  --dexter-prestart-quiet-seconds 60 \
  --dexter-wslogs-ready-timeout-seconds 90 \
  --dexter-wslogs-settle-seconds 20 \
  --dexter-retry-backoff-seconds 90
```

This helper requests explicit Dexter `paper_live`, prefers `MODE=sim` for Mew-X, gives Mew-X a configurable prewarm window before Dexter starts, clears stale Dexter / `wsLogs` / Mew-X processes from prior attempts, and can insert a Dexter-side quiet period plus a Dexter head-start before `wsLogs` comes up so Helius startup pressure stays serialized. It records the measurement end after graceful stop so run-level finalizers have a chance to land, captures exact Dexter retry timing and `HTTP 429` evidence in the remote collection payload, and fails fast when either source exits before its first raw event. It then pushes the current collector script to `win-lan` and copies the packaged directories into local `artifacts/tmp/`.

After copying the two package directories into the Mac control plane, run:

```bash
python scripts/comparison_analysis.py validate \
  --package-dir /path/to/dexter-package
```

```bash
python scripts/comparison_analysis.py derive-metrics \
  --package-dir /path/to/mewx-package
```

```bash
python scripts/comparison_analysis.py build-pack \
  --dexter-package /path/to/dexter-package \
  --mewx-package /path/to/mewx-package \
  --output-dir artifacts/tmp/live-comparison-window-a
```

The output directory will contain:

- normalized validation JSON for each source
- derived metrics JSON for each source
- `comparison_matrix.json`
- `comparison_matrix.md`
- `comparison_pack.json`
- `summary.md`

## Guardrails

- Do not edit Dexter or Mew-X instrumentation while collecting comparison evidence.
- Use matched measurement windows whenever possible.
- If one source package validates as `partial`, record the gap and keep TASK-005 blocked.
- If only fixture/sample data is available, keep winner columns deferred and mark live comparison as pending.
