# S_BUCKET_F009_PROOF_OF_MAPPING_V1

## 角色

- 本目录只用于 `SBKT_F009` 的 `proof-of-mapping`。
- 当前目标是证明 `excess_return_input + large_order_buy_ratio_input + net_main_buy_ratio_input + prior_holding_change_input + disclosure_lag_days`
  如何映射到 `F009` 的持仓变化预估与偏离监测 supporting 输出合同。
- 当前不把任何结果写回主 runtime CSV，不宣称已真实接入或已形成交易信号。

## 当前三件套

- `real_input_csv`
  - `real_input_samples\f009_proof_input_sample_v1.csv`
- `proof_script_py`
  - `s_bucket_f009_proof_of_mapping_v1.py`
- `proof_output_csv`
  - `real_input_samples\f009_proof_output_v1.csv`

## 默认读法

- 先看 `S_BUCKET_proof_of_mapping_priority_queue_v1.tsv`，确认 `F009` 是 `F007` 之后的 supporting 对象。
- 再看 `S_BUCKET_function_object_master_registry_v1.tsv`，确认 `F009` 的 `HOLDING_INFERENCE_FILTER` 角色。
- 再看 `S_BUCKET_batch2_evidence_excerpt_table_v1.tsv`，确认高持仓解释力与季报滞后边界。
- 最后在本目录运行脚本，落本地 proof 输出 CSV。

## 复现命令

```bash
python 02_runtime\s_bucket_f009_proof_of_mapping_v1\s_bucket_f009_proof_of_mapping_v1.py
```

## 最小验收

- `proof_output_csv` 成功生成。
- 输出行数与 `real_input_csv` 一致。
- 每行都明确标出：
  - `holding_change_estimate_signal`
  - `style_deviation_monitor_flag`
  - `high_holding_strength_flag`
  - `low_freq_cross_check_flag`
- 所有结果只表示“supporting holding inference 映射证据已落盘”，不表示“已实现持仓预测模型”。
