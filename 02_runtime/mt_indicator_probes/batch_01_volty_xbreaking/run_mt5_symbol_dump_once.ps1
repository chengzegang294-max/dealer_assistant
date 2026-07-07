param(
    [string]$InstallRoot = "",
    [string]$DataRootOverride = "",
    [string]$EnvironmentInventoryJson = "",
    [string]$EnvironmentSelector = "",
    [string]$OutDir = "",
    [int]$RunTimeoutSeconds = 120
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Step {
    param(
        [string]$Message
    )
    Write-Host ("[step] " + $Message)
}

function Get-LatestFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$PathPattern
    )
    Get-ChildItem -Path $PathPattern -ErrorAction SilentlyContinue |
        Where-Object { -not $_.PSIsContainer } |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
}

function Wait-ForNewArtifact {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Pattern,
        [Parameter(Mandatory = $true)]
        [datetime]$BaselineTime,
        [int]$TimeoutSeconds = 60
    )
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $latest = Get-LatestFile -PathPattern $Pattern
        if ($null -ne $latest -and $latest.LastWriteTime -gt $BaselineTime) {
            return $latest
        }
        Start-Sleep -Seconds 2
    }
    return $null
}

function Wait-ForProcessExit {
    param(
        [Parameter(Mandatory = $true)]
        [System.Diagnostics.Process]$Process,
        [int]$TimeoutSeconds = 120
    )
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $Process.Refresh()
        if ($Process.HasExited) {
            return $true
        }
        Start-Sleep -Seconds 2
    }
    return $false
}

function Copy-IfDifferent {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SourcePath,
        [Parameter(Mandatory = $true)]
        [string]$TargetPath
    )
    $targetDir = Split-Path -Parent $TargetPath
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    if (Test-Path $TargetPath) {
        $srcHash = (Get-FileHash -Algorithm SHA256 -Path $SourcePath).Hash
        $dstHash = (Get-FileHash -Algorithm SHA256 -Path $TargetPath).Hash
        if ($srcHash -eq $dstHash) {
            return "unchanged"
        }
        $stamp = Get-Date -Format "yyyyMMddTHHmmss"
        [System.IO.File]::Copy($TargetPath, ($TargetPath + ".backup_" + $stamp), $true)
    }
    [System.IO.File]::Copy($SourcePath, $TargetPath, $true)
    return "updated"
}

function Resolve-Mt5DataRoot {
    param(
        [Parameter(Mandatory = $true)]
        [string]$InstallRootValue,
        [string]$DataRootOverrideValue = ""
    )
    if ($DataRootOverrideValue) {
        $resolvedOverride = [System.IO.Path]::GetFullPath($DataRootOverrideValue)
        if (-not (Test-Path $resolvedOverride)) {
            throw "MT5 data root override not found: $resolvedOverride"
        }
        return $resolvedOverride
    }

    $metaQuotesRoot = Join-Path $env:APPDATA "MetaQuotes\Terminal"
    if (-not (Test-Path $metaQuotesRoot)) {
        throw "MetaQuotes terminal root not found: $metaQuotesRoot"
    }

    $normalizedInstallRoot = [System.IO.Path]::GetFullPath($InstallRootValue).TrimEnd("\").ToLowerInvariant()
    foreach ($candidate in Get-ChildItem -Path $metaQuotesRoot -Directory -ErrorAction SilentlyContinue) {
        $originPath = Join-Path $candidate.FullName "origin.txt"
        if (-not (Test-Path $originPath)) {
            continue
        }
        $origin = (Get-Content -Path $originPath -Raw -ErrorAction SilentlyContinue).Trim()
        if (-not $origin) {
            continue
        }
        $normalizedOrigin = [System.IO.Path]::GetFullPath($origin).TrimEnd("\").ToLowerInvariant()
        if ($normalizedOrigin -eq $normalizedInstallRoot) {
            return $candidate.FullName
        }
    }
    throw "MT5 data root not found for install root: $InstallRootValue"
}

function Get-InventoryStringValue {
    param(
        [AllowNull()]
        [object]$Value
    )
    if ($null -eq $Value) {
        return ""
    }
    return ([string]$Value).Trim()
}

function Test-EnvironmentSelectorMatch {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Selector,
        [Parameter(Mandatory = $true)]
        [AllowEmptyString()]
        [string]$CandidateValue,
        [bool]$AllowPrefix = $false
    )
    if (-not $CandidateValue) {
        return $false
    }
    if ($CandidateValue.Equals($Selector, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $true
    }
    if ($AllowPrefix -and $CandidateValue.StartsWith($Selector, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $true
    }
    return $false
}

function Resolve-Mt5InventorySelection {
    param(
        [Parameter(Mandatory = $true)]
        [string]$InventoryJsonPath,
        [Parameter(Mandatory = $true)]
        [string]$Selector,
        [Parameter(Mandatory = $true)]
        [AllowEmptyString()]
        [string]$InstallRootValue
    )
    if (-not (Test-Path $InventoryJsonPath)) {
        throw "environment inventory json not found: $InventoryJsonPath"
    }

    $inventoryText = Get-Content -Path $InventoryJsonPath -Raw -Encoding UTF8
    $inventory = $inventoryText | ConvertFrom-Json
    if ($null -eq $inventory -or $null -eq $inventory.items) {
        throw "environment inventory json has no items: $InventoryJsonPath"
    }

    $normalizedInstallRoot = ""
    if ($InstallRootValue) {
        $normalizedInstallRoot = [System.IO.Path]::GetFullPath($InstallRootValue).TrimEnd("\").ToLowerInvariant()
    }
    $matches = New-Object System.Collections.Generic.List[object]
    foreach ($item in $inventory.items) {
        $platformValue = Get-InventoryStringValue -Value $item.platform
        if ($platformValue.ToLowerInvariant() -ne "mt5") {
            continue
        }

        $originPathValue = Get-InventoryStringValue -Value $item.origin_path
        if ($normalizedInstallRoot -and $originPathValue) {
            $normalizedOriginPath = [System.IO.Path]::GetFullPath($originPathValue).TrimEnd("\").ToLowerInvariant()
            if ($normalizedOriginPath -ne $normalizedInstallRoot) {
                continue
            }
        }

        $fieldMatches = @(
            @{ name = "environment_label"; value = (Get-InventoryStringValue -Value $item.environment_label); allow_prefix = $false }
            @{ name = "data_root_hash"; value = (Get-InventoryStringValue -Value $item.data_root_hash); allow_prefix = $true }
            @{ name = "data_root"; value = (Get-InventoryStringValue -Value $item.data_root); allow_prefix = $false }
            @{ name = "origin_path"; value = $originPathValue; allow_prefix = $false }
            @{ name = "terminal_path"; value = (Get-InventoryStringValue -Value $item.terminal_path); allow_prefix = $false }
            @{ name = "server"; value = (Get-InventoryStringValue -Value $item.server); allow_prefix = $false }
            @{ name = "login"; value = (Get-InventoryStringValue -Value $item.login); allow_prefix = $false }
            @{ name = "access_server"; value = (Get-InventoryStringValue -Value $item.access_server); allow_prefix = $false }
            @{ name = "server_login"; value = ((Get-InventoryStringValue -Value $item.server) + "/" + (Get-InventoryStringValue -Value $item.login)).Trim("/"); allow_prefix = $false }
        )

        foreach ($fieldMatch in $fieldMatches) {
            if (Test-EnvironmentSelectorMatch -Selector $Selector -CandidateValue $fieldMatch.value -AllowPrefix $fieldMatch.allow_prefix) {
                $matches.Add([ordered]@{
                    data_root = Get-InventoryStringValue -Value $item.data_root
                    data_root_hash = Get-InventoryStringValue -Value $item.data_root_hash
                    origin_path = $originPathValue
                    environment_label = Get-InventoryStringValue -Value $item.environment_label
                    matched_field = $fieldMatch.name
                    matched_value = $fieldMatch.value
                    inventory_json = $InventoryJsonPath
                })
                break
            }
        }
    }

    if ($matches.Count -eq 0) {
        throw "no MT5 environment matched selector '$Selector' in inventory: $InventoryJsonPath"
    }
    if ($matches.Count -gt 1) {
        $descriptions = @()
        foreach ($match in $matches) {
            $descriptions += ($match.environment_label + " [" + $match.data_root_hash + "]")
        }
        throw ("environment selector matched multiple MT5 entries: " + [string]::Join("; ", $descriptions))
    }
    return $matches[0]
}

$batchDir = Split-Path -Parent $PSCommandPath
$projectRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $batchDir))
$archiveDir = Join-Path $projectRoot "12_tooling_runtime_archive\batch_02_mt_indicator_family"
$defaultInventoryPath = Join-Path $batchDir "environment_snapshots\mt_environment_inventory_latest.json"
$installRootExplicit = $PSBoundParameters.ContainsKey("InstallRoot")

$inventorySelection = $null
if (-not $DataRootOverride -and $EnvironmentSelector) {
    $inventoryJsonPath = $EnvironmentInventoryJson
    if (-not $inventoryJsonPath) {
        $inventoryJsonPath = $defaultInventoryPath
    }
    $selectionInstallRoot = ""
    if ($installRootExplicit) {
        $selectionInstallRoot = $InstallRoot
    }
    $inventorySelection = Resolve-Mt5InventorySelection -InventoryJsonPath $inventoryJsonPath -Selector $EnvironmentSelector -InstallRootValue $selectionInstallRoot
    if (-not $installRootExplicit -and $inventorySelection.origin_path) {
        $InstallRoot = $inventorySelection.origin_path
    }
    $DataRootOverride = $inventorySelection.data_root
}
if ([string]::IsNullOrWhiteSpace($InstallRoot)) {
    throw "InstallRoot is required. Pass -InstallRoot explicitly, or pass -EnvironmentSelector with an inventory entry that resolves origin_path."
}

$terminalExe = Join-Path $InstallRoot "terminal64.exe"
$dataRoot = Resolve-Mt5DataRoot -InstallRootValue $InstallRoot -DataRootOverrideValue $DataRootOverride
$commonFilesDir = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
$expertTarget = Join-Path $dataRoot "MQL5\Experts\MT5SymbolDumpProbe.ex5"
$runtimeIniPath = Join-Path $batchDir "_tmp_mt5_symbol_dump_runtime.ini"

if (-not $OutDir) {
    $OutDir = Join-Path $batchDir "environment_snapshots"
}

$expertSource = Join-Path $archiveDir "MT5SymbolDumpProbe.ex5"

if (-not (Test-Path $terminalExe)) {
    throw "terminal64.exe not found: $terminalExe"
}
if (-not (Test-Path $expertSource)) {
    throw "MT5SymbolDumpProbe.ex5 not found: $expertSource"
}

New-Item -ItemType Directory -Path $commonFilesDir -Force | Out-Null
New-Item -ItemType Directory -Path (Split-Path -Parent $expertTarget) -Force | Out-Null
New-Item -ItemType Directory -Path $OutDir -Force | Out-Null

Write-Step "Copy expert into data root"
Copy-IfDifferent -SourcePath $expertSource -TargetPath $expertTarget | Out-Null

$ini = @()
$ini += "[Tester]"
$ini += "Expert=MT5SymbolDumpProbe.ex5"
$ini += "Symbol=EURUSD"
$ini += "Period=H1"
$ini += "Model=0"
$ini += "FromDate=2025.01.01"
$ini += "ToDate=2025.01.02"
$ini += "ForwardMode=0"
$ini += "Optimization=0"
$ini += "OptimizationCriterion=0"
$ini += "Visual=0"
$ini += "ReplaceReport=1"
$ini += "ShutdownTerminal=1"
$ini += "Deposit=10000"
$ini += "Currency=USD"
$ini += "Leverage=100"
$ini += "ExecutionMode=0"
$ini += "UseLocal=1"

$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
[System.IO.File]::WriteAllText($runtimeIniPath, ($ini -join [Environment]::NewLine) + [Environment]::NewLine, $utf8NoBom)

$baseline = Get-Date
Write-Step "Run MT5 via /config"
$process = Start-Process -FilePath $terminalExe -ArgumentList ("/config:" + $runtimeIniPath) -PassThru
$exited = Wait-ForProcessExit -Process $process -TimeoutSeconds $RunTimeoutSeconds
if (-not $exited) {
    try { $process.Kill() | Out-Null } catch {}
    throw "MT5 symbol dump timed out after $RunTimeoutSeconds seconds"
}

Write-Step "Collect outputs from common files"
$mw = Wait-ForNewArtifact -Pattern (Join-Path $commonFilesDir "mt5_symbols_marketwatch__*.txt") -BaselineTime $baseline -TimeoutSeconds 60
$all = Wait-ForNewArtifact -Pattern (Join-Path $commonFilesDir "mt5_symbols_all__*.txt") -BaselineTime $baseline -TimeoutSeconds 60

if ($null -eq $mw -and $null -eq $all) {
    throw "no symbol dump outputs found in common files after run"
}

if ($null -ne $mw) {
    Copy-IfDifferent -SourcePath $mw.FullName -TargetPath (Join-Path $OutDir $mw.Name) | Out-Null
    Write-Host ("marketwatch: " + (Join-Path $OutDir $mw.Name))
}
if ($null -ne $all) {
    Copy-IfDifferent -SourcePath $all.FullName -TargetPath (Join-Path $OutDir $all.Name) | Out-Null
    Write-Host ("all_symbols: " + (Join-Path $OutDir $all.Name))
}
