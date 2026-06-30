# S_BUCKET_F006_PROOF_OF_MAPPING_EXECUTION_CARD_V1

## 对象

- `object_id`：`SBKT_F006`
- `current_role`：`ENTER_FUNCTION_CORE_WITH_BOUNDARY`
- `mapping_target`：`field_to_library_mapping`

## 生成入口

- `source_path`：`10_source_library_archive\mirror_kimi_inbox\S_BUCKET_round3_function_core_f006_combo_fields_v1.tsv`
- `producer`：`02_runtime\s_bucket_f006_proof_of_mapping_v1\s_bucket_f006_proof_of_mapping_v1.py`
- `scope`：`proof-of-mapping only`
- `status`：`diag_only_proof`

## 当前三件套

- `real_input_csv`：`02_runtime\s_bucket_f006_proof_of_mapping_v1\real_input_samples\f006_proof_input_sample_v1.csv`
- `proof_script_py`：`02_runtime\s_bucket_f006_proof_of_mapping_v1\s_bucket_f006_proof_of_mapping_v1.py`
- `proof_output_csv`：`02_runtime\s_bucket_f006_proof_of_mapping_v1\real_input_samples\f006_proof_output_v1.csv`

## 当前作用

- 证明 `F006` 的字段合同可被 repo 内样本和脚本稳定复现。
- 不把 `proof_output_csv` 写入任何主 runtime CSV。

## 当前禁令

- 不宣称 `industry_mv_neutralizer` 的数值中性化公式已被完整工程化实现。
- 不宣称 `F006` 已接入任何主 runtime CSV。
