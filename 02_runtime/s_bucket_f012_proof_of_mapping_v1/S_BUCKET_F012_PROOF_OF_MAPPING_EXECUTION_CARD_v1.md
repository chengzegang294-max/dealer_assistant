# S_BUCKET_F012_PROOF_OF_MAPPING_EXECUTION_CARD_V1

## 对象

- `object_id`：`SBKT_F012`
- `current_role`：`LABELING_METHOD`
- `mapping_target`：`method_support_mapping`

## 生成入口

- `source_path`：`10_source_library_archive\mirror_kimi_inbox\S_BUCKET_batch2_evidence_excerpt_table_v1.tsv`
- `detail_truth_anchor`：`10_source_library_archive\mirror_kimi_inbox\99_回收与外部回帖_IMPORTS\S_BUCKET_batch2_priority_read_v1__text_review__imported_2026-06-26.md`
- `producer`：`02_runtime\s_bucket_f012_proof_of_mapping_v1\s_bucket_f012_proof_of_mapping_v1.py`
- `scope`：`supporting proof-of-mapping only`
- `status`：`diag_only_proof`

## 当前三件套

- `real_input_csv`：`02_runtime\s_bucket_f012_proof_of_mapping_v1\real_input_samples\f012_proof_input_sample_v1.csv`
- `proof_script_py`：`02_runtime\s_bucket_f012_proof_of_mapping_v1\s_bucket_f012_proof_of_mapping_v1.py`
- `proof_output_csv`：`02_runtime\s_bucket_f012_proof_of_mapping_v1\real_input_samples\f012_proof_output_v1.csv`

## 当前作用

- 证明 `F012` 的数据标注 supporting 合同可被 repo 内样本和脚本稳定复现。
- 为 `F005` 蓝图层与 `F004` 验证层提供下游标注层入口。
- 不把 `proof_output_csv` 写入任何主 runtime CSV。

## 当前禁令

- 不宣称 `F012` 已锁定唯一最优标签方案。
- 不宣称 `F012` 已接入任何主 runtime CSV。
- 不在标注或回测中混入未来信息。
