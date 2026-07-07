Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Windows.Forms

$signature = @"
using System;
using System.Runtime.InteropServices;
public static class Win32 {
    [DllImport("user32.dll")]
    public static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);

    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
}
"@

Add-Type -TypeDefinition $signature

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

function Get-FileSnapshot {
    param(
        [Parameter(Mandatory = $true)]
        [string]$PathPattern
    )
    Get-ChildItem -Path $PathPattern -ErrorAction SilentlyContinue |
        Where-Object { -not $_.PSIsContainer } |
        Sort-Object LastWriteTime -Descending |
        Select-Object FullName, Name, Length, LastWriteTime
}

function Wait-ForMainWindow {
    param(
        [Parameter(Mandatory = $true)]
        [System.Diagnostics.Process]$Process,
        [int]$TimeoutSeconds = 20
    )
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $Process.Refresh()
        if ($Process.HasExited) {
            throw "terminal.exe exited before exposing a main window"
        }
        if ($Process.MainWindowHandle -ne 0) {
            return
        }
        Start-Sleep -Milliseconds 500
    }
    throw "terminal.exe main window handle not found within timeout"
}

function Activate-Window {
    param(
        [Parameter(Mandatory = $true)]
        [System.Diagnostics.Process]$Process
    )
    $null = [Win32]::ShowWindowAsync($Process.MainWindowHandle, 9)
    Start-Sleep -Milliseconds 300
    $null = [Win32]::SetForegroundWindow($Process.MainWindowHandle)
    Start-Sleep -Milliseconds 500
}

function Send-TesterKeys {
    param(
        [Parameter(Mandatory = $true)]
        [System.Diagnostics.Process]$Process
    )
    $shell = New-Object -ComObject WScript.Shell
    if (-not $shell.AppActivate($Process.Id)) {
        throw "failed to activate MT4 window by process id"
    }
    Start-Sleep -Milliseconds 700

    # Show the strategy tester pane, then best-effort hit Start.
    [System.Windows.Forms.SendKeys]::SendWait("^r")
    Start-Sleep -Milliseconds 1000
    [System.Windows.Forms.SendKeys]::SendWait("%s")
    Start-Sleep -Milliseconds 700
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
    Start-Sleep -Milliseconds 700
    [System.Windows.Forms.SendKeys]::SendWait("%s")
}

function Wait-ForNewArtifact {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Pattern,
        [Parameter(Mandatory = $true)]
        [datetime]$BaselineTime,
        [int]$TimeoutSeconds = 90
    )
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $latest = Get-ChildItem -Path $Pattern -ErrorAction SilentlyContinue |
            Where-Object { -not $_.PSIsContainer } |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 1
        if ($null -ne $latest -and $latest.LastWriteTime -gt $BaselineTime) {
            return $latest
        }
        Start-Sleep -Seconds 2
    }
    return $null
}

function Resolve-PortableMt4Root {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$BaseRoots
    )
    foreach ($baseRoot in $BaseRoots) {
        if (-not (Test-Path $baseRoot)) {
            continue
        }
        $toolingRoot = Get-ChildItem -Path $baseRoot -Directory -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -like "12_*TOOLING_RUNTIME" } |
            Select-Object -First 1
        if ($null -eq $toolingRoot) {
            continue
        }

        $portableCandidate = Get-ChildItem -Path $toolingRoot.FullName -Directory -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -like "03_MT4*" -or $_.Name -eq "mt4_probe_instance" } |
            Select-Object -First 1
        if ($null -eq $portableCandidate) {
            continue
        }

        $terminalExe = Join-Path $portableCandidate.FullName "terminal.exe"
        if (Test-Path $terminalExe) {
            return $portableCandidate.FullName
        }
    }
    throw "legacy MT4 portable instance not found"
}

$batchDir = Split-Path -Parent $PSCommandPath
$projectRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $batchDir))
$terminalRoot = $env:MT4_PORTABLE_ROOT
if ([string]::IsNullOrWhiteSpace($terminalRoot)) {
    throw "MT4_PORTABLE_ROOT is required (path to a portable MT4 instance directory containing terminal.exe)"
}

$terminalExe = Join-Path $terminalRoot "terminal.exe"
$configPath = Join-Path $terminalRoot "config\mt4probe_volty_portable.ini"
$testerIniPath = Join-Path $terminalRoot "tester\MT4Probe_Volty.ini"
$configBackupPath = Join-Path $terminalRoot "config\mt4probe_volty_portable__backup_before_gui_once.ini"
$testerBackupPath = Join-Path $terminalRoot "tester\MT4Probe_Volty__backup_before_gui_once.ini"
$templateConfigPath = Join-Path $batchDir "mt4probe_volty_dumpseries_portable.ini"
$templateTesterIniPath = Join-Path $batchDir "MT4Probe_Volty_dumpseries_0_6.ini"
$testerFilesDir = Join-Path $terminalRoot "tester\files"
$testerLogsDir = Join-Path $terminalRoot "tester\logs"

if (-not (Test-Path $terminalExe)) {
    throw "terminal.exe not found: $terminalExe"
}

Write-Step "target terminal root: $terminalRoot"
$csvBefore = @(Get-FileSnapshot -PathPattern (Join-Path $testerFilesDir "MT4_probe_Volty_*.csv"))
$reportBefore = @(Get-FileSnapshot -PathPattern (Join-Path $testerFilesDir "mt4probe_volty*.htm*"))
$logBefore = @(Get-FileSnapshot -PathPattern (Join-Path $testerLogsDir "*.log"))
$baselineTime = Get-Date

Write-Step "backing up default MT4 config files"
Copy-Item $configPath $configBackupPath -Force
Copy-Item $testerIniPath $testerBackupPath -Force

try {
    Write-Step "injecting batch-local DumpSeries templates"
    Copy-Item $templateConfigPath $configPath -Force
    Copy-Item $templateTesterIniPath $testerIniPath -Force

    Write-Step "stopping existing terminal.exe for this portable instance"
    Get-Process terminal -ErrorAction SilentlyContinue |
        Where-Object { $_.Path -eq $terminalExe } |
        Stop-Process -Force
    Start-Sleep -Seconds 1

    Write-Step "starting MT4 portable instance"
    $process = Start-Process -FilePath $terminalExe -ArgumentList "config\mt4probe_volty_portable.ini", "/portable" -WorkingDirectory $terminalRoot -PassThru
    Wait-ForMainWindow -Process $process
    Activate-Window -Process $process

    Write-Step "sending tester hotkeys"
    Send-TesterKeys -Process $process

    Write-Step "waiting for new csv or tester report"
    $newCsv = Wait-ForNewArtifact -Pattern (Join-Path $testerFilesDir "MT4_probe_Volty_*.csv") -BaselineTime $baselineTime
    $newReport = Wait-ForNewArtifact -Pattern (Join-Path $testerFilesDir "mt4probe_volty*.htm*") -BaselineTime $baselineTime -TimeoutSeconds 20

    Write-Host ""
    Write-Host "result=best_effort_gui_run"
    Write-Host ("new_csv_found=" + (Format-Bool -Value ($null -ne $newCsv)))
    if ($null -ne $newCsv) {
        Write-Host ("new_csv_path=" + $newCsv.FullName)
        Write-Host ("new_csv_mtime=" + $newCsv.LastWriteTime.ToString("s"))
    }
    Write-Host ("new_report_found=" + (Format-Bool -Value ($null -ne $newReport)))
    if ($null -ne $newReport) {
        Write-Host ("new_report_path=" + $newReport.FullName)
        Write-Host ("new_report_mtime=" + $newReport.LastWriteTime.ToString("s"))
    }
    Write-Host ("csv_before_count=" + $csvBefore.Count)
    Write-Host ("report_before_count=" + $reportBefore.Count)
    Write-Host ("log_before_count=" + $logBefore.Count)
} finally {
    Write-Step "restoring default MT4 config files"
    if (Test-Path $configBackupPath) {
        Copy-Item $configBackupPath $configPath -Force
    }
    if (Test-Path $testerBackupPath) {
        Copy-Item $testerBackupPath $testerIniPath -Force
    }
}
