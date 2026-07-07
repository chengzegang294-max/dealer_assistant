param(
    [string]$InstallRoot = "",
    [string]$DataRootOverride = "",
    [string]$EnvironmentInventoryJson = "",
    [string]$EnvironmentSelector = "",
    [string]$Symbol = "EURUSD",
    [ValidateSet("M1", "M5", "M15", "M30", "H1", "H4", "D1")]
    [string]$ChartPeriod = "H1",
    [string]$IndicatorPeriod = "",
    [string]$FromDate = "2025.01.01",
    [string]$ToDate = "2025.01.15",
    [string]$IndicatorName = "XBreaking",
    [int]$BarsToProbe = 200,
    [int]$MaxBuffers = 8,
    [string]$ReportStem = "xbreaking_probe_portable",
    [string]$ArchiveTag = "",
    [int]$RunTimeoutSeconds = 180
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not $IndicatorPeriod) {
    $IndicatorPeriod = $ChartPeriod
}

function Write-Step {
    param(
        [string]$Message
    )
    Write-Host ("[step] " + $Message)
}

function Format-Bool {
    param(
        [bool]$Value
    )
    if ($Value) {
        return "true"
    }
    return "false"
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
        [int]$TimeoutSeconds = 120
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
        [int]$TimeoutSeconds = 180
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

function Resolve-Mt5EnvironmentMetadata {
    param(
        [Parameter(Mandatory = $true)]
        [string]$DataRoot,
        [Parameter(Mandatory = $true)]
        [string]$InstallRootValue
    )

    $configPath = Join-Path $DataRoot "Config\common.ini"
    $login = ""
    $server = ""
    $accountMode = ""
    if (Test-Path $configPath) {
        foreach ($line in Get-Content -Path $configPath -ErrorAction SilentlyContinue) {
            if (-not $login -and $line -match "^Login=(.+)$") {
                $login = $Matches[1].Trim()
                continue
            }
            if (-not $server -and $line -match "^Server=(.+)$") {
                $server = $Matches[1].Trim()
                continue
            }
            if (-not $accountMode -and $line -match "^Account=(.+)$") {
                $accountMode = $Matches[1].Trim()
                continue
            }
        }
    }

    $accessServer = ""
    $terminalLogDirValue = Join-Path $DataRoot "logs"
    $latestTerminalLog = Get-LatestFile -PathPattern (Join-Path $terminalLogDirValue "*.log")
    if ($null -ne $latestTerminalLog) {
        $lines = Get-Content -Path $latestTerminalLog.FullName -ErrorAction SilentlyContinue
        for ($idx = $lines.Count - 1; $idx -ge 0; $idx--) {
            $lineValue = [string]$lines[$idx]
            if ($lineValue -match "authorized on (.+?) through Access Server (.+?) \(ping:") {
                if (-not $server) {
                    $server = $Matches[1].Trim()
                }
                $accessServer = $Matches[2].Trim()
                break
            }
        }
    }

    $environmentLabel = ""
    if ($server -and $login) {
        $environmentLabel = ($server + "__" + $login)
    } elseif ($server) {
        $environmentLabel = $server
    } else {
        $environmentLabel = Split-Path -Leaf $DataRoot
    }

    return @{
        install_root = $InstallRootValue
        data_root = $DataRoot
        data_root_hash = Split-Path -Leaf $DataRoot
        config_path = $configPath
        login = $login
        server = $server
        access_server = $accessServer
        account_mode = $accountMode
        environment_label = $environmentLabel
    }
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

function Normalize-ReportStem {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Value
    )
    $leaf = [System.IO.Path]::GetFileNameWithoutExtension($Value)
    if (-not $leaf) {
        throw "empty report stem is not allowed"
    }
    return $leaf
}

function Get-Mt5EnumTimeframeValue {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Label
    )
    switch ($Label.ToUpperInvariant()) {
        "M1" { return 1 }
        "M5" { return 5 }
        "M15" { return 15 }
        "M30" { return 30 }
        "H1" { return 16385 }
        "H4" { return 16388 }
        "D1" { return 16408 }
        default { throw "unsupported timeframe label: $Label" }
    }
}

function Set-IniValue {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Text,
        [Parameter(Mandatory = $true)]
        [string]$Key,
        [Parameter(Mandatory = $true)]
        [string]$Value
    )
    $replacement = $Key + "=" + $Value
    $pattern = "(?im)^" + [System.Text.RegularExpressions.Regex]::Escape($Key) + "=.*$"
    if ([System.Text.RegularExpressions.Regex]::IsMatch($Text, $pattern)) {
        return [System.Text.RegularExpressions.Regex]::Replace($Text, $pattern, $replacement)
    }
    return $Text.TrimEnd() + [Environment]::NewLine + $replacement + [Environment]::NewLine
}

function Remove-IniValue {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Text,
        [Parameter(Mandatory = $true)]
        [string]$Key
    )
    $pattern = "(?im)^" + [System.Text.RegularExpressions.Regex]::Escape($Key) + "=.*(?:\r?\n)?"
    return [System.Text.RegularExpressions.Regex]::Replace($Text, $pattern, "")
}

function Normalize-TextForComparison {
    param(
        [Parameter(Mandatory = $true)]
        [AllowEmptyString()]
        [string]$Text
    )
    $normalized = $Text -replace "`r`n", "`n"
    $normalized = $normalized -replace "`r", "`n"
    return $normalized.Trim()
}

function Write-ArchiveSummary {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ArchiveRoot,
        [Parameter(Mandatory = $true)]
        [hashtable]$Payload
    )
    $summaryPath = Join-Path $ArchiveRoot "run_summary.json"
    $json = $Payload | ConvertTo-Json -Depth 6
    $utf8NoBom = [System.Text.UTF8Encoding]::new($false)
    [System.IO.File]::WriteAllText($summaryPath, $json + [Environment]::NewLine, $utf8NoBom)
}

function Stage-ArtifactIntoArchive {
    param(
        [Parameter(Mandatory = $true)]
        [System.IO.FileInfo]$SourceFile,
        [Parameter(Mandatory = $true)]
        [string]$ArchiveRoot,
        [Parameter(Mandatory = $true)]
        [string]$Kind
    )
    $targetPath = Join-Path (Join-Path $ArchiveRoot $Kind) $SourceFile.Name
    return Copy-IfDifferent -SourcePath $SourceFile.FullName -TargetPath $targetPath
}

$batchDir = Split-Path -Parent $PSCommandPath
$projectRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $batchDir))
$archiveDir = Join-Path $projectRoot "12_tooling_runtime_archive\batch_02_mt_indicator_family"
$defaultInventoryPath = Join-Path $batchDir "environment_snapshots\mt_environment_inventory_latest.json"
$installRootExplicit = $PSBoundParameters.ContainsKey("InstallRoot")

$reportFileStem = Normalize-ReportStem -Value $ReportStem
$reportFileName = $reportFileStem + ".htm"
$indicatorTimeframeValue = Get-Mt5EnumTimeframeValue -Label $IndicatorPeriod
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
$environmentMeta = Resolve-Mt5EnvironmentMetadata -DataRoot $dataRoot -InstallRootValue $InstallRoot
if ($null -ne $inventorySelection) {
    $environmentMeta.selection_mode = "inventory_selector"
    $environmentMeta.inventory_json = $inventorySelection.inventory_json
    $environmentMeta.inventory_selector = $EnvironmentSelector
    $environmentMeta.inventory_match_field = $inventorySelection.matched_field
    $environmentMeta.inventory_match_value = $inventorySelection.matched_value
} elseif ($DataRootOverride) {
    $environmentMeta.selection_mode = "data_root_override"
} else {
    $environmentMeta.selection_mode = "origin_autodiscovery"
}
$commonFilesDir = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
$reportDir = Join-Path $dataRoot "tester\files"
$rootReportDir = $dataRoot
$terminalLogDir = Join-Path $dataRoot "logs"
$testerLogDir = Join-Path $dataRoot "Tester\logs"
$profilesTesterDir = Join-Path $dataRoot "MQL5\Profiles\Tester"
$expertTarget = Join-Path $dataRoot "MQL5\Experts\XBreakingProbe.ex5"
$indicatorTarget = Join-Path $dataRoot "MQL5\Indicators\XBreaking.ex5"
$runtimeIniPath = Join-Path $batchDir "_tmp_xbreaking_probe_runtime.ini"
$runtimeSetFileName = "XBreakingProbe.runtime." + $reportFileStem + ".set"
$runtimeSetPath = Join-Path $profilesTesterDir $runtimeSetFileName
$absoluteReportPath = Join-Path $reportDir $reportFileName

$expertSource = Join-Path $archiveDir "XBreakingProbe.ex5"
$indicatorSource = Join-Path $archiveDir "XBreaking.ex5"
$iniTemplateSource = Join-Path $archiveDir "XBreakingProbe.ini"
$archiveRoot = ""
if ($ArchiveTag) {
    $archiveRoot = Join-Path $batchDir ("artifacts\xbreaking\validation_matrix\" + $ArchiveTag)
}

if (-not (Test-Path $terminalExe)) {
    throw "terminal64.exe not found: $terminalExe"
}
if (-not (Test-Path $expertSource)) {
    throw "XBreakingProbe.ex5 not found: $expertSource"
}
if (-not (Test-Path $indicatorSource)) {
    throw "XBreaking.ex5 not found: $indicatorSource"
}
if (-not (Test-Path $iniTemplateSource)) {
    throw "XBreakingProbe.ini not found: $iniTemplateSource"
}

New-Item -ItemType Directory -Path $reportDir -Force | Out-Null
New-Item -ItemType Directory -Path $commonFilesDir -Force | Out-Null
New-Item -ItemType Directory -Path $testerLogDir -Force | Out-Null
New-Item -ItemType Directory -Path $profilesTesterDir -Force | Out-Null
if ($archiveRoot) {
    New-Item -ItemType Directory -Path $archiveRoot -Force | Out-Null
}

Write-Step "mt5 install root: $InstallRoot"
Write-Step "mt5 data root: $dataRoot"
if ($null -ne $inventorySelection) {
    Write-Step ("mt5 inventory selector: " + $EnvironmentSelector + " (" + $inventorySelection.matched_field + ")")
} elseif ($DataRootOverride) {
    Write-Step "mt5 data root override: enabled"
}
if ($environmentMeta.server -or $environmentMeta.login) {
    Write-Step ("mt5 environment: " + $environmentMeta.environment_label)
}
Write-Step ("mt5 selection mode: " + $environmentMeta.selection_mode)
Write-Step "symbol=$Symbol chart_period=$ChartPeriod indicator_period=$IndicatorPeriod from=$FromDate to=$ToDate"
Write-Step "common files dir: $commonFilesDir"

$baselineTime = Get-Date
$csvBefore = Get-LatestFile -PathPattern (Join-Path $commonFilesDir "XBreaking_probe_*.csv")
$reportBefore = Get-LatestFile -PathPattern (Join-Path $reportDir ("*" + $reportFileStem + "*.htm*"))
$rootReportBefore = Get-LatestFile -PathPattern (Join-Path $rootReportDir ("*" + $reportFileStem + "*.htm*"))
$terminalLogBefore = Get-LatestFile -PathPattern (Join-Path $terminalLogDir "*.log")
$testerLogBefore = Get-LatestFile -PathPattern (Join-Path $testerLogDir "*.log")

Write-Step "deploying XBreaking binaries into MT5 data folder"
$expertDeployStatus = Copy-IfDifferent -SourcePath $expertSource -TargetPath $expertTarget
$indicatorDeployStatus = Copy-IfDifferent -SourcePath $indicatorSource -TargetPath $indicatorTarget
$runtimeSetWriteMode = "not_attempted"

function Write-RuntimeSet {
    $desiredText = (
        @(
            "InpIndicatorName=$IndicatorName"
            "InpIndicatorTf=$indicatorTimeframeValue"
            "InpBarsToProbe=$BarsToProbe"
            "InpMaxBuffers=$MaxBuffers"
        ) -join [Environment]::NewLine
    ) + [Environment]::NewLine
    $runtimeSetDir = Split-Path -Parent $runtimeSetPath
    New-Item -ItemType Directory -Path $runtimeSetDir -Force | Out-Null
    try {
        [System.IO.File]::WriteAllText($runtimeSetPath, $desiredText, [System.Text.Encoding]::ASCII)
        $script:runtimeSetWriteMode = "written"
        return
    } catch {
        $isSandboxRestriction = $_.FullyQualifiedErrorId -like "*PathNotAllowed*"
        if (-not $isSandboxRestriction) {
            throw
        }
        if (-not (Test-Path $runtimeSetPath)) {
            throw
        }
        $existingText = Get-Content -Path $runtimeSetPath -Raw -Encoding ASCII -ErrorAction SilentlyContinue
        if ((Normalize-TextForComparison -Text $existingText) -ne (Normalize-TextForComparison -Text $desiredText)) {
            throw "sandbox_blocked_runtime_set_write and pre-staged runtime set does not match desired inputs: $runtimeSetPath"
        }
        Write-Step "sandbox blocked runtime set write; reusing pre-staged tester set"
        $script:runtimeSetWriteMode = "pre_staged_reused"
    }
}

function Write-RuntimeIni {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ReportValue
    )
    $iniText = Get-Content -Path $iniTemplateSource -Raw -Encoding UTF8
    $iniText = Set-IniValue -Text $iniText -Key "Symbol" -Value $Symbol
    $iniText = Set-IniValue -Text $iniText -Key "Period" -Value $ChartPeriod
    $iniText = Set-IniValue -Text $iniText -Key "FromDate" -Value $FromDate
    $iniText = Set-IniValue -Text $iniText -Key "ToDate" -Value $ToDate
    $iniText = Set-IniValue -Text $iniText -Key "Report" -Value $ReportValue
    $iniText = Set-IniValue -Text $iniText -Key "ExpertParameters" -Value $runtimeSetFileName
    $iniText = Remove-IniValue -Text $iniText -Key "InpIndicatorName"
    $iniText = Remove-IniValue -Text $iniText -Key "InpIndicatorTf"
    $iniText = Remove-IniValue -Text $iniText -Key "InpBarsToProbe"
    $iniText = Remove-IniValue -Text $iniText -Key "InpMaxBuffers"
    [System.IO.File]::WriteAllText($runtimeIniPath, $iniText, [System.Text.Encoding]::ASCII)
}

function Invoke-Mt5ConfigRun {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ReportValue
    )
    Write-Step "writing runtime tester set with InpIndicatorTf=$indicatorTimeframeValue"
    Write-RuntimeSet
    Write-Step "writing runtime tester ini with Report=$ReportValue"
    Write-RuntimeIni -ReportValue $ReportValue

    Write-Step "stopping existing MT5 terminal64.exe for this install root"
    Get-Process terminal64 -ErrorAction SilentlyContinue |
        Where-Object { $_.Path -eq $terminalExe } |
        Stop-Process -Force
    Start-Sleep -Seconds 1

    Write-Step "starting MT5 tester run via /config"
    $argumentList = @("/config:$runtimeIniPath")
    $process = Start-Process -FilePath $terminalExe -ArgumentList $argumentList -WorkingDirectory $InstallRoot -PassThru
    $processExited = Wait-ForProcessExit -Process $process -TimeoutSeconds $RunTimeoutSeconds
    if (-not $processExited) {
        Write-Step "terminal64.exe still running after timeout; stopping it to finish this batch step"
        Stop-Process -Id $process.Id -Force
        $process.Refresh()
    }
    return $processExited
}

try {
    $processExited = Invoke-Mt5ConfigRun -ReportValue $absoluteReportPath
    $newReport = Wait-ForNewArtifact -Pattern (Join-Path $reportDir ("*" + $reportFileStem + "*.htm*")) -BaselineTime $baselineTime -TimeoutSeconds 15
    $fallbackAttempted = $false
    if ($null -eq $newReport) {
        $newReport = Wait-ForNewArtifact -Pattern (Join-Path $rootReportDir ("*" + $reportFileStem + "*.htm*")) -BaselineTime $baselineTime -TimeoutSeconds 5
    }
    if ($null -eq $newReport) {
        $fallbackAttempted = $true
        Write-Step "no report found after absolute path run; retrying with bare report stem"
        $processExited = Invoke-Mt5ConfigRun -ReportValue $reportFileStem
        $newReport = Wait-ForNewArtifact -Pattern (Join-Path $rootReportDir ("*" + $reportFileStem + "*.htm*")) -BaselineTime $baselineTime -TimeoutSeconds 15
        if ($null -eq $newReport) {
            $newReport = Wait-ForNewArtifact -Pattern (Join-Path $reportDir ("*" + $reportFileStem + "*.htm*")) -BaselineTime $baselineTime -TimeoutSeconds 5
        }
    }

    $newCsv = Wait-ForNewArtifact -Pattern (Join-Path $commonFilesDir "XBreaking_probe_*.csv") -BaselineTime $baselineTime -TimeoutSeconds 15
    $newTerminalLog = Wait-ForNewArtifact -Pattern (Join-Path $terminalLogDir "*.log") -BaselineTime $baselineTime -TimeoutSeconds 10
    $newTesterLog = Wait-ForNewArtifact -Pattern (Join-Path $testerLogDir "*.log") -BaselineTime $baselineTime -TimeoutSeconds 10

    $archiveSummary = @{
        archive_tag = $ArchiveTag
        archive_root = $archiveRoot
        environment = $environmentMeta
        symbol = $Symbol
        chart_period = $ChartPeriod
        indicator_period = $IndicatorPeriod
        from_date = $FromDate
        to_date = $ToDate
        indicator_name = $IndicatorName
        bars_to_probe = $BarsToProbe
        max_buffers = $MaxBuffers
        report_stem = $reportFileStem
        process_exited = $processExited
        report_fallback_attempted = $fallbackAttempted
        run_timeout_seconds = $RunTimeoutSeconds
        runtime_set_write_mode = $runtimeSetWriteMode
        files = @{}
    }

    if ($archiveRoot) {
        $archiveSummary.files.runtime_ini = @{
            source = $runtimeIniPath
            archive_status = Stage-ArtifactIntoArchive -SourceFile (Get-Item -Path $runtimeIniPath) -ArchiveRoot $archiveRoot -Kind "runtime_config"
        }
        $archiveSummary.files.runtime_set = @{
            source = $runtimeSetPath
            archive_status = Stage-ArtifactIntoArchive -SourceFile (Get-Item -Path $runtimeSetPath) -ArchiveRoot $archiveRoot -Kind "runtime_config"
        }
        if ($null -ne $newCsv) {
            $archiveSummary.files.csv = @{
                source = $newCsv.FullName
                archive_status = Stage-ArtifactIntoArchive -SourceFile $newCsv -ArchiveRoot $archiveRoot -Kind "csv"
            }
        }
        if ($null -ne $newReport) {
            $archiveSummary.files.report = @{
                source = $newReport.FullName
                archive_status = Stage-ArtifactIntoArchive -SourceFile $newReport -ArchiveRoot $archiveRoot -Kind "report"
            }
        }
        if ($null -ne $newTerminalLog) {
            $archiveSummary.files.terminal_log = @{
                source = $newTerminalLog.FullName
                archive_status = Stage-ArtifactIntoArchive -SourceFile $newTerminalLog -ArchiveRoot $archiveRoot -Kind "log"
            }
        }
        if ($null -ne $newTesterLog) {
            $archiveSummary.files.tester_log = @{
                source = $newTesterLog.FullName
                archive_status = Stage-ArtifactIntoArchive -SourceFile $newTesterLog -ArchiveRoot $archiveRoot -Kind "log"
            }
        }
        Write-ArchiveSummary -ArchiveRoot $archiveRoot -Payload $archiveSummary
    }

    Write-Host ""
    Write-Host "result=best_effort_mt5_config_run"
    Write-Host ("symbol=" + $Symbol)
    Write-Host ("chart_period=" + $ChartPeriod)
    Write-Host ("indicator_period=" + $IndicatorPeriod)
    Write-Host ("from_date=" + $FromDate)
    Write-Host ("to_date=" + $ToDate)
    Write-Host ("report_stem=" + $reportFileStem)
    Write-Host ("archive_tag=" + $ArchiveTag)
    Write-Host ("process_exited=" + (Format-Bool -Value $processExited))
    Write-Host ("report_fallback_attempted=" + (Format-Bool -Value $fallbackAttempted))
    Write-Host ("runtime_set_file=" + $runtimeSetFileName)
    Write-Host ("runtime_set_path=" + $runtimeSetPath)
    Write-Host ("runtime_set_write_mode=" + $runtimeSetWriteMode)
    Write-Host ("environment_selection_mode=" + $environmentMeta.selection_mode)
    Write-Host ("environment_label=" + $environmentMeta.environment_label)
    if ($environmentMeta.server) {
        Write-Host ("environment_server=" + $environmentMeta.server)
    }
    if ($environmentMeta.login) {
        Write-Host ("environment_login=" + $environmentMeta.login)
    }
    if ($environmentMeta.access_server) {
        Write-Host ("environment_access_server=" + $environmentMeta.access_server)
    }
    $inventoryJsonValue = ""
    if ($environmentMeta.ContainsKey("inventory_json")) {
        $inventoryJsonValue = [string]$environmentMeta["inventory_json"]
    }
    if ($inventoryJsonValue) {
        Write-Host ("environment_inventory_json=" + $inventoryJsonValue)
    }
    $inventorySelectorValue = ""
    if ($environmentMeta.ContainsKey("inventory_selector")) {
        $inventorySelectorValue = [string]$environmentMeta["inventory_selector"]
    }
    if ($inventorySelectorValue) {
        Write-Host ("environment_inventory_selector=" + $inventorySelectorValue)
    }
    $inventoryMatchFieldValue = ""
    if ($environmentMeta.ContainsKey("inventory_match_field")) {
        $inventoryMatchFieldValue = [string]$environmentMeta["inventory_match_field"]
    }
    if ($inventoryMatchFieldValue) {
        Write-Host ("environment_inventory_match_field=" + $inventoryMatchFieldValue)
    }
    $inventoryMatchValueValue = ""
    if ($environmentMeta.ContainsKey("inventory_match_value")) {
        $inventoryMatchValueValue = [string]$environmentMeta["inventory_match_value"]
    }
    if ($inventoryMatchValueValue) {
        Write-Host ("environment_inventory_match_value=" + $inventoryMatchValueValue)
    }
    Write-Host ("expert_deploy_status=" + $expertDeployStatus)
    Write-Host ("indicator_deploy_status=" + $indicatorDeployStatus)
    Write-Host ("new_csv_found=" + (Format-Bool -Value ($null -ne $newCsv)))
    if ($null -ne $newCsv) {
        Write-Host ("new_csv_path=" + $newCsv.FullName)
        Write-Host ("new_csv_mtime=" + $newCsv.LastWriteTime.ToString("s"))
    } elseif ($null -ne $csvBefore) {
        Write-Host ("latest_csv_path=" + $csvBefore.FullName)
        Write-Host ("latest_csv_mtime=" + $csvBefore.LastWriteTime.ToString("s"))
    }
    Write-Host ("new_report_found=" + (Format-Bool -Value ($null -ne $newReport)))
    if ($null -ne $newReport) {
        Write-Host ("new_report_path=" + $newReport.FullName)
        Write-Host ("new_report_mtime=" + $newReport.LastWriteTime.ToString("s"))
    } elseif ($null -ne $reportBefore) {
        Write-Host ("latest_report_path=" + $reportBefore.FullName)
        Write-Host ("latest_report_mtime=" + $reportBefore.LastWriteTime.ToString("s"))
    } elseif ($null -ne $rootReportBefore) {
        Write-Host ("latest_report_path=" + $rootReportBefore.FullName)
        Write-Host ("latest_report_mtime=" + $rootReportBefore.LastWriteTime.ToString("s"))
    }
    Write-Host ("new_terminal_log_found=" + (Format-Bool -Value ($null -ne $newTerminalLog)))
    if ($null -ne $newTerminalLog) {
        Write-Host ("new_terminal_log_path=" + $newTerminalLog.FullName)
        Write-Host ("new_terminal_log_mtime=" + $newTerminalLog.LastWriteTime.ToString("s"))
    } elseif ($null -ne $terminalLogBefore) {
        Write-Host ("latest_terminal_log_path=" + $terminalLogBefore.FullName)
        Write-Host ("latest_terminal_log_mtime=" + $terminalLogBefore.LastWriteTime.ToString("s"))
    }
    Write-Host ("new_tester_log_found=" + (Format-Bool -Value ($null -ne $newTesterLog)))
    if ($null -ne $newTesterLog) {
        Write-Host ("new_tester_log_path=" + $newTesterLog.FullName)
        Write-Host ("new_tester_log_mtime=" + $newTesterLog.LastWriteTime.ToString("s"))
    } elseif ($null -ne $testerLogBefore) {
        Write-Host ("latest_tester_log_path=" + $testerLogBefore.FullName)
        Write-Host ("latest_tester_log_mtime=" + $testerLogBefore.LastWriteTime.ToString("s"))
    }
    if ($archiveRoot) {
        Write-Host ("archive_root=" + $archiveRoot)
    }
} finally {
    if (Test-Path $runtimeIniPath) {
        Remove-Item $runtimeIniPath -Force
    }
}
