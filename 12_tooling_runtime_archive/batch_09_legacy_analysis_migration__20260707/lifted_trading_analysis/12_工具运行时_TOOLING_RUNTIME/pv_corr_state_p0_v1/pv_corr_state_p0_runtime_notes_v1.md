# pv_corr_state_p0_runtime_notes_v1

- ARCHIVE_ONLY_RUNTIME_MIRROR: 本文件记录旧 `PV Corr State P0` 运行时快照，不作为默认入口。
- repo-first 历史入口参考：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 角色

- 这份文件属于 `12_工具运行时_TOOLING_RUNTIME`。
- 作用是记录 `PV Corr State P0` 历史运行口径与可宣称边界。

## 历史状态

- 历史目录当时已创建：
  - `12_工具运行时_TOOLING_RUNTIME\pv_corr_state_p0_v1\`
- 历史上已新增：
  - `pv_corr_state_p0_min_contract_v1.md`
  - `pv_corr_state_p0_proof_of_mapping_v1.md`
  - `pv_corr_state_p0_fields_output_header_v1.txt`
  - `pv_corr_state_p0_runtime_params_template_v1.json`
  - `pv_corr_state_p0_runtime_append_stub_v1.py`
  - `pv_corr_state_p0_runtime_append_acceptance_v1.md`
  - `pv_corr_state_p0_append_from_bar_window_stub_v1.py`
  - `pv_corr_state_p0_bar_window_stub_acceptance_v1.md`
  - `pv_corr_state_p0_bar_window_input_contract_v1.md`
  - `pv_corr_state_p0_bar_window_input_header_v1.txt`
  - `pv_corr_state_p0_bar_window_sample_schema_v1.md`
  - `pv_corr_state_p0_validate_bar_window_sample_v1.py`
  - `pv_corr_state_p0_bar_window_sample_acceptance_v1.md`
  - `pv_corr_state_p0_validate_bar_window_mapping_v1.py`
  - `pv_corr_state_p0_bar_window_mapping_acceptance_v1.md`
  - `pv_corr_state_p0_validate_append_compatibility_v1.py`
  - `pv_corr_state_p0_append_compatibility_acceptance_v1.md`
  - `pv_corr_state_p0_simulate_append_diff_v1.py`
  - `pv_corr_state_p0_simulate_append_diff_acceptance_v1.md`
  - `pv_corr_state_p0_export_replay_preview_v1.py`
  - `pv_corr_state_p0_replay_preview_rows_v1.csv`
  - `pv_corr_state_p0_replay_preview_acceptance_v1.md`
  - `pv_corr_state_p0_validate_replay_preview_acceptance_v1.py`
  - `pv_corr_state_p0_replay_preview_acceptance_validation_v1.md`
  - `pv_corr_state_p0_validate_replay_chain_v1.py`
  - `pv_corr_state_p0_replay_chain_acceptance_v1.md`
  - `pv_corr_state_p0_export_chain_summary_index_v1.py`
  - `pv_corr_state_p0_chain_summary_index_v1.md`
  - `pv_corr_state_p0_validate_chain_summary_acceptance_compare_v1.py`
  - `pv_corr_state_p0_chain_summary_acceptance_compare_v1.md`
  - `pv_corr_state_p0_export_manifest_freeze_v1.py`
  - `pv_corr_state_p0_manifest_freeze_v1.md`
  - `pv_corr_state_p0_fields_runtime_v1.csv`
  - `real_input_samples\pv_corr_state_p0_bar_window_sample_input_v1.csv`
  - `real_input_samples\pv_corr_state_p0_proof_input_v1.csv`
  - `real_input_samples\pv_corr_state_p0_proof_output_v1.csv`
- 这批历史文件的角色是：
  - 固定 `价量相关性` 的最小输入/输出合同
  - 固定第一版表头
  - 固定第一版手工 proof-of-mapping 样本
  - 固定第一版 `params template + append stub`
  - 固定第一版 `proof -> runtime csv` 的最小闭环
- 历史上不应把本目录内容描述为：
  - 已接 repo-first 历史运行链路
  - 已回测完成
  - 已成为 repo-first 历史价量因子

## 历史冻结表头

- `trade_id`
- `pv_sync_state`
- `pv_pressure_bias`
- `pv_extreme_flag`
- `pv_model_state`
- `proof_basis`

## 历史冻结边界

- 只覆盖 `PV Corr State P0` 的最小标签映射字段。
- 历史边界不含：
  - 相关性最优窗口搜索
  - A 股分层中性化
  - 多因子综合打分
  - 入场/离场规则
  - 仓位倍率

## 历史旧链路口径

- `pv_sync_state`：
  - `abs(pv_corr_score) >= 0.30` 且价量同号 -> `confirm`
  - `abs(pv_corr_score) >= 0.30` 且价量异号 -> `diverge`
  - 其余 -> `neutral`
- `pv_pressure_bias`：
  - `confirm + price_up -> up_confirm`
  - `confirm + price_down -> down_confirm`
  - `diverge -> mixed`
  - `neutral -> none`

## 字段枚举约束

- `pv_sync_state`
  - `confirm / diverge / neutral / unknown`
- `pv_pressure_bias`
  - `up_confirm / down_confirm / mixed / none / unknown`
- `pv_extreme_flag`
  - `price_up_volume_down / price_down_volume_up / none / unknown`
- `pv_model_state`
  - `valid / invalid / unknown`

## 历史可宣称

- 已进入工具运行时准备阶段。
- 已固定第一版最小合同。
- 已冻结第一版输出表头。
- 已固定第一版 proof-of-mapping 样本。
- 已固定第一版 `params template`。
- 已固定第一版 `append stub`。
- 已完成一次 dry-run。
- 已完成一次 `--persist`。
- 当时 runtime csv 行数：
  - `5`
- 已固定第一版 `append_from_bar_window` 接口空壳。
- 已完成一次 `append_from_bar_window --dry-run`。
- 已冻结第一版 `bar window input contract`。
- 已冻结第一版 `bar window sample schema`。
- 已落第一版 `bar window sample input csv`。
- 已完成一次 `bar window sample` 只读读取校验。
- 已完成一次 `bar window sample -> append-ready row` 只读映射校验。
- 已完成一次 `append-ready row -> append stub` 无写入兼容性联调。
- 已完成一次 `proof runtime csv -> simulated append diff` 无写入前后对照。
- 已完成一次 `replay preview csv` 导出。
- 已完成一次 `preview csv <-> acceptance` 自动对照校验。
- 已完成一次 `replay chain validation` 总链路只读校验。
- 已完成一次 `chain summary index export`。
- 已完成一次 `chain summary acceptance compare`。
- 已完成一次 `manifest freeze export`。
- 已纳入根层 `cross_line_frozen_manifest_index_v1` 跨线统一入口。

## 历史不可宣称

- 不可宣称已进入 repo-first 历史 runtime append 链路。
- 不可宣称 `价量相关性` 已成为主线历史入场字段。
- 不可宣称当时记录中的相关性阈值已经过历史最优化验证。
