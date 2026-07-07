# rsj_state_p0_runtime_append_acceptance_v1

- ARCHIVE_ONLY: 该目录为旧库运行时快照；任何执行必须人工确认并设置 `ALLOW_ARCHIVE_ONLY_RUN=1`
- repo-first 历史入口参考：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 目的

- 记录 `RSJ State P0` 首批 `params template + append stub` 的历史 `dry-run + persist` 验收结论。
- 把“手工 proof 已存在”推进到“runtime csv 已有首批 persist proof 行”的历史收口状态。

## 本次验收对象

- params 模板：
  - `rsj_state_p0_runtime_params_template_v1.json`
- append stub：
  - `rsj_state_p0_runtime_append_stub_v1.py`
- proof 输出：
  - `real_input_samples\rsj_state_p0_proof_output_v1.csv`
- runtime csv：
  - `rsj_state_p0_fields_runtime_v1.csv`

## ARCHIVE_ONLY 历史命令样例

```bash
$env:ALLOW_ARCHIVE_ONLY_RUN = "1"
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_runtime_append_stub_v1.py
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\12_工具运行时_TOOLING_RUNTIME\rsj_state_p0_v1\rsj_state_p0_runtime_append_stub_v1.py --persist
```

## dry-run 结果

- 已成功读取：
  - `rsj_state_p0_runtime_params_template_v1.json`
  - `real_input_samples\rsj_state_p0_proof_output_v1.csv`
- 已成功校验：
  - `rsj_state_p0_fields_runtime_v1.csv` 表头与 `v1` 合同一致
- 已成功完成 dry-run 内存追加：
  - `rows_before_cleanup = 1`
  - `proof_rows_loaded = 5`
  - `rows_before_append = 0`
  - `rows_after_append = 5`
- 已确认：
  - 第一条 proof 行可被 stub 正常读取
  - `placeholder` 行在内存态会被清除
-  - 当时样例默认 `dry_run_only = true`

## persist 结果

- 已成功执行：
  - `--persist`
- 已成功写回：
  - `rsj_state_p0_fields_runtime_v1.csv`
- 已确认当时 runtime csv 为：
  - `RSJ_P0_001`
  - `RSJ_P0_002`
  - `RSJ_P0_003`
  - `RSJ_P0_004`
  - `RSJ_P0_005`
- 已确认：
  - `__PLACEHOLDER__` 不再保留
  - 当时 runtime 行数 = `5`

## 历史可接受结论

- `RSJ State P0` 已具备：
  - `params template`
  - `append stub`
  - `proof -> runtime` 的最小 dry-run 验证
  - `proof -> runtime` 的首批 persist 验证
- 历史上还不能宣称：
  - 已接 repo-first 历史收益率流重建
  - 已成为 `N01` 或主线择时字段

## 当时下一步（历史计划备注）

- 若继续推进同一条线，最顺动作是：
  - 再决定是否值得补 `append_from_raw_window` 独立脚本
  - 再决定是否需要第二批 proof 或多周期扩样


