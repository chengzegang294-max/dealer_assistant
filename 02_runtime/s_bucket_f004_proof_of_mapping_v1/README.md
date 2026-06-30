# S_BUCKET_F004_PROOF_OF_MAPPING_V1

## 角色

- 本目录只用于 `SBKT_F004` 的 `proof-of-mapping`。
- 当前目标是证明 `monthly_factor_pool_input + annual_rolling_window_input + group_time_series_split_input + base_model_input`
  如何映射到 `F004` 的训练流程验证规范 supporting 输出合同。
- 当前不把任何结果写回主 runtime CSV，不宣称已真实接入或已形成交易信号。

## 当前三件套

- `real_input_csv`
  - `real_input_samples\f004_proof_input_sample_v1.csv`
- `proof_script_py`
  - `s_bucket_f004_proof_of_mapping_v1.py`
- `proof_output_csv`
  - `real_input_samples\f004_proof_output_v1.csv`

## 默认读法

- 先看 `S_BUCKET_proof_of_mapping_priority_queue_v1.tsv`，确认 `F004` 是 `F010` 之后的 method-support 对象。
- 再看 `S_BUCKET_function_object_master_registry_v1.tsv`，确认 `F004` 的 `TRAINING_RISK_METHOD` 角色。
- 再看 `S_BUCKET_功能映射表_v1.tsv` 与 `S_BUCKET_batch1_priority_read_v1__text_review__imported_2026-06-24.md`，确认 `GroupTimeSeriesSplit`、年度滚动训练与欠拟合边界。
- 最后在本目录运行脚本，落本地 proof 输出 CSV。

## 复现命令

```bash
python 02_runtime\s_bucket_f004_proof_of_mapping_v1\s_bucket_f004_proof_of_mapping_v1.py
```

## 最小验收

- `proof_output_csv` 成功生成。
- 输出行数与 `real_input_csv` 一致。
- 每行都明确标出：
  - `cv_protocol_decision`
  - `leakage_control_flag`
  - `underfit_risk_flag`
  - `method_scope_label`
- 所有结果只表示“method-support 映射证据已落盘”，不表示“已实现完整训练引擎”。
