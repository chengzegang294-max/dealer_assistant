Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not $env:ALLOW_ARCHIVE_ONLY_RUN) { throw "ARCHIVE_ONLY: legacy script expects old repo layout under D:\\Stock\\trading_analysis. Set ALLOW_ARCHIVE_ONLY_RUN=1 to run intentionally." }

$root = $env:TRADING_ANALYSIS_ROOT
if ([string]::IsNullOrWhiteSpace($root)) { $root = "d:\Stock\trading_analysis" }
Set-Location $root

$py = ".\.venv\Scripts\python.exe"
if (!(Test-Path $py)) { throw "未找到 $py，请先建好venv或改成你本机python路径" }

$dataDir = Join-Path $root "data"
if (!(Test-Path $dataDir)) { throw "未找到 data 目录：$dataDir" }

$outRoot = Join-Path $root "backtest_out\p0_sweep"
New-Item -ItemType Directory -Force -Path $outRoot | Out-Null

# 定义多个测试 Profile
$profiles = @{
    "A_universal" = @(
        "--enable-score-sizing","1",
        "--enable-score-filter","0",
        "--e1-bb-squeeze-veto","0",
        "--e1-bb-squeeze-penalty","0.6",
        "--e1-fail-k","1.5",
        "--enable-e1-atr-regime-gate","0",
        "--enable-e2-break-confirm","1",
        "--e2-touch-requires-strong","1"
    )
    "A_strict" = @(
        "--enable-score-sizing","1",
        "--enable-score-filter","1",
        "--min-score-to-trade-e1","4.0",
        "--min-score-to-trade-e2","4.15",
        "--e1-bb-squeeze-veto","1",
        "--e1-fail-k","1.5",
        "--enable-e1-atr-regime-gate","1",
        "--enable-e2-break-confirm","1",
        "--e2-touch-requires-strong","1"
    )
    "A_relaxed" = @(
        "--enable-score-sizing","1",
        "--enable-score-filter","0",
        "--e1-bb-squeeze-veto","0",
        "--e1-bb-squeeze-penalty","0.0",
        "--e1-fail-k","0",
        "--enable-e1-atr-regime-gate","0",
        "--enable-e2-break-confirm","0",
        "--e2-touch-requires-strong","0",
        "--stop-k","2.0"
    )
}

$minWindowDays = 365
$anchorPost = Get-Date "2022-01-01"
$anchorPreEnd = Get-Date "2021-12-31"

$csvFiles = Get-ChildItem -Path $dataDir -Filter "*_1h.csv" -File -Recurse |
  Where-Object { $_.FullName -notmatch "\\ashare_watchlist\\" } |
  Sort-Object FullName
if ($csvFiles.Count -eq 0) { throw "data 目录下没有任何 *_1h.csv" }

$rows = New-Object System.Collections.Generic.List[object]

foreach ($f in $csvFiles) {
  $stem = [System.IO.Path]::GetFileNameWithoutExtension($f.Name)
  $sym = ($stem -replace "_1h$","").ToUpper()

  $meta = $null
  $metaErr = ""
  try {
    $metaPy = @'
import importlib.util, json, sys
from pathlib import Path

csv_path = Path(sys.argv[1])
root = Path(sys.argv[2])

spec = importlib.util.spec_from_file_location("bt", str(root / "backtest_p0.py"))
bt = importlib.util.module_from_spec(spec)
sys.modules["bt"] = bt
spec.loader.exec_module(bt)  # type: ignore

df = bt.load_ohlcv_1h(csv_path, tz="UTC")
out = {
  "bars": int(len(df)),
  "start": (df.index.min().isoformat() if len(df) else ""),
  "end": (df.index.max().isoformat() if len(df) else ""),
  "has_ohlc": True,
}
print(json.dumps(out, ensure_ascii=False))
'@

    $metaJson = $metaPy | & $py - $f.FullName $root

    $meta = $metaJson | ConvertFrom-Json
  } catch {
    $metaErr = $_.Exception.Message
  }

  if ($meta -eq $null -or !$meta.has_ohlc -or [string]::IsNullOrWhiteSpace($meta.start) -or [string]::IsNullOrWhiteSpace($meta.end)) {
    $rows.Add([pscustomobject]@{
      symbol = $sym
      split = "SKIP"
      profile = ""
      trades = $null
      net_pnl = $null
      win_rate = $null
      final_max_drawdown_pct = $null
      dd_controlled_success = $null
      e2_share = $null
      diag_entry_n = $null
      diag_sample_ok = $null
      diag_vol_state_mode = $null
      diag_vol_state_squeeze_frac = $null
      diag_vol_state_expanding_frac = $null
      diag_vol_state_normal_frac = $null
      diag_squeeze_frac = $null
      diag_expanding_frac = $null
      diag_normal_frac = $null
      diag_vol_transition = $null
      diag_vol_transition_s2e_frac = $null
      diag_vol_transition_any_frac = $null
      diag_entry_vol_ratio_median = $null
      diag_entry_vol_ratio_q25 = $null
      diag_entry_vol_ratio_q75 = $null
      diag_entry_vol_ratio_p75 = $null
      diag_entry_vol_ratio_p90 = $null
      diag_entry_vol_ratio_high_frac = $null
      diag_session_entry_vol_ratio = $null
      diag_session_entry_vol_ratio_asia_median = $null
      diag_session_entry_vol_ratio_asia_n = $null
      diag_session_entry_vol_ratio_london_median = $null
      diag_session_entry_vol_ratio_london_n = $null
      diag_session_entry_vol_ratio_ny_median = $null
      diag_session_entry_vol_ratio_ny_n = $null
      diag_session_best = $null
      diag_best_session = $null
      diag_session_pnl_asia = $null
      diag_session_pnl_london = $null
      diag_session_pnl_ny = $null
      diag_session_count_asia = $null
      diag_session_count_london = $null
      diag_session_count_ny = $null
      diag_session_trades_asia = $null
      diag_session_trades_london = $null
      diag_session_trades_ny = $null
      diag_session_skew_ratio = $null
      diag_adx_available = $null
      diag_adx_median = $null
      diag_adx_p75 = $null
      diag_adx_weak_frac = $null
      diag_adx_trend_frac = $null
      diag_adx_strong_frac = $null
      diag_ema144_regime_long_frac = $null
      diag_ema144_regime_short_frac = $null
      diag_ema_stack_bull_frac = $null
      diag_ema_stack_bear_frac = $null
      diag_ema_stack_mixed_frac = $null
      diag_kd_align_4h_1d_frac = $null
      diag_kd_align_3tf_frac = $null
      diag_kd_4h_k_median = $null
      diag_kd_1d_k_median = $null
      csv = $f.Name
      out_dir = ""
      ok = $false
      error = $(if ($metaErr) { "skip:not_ohlc_or_parse_failed: $metaErr" } else { "skip:not_ohlc_or_parse_failed" })
      data_start = ""
      data_end = ""
      window_from = ""
      window_to = ""
      window_days = $null
      bars = $null
    })
    continue
  }

  $dataStart = Get-Date $meta.start
  $dataEnd = Get-Date $meta.end
  $bars = [int]$meta.bars

  $windows = @()

  if ($dataEnd -ge $anchorPost) {
    $wf = $dataStart
    if ($wf -lt $anchorPost) { $wf = $anchorPost }
    $wt = $dataEnd
    $days = ($wt - $wf).TotalDays
    if ($days -ge $minWindowDays) {
      $windows += @{ name = "since2022"; from = $wf.ToString("yyyy-MM-dd"); to = $wt.ToString("yyyy-MM-dd"); days = [int][math]::Floor($days) }
    }
  }

  if ($dataStart -lt $anchorPost) {
    $wf = $dataStart
    $wt = $dataEnd
    if ($wt -gt $anchorPreEnd) { $wt = $anchorPreEnd }
    $days = ($wt - $wf).TotalDays
    if ($days -ge $minWindowDays) {
      $windows += @{ name = "pre2022"; from = $wf.ToString("yyyy-MM-dd"); to = $wt.ToString("yyyy-MM-dd"); days = [int][math]::Floor($days) }
    }
  }

  if ($windows.Count -eq 0) {
    $rows.Add([pscustomobject]@{
      symbol = $sym
      split = "SKIP"
      profile = ""
      trades = $null
      net_pnl = $null
      win_rate = $null
      final_max_drawdown_pct = $null
      dd_controlled_success = $null
      e2_share = $null
      diag_entry_n = $null
      diag_sample_ok = $null
      diag_vol_state_mode = $null
      diag_vol_state_squeeze_frac = $null
      diag_vol_state_expanding_frac = $null
      diag_vol_state_normal_frac = $null
      diag_squeeze_frac = $null
      diag_expanding_frac = $null
      diag_normal_frac = $null
      diag_vol_transition = $null
      diag_vol_transition_s2e_frac = $null
      diag_vol_transition_any_frac = $null
      diag_entry_vol_ratio_median = $null
      diag_entry_vol_ratio_q25 = $null
      diag_entry_vol_ratio_q75 = $null
      diag_entry_vol_ratio_p75 = $null
      diag_entry_vol_ratio_p90 = $null
      diag_entry_vol_ratio_high_frac = $null
      diag_session_entry_vol_ratio = $null
      diag_session_entry_vol_ratio_asia_median = $null
      diag_session_entry_vol_ratio_asia_n = $null
      diag_session_entry_vol_ratio_london_median = $null
      diag_session_entry_vol_ratio_london_n = $null
      diag_session_entry_vol_ratio_ny_median = $null
      diag_session_entry_vol_ratio_ny_n = $null
      diag_session_best = $null
      diag_best_session = $null
      diag_session_pnl_asia = $null
      diag_session_pnl_london = $null
      diag_session_pnl_ny = $null
      diag_session_count_asia = $null
      diag_session_count_london = $null
      diag_session_count_ny = $null
      diag_session_trades_asia = $null
      diag_session_trades_london = $null
      diag_session_trades_ny = $null
      diag_session_skew_ratio = $null
      diag_adx_available = $null
      diag_adx_median = $null
      diag_adx_p75 = $null
      diag_adx_weak_frac = $null
      diag_adx_trend_frac = $null
      diag_adx_strong_frac = $null
      diag_ema144_regime_long_frac = $null
      diag_ema144_regime_short_frac = $null
      diag_ema_stack_bull_frac = $null
      diag_ema_stack_bear_frac = $null
      diag_ema_stack_mixed_frac = $null
      diag_kd_align_4h_1d_frac = $null
      diag_kd_align_3tf_frac = $null
      diag_kd_4h_k_median = $null
      diag_kd_1d_k_median = $null
      csv = $f.Name
      out_dir = ""
      ok = $false
      error = "skip:window_too_short_or_outside_anchor"
      data_start = $dataStart.ToString("yyyy-MM-dd")
      data_end = $dataEnd.ToString("yyyy-MM-dd")
      window_from = ""
      window_to = ""
      window_days = $null
      bars = $bars
    })
    continue
  }

  foreach ($sp in $windows) {
    $splitName = $sp.name
    $fromS = $sp.from
    $toS = $sp.to
    $winDays = $sp.days

    foreach ($prof in $profiles.GetEnumerator()) {
      $profileName = $prof.Name
      $profileArgs = $prof.Value

      $outDir = Join-Path $outRoot "$sym\$splitName\$profileName"
      New-Item -ItemType Directory -Force -Path $outDir | Out-Null

      Write-Host ">>> Running: $sym | $splitName ($fromS -> $toS) | $profileName" -ForegroundColor Cyan

      $ok = $true
      $err = ""

      try {
        & $py .\backtest_p0.py --baseline --csv $f.FullName --symbol $sym --out_dir $outDir --from $fromS --to $toS @profileArgs | Out-Null
      } catch {
        $ok = $false
        $err = $_.Exception.Message
      }

      $metricsPath = Join-Path $outDir "baseline_metrics.csv"
      if ($ok -and (Test-Path $metricsPath)) {
        $m = Import-Csv $metricsPath | Select-Object -First 1
        $rows.Add([pscustomobject]@{
          symbol = $sym
          split = $splitName
          profile = $profileName
          trades = [double]$m.trades
          net_pnl = [double]$m.net_pnl
          win_rate = [double]$m.win_rate
          final_max_drawdown_pct = [double]$m.final_max_drawdown_pct
          dd_controlled_success = [string]$m.dd_controlled_success
          e2_share = [double]$m.e2_share
          diag_entry_n = $(if ($m.diag_entry_n -ne $null -and $m.diag_entry_n -ne "") { [double]$m.diag_entry_n } else { $null })
          diag_sample_ok = $(if ($m.diag_sample_ok -ne $null -and $m.diag_sample_ok -ne "") { [double]$m.diag_sample_ok } else { $null })
          diag_vol_state_mode = [string]$m.diag_vol_state_mode
          diag_vol_state_squeeze_frac = $(if ($m.diag_vol_state_squeeze_frac -ne $null -and $m.diag_vol_state_squeeze_frac -ne "") { [double]$m.diag_vol_state_squeeze_frac } else { $null })
          diag_vol_state_expanding_frac = $(if ($m.diag_vol_state_expanding_frac -ne $null -and $m.diag_vol_state_expanding_frac -ne "") { [double]$m.diag_vol_state_expanding_frac } else { $null })
          diag_vol_state_normal_frac = $(if ($m.diag_vol_state_normal_frac -ne $null -and $m.diag_vol_state_normal_frac -ne "") { [double]$m.diag_vol_state_normal_frac } else { $null })
          diag_squeeze_frac = $(if ($m.diag_squeeze_frac -ne $null -and $m.diag_squeeze_frac -ne "") { [double]$m.diag_squeeze_frac } else { $null })
          diag_expanding_frac = $(if ($m.diag_expanding_frac -ne $null -and $m.diag_expanding_frac -ne "") { [double]$m.diag_expanding_frac } else { $null })
          diag_normal_frac = $(if ($m.diag_normal_frac -ne $null -and $m.diag_normal_frac -ne "") { [double]$m.diag_normal_frac } else { $null })
          diag_vol_transition = $(if ($m.diag_vol_transition -ne $null -and $m.diag_vol_transition -ne "") { [double]$m.diag_vol_transition } else { $null })
          diag_vol_transition_s2e_frac = $(if ($m.diag_vol_transition_s2e_frac -ne $null -and $m.diag_vol_transition_s2e_frac -ne "") { [double]$m.diag_vol_transition_s2e_frac } else { $null })
          diag_vol_transition_any_frac = $(if ($m.diag_vol_transition_any_frac -ne $null -and $m.diag_vol_transition_any_frac -ne "") { [double]$m.diag_vol_transition_any_frac } else { $null })
          diag_entry_vol_ratio_median = $(if ($m.diag_entry_vol_ratio_median -ne $null -and $m.diag_entry_vol_ratio_median -ne "") { [double]$m.diag_entry_vol_ratio_median } else { $null })
          diag_entry_vol_ratio_q25 = $(if ($m.diag_entry_vol_ratio_q25 -ne $null -and $m.diag_entry_vol_ratio_q25 -ne "") { [double]$m.diag_entry_vol_ratio_q25 } else { $null })
          diag_entry_vol_ratio_q75 = $(if ($m.diag_entry_vol_ratio_q75 -ne $null -and $m.diag_entry_vol_ratio_q75 -ne "") { [double]$m.diag_entry_vol_ratio_q75 } else { $null })
          diag_entry_vol_ratio_p75 = $(if ($m.diag_entry_vol_ratio_p75 -ne $null -and $m.diag_entry_vol_ratio_p75 -ne "") { [double]$m.diag_entry_vol_ratio_p75 } else { $null })
          diag_entry_vol_ratio_p90 = $(if ($m.diag_entry_vol_ratio_p90 -ne $null -and $m.diag_entry_vol_ratio_p90 -ne "") { [double]$m.diag_entry_vol_ratio_p90 } else { $null })
          diag_entry_vol_ratio_high_frac = $(if ($m.diag_entry_vol_ratio_high_frac -ne $null -and $m.diag_entry_vol_ratio_high_frac -ne "") { [double]$m.diag_entry_vol_ratio_high_frac } else { $null })
          diag_session_entry_vol_ratio = $(if ($m.diag_session_entry_vol_ratio -ne $null -and $m.diag_session_entry_vol_ratio -ne "") { [double]$m.diag_session_entry_vol_ratio } else { $null })
          diag_session_entry_vol_ratio_asia_median = $(if ($m.diag_session_entry_vol_ratio_asia_median -ne $null -and $m.diag_session_entry_vol_ratio_asia_median -ne "") { [double]$m.diag_session_entry_vol_ratio_asia_median } else { $null })
          diag_session_entry_vol_ratio_asia_n = $(if ($m.diag_session_entry_vol_ratio_asia_n -ne $null -and $m.diag_session_entry_vol_ratio_asia_n -ne "") { [double]$m.diag_session_entry_vol_ratio_asia_n } else { $null })
          diag_session_entry_vol_ratio_london_median = $(if ($m.diag_session_entry_vol_ratio_london_median -ne $null -and $m.diag_session_entry_vol_ratio_london_median -ne "") { [double]$m.diag_session_entry_vol_ratio_london_median } else { $null })
          diag_session_entry_vol_ratio_london_n = $(if ($m.diag_session_entry_vol_ratio_london_n -ne $null -and $m.diag_session_entry_vol_ratio_london_n -ne "") { [double]$m.diag_session_entry_vol_ratio_london_n } else { $null })
          diag_session_entry_vol_ratio_ny_median = $(if ($m.diag_session_entry_vol_ratio_ny_median -ne $null -and $m.diag_session_entry_vol_ratio_ny_median -ne "") { [double]$m.diag_session_entry_vol_ratio_ny_median } else { $null })
          diag_session_entry_vol_ratio_ny_n = $(if ($m.diag_session_entry_vol_ratio_ny_n -ne $null -and $m.diag_session_entry_vol_ratio_ny_n -ne "") { [double]$m.diag_session_entry_vol_ratio_ny_n } else { $null })
          diag_session_best = [string]$m.diag_session_best
          diag_best_session = [string]$m.diag_best_session
          diag_session_pnl_asia = $(if ($m.diag_session_pnl_asia -ne $null -and $m.diag_session_pnl_asia -ne "") { [double]$m.diag_session_pnl_asia } else { $null })
          diag_session_pnl_london = $(if ($m.diag_session_pnl_london -ne $null -and $m.diag_session_pnl_london -ne "") { [double]$m.diag_session_pnl_london } else { $null })
          diag_session_pnl_ny = $(if ($m.diag_session_pnl_ny -ne $null -and $m.diag_session_pnl_ny -ne "") { [double]$m.diag_session_pnl_ny } else { $null })
          diag_session_count_asia = $(if ($m.diag_session_count_asia -ne $null -and $m.diag_session_count_asia -ne "") { [double]$m.diag_session_count_asia } else { $null })
          diag_session_count_london = $(if ($m.diag_session_count_london -ne $null -and $m.diag_session_count_london -ne "") { [double]$m.diag_session_count_london } else { $null })
          diag_session_count_ny = $(if ($m.diag_session_count_ny -ne $null -and $m.diag_session_count_ny -ne "") { [double]$m.diag_session_count_ny } else { $null })
          diag_session_trades_asia = $(if ($m.diag_session_trades_asia -ne $null -and $m.diag_session_trades_asia -ne "") { [double]$m.diag_session_trades_asia } else { $null })
          diag_session_trades_london = $(if ($m.diag_session_trades_london -ne $null -and $m.diag_session_trades_london -ne "") { [double]$m.diag_session_trades_london } else { $null })
          diag_session_trades_ny = $(if ($m.diag_session_trades_ny -ne $null -and $m.diag_session_trades_ny -ne "") { [double]$m.diag_session_trades_ny } else { $null })
          diag_session_skew_ratio = $(if ($m.diag_session_skew_ratio -ne $null -and $m.diag_session_skew_ratio -ne "") { [double]$m.diag_session_skew_ratio } else { $null })
          diag_adx_available = $(if ($m.diag_adx_available -ne $null -and $m.diag_adx_available -ne "") { [double]$m.diag_adx_available } else { $null })
          diag_adx_median = $(if ($m.diag_adx_median -ne $null -and $m.diag_adx_median -ne "") { [double]$m.diag_adx_median } else { $null })
          diag_adx_p75 = $(if ($m.diag_adx_p75 -ne $null -and $m.diag_adx_p75 -ne "") { [double]$m.diag_adx_p75 } else { $null })
          diag_adx_weak_frac = $(if ($m.diag_adx_weak_frac -ne $null -and $m.diag_adx_weak_frac -ne "") { [double]$m.diag_adx_weak_frac } else { $null })
          diag_adx_trend_frac = $(if ($m.diag_adx_trend_frac -ne $null -and $m.diag_adx_trend_frac -ne "") { [double]$m.diag_adx_trend_frac } else { $null })
          diag_adx_strong_frac = $(if ($m.diag_adx_strong_frac -ne $null -and $m.diag_adx_strong_frac -ne "") { [double]$m.diag_adx_strong_frac } else { $null })
          diag_ema144_regime_long_frac = $(if ($m.diag_ema144_regime_long_frac -ne $null -and $m.diag_ema144_regime_long_frac -ne "") { [double]$m.diag_ema144_regime_long_frac } else { $null })
          diag_ema144_regime_short_frac = $(if ($m.diag_ema144_regime_short_frac -ne $null -and $m.diag_ema144_regime_short_frac -ne "") { [double]$m.diag_ema144_regime_short_frac } else { $null })
          diag_ema_stack_bull_frac = $(if ($m.diag_ema_stack_bull_frac -ne $null -and $m.diag_ema_stack_bull_frac -ne "") { [double]$m.diag_ema_stack_bull_frac } else { $null })
          diag_ema_stack_bear_frac = $(if ($m.diag_ema_stack_bear_frac -ne $null -and $m.diag_ema_stack_bear_frac -ne "") { [double]$m.diag_ema_stack_bear_frac } else { $null })
          diag_ema_stack_mixed_frac = $(if ($m.diag_ema_stack_mixed_frac -ne $null -and $m.diag_ema_stack_mixed_frac -ne "") { [double]$m.diag_ema_stack_mixed_frac } else { $null })
          diag_kd_align_4h_1d_frac = $(if ($m.diag_kd_align_4h_1d_frac -ne $null -and $m.diag_kd_align_4h_1d_frac -ne "") { [double]$m.diag_kd_align_4h_1d_frac } else { $null })
          diag_kd_align_3tf_frac = $(if ($m.diag_kd_align_3tf_frac -ne $null -and $m.diag_kd_align_3tf_frac -ne "") { [double]$m.diag_kd_align_3tf_frac } else { $null })
          diag_kd_4h_k_median = $(if ($m.diag_kd_4h_k_median -ne $null -and $m.diag_kd_4h_k_median -ne "") { [double]$m.diag_kd_4h_k_median } else { $null })
          diag_kd_1d_k_median = $(if ($m.diag_kd_1d_k_median -ne $null -and $m.diag_kd_1d_k_median -ne "") { [double]$m.diag_kd_1d_k_median } else { $null })
          csv = $f.Name
          out_dir = $outDir
          ok = $true
          error = ""
          data_start = $dataStart.ToString("yyyy-MM-dd")
          data_end = $dataEnd.ToString("yyyy-MM-dd")
          window_from = $fromS
          window_to = $toS
          window_days = $winDays
          bars = $bars
        })
      } else {
        $rows.Add([pscustomobject]@{
          symbol = $sym
          split = $splitName
          profile = $profileName
          trades = $null
          net_pnl = $null
          win_rate = $null
          final_max_drawdown_pct = $null
          dd_controlled_success = $null
          e2_share = $null
          diag_entry_n = $null
          diag_sample_ok = $null
          diag_vol_state_mode = $null
          diag_vol_state_squeeze_frac = $null
          diag_vol_state_expanding_frac = $null
          diag_vol_state_normal_frac = $null
          diag_squeeze_frac = $null
          diag_expanding_frac = $null
          diag_normal_frac = $null
          diag_vol_transition = $null
          diag_vol_transition_s2e_frac = $null
          diag_vol_transition_any_frac = $null
          diag_entry_vol_ratio_median = $null
          diag_entry_vol_ratio_q25 = $null
          diag_entry_vol_ratio_q75 = $null
          diag_entry_vol_ratio_p75 = $null
          diag_entry_vol_ratio_p90 = $null
          diag_entry_vol_ratio_high_frac = $null
          diag_session_entry_vol_ratio = $null
          diag_session_entry_vol_ratio_asia_median = $null
          diag_session_entry_vol_ratio_asia_n = $null
          diag_session_entry_vol_ratio_london_median = $null
          diag_session_entry_vol_ratio_london_n = $null
          diag_session_entry_vol_ratio_ny_median = $null
          diag_session_entry_vol_ratio_ny_n = $null
          diag_session_best = $null
          diag_best_session = $null
          diag_session_pnl_asia = $null
          diag_session_pnl_london = $null
          diag_session_pnl_ny = $null
          diag_session_count_asia = $null
          diag_session_count_london = $null
          diag_session_count_ny = $null
          diag_session_trades_asia = $null
          diag_session_trades_london = $null
          diag_session_trades_ny = $null
          diag_session_skew_ratio = $null
          diag_adx_available = $null
          diag_adx_median = $null
          diag_adx_p75 = $null
          diag_adx_weak_frac = $null
          diag_adx_trend_frac = $null
          diag_adx_strong_frac = $null
          diag_ema144_regime_long_frac = $null
          diag_ema144_regime_short_frac = $null
          diag_ema_stack_bull_frac = $null
          diag_ema_stack_bear_frac = $null
          diag_ema_stack_mixed_frac = $null
          diag_kd_align_4h_1d_frac = $null
          diag_kd_align_3tf_frac = $null
          diag_kd_4h_k_median = $null
          diag_kd_1d_k_median = $null
          csv = $f.Name
          out_dir = $outDir
          ok = $false
          error = $(if ($err) { $err } else { "baseline_metrics.csv not found" })
          data_start = $dataStart.ToString("yyyy-MM-dd")
          data_end = $dataEnd.ToString("yyyy-MM-dd")
          window_from = $fromS
          window_to = $toS
          window_days = $winDays
          bars = $bars
        })
      }
    }
  }
}

$summaryPath = Join-Path $outRoot "p0_sweep_summary.csv"
$rows | Export-Csv -Path $summaryPath -NoTypeInformation -Encoding UTF8
Write-Host "`n>>> All done! Summary saved at:" -ForegroundColor Green
Write-Host $summaryPath -ForegroundColor Yellow

$today = Get-Date -Format "yyyyMMdd"
$postPy = @'
import os
import glob
import re
import shutil
from datetime import datetime
import pandas as pd

root = os.environ.get("P0_SWEEP_ROOT", r"d:\Stock\trading_analysis")
out_dir = os.path.join(root, "backtest_out", "p0_sweep")
summary_path = os.path.join(out_dir, "p0_sweep_summary.csv")

df = pd.read_csv(summary_path)
df = df[(df["ok"] == True) & df["symbol"].notna() & df["profile"].notna()].copy()
df = df[df["split"].astype(str).ne("SKIP")]

df["pass_A"] = df["net_pnl"].astype(float) > 0
df["pass_B"] = df["pass_A"] & (df["dd_controlled_success"].astype(str).str.upper() == "OK")

agg = (
    df.groupby(["symbol", "profile"], as_index=False)
    .agg(
        splits=("split", lambda s: ";".join(sorted(set(map(str, s))))),
        n_rows=("split", "size"),
        net_pnl_sum=("net_pnl", "sum"),
        pass_A_any=("pass_A", "any"),
        pass_B_all=("pass_B", "all"),
    )
)

best_rows = []
for sym, g in agg.groupby("symbol"):
    g = g.copy()
    g1 = g[g["pass_B_all"]].sort_values(["net_pnl_sum"], ascending=False)
    if len(g1):
        pick = g1.iloc[0]
        tier = "core"
        sub_tier = ""
        reason = "B_v2: pass_B_all==1"
    else:
        g2 = g[g["pass_A_any"]].sort_values(["net_pnl_sum"], ascending=False)
        if len(g2):
            pick = g2.iloc[0]
            if float(pick["net_pnl_sum"]) > 0:
                tier = "observe"
                sub_tier = "observe_profit"
                reason = "B_v2: pass_B_all==0 & pass_A_any==1 & net_pnl_sum>0"
            else:
                tier = "exclude"
                sub_tier = ""
                reason = "B_v2: net_pnl_sum<=0"
        else:
            g3 = g.sort_values(["net_pnl_sum"], ascending=False)
            pick = g3.iloc[0]
            tier = "exclude"
            sub_tier = ""
            reason = "B_v2: pass_A_any==0"

    diag_vol_state_gate = "C03_SQUEEZE_ONLY" if tier == "core" else "NONE"

    best_rows.append(
        {
            "symbol": sym,
            "tier": tier,
            "sub_tier": sub_tier,
            "reason": reason,
            "best_profile": pick["profile"],
            "splits": pick["splits"],
            "net_pnl_sum": float(pick["net_pnl_sum"]),
            "pass_B_all": int(bool(pick["pass_B_all"])),
            "pass_A_any": int(bool(pick["pass_A_any"])),
            "diag_vol_state_gate": diag_vol_state_gate,
        }
    )

best = pd.DataFrame(best_rows).sort_values(["tier", "net_pnl_sum"], ascending=[True, False])

stamp = os.environ.get("P0_SWEEP_STAMP", datetime.now().strftime("%Y%m%d"))
def _scan_versions(pattern: str) -> list[int]:
    vs: list[int] = []
    for p in glob.glob(pattern):
        m = re.search(r"_v(\d+)\.csv$", os.path.basename(p))
        if m:
            vs.append(int(m.group(1)))
    return vs

existing_vs: list[int] = []
existing_vs += _scan_versions(os.path.join(out_dir, f"p0_sweep_decision_table_{stamp}_v*.csv"))
existing_vs += _scan_versions(os.path.join(out_dir, f"deploy_core_{stamp}_v*.csv"))
existing_vs += _scan_versions(os.path.join(out_dir, f"deploy_observe_{stamp}_v*.csv"))
existing_vs += _scan_versions(os.path.join(out_dir, f"deploy_exclude_{stamp}_v*.csv"))
existing_vs += _scan_versions(os.path.join(out_dir, f"p0_sweep_summary_{stamp}_v*.csv"))
v = (max(existing_vs) + 1) if existing_vs else 2

summary_snapshot_path = os.path.join(out_dir, f"p0_sweep_summary_{stamp}_v{v}.csv")
shutil.copyfile(summary_path, summary_snapshot_path)

decision_path = os.path.join(out_dir, f"p0_sweep_decision_table_{stamp}_v{v}.csv")
best.to_csv(decision_path, index=False)

def _write_deploy(tag: str, sub: pd.DataFrame) -> str:
    p = os.path.join(out_dir, f"deploy_{tag}_{stamp}_v{v}.csv")
    sub.to_csv(p, index=False, encoding="utf-8")
    return p

def _block_split_from_allow(allow_splits: str) -> str:
    parts = [p for p in str(allow_splits or "").split(";") if p]
    if "since2022" in parts:
        return "since2022"
    return parts[0] if parts else ""

def _mk_deploy_rows(df_in: pd.DataFrame, target_tier: str) -> pd.DataFrame:
    action = target_tier.upper()
    out = pd.DataFrame(
        {
            "symbol": df_in["symbol"].astype(str),
            "action": action,
            "profile_override": df_in["best_profile"].astype(str),
            "block_split": df_in["splits"].map(_block_split_from_allow),
            "allow_splits": df_in["splits"].astype(str),
            "target_tier": target_tier,
            "rationale": df_in["reason"].astype(str),
            "diag_vol_state_gate": df_in["diag_vol_state_gate"].astype(str) if "diag_vol_state_gate" in df_in.columns else "",
        }
    )
    return out.fillna("")

core = _mk_deploy_rows(best[best["tier"].eq("core")], "core")
obs = _mk_deploy_rows(best[best["tier"].eq("observe")], "observe")
exc = _mk_deploy_rows(best[best["tier"].eq("exclude")], "exclude")

core_path = _write_deploy("core", core)
obs_path = _write_deploy("observe", obs)
exc_path = _write_deploy("exclude", exc)

print("WROTE", summary_snapshot_path)
print("WROTE", decision_path)
print("WROTE", core_path)
print("WROTE", obs_path)
print("WROTE", exc_path)
print("COUNTS", best["tier"].value_counts().to_dict())
'@

$env:P0_SWEEP_ROOT = $root
$env:P0_SWEEP_STAMP = $today
$postPyB64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($postPy))
$bootstrap = "import base64; exec(base64.b64decode('$postPyB64').decode('utf-8'))"
& $py -c $bootstrap
if ($LASTEXITCODE -ne 0) { throw "postprocess failed (exit=$LASTEXITCODE)" }
Write-Host ">>> Post-process done (B_v2 decision/deploy tables written)." -ForegroundColor Green
