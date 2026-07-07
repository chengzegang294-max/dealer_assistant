# pv_corr_state_p0_bar_window_sample_acceptance_v1

- ARCHIVE_ONLY: 该目录为旧库运行时快照；任何执行必须人工确认并设置 `ALLOW_ARCHIVE_ONLY_RUN=1`

## 目的

- 记录 `PV Corr State P0` 第一版 `bar window sample` 读取校验已经通过。
- 历史目标不是回写任何仓内运行产物，而是确认样例 csv 与 header、字段约束、参数索引一致。

## 本次验收对象

- params 模板：
  - `pv_corr_state_p0_runtime_params_template_v1.json`
- sample schema：
  - `pv_corr_state_p0_bar_window_sample_schema_v1.md`
- sample input：
  - `real_input_samples\pv_corr_state_p0_bar_window_sample_input_v1.csv`
- sample validator：
  - `pv_corr_state_p0_validate_bar_window_sample_v1.py`

## ARCHIVE_ONLY 历史命令样例

```bash
$env:ALLOW_ARCHIVE_ONLY_RUN = "1"
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\pv_corr_state_p0_validate_bar_window_sample_v1.py
```

## 校验结果

- 已成功读取：
  - `pv_corr_state_p0_runtime_params_template_v1.json`
  - `pv_corr_state_p0_bar_window_input_header_v1.txt`
  - `real_input_samples\pv_corr_state_p0_bar_window_sample_input_v1.csv`
- 校验输出确认：
  - `validation_mode = archive_history_read_only`
  - `sample_csv_exists = True`
  - `header_match = true`
  - `rows_loaded = 3`
  - `trade_id_unique = True`
  - `invalid_rows = 0`
  - `input_source_tiers = ["archive_history", "synthetic_window"]`
  - `input_volume_kinds = ["synthetic_volume", "tick_volume"]`
  - `write_attempted = false`
  - `validation_passed = true`

## 历史可接受结论

- `PV Corr State P0` 已具备：
  - 可被参数模板稳定索引的 `bar window sample input`
  - 一次只读样例读取校验闭环
- 历史上还不能宣称：
  - 已接 repo-first 历史 bar window 数据
  - 已把 sample csv 接入 runtime append

## 当时下一步（非当前 repo-first 计划）

- 若继续推进同一条线，最顺动作是：
  - 再决定是否要补“sample -> append 映射校验”而不是直接扩展到 repo-first 历史绑定说明


