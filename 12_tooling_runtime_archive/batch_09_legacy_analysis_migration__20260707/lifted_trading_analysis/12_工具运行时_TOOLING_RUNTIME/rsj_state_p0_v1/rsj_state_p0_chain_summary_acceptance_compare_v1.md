# rsj_state_p0_chain_summary_acceptance_compare_v1

- ARCHIVE_ONLY: 该目录为旧库运行时快照；任何执行必须人工确认并设置 `ALLOW_ARCHIVE_ONLY_RUN=1`
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`
- 当前动作已切到“维护态抽查”：
  - 继续逐份人工过眼 archive 壳，不回到旧链路入口（ARCHIVE_ONLY）

## 目的

- 记录 `RSJ State P0` 第一版 `chain summary acceptance compare` 已经通过。
- 历史目标不是改写总索引，而是确认总索引文档中的 `10` 个 stage 文件列表与实际预期清单完全一致。

## 本次验收对象

- chain summary index：
  - `rsj_state_p0_chain_summary_index_v1.md`
- compare validator：
  - `rsj_state_p0_validate_chain_summary_acceptance_compare_v1.py`

## ARCHIVE_ONLY 历史命令样例

```bash
$env:ALLOW_ARCHIVE_ONLY_RUN = "1"
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_validate_chain_summary_acceptance_compare_v1.py
```

## 校验结果

- validation 输出确认：
  - `validation_mode = chain_summary_acceptance_compare`
  - `chain_summary_md_exists = True`
  - `indexed_stage_count = 10`
  - `expected_stage_count = 10`
  - `rows_match = true`
  - `write_attempted = false`
  - `chain_summary_acceptance_compare_passed = true`

## 历史可接受结论

- `RSJ State P0` 的总索引正文与预期冻结 stage 清单一致。
- 历史上还不能宣称：
  - 已进入 repo-first 历史 runtime append
  - 已接 repo-first 历史 raw window 数据


