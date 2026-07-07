param(
    [string]$MetaQuotesRoot = "",
    [string]$OutputJson = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not $MetaQuotesRoot) {
    $MetaQuotesRoot = Join-Path $env:APPDATA "MetaQuotes\Terminal"
}

if (-not (Test-Path $MetaQuotesRoot)) {
    throw "MetaQuotes terminal root not found: $MetaQuotesRoot"
}

function Get-IniValue {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FilePath,
        [Parameter(Mandatory = $true)]
        [string]$Key
    )

    if (-not (Test-Path $FilePath)) {
        return ""
    }
    foreach ($line in Get-Content -Path $FilePath -ErrorAction SilentlyContinue) {
        if ($line -match ("^" + [regex]::Escape($Key) + "=(.*)$")) {
            return $Matches[1].Trim()
        }
    }
    return ""
}

function Get-LatestAccessServer {
    param(
        [Parameter(Mandatory = $true)]
        [string]$LogDir
    )

    if (-not (Test-Path $LogDir)) {
        return ""
    }
    $latestLog = Get-ChildItem -Path $LogDir -File -Filter *.log -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
    if ($null -eq $latestLog) {
        return ""
    }
    $lines = Get-Content -Path $latestLog.FullName -ErrorAction SilentlyContinue
    for ($idx = $lines.Count - 1; $idx -ge 0; $idx--) {
        $lineValue = [string]$lines[$idx]
        if ($lineValue -match "authorized on (.+?) through Access Server (.+?) \(ping:") {
            return $Matches[2].Trim()
        }
    }
    return ""
}

$items = New-Object System.Collections.Generic.List[object]

foreach ($candidate in Get-ChildItem -Path $MetaQuotesRoot -Directory -ErrorAction SilentlyContinue) {
    $originPath = Join-Path $candidate.FullName "origin.txt"
    $originPresent = Test-Path $originPath
    $originValue = ""
    if ($originPresent) {
        $originValue = (Get-Content -Path $originPath -Raw -ErrorAction SilentlyContinue).Trim()
    }
    $platform = "unknown"
    $terminalPath = ""
    if ($originValue) {
        if (Test-Path (Join-Path $originValue "terminal64.exe")) {
            $platform = "mt5"
            $terminalPath = Join-Path $originValue "terminal64.exe"
        } elseif (Test-Path (Join-Path $originValue "terminal.exe")) {
            $platform = "mt4"
            $terminalPath = Join-Path $originValue "terminal.exe"
        }
    }
    if ($platform -eq "unknown") {
        if (Test-Path (Join-Path $candidate.FullName "MQL5")) {
            $platform = "mt5"
        } elseif (Test-Path (Join-Path $candidate.FullName "MQL4")) {
            $platform = "mt4"
        }
    }
    if ($platform -eq "unknown") {
        continue
    }

    $configPath = Join-Path $candidate.FullName "Config\common.ini"
    $loginValue = Get-IniValue -FilePath $configPath -Key "Login"
    $serverValue = Get-IniValue -FilePath $configPath -Key "Server"
    $accountModeValue = Get-IniValue -FilePath $configPath -Key "Account"
    $accessServerValue = Get-LatestAccessServer -LogDir (Join-Path $candidate.FullName "logs")
    $discoveryModeValue = "origin_txt"
    if (-not $originPresent) {
        $discoveryModeValue = "structure_only"
    } elseif (-not $originValue) {
        $discoveryModeValue = "origin_txt_empty"
    } elseif (-not $terminalPath) {
        $discoveryModeValue = "origin_txt_no_terminal"
    }
    $environmentLabelValue = ""
    if ($serverValue -and $loginValue) {
        $environmentLabelValue = $serverValue + "__" + $loginValue
    } elseif ($serverValue) {
        $environmentLabelValue = $serverValue
    } else {
        $environmentLabelValue = $candidate.Name
    }

    $items.Add([ordered]@{
        platform = $platform
        data_root_hash = $candidate.Name
        data_root = $candidate.FullName
        origin_present = $originPresent
        origin_path = $originValue
        discovery_mode = $discoveryModeValue
        terminal_path = $terminalPath
        config_path = $configPath
        login = $loginValue
        server = $serverValue
        access_server = $accessServerValue
        account_mode = $accountModeValue
        environment_label = $environmentLabelValue
    })
}

$itemArray = @()
foreach ($entry in $items) {
    $itemArray += $entry
}

$payload = @{
    generated_at = (Get-Date).ToString("s")
    metaquotes_root = $MetaQuotesRoot
    item_count = $items.Count
    items = $itemArray
}

if ($OutputJson) {
    $outputDir = Split-Path -Parent $OutputJson
    if ($outputDir) {
        New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
    }
    $utf8NoBom = [System.Text.UTF8Encoding]::new($false)
    [System.IO.File]::WriteAllText($OutputJson, (($payload | ConvertTo-Json -Depth 5) + [Environment]::NewLine), $utf8NoBom)
}

Write-Host ("generated_at=" + $payload.generated_at)
Write-Host ("metaquotes_root=" + $MetaQuotesRoot)
Write-Host ("item_count=" + $items.Count)
if ($OutputJson) {
    Write-Host ("output_json=" + $OutputJson)
}

foreach ($item in $items) {
    Write-Host ""
    Write-Host ("platform=" + $item.platform)
    Write-Host ("data_root_hash=" + $item.data_root_hash)
    Write-Host ("origin_path=" + $item.origin_path)
    Write-Host ("discovery_mode=" + $item.discovery_mode)
    if ($item.terminal_path) {
        Write-Host ("terminal_path=" + $item.terminal_path)
    }
    if ($item.server) {
        Write-Host ("server=" + $item.server)
    }
    if ($item.login) {
        Write-Host ("login=" + $item.login)
    }
    if ($item.access_server) {
        Write-Host ("access_server=" + $item.access_server)
    }
    if ($item.environment_label) {
        Write-Host ("environment_label=" + $item.environment_label)
    }
}
