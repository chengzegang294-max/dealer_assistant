# N02 运行引用核对说明 v1

## 作用

- 给 `REOPEN_B9_N02_SESSION_OR_P0` 提供一个只读的 runtime/ref-check：不重跑生成链、不改写主 runtime，只核对关键产物与当前停点一致性。
- 目标是让“主线入口 + 迁移地图 + runtime 总览”在 `NO failed breakout` 边界下保持单一真值。

## 输入/输出

- `GENERATOR`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_runtime_ref_check_v1.py`
- `ARTIFACT`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_runtime_ref_check_report_v1.json`
- `INDEX_NOTE`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_runtime_ref_check_runtime_notes_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_runtime_ref_check_acceptance_v1.md`

## 核对范围（写死）

- `downstream summary gate.status` 必须为：
  - `gbpusd_m15_slice_downstream_plus_or_break_only_beyond_multi_session_persistence_done_without_failed_breakout`
- `or_break_only beyond multi-session` 的 summary 与 card_summary：
  - `rows == sum(status_counts)`
- `00_主线检索索引.md` 与 `FULL_REPO_MIGRATION_MAP.md` 必须包含上述 `expected_gate_status`

## 运行方式

```bash
python 12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_runtime_ref_check_v1.py --strict
```

## 2026-07-06 fresh-run

- `writes_main_runtime=false`
- `includes_failed_breakout=false`
- `ok=true`
- `report_json=12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\n02_runtime_ref_check_report_v1.json`
