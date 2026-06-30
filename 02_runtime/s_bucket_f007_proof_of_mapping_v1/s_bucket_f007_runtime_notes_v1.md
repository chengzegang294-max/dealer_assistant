# s_bucket_f007_runtime_notes_v1

## 当前状态

- 当前运行时目录：
  - `02_runtime\s_bucket_f007_proof_of_mapping_v1`
- 当前已具备：
  - `README.md`
  - `S_BUCKET_F007_PROOF_OF_MAPPING_EXECUTION_CARD_v1.md`
  - `S_BUCKET_F007_PROOF_OF_MAPPING_ARTIFACT_INDEX_v1.md`
  - `s_bucket_f007_proof_of_mapping_v1.py`
  - `real_input_samples\f007_proof_input_sample_v1.csv`
  - `real_input_samples\f007_proof_output_v1.csv`
- 当前实跑结果：
  - `proof_output_path=02_runtime\s_bucket_f007_proof_of_mapping_v1\real_input_samples\f007_proof_output_v1.csv`
  - `row_count=3`

## 当前可宣称

- 已完成 `SBKT_F007` 的 supporting proof-of-mapping 最小三件套落盘。
- 已把 proof 与 `F007` 的对象级 truth anchor 绑定到 repo 内。
- 已形成一条可复现命令。
- 已实际运行一次脚本并生成 `3` 行 `proof_output_csv`。

## 当前不可宣称

- 不可宣称 `F007` 的基金重仓股筛选逻辑已完整工程化实现。
- 不可宣称 `F007` 已接入任何主 runtime CSV。
- 不可宣称 `F007` 已升级为 `round3 function core`。

## 复现命令

```bash
python 02_runtime\s_bucket_f007_proof_of_mapping_v1\s_bucket_f007_proof_of_mapping_v1.py
```
