param(
    [string]$InstallRoot = "",
    [string]$DataRootOverride = "",
    [string]$EnvironmentInventoryJson = "",
    [string]$EnvironmentSelector = "",
    [string[]]$Symbols = @("EURUSD", "GBPUSD", "USDJPY"),
    [ValidateSet("M1", "M5", "M15", "M30", "H1", "H4", "D1")]
    [string[]]$Periods = @("H1", "H4"),
    [string]$FromDate = "2025.01.01",
    [string]$ToDate = "2025.01.15",
    [string]$IndicatorName = "XBreaking",
    [int]$BarsToProbe = 200,
    [int]$MaxBuffers = 8,
    [int]$RunTimeoutSeconds = 180,
    [string]$WindowTag = "",
    [string]$TagSuffix = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$batchDir = Split-Path -Parent $PSCommandPath
$runnerPath = Join-Path $batchDir "run_xbreaking_probe_once.ps1"
if (-not (Test-Path $runnerPath)) {
    throw "runner not found: $runnerPath"
}

function Normalize-TagToken {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Value
    )

    $trimmed = $Value.Trim()
    if (-not $trimmed) {
        return ""
    }
    return ($trimmed -replace "[^A-Za-z0-9]+", "").ToLowerInvariant()
}

$stamp = Get-Date -Format "yyyyMMddTHHmmss"
$suffix = $TagSuffix
if ($suffix) {
    $suffix = $suffix.Trim()
}
$windowToken = Normalize-TagToken -Value $WindowTag
if (-not $windowToken) {
    $fromToken = Normalize-TagToken -Value $FromDate
    $toToken = Normalize-TagToken -Value $ToDate
    if ($fromToken -and $toToken) {
        $windowToken = $fromToken + "_" + $toToken
    }
}
$failedRuns = New-Object System.Collections.Generic.List[string]

foreach ($symbol in $Symbols) {
    $symbolValue = ""
    if ($null -ne $symbol) {
        $symbolValue = ([string]$symbol).Trim()
    }
    if (-not $symbolValue) {
        continue
    }
    foreach ($period in $Periods) {
        $periodValue = ""
        if ($null -ne $period) {
            $periodValue = ([string]$period).Trim()
        }
        if (-not $periodValue) {
            continue
        }
        $reportStem = ("xbreaking_probe_" + $symbolValue.ToLowerInvariant() + "_" + $periodValue.ToLowerInvariant())
        if ($windowToken) {
            $reportStem = $reportStem + "_" + $windowToken
        }
        $archiveTag = ($symbolValue.ToLowerInvariant() + "_" + $periodValue.ToLowerInvariant())
        if ($windowToken) {
            $archiveTag = $archiveTag + "_" + $windowToken
        }
        $archiveTag = $archiveTag + "_" + $stamp
        if ($suffix) {
            $archiveTag = $archiveTag + "_" + $suffix
        }
        try {
            & $runnerPath `
                -InstallRoot $InstallRoot `
                -DataRootOverride $DataRootOverride `
                -EnvironmentInventoryJson $EnvironmentInventoryJson `
                -EnvironmentSelector $EnvironmentSelector `
                -Symbol $symbolValue `
                -ChartPeriod $periodValue `
                -IndicatorPeriod $periodValue `
                -FromDate $FromDate `
                -ToDate $ToDate `
                -IndicatorName $IndicatorName `
                -BarsToProbe $BarsToProbe `
                -MaxBuffers $MaxBuffers `
                -ReportStem $reportStem `
                -ArchiveTag $archiveTag `
                -RunTimeoutSeconds $RunTimeoutSeconds
            if (-not $?) {
                throw "runner returned failure for $symbolValue/$periodValue"
            }
        } catch {
            $failedRuns.Add(($symbolValue + "/" + $periodValue + ": " + $_.Exception.Message))
        } finally {
            $global:LASTEXITCODE = 0
        }
    }
}

if ($failedRuns.Count -gt 0) {
    throw ("validation matrix failed: " + [string]::Join("; ", $failedRuns))
}

$global:LASTEXITCODE = 0
