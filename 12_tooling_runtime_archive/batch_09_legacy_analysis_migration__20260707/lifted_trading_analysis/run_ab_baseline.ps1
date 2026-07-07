$py = ".\.venv\Scripts\python.exe"
$symbols = @("XAUUSD", "GER40", "NAS100")

# 增强基线 (A) - 显式开启所有工程增强开关 (使用1代表True)
$enhArgs = @(
  "--enable-score-filter", "1",
  "--enable-score-sizing", "1",
  "--e1-fail-k", "1.5",
  "--e1-bb-squeeze-veto", "1",
  "--enable-e1-atr-regime-gate", "1",
  "--enable-e2-break-confirm", "1",
  "--e2-touch-requires-strong", "1"
)

# 严格基线 (B) - 显式关闭所有增强 (严格复刻P0文档)
$docArgs = @(
  "--enable-score-filter", "0",
  "--enable-score-sizing", "0",
  "--e1-fail-k", "0",
  "--e1-bb-squeeze-veto", "0",
  "--e1-min-break-strength-atr", "0",
  "--e1-max-retest-depth-atr", "0",
  "--enable-e1-atr-regime-gate", "0",
  "--enable-e2-break-confirm", "0",
  "--e2-touch-requires-strong", "0"
)

# 1. 批量运行 3 个品种的 A / B 基线回测
foreach ($sym in $symbols) {
    Write-Host "`n>>> 正在运行 $sym 的 A_enhanced (工程增强) ..." -ForegroundColor Green
    & $py .\backtest_p0.py --baseline --csv "data\${sym}_1h.csv" --out_dir "backtest_out\p0_lab\${sym}\A_enhanced" @enhArgs

    Write-Host ">>> 正在运行 $sym 的 B_doc (严格文档) ..." -ForegroundColor Yellow
    & $py .\backtest_p0.py --baseline --csv "data\${sym}_1h.csv" --out_dir "backtest_out\p0_lab\${sym}\B_doc" @docArgs
}

# 2. 自动摘取关键 metrics 方便你复制给 Chatbox
Write-Host "`n================ 回测结果摘要 (请复制以下内容给AI面板) ================" -ForegroundColor Cyan
$roots = @()
foreach ($sym in $symbols) {
    $roots += ".\backtest_out\p0_lab\${sym}\A_enhanced\baseline_summary.csv"
    $roots += ".\backtest_out\p0_lab\${sym}\B_doc\baseline_summary.csv"
}

Get-Item $roots -ErrorAction SilentlyContinue | ForEach-Object {
    "`n==== " + $_.FullName.Substring($_.FullName.IndexOf("p0_lab")) + " ===="
    # 只提取最核心的前8行指标 (交易笔数, PnL, 胜率, 均盈, 回撤等)
    Get-Content $_.FullName | Select-Object -First 8
}