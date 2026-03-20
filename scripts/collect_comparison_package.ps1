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

    [string]$StartedAtUtc,

    [string]$EndedAtUtc,

    [Parameter(Mandatory = $true)]
    [string]$EventFile,

    [string]$RuntimeRoot = "C:\Users\bot\quant\Vexter",
    [string]$OutputRoot = "C:\Users\bot\quant\Vexter\artifacts\unified\comparison_inputs",
    [string]$ConfigSnapshot,
    [string]$ExportDir,
    [string]$ReplayDir,
    [string]$LogDir,
    [int]$HoursWindow = 6,
    [int]$MinutesPadding = 10
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

function Get-TimeBounds {
    param(
        [string]$StartedAt,
        [string]$EndedAt,
        [datetime]$AnchorTime,
        [int]$Hours,
        [int]$PaddingMinutes
    )

    $started = $null
    $ended = $null
    try {
        $started = [datetime]::Parse($StartedAt).ToUniversalTime()
    } catch {
    }
    try {
        $ended = [datetime]::Parse($EndedAt).ToUniversalTime()
    } catch {
    }

    if ($started -and $ended -and $ended -lt $started) {
        throw "EndedAtUtc must be greater than or equal to StartedAtUtc"
    }

    if ($started -and $ended) {
        return @{
            LowerBound = $started.AddMinutes(-1 * $PaddingMinutes)
            UpperBound = $ended.AddMinutes($PaddingMinutes)
        }
    }

    return @{
        LowerBound = $AnchorTime.AddHours(-1 * $Hours)
        UpperBound = $AnchorTime.AddHours($Hours)
    }
}

function Get-ScopedFiles {
    param(
        [string]$SearchRoot,
        [datetime]$LowerBound,
        [datetime]$UpperBound,
        [string]$RunId,
        [switch]$PreferRunId
    )

    if (-not (Test-Path $SearchRoot)) {
        return @()
    }

    $files = @(
        Get-ChildItem -Path $SearchRoot -File -Recurse |
            Where-Object { $_.LastWriteTimeUtc -ge $LowerBound -and $_.LastWriteTimeUtc -le $UpperBound } |
            Sort-Object LastWriteTimeUtc, FullName
    )

    if ($PreferRunId -and $RunId) {
        $runScoped = @($files | Where-Object { $_.Name -like "*$RunId*" })
        if ($runScoped.Count -gt 0) {
            return $runScoped
        }
    }

    return $files
}

function Copy-Files {
    param(
        [object[]]$Files,
        [string]$DestinationPath
    )

    $copied = @()
    foreach ($file in @($Files)) {
        $target = Join-Path $DestinationPath $file.Name
        Copy-Item $file.FullName $target -Force
        $copied += $target
    }

    return $copied
}

function Copy-EventStream {
    param(
        [string]$SourcePath,
        [string]$DestinationPath,
        [string]$StartedAt,
        [string]$EndedAt
    )

    $started = $null
    $ended = $null
    try {
        $started = [datetime]::Parse($StartedAt).ToUniversalTime()
    } catch {
    }
    try {
        $ended = [datetime]::Parse($EndedAt).ToUniversalTime()
    } catch {
    }

    if (-not $started -or -not $ended) {
        Copy-Item $SourcePath $DestinationPath -Force
        return
    }

    $selected = New-Object System.Collections.Generic.List[string]
    foreach ($line in [System.IO.File]::ReadLines($SourcePath)) {
        if ([string]::IsNullOrWhiteSpace($line)) {
            continue
        }

        try {
            $event = $line | ConvertFrom-Json -Depth 8
            $timestamp = [datetime]::Parse([string]$event.ts_utc).ToUniversalTime()
        } catch {
            continue
        }

        if ($timestamp -ge $started -and $timestamp -le $ended) {
            [void]$selected.Add($line)
        }
    }

    if ($selected.Count -eq 0) {
        throw "No events fell within the selected measurement window: $StartedAt -> $EndedAt"
    }

    [System.IO.File]::WriteAllLines($DestinationPath, $selected)
}

function Select-LatestMatchingFile {
    param(
        [string]$SearchRoot,
        [string[]]$Patterns,
        [string]$RunId
    )

    if (-not (Test-Path $SearchRoot)) {
        return $null
    }

    $files = @(
        Get-ChildItem -Path $SearchRoot -File -Recurse
    )
    if ($RunId) {
        $runScoped = @($files | Where-Object { $_.Name -like "*$RunId*" })
        if ($runScoped.Count -gt 0) {
            $files = $runScoped
        }
    }

    $matches = foreach ($pattern in $Patterns) {
        $files | Where-Object { $_.Name -match $pattern }
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
$timeBounds = Get-TimeBounds -StartedAt $StartedAtUtc -EndedAt $EndedAtUtc -AnchorTime $anchorTime -Hours $HoursWindow -PaddingMinutes $MinutesPadding

if (-not $ConfigSnapshot) {
    $configCandidates = @(Get-ScopedFiles -SearchRoot $defaultPaths.ConfigDir -LowerBound $timeBounds.LowerBound -UpperBound $timeBounds.UpperBound -RunId $RunId -PreferRunId)
    if ($configCandidates.Count -eq 0 -and (Test-Path $defaultPaths.ConfigDir)) {
        $configCandidates = @(
            Get-ChildItem -Path $defaultPaths.ConfigDir -File -Recurse -ErrorAction SilentlyContinue |
                Sort-Object LastWriteTimeUtc -Descending
        )
    }
    $configCandidate = $configCandidates | Select-Object -First 1
    if ($configCandidate) {
        $ConfigSnapshot = $configCandidate.FullName
    }
}

$packageDir = Join-Path $OutputRoot ($Source + "\" + $RunId)
$configOut = Join-Path $packageDir "config"
$exportsOut = Join-Path $packageDir "exports"
$replaysOut = Join-Path $packageDir "replays"
$logsOut = Join-Path $packageDir "logs"
if (Test-Path $packageDir) {
    Remove-Item -LiteralPath $packageDir -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $configOut, $exportsOut, $replaysOut, $logsOut | Out-Null

$eventTarget = Join-Path $packageDir "events.ndjson"
Copy-EventStream -SourcePath $eventItem.FullName -DestinationPath $eventTarget -StartedAt $StartedAtUtc -EndedAt $EndedAtUtc

$configTarget = $null
if ($ConfigSnapshot -and (Test-Path $ConfigSnapshot)) {
    $configTarget = Join-Path $configOut (Split-Path $ConfigSnapshot -Leaf)
    Copy-Item $ConfigSnapshot $configTarget -Force
}

$exportFiles = Copy-Files -Files (Get-ScopedFiles -SearchRoot $ExportDir -LowerBound $timeBounds.LowerBound -UpperBound $timeBounds.UpperBound -RunId $RunId -PreferRunId) -DestinationPath $exportsOut
$replayFiles = Copy-Files -Files (Get-ScopedFiles -SearchRoot $ReplayDir -LowerBound $timeBounds.LowerBound -UpperBound $timeBounds.UpperBound -RunId $RunId) -DestinationPath $replaysOut
$logFiles = Copy-Files -Files (Get-ScopedFiles -SearchRoot $LogDir -LowerBound $timeBounds.LowerBound -UpperBound $timeBounds.UpperBound -RunId $RunId -PreferRunId) -DestinationPath $logsOut

$sourceExports = @{}
if ($Source -eq "dexter") {
    $leaderboard = Select-LatestMatchingFile -SearchRoot $exportsOut -Patterns @("leaderboard") -RunId $RunId
    $replay = Select-LatestMatchingFile -SearchRoot $replaysOut -Patterns @("stagnant", "replay") -RunId $RunId
    if (-not $replay) {
        $replay = Get-ChildItem -Path $replaysOut -File -Recurse -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTimeUtc -Descending |
            Select-Object -First 1
    }
    if ($leaderboard) { $sourceExports["leaderboard_snapshot"] = To-PackageRef -Bucket "exports" -LeafName $leaderboard.Name }
    if ($replay) { $sourceExports["stagnant_mint_replay"] = To-PackageRef -Bucket "replays" -LeafName $replay.Name }
}
if ($Source -eq "mewx") {
    $refresh = Select-LatestMatchingFile -SearchRoot $exportsOut -Patterns @("candidate", "refresh") -RunId $RunId
    $session = Select-LatestMatchingFile -SearchRoot $exportsOut -Patterns @("session", "summary") -RunId $RunId
    if (-not $session) {
        $sessionCandidate = Get-ScopedFiles -SearchRoot $ExportDir -LowerBound $timeBounds.LowerBound -UpperBound $timeBounds.UpperBound -RunId $RunId
        $session = @($sessionCandidate | Where-Object { $_.Name -match "session|summary" } |
            Sort-Object LastWriteTimeUtc -Descending |
            Select-Object -First 1)
        if ($session) {
            $session = $session[0]
            $copiedSession = Join-Path $exportsOut $session.Name
            Copy-Item $session.FullName $copiedSession -Force
            $exportFiles += $copiedSession
            $session = Get-Item $copiedSession
        }
    }
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

$proofManifest = [ordered]@{}
$proofManifest["raw_events"] = @("events.ndjson")
$proofManifest["logs"] = @($logFiles | ForEach-Object { To-PackageRef -Bucket "logs" -LeafName (Split-Path $_ -Leaf) })
$proofManifest["replays"] = @($replayFiles | ForEach-Object { To-PackageRef -Bucket "replays" -LeafName (Split-Path $_ -Leaf) })
$proofManifest["db_exports"] = @($replayFiles | ForEach-Object { To-PackageRef -Bucket "replays" -LeafName (Split-Path $_ -Leaf) })
$proofManifest["exports"] = @($exportFiles | ForEach-Object { To-PackageRef -Bucket "exports" -LeafName (Split-Path $_ -Leaf) })
$proofManifest["config"] = if ($configTarget) { ,(To-PackageRef -Bucket "config" -LeafName (Split-Path $configTarget -Leaf)) } else { @() }

$metadata | ConvertTo-Json -Depth 8 | Set-Content -Path (Join-Path $packageDir "run_metadata.json")
$proofManifest | ConvertTo-Json -Depth 8 | Set-Content -Path (Join-Path $packageDir "proof_manifest.json")

Write-Output $packageDir
