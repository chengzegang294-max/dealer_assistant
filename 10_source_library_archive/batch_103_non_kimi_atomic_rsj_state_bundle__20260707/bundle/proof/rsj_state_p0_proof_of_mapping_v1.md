# rsj_state_p0_proof_of_mapping_v1

- ARCHIVE_ONLY_PROOF_MAPPING: 本文件只保留旧 `RSJ State P0` 的历史映射样本说明，不作为默认入口。
- repo-first 历史入口参考：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 目的

- 用一组手工样本证明 `rsj_state_p0_min_contract_v1` 的字段映射可复核。
- 历史 proof 样本不代表 repo-first 历史运行时落盘，只用于映射核对。

## 文件

- proof_input：
  - `real_input_samples\rsj_state_p0_proof_input_v1.csv`
- proof_output：
  - `real_input_samples\rsj_state_p0_proof_output_v1.csv`

## proof 样本说明

- 样本数：`5`
- 目标覆盖：
  - `warm`
  - `cold`
  - `neutral`
  - `extreme_high`
  - `extreme_low`

## 映射核对点

- `rsj_score = (rv_up - rv_down) / (rv_up + rv_down)`
- `rsj_state`：
  - `>= 0.20 -> warm`
  - `<= -0.20 -> cold`
  - 其余 -> `neutral`
- `rsj_extreme_flag`：
  - `>= 0.50 -> extreme_high`
  - `<= -0.50 -> extreme_low`
  - 其余 -> `none`
- `rsj_timing_bias`：
  - `warm -> risk_on`
  - `cold -> risk_off`
  - `neutral -> wait`

## 历史边界

- v1 proof 不证明 `RSJ` 的最佳窗口或最佳阈值，只证明字段映射口径。
- v1 proof 不接入 `N01`、不进入历史主线，不作为交易建议。
