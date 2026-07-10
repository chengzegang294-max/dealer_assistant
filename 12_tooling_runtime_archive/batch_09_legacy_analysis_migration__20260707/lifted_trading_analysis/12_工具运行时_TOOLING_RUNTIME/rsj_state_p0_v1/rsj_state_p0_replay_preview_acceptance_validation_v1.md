# RSJ State P0 回放预览验收校验 v1

- ARCHIVE_ONLY: 该目录为旧库运行时快照；任何执行必须人工确认并设置 `ALLOW_ARCHIVE_ONLY_RUN=1`
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`


## 目的

- 记录 `RSJ State P0` 第一版 `archive preview csv <-> acceptance` 自动对照校验已经通过。
- 历史目标不是重写 acceptance，而是确认 acceptance 中写明的 3 行 preview 样例与实际 preview csv 完全一致。

## 本次验收对象

- preview csv：
  - `rsj_state_p0_replay_preview_rows_v1.csv`
- preview acceptance：
  - `rsj_state_p0_replay_preview_acceptance_v1.md`
- validation script：
  - `rsj_state_p0_validate_replay_preview_acceptance_v1.py`

## ARCHIVE_ONLY 历史命令样例

```bash
$env:ALLOW_ARCHIVE_ONLY_RUN = "1"
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_validate_replay_preview_acceptance_v1.py
```

## 校验结果

- validation 输出确认：
  - `validation_mode = archive_preview_acceptance_compare`
  - `preview_csv_exists = True`
  - `acceptance_md_exists = True`
  - `preview_row_count = 3`
  - `acceptance_row_count = 3`
  - `rows_match = true`
  - `preview_trade_ids = ["RSJ_RAW_SAMPLE_001", "RSJ_RAW_SAMPLE_002", "RSJ_RAW_SAMPLE_003"]`
  - `write_attempted = false`
  - `archive_preview_acceptance_validation_passed = true`

## 历史可接受结论

- `RSJ State P0` 已具备：
  - `preview csv` 与 `acceptance` 文本之间的一致性自动校验
- 历史上还不能宣称：
  - 已把 preview 行回写仓内运行产物
  - 已接 repo-first 历史 raw window 数据



