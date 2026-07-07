# rsj_state_p0_append_compatibility_acceptance_v1

- ARCHIVE_ONLY: 该目录为旧库运行时快照；任何执行必须人工确认并设置 `ALLOW_ARCHIVE_ONLY_RUN=1`
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`


## 目的

- 记录 `RSJ State P0` 第一版 `sample mapping -> append stub` 无写入兼容性联调已经通过。
- 历史目标不是回写任何仓内运行产物，而是确认 `mapping validator` 产出的 append-ready 行，可以被现有 `append stub` 的表头校验、去重逻辑和内存追加流程稳定接受。

## 本次验收对象

- params 模板：
  - `rsj_state_p0_runtime_params_template_v1.json`
- sample input：
  - `real_input_samples\rsj_state_p0_raw_window_sample_input_v1.csv`
- mapping validator：
  - `rsj_state_p0_validate_raw_window_mapping_v1.py`
- append compatibility validator：
  - `rsj_state_p0_validate_append_compatibility_v1.py`
- runtime append stub：
  - `rsj_state_p0_runtime_append_stub_v1.py`
- runtime csv：
  - `rsj_state_p0_fields_runtime_v1.csv`

## ARCHIVE_ONLY 历史命令样例

```bash
$env:ALLOW_ARCHIVE_ONLY_RUN = "1"
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_validate_append_compatibility_v1.py
```

## 联调结果

- 已成功校验：
  - `rsj_state_p0_fields_runtime_v1.csv` 表头与 append 合同一致
  - `sample mapping` 产出的字段顺序与 `append stub` 期望一致
- 无写入联调输出确认：
  - `compatibility_mode = archive_history_to_append_stub`
  - `runtime_csv_exists = True`
  - `sample_csv_exists = True`
  - `append_header_match = true`
  - `rows_before_cleanup = 5`
  - `mapped_rows_loaded = 3`
  - `rows_before_append = 5`
  - `rows_after_dedupe = 5`
  - `rows_after_append = 8`
  - `mapped_trade_ids = ["RSJ_RAW_SAMPLE_001", "RSJ_RAW_SAMPLE_002", "RSJ_RAW_SAMPLE_003"]`
  - `write_attempted = false`
  - `compatibility_passed = true`

## 历史可接受结论

- `RSJ State P0` 已具备：
  - `sample input -> append-ready row` 的映射闭环
  - `append-ready row -> append stub` 的无写入兼容性闭环
- 历史上还不能宣称：
  - 已把历史样例映射结果回写仓内运行产物
  - 已接 repo-first 历史 raw window 数据

## 当时下一步（非当前 repo-first 计划）

- 若继续推进同一条线，最顺动作是：
  - 再决定是否补“sample mapping 与 append stub 的模拟落盘对照”，仍默认不扩展到 repo-first 当前来源



