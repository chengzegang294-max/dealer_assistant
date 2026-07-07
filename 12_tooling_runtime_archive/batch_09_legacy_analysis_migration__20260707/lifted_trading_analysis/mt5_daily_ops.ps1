param(
  [ValidateSet("help","status","summary","plan","test18","monitor","monitor_1h","auto","close","close_all")]
  [string]$Mode = "help",
  [int]$IntervalSec = 60,
  [int]$EntryMaxOrders = 1,
  [double]$EntryLot = 0.0,
  [int]$EntryLookbackBars = 1,
  [int]$EntryGateSnapshot = 0,
  [int]$EntryStatus = 1,
  [int]$EntryShowAll = 0,
  [string]$Test18Symbol = "GER40",
  [double]$Test18Volume = 0.01
)

$ErrorActionPreference = "Stop"
$OutputEncoding = [System.Text.Encoding]::UTF8
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $root

function Resolve-Python {
  $venvPy = Join-Path $root ".venv\Scripts\python.exe"
  if (Test-Path -LiteralPath $venvPy) { return $venvPy }
  return "python"
}

function Run-Mt5Assistant {
  param([string[]]$Mt5Args)
  $py = Resolve-Python
  & $py (Join-Path $root "mt5_exit_assistant.py") @Mt5Args
}

function Show-Help {
  Write-Host ""
  Write-Host "MT5 Daily Ops (PowerShell)"
  Write-Host "  .\mt5_daily_ops.ps1 -Mode status"
  Write-Host "  .\mt5_daily_ops.ps1 -Mode summary"
  Write-Host "  .\mt5_daily_ops.ps1 -Mode plan"
  Write-Host "  .\mt5_daily_ops.ps1 -Mode test18 -Test18Symbol GER40 -Test18Volume 0.01"
  Write-Host "  .\mt5_daily_ops.ps1 -Mode monitor -IntervalSec 60 -EntryLookbackBars 1"
  Write-Host "  .\mt5_daily_ops.ps1 -Mode monitor_1h -IntervalSec 10"
  Write-Host "  .\mt5_daily_ops.ps1 -Mode monitor_1h -IntervalSec 30 -EntryLookbackBars 1 -EntryShowAll 0 -EntryGateSnapshot 1"
  Write-Host "  .\mt5_daily_ops.ps1 -Mode auto -IntervalSec 60 -EntryMaxOrders 1 -EntryLookbackBars 1"
  Write-Host "  .\mt5_daily_ops.ps1 -Mode auto -IntervalSec 60 -EntryMaxOrders 1 -EntryLot 0.01 -EntryLookbackBars 1"
  Write-Host "  .\mt5_daily_ops.ps1 -Mode close_all"
  Write-Host "  .\mt5_daily_ops.ps1 -Mode close"
  Write-Host ""
  Write-Host "If ExecutionPolicy blocks .ps1, use:"
  Write-Host "  powershell -NoProfile -ExecutionPolicy Bypass -File .\mt5_daily_ops.ps1 -Mode auto"
  Write-Host ""
  Write-Host "Mode:"
  Write-Host "  status   print MT5 connection/trade permission flags"
  Write-Host "  summary  export today's deals/orders (reconcile)"
  Write-Host "  monitor  intraday monitor (no trading)"
  Write-Host "  auto     intraday auto execution (trade CORE only; OBSERVE scan only)"
  Write-Host "  close_all emergency close ALL positions (account-wide)"
  Write-Host "  close    end-of-day export today's deals/orders"
  Write-Host "  test18   end-to-end trade chain test (open -> set SL -> partial close -> close)"
  Write-Host ""
}

if ($Mode -eq "help") {
  Show-Help
  exit 0
}

if ($Mode -eq "status") {
  Run-Mt5Assistant @("--mt5-status")
  exit 0
}

if ($Mode -eq "summary" -or $Mode -eq "close") {
  Run-Mt5Assistant @("--summary-today")
  exit 0
}

if ($Mode -eq "close_all") {
  $mt5Args = @(
    "--execute",
    "--pool", "all",
    "--close-all",
    "--enable-entry", "0",
    "--enable-cam", "0",
    "--max-loops", "1"
  )
  Run-Mt5Assistant $mt5Args
  exit 0
}

if ($Mode -eq "test18") {
  $mt5Args = @(
    "--test18",
    "--test18-symbol", "$Test18Symbol",
    "--test18-volume", "$Test18Volume"
  )
  Run-Mt5Assistant $mt5Args
  exit 0
}

if ($Mode -eq "plan") {
  $mt5Args = @(
    "--dry-run",
    "--max-loops", "1",
    "--pool", "core",
    "--enable-entry", "1",
    "--entry-universe", "marketwatch",
    "--entry-scan-pools", "core,observe",
    "--entry-trade-pool", "core",
    "--entry-execute", "0",
    "--entry-lookback-bars", "48",
    "--entry-show-all", "1",
    "--entry-status", "1",
    "--entry-gate-snapshot", "1"
  )
  Run-Mt5Assistant $mt5Args
  exit 0
}

if ($Mode -eq "monitor") {
  $mt5Args = @(
    "--dry-run",
    "--watch",
    "--interval-sec", "$IntervalSec",
    "--pool", "core",
    "--enable-entry", "1",
    "--entry-universe", "marketwatch",
    "--entry-scan-pools", "core,observe",
    "--entry-trade-pool", "core",
    "--entry-execute", "0",
    "--entry-lookback-bars", "$EntryLookbackBars",
    "--entry-show-all", "$EntryShowAll",
    "--entry-status", "$EntryStatus"
  )
  if ($EntryGateSnapshot -ne 0) {
    $mt5Args += @("--entry-gate-snapshot", "1")
  }
  Run-Mt5Assistant $mt5Args
  exit 0
}

if ($Mode -eq "monitor_1h") {
  $mt5Args = @(
    "--dry-run",
    "--watch",
    "--interval-sec", "$IntervalSec",
    "--watch-on-new-h1", "1",
    "--pool", "core",
    "--enable-entry", "1",
    "--entry-universe", "marketwatch",
    "--entry-scan-pools", "core,observe",
    "--entry-trade-pool", "core",
    "--entry-execute", "0",
    "--entry-lookback-bars", "$EntryLookbackBars",
    "--entry-show-all", "$EntryShowAll",
    "--entry-status", "$EntryStatus"
  )
  if ($EntryGateSnapshot -ne 0) {
    $mt5Args += @("--entry-gate-snapshot", "1")
  }
  Run-Mt5Assistant $mt5Args
  exit 0
}

if ($Mode -eq "auto") {
  $mt5Args = @(
    "--execute",
    "--watch",
    "--interval-sec", "$IntervalSec",
    "--pool", "core",
    "--enable-entry", "1",
    "--entry-universe", "marketwatch",
    "--entry-scan-pools", "core,observe",
    "--entry-trade-pool", "core",
    "--entry-execute", "1",
    "--entry-max-orders", "$EntryMaxOrders",
    "--entry-lookback-bars", "$EntryLookbackBars",
    "--entry-show-all", "$EntryShowAll",
    "--entry-status", "$EntryStatus"
  )
  if ($EntryLot -gt 0) {
    $mt5Args += @("--entry-lot", "$EntryLot")
  } else {
    $mt5Args += @("--entry-lot", "0")
  }
  if ($EntryGateSnapshot -ne 0) {
    $mt5Args += @("--entry-gate-snapshot", "1")
  }
  Run-Mt5Assistant $mt5Args
  exit 0
}

Show-Help
exit 1

