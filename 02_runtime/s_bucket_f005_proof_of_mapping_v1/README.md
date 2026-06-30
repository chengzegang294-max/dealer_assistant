# S_BUCKET_F005_PROOF_OF_MAPPING_V1

## 角色

- 本目录只用于 `SBKT_F005` 的 `proof-of-mapping`。
- 当前目标是证明 `raw_ohlcv_universe_input + genetic_programming_factor_input + random_forest_selection_input + shap_explanation_input`
  如何映射到 `F005` 的 AI 选股体系蓝图 supporting 输出合同。
- 当前不把任何结果写回主 runtime CSV，不宣称已真实接入或已形成交易信号。

## 当前三件套

- `real_input_csv`
  - `real_input_samples\f005_proof_input_sample_v1.csv`
- `proof_script_py`
  - `s_bucket_f005_proof_of_mapping_v1.py`
- `proof_output_csv`
  - `real_input_samples\f005_proof_output_v1.csv`

## 默认读法

- 先看 `S_BUCKET_proof_of_mapping_priority_queue_v1.tsv`，确认 `F005` 是 `F004` 之后的 blueprint-support 对象。
- 再看 `S_BUCKET_function_object_master_registry_v1.tsv`，确认 `F005` 的 `AI_SYSTEM_BLUEPRINT` 角色。
- 再看 `S_BUCKET_batch2_evidence_excerpt_table_v1.tsv` 与 `S_BUCKET_batch2_priority_read_v1__text_review__imported_2026-06-26.md`，确认遗传规划、随机森林与 SHAP 的层级关系。
- 最后在本目录运行脚本，落本地 proof 输出 CSV。

## 复现命令

```bash
python 02_runtime\s_bucket_f005_proof_of_mapping_v1\s_bucket_f005_proof_of_mapping_v1.py
```

## 最小验收

- `proof_output_csv` 成功生成。
- 输出行数与 `real_input_csv` 一致。
- 每行都明确标出：
  - `factor_mining_stage`
  - `feature_selection_stage`
  - `explanation_stage`
  - `blueprint_scope_label`
- 所有结果只表示“blueprint-support 映射证据已落盘”，不表示“已实现端到端 AI 交易系统”。
