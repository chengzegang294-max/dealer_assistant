# RSJ State P0 回放预览验收 v1

- ARCHIVE_ONLY: 该目录为旧库运行时快照；任何执行必须人工确认并设置 `ALLOW_ARCHIVE_ONLY_RUN=1`
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`
- 当前动作已切到“维护态抽查”：
  - 继续逐份人工过眼 archive 壳，不回到旧链路入口（ARCHIVE_ONLY）

## 目的

- 记录 `RSJ State P0` 第一版 replay preview 导出的历史验收结果。
- 历史目标不是写入 runtime csv，而是把 replay 中会新增的 3 行 append-ready row 固化到独立 preview csv，作为旧链路的肉眼复核样例。

## 本次验收对象

- params 模板：
  - `rsj_state_p0_runtime_params_template_v1.json`
- preview 导出脚本：
  - `rsj_state_p0_export_replay_preview_v1.py`
- preview csv：
  - `rsj_state_p0_replay_preview_rows_v1.csv`
- replay 脚本：
  - `rsj_state_p0_simulate_append_diff_v1.py`

## ARCHIVE_ONLY 历史命令样例

```bash
$env:ALLOW_ARCHIVE_ONLY_RUN = "1"
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_export_replay_preview_v1.py
```

## 导出结果

- preview 导出输出确认：
  - `preview_mode = archive_replay_preview_export`
  - `runtime_csv_exists = True`
  - `sample_csv_exists = True`
  - `preview_csv = rsj_state_p0_replay_preview_rows_v1.csv`
  - `before_row_count = 5`
  - `preview_row_count = 3`
  - `after_replay_row_count = 8`
  - `preview_trade_ids = ["RSJ_RAW_SAMPLE_001", "RSJ_RAW_SAMPLE_002", "RSJ_RAW_SAMPLE_003"]`
  - `runtime_write_attempted = false`
  - `archive_preview_export_passed = true`
- preview csv 当时内容：
  - `RSJ_RAW_SAMPLE_001,0.6727,warm,extreme_high,risk_on,valid,rv_up_gt_rv_down_strong`
  - `RSJ_RAW_SAMPLE_002,0.0200,neutral,none,wait,valid,balanced_window`
  - `RSJ_RAW_SAMPLE_003,-0.6800,cold,extreme_low,risk_off,valid,rv_down_gt_rv_up_strong`

## 历史可接受结论

- `RSJ State P0` 在旧链路中已具备：
  - `sample -> mapping -> compatibility -> replay diff -> preview csv` 的只读闭环
  - 可单独抽看 replay 会新增的 3 行样例
- 历史上仍不能宣称：
  - 已把 preview 结果回写仓内运行产物
  - 已接 repo-first 历史 raw window 数据

## 当时下一步（非当前 repo-first 计划）

- 若当时继续推进同一条线，最顺动作是：
  - 维持 archive 壳抽查口径；若无新异常，仍维持不写 runtime
