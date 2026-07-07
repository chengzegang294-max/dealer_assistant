# rsj_state_p0_raw_window_stub_acceptance_v1

- ARCHIVE_ONLY: 该目录为旧库运行时快照；任何执行必须人工确认并设置 `ALLOW_ARCHIVE_ONLY_RUN=1`
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`


## 目的

- 记录 `RSJ State P0` 的 `append_from_raw_window` 接口空壳已完成只读 dry-run 验证。
- 历史目标不是接 repo-first 历史外部数据，而是确认接口壳、参数口径、目标 CSV 指向都成立。

## 本次验收对象

- params 模板：
  - `rsj_state_p0_runtime_params_template_v1.json`
- raw-window stub：
  - `rsj_state_p0_append_from_raw_window_stub_v1.py`
- target csv：
  - `rsj_state_p0_fields_runtime_v1.csv`

## ARCHIVE_ONLY 历史命令样例

```bash
$env:ALLOW_ARCHIVE_ONLY_RUN = "1"
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_append_from_raw_window_stub_v1.py --dry-run
```

## dry-run 结果

- 已成功读取：
  - `rsj_state_p0_runtime_params_template_v1.json`
- dry-run 输出确认：
  - `interface_mode = dry_run`
  - `binding_state = unbound`
  - `source_kind = pending_raw_window_series`
  - `allow_live_binding = False`
  - `allow_raw_window_append = False`
  - `target_csv_exists = True`
  - `write_attempted = false`
  - `dry_run_only = true`
- 已确认 required fields：
  - `window_bars`
  - `rv_up`
  - `rv_down`

## 历史可接受结论

- `RSJ State P0` 已具备：
  - `proof -> runtime` 的最小 persist 闭环
  - 面向未来 raw-window 绑定的接口空壳
- 历史上还不能宣称：
  - 已接 repo-first 历史 raw window 数据
-  - 已触发任何历史 append 写入

## 当时下一步（非当前 repo-first 计划）

- 若继续推进同一条线，最顺动作是：
  - 再决定 raw-window 输入契约是否要显式拆成独立 CSV/JSON schema



