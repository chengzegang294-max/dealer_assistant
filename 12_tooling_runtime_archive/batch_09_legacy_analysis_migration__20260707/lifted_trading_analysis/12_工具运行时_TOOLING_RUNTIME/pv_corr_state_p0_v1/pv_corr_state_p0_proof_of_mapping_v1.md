# pv_corr_state_p0_proof_of_mapping_v1

- ARCHIVE_ONLY_PROOF_MAPPING: 本文件只保留旧 `PV Corr State P0` 的历史映射样本说明，不作为默认入口。
- repo-first 历史入口参考：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 目的

- 用一组手工样本证明 `pv_corr_state_p0_min_contract_v1` 的字段映射可复核。
- 历史 proof 样本不代表 repo-first 历史运行时落盘，只用于映射核对。

## 文件

- proof_input：
  - `real_input_samples\pv_corr_state_p0_proof_input_v1.csv`
- proof_output：
  - `real_input_samples\pv_corr_state_p0_proof_output_v1.csv`

## proof 样本说明

- 样本数：`5`
- 目标覆盖：
  - `confirm`
  - `diverge`
  - `neutral`
  - `up_confirm`
  - `down_confirm`
  - `price_up_volume_down`
  - `price_down_volume_up`

## 映射核对点

- `pv_sync_state`
  - `abs(pv_corr_score) >= 0.30` 且价量同号 -> `confirm`
  - `abs(pv_corr_score) >= 0.30` 且价量异号 -> `diverge`
  - `abs(pv_corr_score) < 0.30` -> `neutral`
- `pv_pressure_bias`
  - `confirm + price_up -> up_confirm`
  - `confirm + price_down -> down_confirm`
  - `diverge -> mixed`
  - `neutral -> none`
- `pv_extreme_flag`
  - `price_up + volume_down -> price_up_volume_down`
  - `price_down + volume_up -> price_down_volume_up`

## 历史边界

- v1 proof 不证明相关性本身如何最优计算，只证明标签映射口径。
- v1 proof 不接入主线执行，不产生交易信号。
