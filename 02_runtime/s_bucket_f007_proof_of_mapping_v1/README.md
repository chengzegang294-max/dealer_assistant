# S_BUCKET_F007_PROOF_OF_MAPPING_V1

## 角色

- 本目录只用于 `SBKT_F007` 的 `proof-of-mapping`。
- 当前目标是证明 `fund_top10_holdings_input + fund_quality_bucket_input + barra_style_regime_input + delta_to_float_ashare_input`
  如何映射到 `F007` 的 supporting filter 输出合同。
- 当前不把任何结果写回主 runtime CSV，不宣称已真实接入或已形成 round3 function core。

## 当前三件套

- `real_input_csv`
  - `real_input_samples\f007_proof_input_sample_v1.csv`
- `proof_script_py`
  - `s_bucket_f007_proof_of_mapping_v1.py`
- `proof_output_csv`
  - `real_input_samples\f007_proof_output_v1.csv`

## 默认读法

- 先看 `S_BUCKET_proof_of_mapping_priority_queue_v1.tsv`，确认 `F007` 是当前 `queue_rank=4` 的 supporting 对象。
- 再看 `S_BUCKET_function_object_master_registry_v1.tsv`，确认 `F007` 的 supporting filter 角色。
- 再看 `S_BUCKET_功能映射表_v1.tsv` 与 `S_BUCKET_batch1_priority_read_v1__text_review__imported_2026-06-24.md`，确认输入边界、风格边界和禁令。
- 最后在本目录运行脚本，落本地 proof 输出 CSV。

## 复现命令

```bash
python 02_runtime\s_bucket_f007_proof_of_mapping_v1\s_bucket_f007_proof_of_mapping_v1.py
```

## 最小验收

- `proof_output_csv` 成功生成。
- 输出行数与 `real_input_csv` 一致。
- 每行都明确标出：
  - `filter_pool_decision`
  - `weight_constraint_bucket`
  - `style_match_flag`
  - `small_fund_exclusion_flag`
  - `cross_check_ready_flag`
- 所有结果只表示“supporting filter 映射证据已落盘”，不表示“已工程化实现基金重仓股策略”。
