#!/usr/bin/env bash
set -euo pipefail

WIN_HOST="${1:-win-lan}"

cat <<'MSG'
[info] Discovering and preparing Windows-side Vexter workspace via SSH.
[info] Git remains on Mac; Windows hosts detached source checkouts plus runtime, DB, logs, and replay data.
MSG

POWERSHELL_SCRIPT="$(cat <<'PS'
$ProgressPreference = 'SilentlyContinue'
$preferred = @(
  'D:\Quant\Vexter',
  ('C:\Users\' + $env:USERNAME + '\quant\Vexter')
)
$target = $null
foreach ($p in $preferred) {
  $parent = Split-Path $p -Parent
  if (Test-Path $parent) {
    $target = $p
    break
  }
}
if (-not $target) {
  $target = 'C:\Users\' + $env:USERNAME + '\quant\Vexter'
}
New-Item -ItemType Directory -Force -Path $target | Out-Null
$dirs = @(
  'runtime\dexter',
  'runtime\mewx',
  'runtime\unified',
  'runtime\unified\contracts',
  'runtime\unified\reports',
  'data\postgres',
  'data\logs',
  'data\replays',
  'data\raw',
  'artifacts',
  'artifacts\unified',
  'artifacts\unified\comparison_inputs',
  'downloads',
  'sources',
  'tools',
  'venvs'
)
foreach ($d in $dirs) {
  New-Item -ItemType Directory -Force -Path (Join-Path $target $d) | Out-Null
}
Write-Output $target
PS
)"

ENCODED_COMMAND="$(printf '%s' "$POWERSHELL_SCRIPT" | iconv -f UTF-8 -t UTF-16LE | base64 | tr -d '\n')"

ssh "$WIN_HOST" "powershell -NoProfile -EncodedCommand $ENCODED_COMMAND"
