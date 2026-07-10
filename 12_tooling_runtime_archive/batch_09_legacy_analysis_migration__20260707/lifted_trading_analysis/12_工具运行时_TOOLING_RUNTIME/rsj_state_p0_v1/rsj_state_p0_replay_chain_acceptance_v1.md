# RSJ State P0 回放链路验收 v1

- ARCHIVE_ONLY: 该目录为旧库运行时快照；任何执行必须人工确认并设置 `ALLOW_ARCHIVE_ONLY_RUN=1`
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 目的

- 记录 `RSJ State P0` 第一版 `replay chain validation` 的历史通过结果。
- 历史目标不是写入 runtime csv，而是把 `simulate append diff -> replay preview export -> preview acceptance compare` 收成一层历史总链路校验。

## 本次验收对象

- replay chain validator：
  - `rsj_state_p0_validate_replay_chain_v1.py`
- replay diff：
  - `rsj_state_p0_simulate_append_diff_v1.py`
- preview export：
  - `rsj_state_p0_export_replay_preview_v1.py`
- preview acceptance validator：
  - `rsj_state_p0_validate_replay_preview_acceptance_v1.py`

## ARCHIVE_ONLY 历史命令样例

```bash
$env:ALLOW_ARCHIVE_ONLY_RUN = "1"
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_validate_replay_chain_v1.py
```

## 校验结果

- validation 输出确认：
  - `validation_mode = archive_replay_chain_validation`
  - `runtime_csv_exists = True`
  - `sample_csv_exists = True`
  - `preview_csv_exists = True`
  - `preview_acceptance_md_exists = True`
  - `runtime_row_count = 5`
  - `mapped_row_count = 3`
  - `appended_row_count = 3`
  - `after_replay_row_count = 8`
  - `preview_row_count = 3`
  - `acceptance_row_count = 3`
  - `preview_trade_ids = ["RSJ_RAW_SAMPLE_001", "RSJ_RAW_SAMPLE_002", "RSJ_RAW_SAMPLE_003"]`
  - `rows_match = true`
  - `write_attempted = false`
  - `archive_replay_chain_passed = true`

## 历史可接受结论

- `RSJ State P0` 在旧链路中已具备：
  - `simulate append diff -> replay preview export -> preview acceptance compare` 的总链路只读校验
  - replay 新增行、preview csv 与 acceptance 文本三者一致性确认
- 历史上仍不能宣称：
  - 已把 replay 结果回写仓内运行产物
  - 已接 repo-first 历史 raw window 数据


