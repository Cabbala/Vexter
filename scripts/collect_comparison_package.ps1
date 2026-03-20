param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("dexter", "mewx")]
    [string]$Source,

    [Parameter(Mandatory = $true)]
    [string]$RunId,

    [Parameter(Mandatory = $true)]
    [string]$SourceCommit,

    [Parameter(Mandatory = $true)]
    [ValidateSet("observe_live", "trade_live", "sim_live", "replay")]
    [string]$Mode,

    [Parameter(Mandatory = $true)]
    [ValidateSet("ws", "grpc", "rpc", "swqos", "mixed")]
    [string]$TransportMode,

    [Parameter(Mandatory = $true)]
    [string]$StartedAtUtc,

    [Parameter(Mandatory = $true)]
    [string]$EndedAtUtc,

    [Parameter(Mandatory = $true)]
    [string]$EventFile,

    [string]$RuntimeRoot = "C:\Users\bot\quant\Vexter",
    [string]$OutputRoot = "C:\Users\bot\quant\Vexter\artifacts\unified\comparison_inputs",
    [string]$ConfigSnapshot,
    [string]$ExportDir,
    [string]$ReplayDir,
    [string]$LogDir,
    [int]$HoursWindow = 6
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-DefaultSourcePaths {
    param([string]$SourceName, [string]$Root)

    return @{
        ConfigDir = Join-Path $Root ("runtime\" + $SourceName + "\config")
        ExportDir = Join-Path $Root ("runtime\" + $SourceName + "\export")
        ReplayDir = Join-Path $Root ("data\replays\" + $SourceName)
        LogDir    = Join-Path $Root ("data\logs\" + $SourceName)
    }
}

function Copy-WindowedFiles {
    param(
        [string]$SourcePath,
        [string]$DestinationPath,
        [datetime]$AnchorTime,
        [int]$Hours
    )

    $copied = @()
    if (-not (Test-Path $SourcePath)) {
        return $copied
    }

    $lowerBound = $AnchorTime.AddHours(-1 * $Hours)
    $upperBound = $AnchorTime.AddHours($Hours)
    Get-ChildItem -Path $SourcePath -File -Recurse |
        Where-Object { $_.LastWriteTimeUtc -ge $lowerBound -and $_.LastWriteTimeUtc -le $upperBound } |
        ForEach-Object {
            $target = Join-Path $DestinationPath $_.Name
            Copy-Item $_.FullName $target -Force
            $copied += $target
        }

    return $copied
}

function Select-LatestMatchingFile {
    param(
        [string]$SearchRoot,
        [string[]]$Patterns
    )

    if (-not (Test-Path $SearchRoot)) {
        return $null
    }

    $matches = foreach ($pattern in $Patterns) {
        Get-ChildItem -Path $SearchRoot -File -Recurse |
            Where-Object { $_.Name -match $pattern }
    }
    return $matches |
        Sort-Object LastWriteTimeUtc -Descending |
        Select-Object -First 1
}

function To-PackageRef {
    param(
        [string]$Bucket,
        [string]$LeafName
    )

    return $Bucket + "/" + $LeafName
}

if (-not (Test-Path $EventFile)) {
    throw "Event file not found: $EventFile"
}

$defaultPaths = Get-DefaultSourcePaths -SourceName $Source -Root $RuntimeRoot
if (-not $ExportDir) { $ExportDir = $defaultPaths.ExportDir }
if (-not $ReplayDir) { $ReplayDir = $defaultPaths.ReplayDir }
if (-not $LogDir) { $LogDir = $defaultPaths.LogDir }

$eventItem = Get-Item $EventFile
$anchorTime = $eventItem.LastWriteTimeUtc

if (-not $ConfigSnapshot) {
    $configCandidate = Get-ChildItem -Path $defaultPaths.ConfigDir -File -Recurse -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTimeUtc -Descending |
        Select-Object -First 1
    if ($configCandidate) {
        $ConfigSnapshot = $configCandidate.FullName
    }
}

$packageDir = Join-Path $OutputRoot ($Source + "\" + $RunId)
$configOut = Join-Path $packageDir "config"
$exportsOut = Join-Path $packageDir "exports"
$replaysOut = Join-Path $packageDir "replays"
$logsOut = Join-Path $packageDir "logs"
New-Item -ItemType Directory -Force -Path $configOut, $exportsOut, $replaysOut, $logsOut | Out-Null

$eventTarget = Join-Path $packageDir "events.ndjson"
Copy-Item $eventItem.FullName $eventTarget -Force

$configTarget = $null
if ($ConfigSnapshot -and (Test-Path $ConfigSnapshot)) {
    $configTarget = Join-Path $configOut (Split-Path $ConfigSnapshot -Leaf)
    Copy-Item $ConfigSnapshot $configTarget -Force
}

$exportFiles = Copy-WindowedFiles -SourcePath $ExportDir -DestinationPath $exportsOut -AnchorTime $anchorTime -Hours $HoursWindow
$replayFiles = Copy-WindowedFiles -SourcePath $ReplayDir -DestinationPath $replaysOut -AnchorTime $anchorTime -Hours $HoursWindow
$logFiles = Copy-WindowedFiles -SourcePath $LogDir -DestinationPath $logsOut -AnchorTime $anchorTime -Hours $HoursWindow

$sourceExports = @{}
if ($Source -eq "dexter") {
    $leaderboard = Select-LatestMatchingFile -SearchRoot $exportsOut -Patterns @("leaderboard")
    $replay = Select-LatestMatchingFile -SearchRoot $replaysOut -Patterns @("stagnant", "replay")
    if (-not $replay) {
        $replay = Get-ChildItem -Path $replaysOut -File -Recurse -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTimeUtc -Descending |
            Select-Object -First 1
    }
    if ($leaderboard) { $sourceExports["leaderboard_snapshot"] = To-PackageRef -Bucket "exports" -LeafName $leaderboard.Name }
    if ($replay) { $sourceExports["stagnant_mint_replay"] = To-PackageRef -Bucket "replays" -LeafName $replay.Name }
}
if ($Source -eq "mewx") {
    $refresh = Select-LatestMatchingFile -SearchRoot $exportsOut -Patterns @("candidate", "refresh")
    $session = Select-LatestMatchingFile -SearchRoot $exportsOut -Patterns @("session", "summary")
    if (-not $session) {
        $session = Get-ChildItem -Path $exportsOut -File -Recurse -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -notmatch "candidate|state" } |
            Sort-Object LastWriteTimeUtc -Descending |
            Select-Object -First 1
    }
    if ($refresh) { $sourceExports["candidate_refresh_snapshot"] = To-PackageRef -Bucket "exports" -LeafName $refresh.Name }
    if ($session) { $sourceExports["session_summary"] = To-PackageRef -Bucket "exports" -LeafName $session.Name }
}

$metadata = [ordered]@{
    run_id = $RunId
    source_system = $Source
    source_commit = $SourceCommit
    mode = $Mode
    transport_mode = $TransportMode
    host_role = "windows_runtime"
    runtime_root = $RuntimeRoot
    started_at_utc = $StartedAtUtc
    ended_at_utc = $EndedAtUtc
    event_stream = "events.ndjson"
    config_snapshot = if ($configTarget) { To-PackageRef -Bucket "config" -LeafName (Split-Path $configTarget -Leaf) } else { $null }
    proof_manifest = "proof_manifest.json"
    source_exports = $sourceExports
}

$proofManifest = [ordered]@{
    raw_events = @("events.ndjson")
    logs = @($logFiles | ForEach-Object { To-PackageRef -Bucket "logs" -LeafName (Split-Path $_ -Leaf) })
    replays = @($replayFiles | ForEach-Object { To-PackageRef -Bucket "replays" -LeafName (Split-Path $_ -Leaf) })
    db_exports = @($replayFiles | ForEach-Object { To-PackageRef -Bucket "replays" -LeafName (Split-Path $_ -Leaf) })
    exports = @($exportFiles | ForEach-Object { To-PackageRef -Bucket "exports" -LeafName (Split-Path $_ -Leaf) })
    config = if ($configTarget) { @(To-PackageRef -Bucket "config" -LeafName (Split-Path $configTarget -Leaf)) } else { @() }
}

$metadata | ConvertTo-Json -Depth 8 | Set-Content -Path (Join-Path $packageDir "run_metadata.json")
$proofManifest | ConvertTo-Json -Depth 8 | Set-Content -Path (Join-Path $packageDir "proof_manifest.json")

Write-Output $packageDir
