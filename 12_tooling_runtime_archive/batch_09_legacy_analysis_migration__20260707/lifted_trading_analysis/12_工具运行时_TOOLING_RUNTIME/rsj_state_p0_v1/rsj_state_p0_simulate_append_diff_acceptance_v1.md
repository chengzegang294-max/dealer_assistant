# RSJ State P0 模拟追加差异验收 v1

- ARCHIVE_ONLY: 该目录为旧库运行时快照；任何执行必须人工确认并设置 `ALLOW_ARCHIVE_ONLY_RUN=1`
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 目的

- 记录 `RSJ State P0` 第一版 `simulate append compare / no-write replay` 已经通过。
- 历史目标不是写入 runtime csv，而是把 `sample mapping` 生成的 3 行 append-ready row，和现有 `proof append` 形成的旧链路 runtime csv 做一次内存态前后对照。

## 本次验收对象

- params 模板：
  - `rsj_state_p0_runtime_params_template_v1.json`
- replay 脚本：
  - `rsj_state_p0_simulate_append_diff_v1.py`
- mapping validator：
  - `rsj_state_p0_validate_raw_window_mapping_v1.py`
- append stub：
  - `rsj_state_p0_runtime_append_stub_v1.py`
- legacy runtime csv：
  - `rsj_state_p0_fields_runtime_v1.csv`

## ARCHIVE_ONLY 历史命令样例

```bash
$env:ALLOW_ARCHIVE_ONLY_RUN = "1"
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_simulate_append_diff_v1.py
```

## 对照结果

- replay 输出确认：
  - `replay_mode = archive_simulate_append_diff`
  - `runtime_csv_exists = True`
  - `sample_csv_exists = True`
  - `before_row_count = 5`
  - `mapped_row_count = 3`
  - `after_replay_row_count = 8`
  - `before_trade_ids = ["RSJ_P0_001", "RSJ_P0_002", "RSJ_P0_003", "RSJ_P0_004", "RSJ_P0_005"]`
  - `mapped_trade_ids = ["RSJ_RAW_SAMPLE_001", "RSJ_RAW_SAMPLE_002", "RSJ_RAW_SAMPLE_003"]`
  - `overlapping_trade_ids = []`
  - `removed_trade_ids = []`
  - `newly_appended_trade_ids = ["RSJ_RAW_SAMPLE_001", "RSJ_RAW_SAMPLE_002", "RSJ_RAW_SAMPLE_003"]`
  - `write_attempted = false`
  - `archive_replay_passed = true`

## 历史可接受结论

- `RSJ State P0` 已具备：
  - `sample input -> mapping -> append compatibility -> simulated append diff` 的无写入闭环
  - 对当时 proof runtime csv 的内存态前后差异说明
- 历史上还不能宣称：
  - 已把 replay 结果回写仓内运行产物
  - 已接 repo-first 历史 raw window 数据

## 当时下一步（非当前 repo-first 计划）

- 若继续推进同一条线，最顺动作是：
  - 再决定是否补一层“replay diff 结果与 acceptance 样例行固化”，仍默认不落盘

