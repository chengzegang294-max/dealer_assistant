# DY_R1_KD_MTF_P0 历史镜像

ARCHIVE_ONLY_RUNTIME_MIRROR: 本目录是旧仓 `KD_MTF_P0` 的历史运行时镜像，不作为当前默认续跑入口。

当前优先入口：
- `d:\Stock\trading_assistant\01_active_objects\`
- `d:\Stock\trading_assistant\02_runtime\`
- `d:\Stock\trading_assistant\04_active_main_docs\`

## 用途

- 这是旧仓 `DY-R1 / KD_MTF_P0` 的历史独立包镜像。
- 目标是保留当时的阅读、复核与运行时追溯关系，不再把本目录当成当前默认续跑工作目录。
- 旧目录当前不移动；后续若有必要，再按同口径双边同步修正。

## 当前独立化范围

- 已内置当前主线文档、append stub、params、header、runtime csv、proof csv。
- 已内置上游 canonical bars 样本：
  - `upstream_samples\n01_first_real_input_bars_v1.csv`
- `kd_mtf_p0_runtime_params_template_v1.json` 已改为指向本目录。

## 包内清单

- 入口卡：
  - `kd_mtf_p0_directory_index_card_v1.md`
  - `kd_mtf_p0_quick_entry_card_v1.md`
  - `kd_mtf_p0_object_responsibility_card_v1.md`
- runtime 与协议：
  - `kd_mtf_p0_fields_runtime_header_v1.txt`
  - `kd_mtf_p0_fields_runtime_v1.csv`
  - `kd_mtf_p0_runtime_params_template_v1.json`
  - `kd_mtf_p0_runtime_append_protocol_v1.md`
  - `kd_mtf_p0_runtime_append_acceptance_v1.md`
  - `kd_mtf_p0_runtime_append_stub_v1.py`
  - `kd_mtf_p0_runtime_notes_v1.md`
  - `kd_mtf_p0_runtime_gaps_v1.md`
  - `kd_mtf_p0_b_blocker_note_v1.md`
- 映射与样本：
  - `kd_mtf_p0_real_input_mapping_draft_v1.md`
  - `real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - `real_input_samples\kd_mtf_p0_proof_output_v1.csv`
  - `upstream_samples\n01_first_real_input_bars_v1.csv`

## 先看什么

1. `kd_mtf_p0_directory_index_card_v1.md`
2. `kd_mtf_p0_quick_entry_card_v1.md`
3. `kd_mtf_p0_object_responsibility_card_v1.md`
4. `kd_mtf_p0_real_input_mapping_draft_v1.md`

## 当前边界

- 本包当前仍是 `v1` 工作副本，不代表旧真源目录已经废弃。
- `kd_mtf_p0_fields_runtime_v1.csv` 当前仍是历史 `5` 行手工 persist 样本，不是最新真实 `7` 行 proof 的 runtime 结果。
- 最新真实 `7` 行 proof 目前只完成 dry-run，尚未在本包内重新执行 `--persist`。

## 历史命令样例（仅供追溯）

```bash
python d:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\DY_R1_KD_MTF_P0\kd_mtf_p0_runtime_append_stub_v1.py
python d:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\DY_R1_KD_MTF_P0\kd_mtf_p0_runtime_append_stub_v1.py --persist
```
