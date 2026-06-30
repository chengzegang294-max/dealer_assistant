# s_bucket_f002_runtime_notes_v1

## 当前状态

- 当前运行时目录：
  - `02_runtime\s_bucket_f002_proof_of_mapping_v1`
- 当前已具备：
  - `README.md`
  - `S_BUCKET_F002_PROOF_OF_MAPPING_EXECUTION_CARD_v1.md`
  - `S_BUCKET_F002_PROOF_OF_MAPPING_ARTIFACT_INDEX_v1.md`
  - `s_bucket_f002_proof_of_mapping_v1.py`
  - `real_input_samples\f002_proof_input_sample_v1.csv`
  - `real_input_samples\f002_proof_output_v1.csv`
- 当前实跑结果：
  - `proof_output_path=02_runtime\s_bucket_f002_proof_of_mapping_v1\real_input_samples\f002_proof_output_v1.csv`
  - `row_count=3`

## 当前可宣称

- 已完成 `SBKT_F002` 的 proof-of-mapping 最小三件套落盘。
- 已把 proof 与 `F002` 的字段级 truth anchor 绑定到 repo 内。
- 已形成一条可复现命令。
- 已把 `guard_decision_output / residualize_required_flag / long_only_block_flag` 落成可复核输出列。

## 当前不可宣称

- 不可宣称 `F002` 已回到多头增强链路。
- 不可宣称 `F002` 已接入任何主 runtime CSV。

## 复现命令

```bash
python 02_runtime\s_bucket_f002_proof_of_mapping_v1\s_bucket_f002_proof_of_mapping_v1.py
```
