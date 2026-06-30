# S_BUCKET_F009_PROOF_OF_MAPPING_EXECUTION_CARD_V1

## 对象

- `object_id`：`SBKT_F009`
- `current_role`：`HOLDING_INFERENCE_FILTER`
- `mapping_target`：`supporting_object_mapping`

## 生成入口

- `source_path`：`10_source_library_archive\mirror_kimi_inbox\S_BUCKET_batch2_evidence_excerpt_table_v1.tsv`
- `detail_truth_anchor`：`10_source_library_archive\mirror_kimi_inbox\99_回收与外部回帖_IMPORTS\S_BUCKET_batch2_priority_read_v1__text_review__imported_2026-06-26.md`
- `producer`：`02_runtime\s_bucket_f009_proof_of_mapping_v1\s_bucket_f009_proof_of_mapping_v1.py`
- `scope`：`supporting proof-of-mapping only`
- `status`：`diag_only_proof`

## 当前三件套

- `real_input_csv`：`02_runtime\s_bucket_f009_proof_of_mapping_v1\real_input_samples\f009_proof_input_sample_v1.csv`
- `proof_script_py`：`02_runtime\s_bucket_f009_proof_of_mapping_v1\s_bucket_f009_proof_of_mapping_v1.py`
- `proof_output_csv`：`02_runtime\s_bucket_f009_proof_of_mapping_v1\real_input_samples\f009_proof_output_v1.csv`

## 当前作用

- 证明 `F009` 的持仓变化预估 supporting 合同可被 repo 内样本和脚本稳定复现。
- 为 `F007` 的低频季报结论提供一个高频互证入口。
- 不把 `proof_output_csv` 写入任何主 runtime CSV。

## 当前禁令

- 不宣称 `F009` 的预估持仓变化等于实际披露。
- 不忽视高持仓与无持仓样本差异。
- 不宣称 `F009` 已接入任何主 runtime CSV。
