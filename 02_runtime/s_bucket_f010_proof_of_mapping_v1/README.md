# S_BUCKET_F010_PROOF_OF_MAPPING_V1

## 角色

- 本目录只用于 `SBKT_F010` 的 `proof-of-mapping`。
- 当前目标是证明 `snapshot_3s_input + order_queue_input + dft_volume_signal_input + peak_ratio_input`
  如何映射到 `F010` 的机构活跃度监测 supporting 输出合同。
- 当前不把任何结果写回主 runtime CSV，不宣称已真实接入或已形成交易信号。

## 当前三件套

- `real_input_csv`
  - `real_input_samples\f010_proof_input_sample_v1.csv`
- `proof_script_py`
  - `s_bucket_f010_proof_of_mapping_v1.py`
- `proof_output_csv`
  - `real_input_samples\f010_proof_output_v1.csv`

## 默认读法

- 先看 `S_BUCKET_proof_of_mapping_priority_queue_v1.tsv`，确认 `F010` 是 `F009` 之后的 supporting 对象。
- 再看 `S_BUCKET_function_object_master_registry_v1.tsv`，确认 `F010` 的 `INSTITUTION_ACTIVITY_MONITOR` 角色。
- 再看 `S_BUCKET_batch2_evidence_excerpt_table_v1.tsv`，确认 `B+S / B-S / B/S` 的方向性与平稳性边界。
- 最后在本目录运行脚本，落本地 proof 输出 CSV。

## 复现命令

```bash
python 02_runtime\s_bucket_f010_proof_of_mapping_v1\s_bucket_f010_proof_of_mapping_v1.py
```

## 最小验收

- `proof_output_csv` 成功生成。
- 输出行数与 `real_input_csv` 一致。
- 每行都明确标出：
  - `b_plus_s_monitor_signal`
  - `b_minus_s_stability_flag`
  - `b_div_s_direction_flag`
  - `f009_cross_check_ready_flag`
- 所有结果只表示“supporting institution monitor 映射证据已落盘”，不表示“已实现机构算法交易识别引擎”。
