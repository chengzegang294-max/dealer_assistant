# RSJ State P0 原始窗口映射验收 v1

- ARCHIVE_ONLY: 该目录为旧库运行时快照；任何执行必须人工确认并设置 `ALLOW_ARCHIVE_ONLY_RUN=1`
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 目的

- 记录 `RSJ State P0` 第一版 `raw window sample -> append-ready row` 映射校验已经通过。
- 历史目标不是回写任何仓内运行产物，而是确认历史样例输入经过 `P0` 合同映射后，能产出与归档输出表头一致的 append-ready 行。

## 本次验收对象

- params 模板：
  - `rsj_state_p0_runtime_params_template_v1.json`
- sample input：
  - `real_input_samples\rsj_state_p0_raw_window_sample_input_v1.csv`
- output header：
  - `rsj_state_p0_fields_output_header_v1.txt`
- mapping validator：
  - `rsj_state_p0_validate_raw_window_mapping_v1.py`

## ARCHIVE_ONLY 历史命令样例

```bash
$env:ALLOW_ARCHIVE_ONLY_RUN = "1"
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_validate_raw_window_mapping_v1.py
```

## 校验结果

- 已成功读取：
  - `rsj_state_p0_runtime_params_template_v1.json`
  - `real_input_samples\rsj_state_p0_raw_window_sample_input_v1.csv`
  - `rsj_state_p0_fields_output_header_v1.txt`
- 映射输出确认：
  - `mapping_mode = archive_history_to_append_ready`
  - `sample_csv_exists = True`
  - `output_header_match = true`
  - `rows_mapped = 3`
  - `mapped_trade_ids = ["RSJ_RAW_SAMPLE_001", "RSJ_RAW_SAMPLE_002", "RSJ_RAW_SAMPLE_003"]`
  - `model_state_counts = {"valid": 3}`
  - `rsj_state_counts = {"cold": 1, "neutral": 1, "warm": 1}`
  - `write_attempted = false`
  - `mapping_passed = true`

## 历史可接受结论

- `RSJ State P0` 已具备：
  - 从 `raw window sample input` 到 `append-ready output row` 的只读映射校验闭环
  - 与 `rsj_state_p0_fields_output_header_v1.txt` 对齐的字段顺序
- 历史上还不能宣称：
  - 已把映射结果回写仓内运行产物
  - 已接 repo-first 历史 raw window 数据

## 当时下一步（非当前 repo-first 计划）

- 若继续推进同一条线，最顺动作是：
  - 再决定是否补“mapping result 与 runtime append stub 的无写入联调”而不是扩展到任何 repo-first 当前来源


