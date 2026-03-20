#!/usr/bin/env bash
set -euo pipefail

WIN_HOST="${1:-win-lan}"

cat <<'MSG'
[info] Recovering Windows runtime prerequisites, detached frozen source checkouts, and PostgreSQL on win-lan.
[info] This script does not change Dexter or Mew-X source logic; it restores only the TASK-005 runtime surface.
MSG

ssh "$WIN_HOST" powershell -NoProfile -Command - <<'PS'
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

$root = 'C:\Users\bot\quant\Vexter'
$downloadDir = "$root\downloads"
$toolsDir = "$root\tools"
$venvDir = "$root\venvs\dexter"
$pgHome = "$toolsDir\postgresql-17.9"
$pgData = "$root\data\postgres\portable17"
$pgLog = "$root\data\logs\postgresql-17.log"
$pgZip = "$downloadDir\postgresql-17.9-2-windows-x64-binaries.zip"
$pgZipUrl = 'https://get.enterprisedb.com/postgresql/postgresql-17.9-2-windows-x64-binaries.zip'
$dexterPath = "$root\sources\Dexter"
$mewxPath = "$root\sources\Mew-X"
$dexterCommit = '69de8b6ca57ca3d03025d85329c88aa4a167da34'
$mewxCommit = 'dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a'

$dirs = @(
  $root,
  "$root\artifacts\unified\comparison_inputs",
  "$root\data\logs",
  "$root\data\postgres",
  "$root\data\raw\dexter",
  "$root\data\raw\mewx",
  "$root\data\replays\dexter",
  "$root\data\replays\mewx",
  "$root\runtime\dexter\config",
  "$root\runtime\dexter\export",
  "$root\runtime\mewx\config",
  "$root\runtime\mewx\export",
  "$root\sources",
  $downloadDir,
  $toolsDir,
  "$root\venvs"
)
foreach ($dir in $dirs) {
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

$gitShellPaths = @('C:\Program Files\Git\bin')
$currentUserPath = [Environment]::GetEnvironmentVariable('Path', 'User')
foreach ($gitPath in $gitShellPaths) {
  if ($currentUserPath -notlike "*$gitPath*") {
    $currentUserPath = if ([string]::IsNullOrWhiteSpace($currentUserPath)) { $gitPath } else { "$currentUserPath;$gitPath" }
  }
}
[Environment]::SetEnvironmentVariable('Path', $currentUserPath, 'User')
$env:Path = "C:\Program Files\Git\bin;$env:USERPROFILE\.cargo\bin;$env:Path"

if (-not (Get-Command protoc -ErrorAction SilentlyContinue)) {
  winget install --id Google.Protobuf --accept-package-agreements --accept-source-agreements --disable-interactivity | Out-Null
}

$protoc = (Get-Command protoc -ErrorAction Stop).Source
$protocRoot = Split-Path (Split-Path $protoc -Parent) -Parent
$protocInclude = Join-Path $protocRoot 'include'
[Environment]::SetEnvironmentVariable('PROTOC', $protoc, 'User')
[Environment]::SetEnvironmentVariable('PROTOC_INCLUDE', $protocInclude, 'User')
[Environment]::SetEnvironmentVariable('INSTALL_DIR', $protocRoot, 'User')
$env:PROTOC = $protoc
$env:PROTOC_INCLUDE = $protocInclude
$env:INSTALL_DIR = $protocRoot

if (-not (Test-Path $pgZip)) {
  curl.exe -L $pgZipUrl -o $pgZip
}
if (-not (Test-Path $pgHome)) {
  Expand-Archive -LiteralPath $pgZip -DestinationPath $pgHome -Force
}

$binDir = Join-Path $pgHome 'pgsql\bin'
$shareDir = Join-Path $pgHome 'pgsql\share'
$psql = Join-Path $binDir 'psql.exe'
$pgCtl = Join-Path $binDir 'pg_ctl.exe'
$pgIsReady = Join-Path $binDir 'pg_isready.exe'
$initdb = Join-Path $binDir 'initdb.exe'
$pwFile = Join-Path $downloadDir 'postgres-password.txt'

Set-Content -Path $pwFile -Value 'admin123' -Encoding ASCII

if (-not (Test-Path (Join-Path $pgData 'PG_VERSION'))) {
  Remove-Item -Recurse -Force $pgData -ErrorAction SilentlyContinue
  New-Item -ItemType Directory -Force -Path $pgData | Out-Null
  & $initdb -D $pgData -U postgres -A password --pwfile=$pwFile -L $shareDir | Out-Null
}

$listener = Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort 5432 -State Listen -ErrorAction SilentlyContinue
if (-not $listener) {
  & $pgCtl -D $pgData -l $pgLog -w start | Out-Null
}

$env:PGPASSWORD = 'admin123'
$roleCheck = (& $psql -h 127.0.0.1 -p 5432 -U postgres -d postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='dexter_user';" | Out-String).Trim()
if ($roleCheck -ne '1') {
  & $psql -h 127.0.0.1 -p 5432 -U postgres -d postgres -c "CREATE ROLE dexter_user LOGIN PASSWORD 'admin123';" | Out-Null
}
foreach ($db in 'dexter_db', 'goldmine', 'vacation') {
  $exists = (& $psql -h 127.0.0.1 -p 5432 -U postgres -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$db';" | Out-String).Trim()
  if ($exists -ne '1') {
    & $psql -h 127.0.0.1 -p 5432 -U postgres -d postgres -c "CREATE DATABASE $db;" | Out-Null
  }
}
& $psql -h 127.0.0.1 -p 5432 -U postgres -d postgres -c "ALTER DATABASE dexter_db OWNER TO dexter_user;" | Out-Null

if (Test-Path "$dexterPath\.git") {
  git -C $dexterPath fetch origin codex/task-002-dexter-instrumentation --prune
} else {
  git clone https://github.com/Cabbala/Dexter.git $dexterPath | Out-Null
  git -C $dexterPath fetch origin codex/task-002-dexter-instrumentation --prune
}
if (Test-Path "$mewxPath\.git") {
  git -C $mewxPath fetch origin codex/task-003-mewx-instrumentation --prune
} else {
  git clone https://github.com/Cabbala/Mew-X.git $mewxPath | Out-Null
  git -C $mewxPath fetch origin codex/task-003-mewx-instrumentation --prune
}
git -C $dexterPath checkout --detach $dexterCommit | Out-Null
git -C $mewxPath checkout --detach $mewxCommit | Out-Null

if (-not (Test-Path "$venvDir\Scripts\python.exe")) {
  python -m venv $venvDir
}
& "$venvDir\Scripts\python.exe" -m pip install --upgrade pip | Out-Null
& "$venvDir\Scripts\python.exe" -m pip install -r "$dexterPath\req.txt" | Out-Null
& "$venvDir\Scripts\python.exe" "$dexterPath\database.py" | Out-Null

$report = [ordered]@{
  selected_root = $root
  postgres = [ordered]@{
    version = (& $psql --version)
    data_dir = $pgData
    log_path = $pgLog
    listener = (& $pgIsReady -h 127.0.0.1 -p 5432 -U postgres)
    process_count = (Get-Process postgres -ErrorAction SilentlyContinue | Measure-Object).Count
  }
  source_checkouts = [ordered]@{
    dexter = [ordered]@{
      path = $dexterPath
      commit = (git -C $dexterPath rev-parse HEAD).Trim()
      env_file = "$dexterPath\.env"
    }
    mewx = [ordered]@{
      path = $mewxPath
      commit = (git -C $mewxPath rev-parse HEAD).Trim()
      env_file = "$mewxPath\.env"
    }
  }
  tool_versions = [ordered]@{
    cargo = (& cargo --version)
    rustc = (& rustc --version)
    python = (& "$venvDir\Scripts\python.exe" --version)
    sh = (& where.exe sh | Select-Object -First 1)
    protoc = $protoc
  }
  mewx_build_env = [ordered]@{
    protoc = $env:PROTOC
    protoc_include = $env:PROTOC_INCLUDE
    install_dir = $env:INSTALL_DIR
  }
}
$report | ConvertTo-Json -Depth 6
PS
