# S_BUCKET_F006_PROOF_OF_MAPPING_V1

## 角色

- 本目录只用于 `SBKT_F006` 的 `proof-of-mapping`。
- 当前目标是证明 `daily_ohlcv_base + industry_mv_neutralizer + id2_std_3m_raw + hml_r_std_5m_raw`
  如何映射到 `F006` 的字段级入口合同。
- 当前不把任何结果写回主 runtime CSV，不宣称已真实接入或已形成门控。

## 当前三件套

- `real_input_csv`
  - `real_input_samples\f006_proof_input_sample_v1.csv`
- `proof_script_py`
  - `s_bucket_f006_proof_of_mapping_v1.py`
- `proof_output_csv`
  - `real_input_samples\f006_proof_output_v1.csv`

## 默认读法

- 先看 `S_BUCKET_proof_of_mapping_priority_queue_v1.tsv`，确认 `F006` 是当前 `queue_rank=2`。
- 再看 `S_BUCKET_round3_function_core_function_library_entry_v1.tsv`，确认 `F006` 的默认组件与顺序。
- 再看 `S_BUCKET_round3_function_core_f006_combo_fields_v1.tsv`，确认字段级输入输出与组合列。
- 最后在本目录运行脚本，落本地 proof 输出 CSV。

## 复现命令

```bash
python 02_runtime\s_bucket_f006_proof_of_mapping_v1\s_bucket_f006_proof_of_mapping_v1.py
```

## 最小验收

- `proof_output_csv` 成功生成。
- 输出行数与 `real_input_csv` 一致。
- 每行都明确标出：
  - `base_input_source`
  - `neutralizer_source`
  - `primary_factor_output`
  - `secondary_factor_output`
  - `combo_output_column`
- 所有结果只表示“字段映射证据已落盘”，不表示“实盘/回测接入已完成”。
