# n02_runtime_ref_check acceptance v1

## 最小验收

- 必须存在：
  - `n02_runtime_ref_check_v1.py`
  - `n02_runtime_ref_check_report_v1.json`
- `n02_runtime_ref_check_report_v1.json` 必须满足：
  - `ok=true`
  - `expected_gate_status=gbpusd_m15_slice_downstream_plus_or_break_only_beyond_multi_session_persistence_done_without_failed_breakout`
  - `checks.downstream_gate_status.ok=true`
  - `checks.or_only_beyond_multi_session_status_counts_match_rows.ok=true`
  - `checks.or_only_beyond_multi_session_card_status_counts_match_rows.ok=true`
  - `checks.main_index_contains_expected_gate.contains=true`
  - `checks.full_repo_migration_map_contains_expected_gate.contains=true`

## 运行命令（强制）

```bash
python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_runtime_ref_check_v1.py --strict
```

## 2026-07-06 验收结论

- `PASS`
