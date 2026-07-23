# 601991_SH 第二只样本 stub 校验记录

更新时间：2026-07-14

## 文件类型

- `INDEX_NOTE`

## 原路径

- `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/chzl_bsd_structure_bundle/601991_SH_structure_seed_v1.tsv`
- `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/chzl_bsd_structure_bundle/auto_series/601991_SH_structure_series_v1.tsv`
- `02_runtime/butler_r0_ohlcv_object_cards/acceptance_outputs/chzl_bsd_601991_sh_semi_auto_output.json`

## 新路径

- `batch_148/00_raw_snapshot/601991_SH_second_sample_stub_validation_note__20260714.md`

## 生成入口

- `run_chzl_bsd_sample_stub_v1.py`

## 当前作用

- 固化第二只样本 `601991.SH` 已进入 runtime bundle，并完成一次半自动 stub 输出校验。
- 把“已有最小人工 seed”推进到“已可生成最小 JSON 证明”，但不冒充完整结构引擎真值。

## 本次校验输入

- `daily_sample`
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/watchlist_subset/601991_SH_1d.csv`
- `weekly_sample`
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/weekly_subset/601991_SH_1w.csv`
- `auto_structure_series`
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/chzl_bsd_structure_bundle/auto_series/601991_SH_structure_series_v1.tsv`
- `annotation_seed`
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/chzl_bsd_structure_bundle/601991_SH_structure_seed_v1.tsv`

## 校验结果

- 输出文件：
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_outputs/chzl_bsd_601991_sh_semi_auto_output.json`
- 当前 `evidence_mode`：
  - `semi_auto_structure_with_seed_override`
- 当前 `input_rows`：
  - `daily = 1538`
  - `weekly = 326`
  - `structure_series_rows = 179`
  - `annotation_rows = 3`
- 当前 `signal_payload` 关键字段：
  - `chzl_bsd_type = 1B`
  - `chzl_filter_action = APPROVE`
  - `chzl_risk_action = HALF_SIZE`
  - `chzl_size_scalar = 0.5`
- 当前 `acceptance_flags`：
  - `passed_annotation_binding = true`
  - `passed_auto_structure_binding = true`
  - `degraded = true`

## 当前边界

- 这次校验只证明：
  - 第二只样本已具备 `daily + weekly + auto_series + seed` 的最小半自动输出链
- 这次校验不证明：
  - `CHZL_BSD` 已完成完整分型/笔/中枢/背驰自动引擎
  - `601991.SH` 的人工 seed 已达到完整结构真值

## 当前结论

- `batch_148` 的真实缺口已从“第二只 seed 未正式落盘”
  收缩为：
  - “第二只样本仍只是半自动 stub 级验证，不是完整结构真值”
- 因而当前可把第二只样本写成：
  - `semi_auto_seed_bound_and_stub_validated`
