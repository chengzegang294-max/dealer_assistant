# S_BUCKET_F012_PROOF_OF_MAPPING_V1

## 角色

- 本目录只用于 `SBKT_F012` 的 `proof-of-mapping`。
- 当前目标是证明 `stock_pool_input + label_scheme_input + xgboost_mode_input + random_seed_batch_input`
  如何映射到 `F012` 的标注方法 supporting 输出合同。
- 当前不把任何结果写回主 runtime CSV，不宣称已真实接入或已形成交易信号。

## 当前三件套

- `real_input_csv`
  - `real_input_samples\f012_proof_input_sample_v1.csv`
- `proof_script_py`
  - `s_bucket_f012_proof_of_mapping_v1.py`
- `proof_output_csv`
  - `real_input_samples\f012_proof_output_v1.csv`

## 默认读法

- 先看 `S_BUCKET_proof_of_mapping_priority_queue_v1.tsv`，确认 `F012` 是 `F005` 之后的 method-support 对象。
- 再看 `S_BUCKET_function_object_master_registry_v1.tsv`，确认 `F012` 的 `LABELING_METHOD` 角色。
- 再看 `S_BUCKET_batch2_evidence_excerpt_table_v1.tsv` 与 `S_BUCKET_batch2_priority_read_v1__text_review__imported_2026-06-26.md`，确认超额收益率、IR、Calmar 与 `XGBR-Combine` 的边界。
- 最后在本目录运行脚本，落本地 proof 输出 CSV。

## 复现命令

```bash
python 02_runtime\s_bucket_f012_proof_of_mapping_v1\s_bucket_f012_proof_of_mapping_v1.py
```

## 最小验收

- `proof_output_csv` 成功生成。
- 输出行数与 `real_input_csv` 一致。
- 每行都明确标出：
  - `label_scheme_scope`
  - `xgbr_combine_flag`
  - `random_seed_stability_flag`
  - `future_leakage_guard_flag`
- 所有结果只表示“method-support 映射证据已落盘”，不表示“已确定唯一最优标签方案”。
