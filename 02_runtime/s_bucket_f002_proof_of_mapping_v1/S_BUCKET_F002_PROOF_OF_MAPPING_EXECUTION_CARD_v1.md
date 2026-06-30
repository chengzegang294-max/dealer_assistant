# S_BUCKET_F002_PROOF_OF_MAPPING_EXECUTION_CARD_V1

## 对象

- `object_id`：`SBKT_F002`
- `current_role`：`KEEP_AS_LIMITED_CANDIDATE`
- `mapping_target`：`guard_to_library_mapping`

## 生成入口

- `source_path`：`10_source_library_archive\mirror_kimi_inbox\S_BUCKET_round3_function_core_f002_guard_fields_v1.tsv`
- `producer`：`02_runtime\s_bucket_f002_proof_of_mapping_v1\s_bucket_f002_proof_of_mapping_v1.py`
- `scope`：`proof-of-mapping only`
- `status`：`diag_only_proof`

## 当前三件套

- `real_input_csv`：`02_runtime\s_bucket_f002_proof_of_mapping_v1\real_input_samples\f002_proof_input_sample_v1.csv`
- `proof_script_py`：`02_runtime\s_bucket_f002_proof_of_mapping_v1\s_bucket_f002_proof_of_mapping_v1.py`
- `proof_output_csv`：`02_runtime\s_bucket_f002_proof_of_mapping_v1\real_input_samples\f002_proof_output_v1.csv`

## 当前作用

- 证明 `F002` 的 guard 字段合同可被 repo 内样本和脚本稳定复现。
- 不把 `proof_output_csv` 写入任何主 runtime CSV。

## 当前禁令

- 不宣称 `F002` 已成为多头 alpha 接口。
- 不宣称 `F002` 已接入任何主 runtime CSV。
