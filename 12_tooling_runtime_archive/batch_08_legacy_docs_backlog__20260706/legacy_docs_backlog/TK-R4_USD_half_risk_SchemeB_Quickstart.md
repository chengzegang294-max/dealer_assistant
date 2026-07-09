# TK-R4 USD 半风险方案 B 快速开始

## 定位

- 这是一个默认关闭的方案 B 风控壳候选：`USD 同向主题暴露 -> 新增仓 half-risk`
- 不改 baseline 默认执行路径；只做 accounting / audit 落盘与摘要输出
- 当前正式角色：`global_candidate_with_watchlist`（observe-only watchlist）

## 一键复跑

```powershell
$env:ALLOW_ARCHIVE_ONLY_RUN=1
cd d:\Stock\trading_assistant
.\.venv\Scripts\python.exe .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\tk_r4_usd_half_risk_scheme_b_runner.py --preset fast --date_tag 20260611 --support_min 3
```

- 如果缺 `b118_position_level`，用 full（自动补齐 `b118 -> b120 -> b122 -> b123 -> b124`）：

```powershell
$env:ALLOW_ARCHIVE_ONLY_RUN=1
cd d:\Stock\trading_assistant
.\.venv\Scripts\python.exe .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\tk_r4_usd_half_risk_scheme_b_runner.py --preset full --date_tag 20260611 --support_min 3 --p0_sweep_dir backtest_out\p0_sweep
```

## 关键产物

- b120（off/on 两 split 的核算与 summary）：
  - `backtest_out\stage2\indicator_audit\{date_tag}_b120_tk_r4_usd_half_risk_scheme_b_*`
- b124（最终角色合约 + watchlist 合约 + 验证摘要）：
  - `backtest_out\stage2\indicator_audit\{date_tag}_b124_tk_r4_usd_half_risk_role_finalize_v1\`
    - `b124_usd_half_risk_role_contract_{date_tag}_v1.csv`
    - `b124_usd_half_risk_watchlist_contract_{date_tag}_v1.csv`
    - `b124_usd_half_risk_validation_summary_{date_tag}_v1.csv`

## 单文件真值（推荐）

- 终端摘要固化（含 coverage + inputs_index）：
  - `...b124_usd_half_risk_terminal_brief_{date_tag}_v1.txt`
- 运行证据包（含 coverage / inputs_index / provenance / outputs_grouped）：
  - `...b124_usd_half_risk_run_manifest_{date_tag}_v1.json`
  - 额外包含：
    - `validation`：off 是否严格等于 baseline（按 split）
    - `status`：`ok / missing_inputs / validation_failed`

## 不变量

- `enabled_default = False`
- `hard_gate_enabled = False`
- baseline 默认行为不变（`off == baseline`）
