# YTC Existing Daily Weekly Runtime Anchor Historical Recovered

更新时间：2026-07-13

- 文件类型：`ARTIFACT`
- 原路径：`02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/*` + `02_runtime/butler_r0_ohlcv_object_cards/acceptance_outputs/ytc_601991_sh_daily_weekly_output.json`
- 新路径：`10_source_library_archive/batch_147_ytc_sample_intake_absorb__20260713/00_raw_snapshot/YTC_existing_daily_weekly_runtime_anchor__historical_recovered.md`
- 生成入口：`historical_recovered_runtime_reference`
- 适用对象：`YTC`
- 当前作用：说明仓内已存在的 `daily+weekly` 降级路径样本与最小运行输出
- 证据强度：`historical_recovered`
- 缺口：仍缺 `60m/5m` 真样本

## 已有锚点

- `601991_SH_1d.csv`
- `601991_SH_1w.csv`
- `ytc_601991_sh_daily_weekly_output.json`
- 对应生成入口：
  - `run_ytc_daily_weekly_minimal_v1.py`

## 当前判断

- 仓内已经证明：
  - `YTC` 能在 `daily+weekly` 降级路径下最小实跑
- 仓内还没有证明：
  - `YTC` 的 `60m/5m` 分钟级样本可追溯落盘
- 所以下一刀不是重做说明，而是补分钟级样本。
