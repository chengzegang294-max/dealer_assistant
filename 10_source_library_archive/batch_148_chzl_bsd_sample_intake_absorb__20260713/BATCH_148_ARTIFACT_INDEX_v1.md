# Batch 148 Artifact Index v1

更新时间：2026-07-15

## 当前批次产物

| 文件类型 | 原路径 | 新路径 | 生成入口 | 适用对象 | 当前作用 | 证据强度 | 状态 | 缺口 |
|---|---|---|---|---|---|---|---|---|
| `INDEX_NOTE` | `batch_148/README.md` | `batch_148/README.md` | `manual_batch_setup` | `CHZL_BSD` | 批次入口 | `hard` | `active` | 无 |
| `INDEX_NOTE` | `batch_148/provenance.md` | `batch_148/provenance.md` | `manual_batch_setup` | `CHZL_BSD` | 来源追溯说明 | `hard` | `active` | 无 |
| `ARTIFACT` | `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/chzl_bsd_structure_bundle/auto_series/601991_SH_structure_series_v1.tsv` | `historical_recovered_reference_only` | `build_chzl_structure_series_v1.py` | `CHZL_BSD` | 第二只样本现有 auto series 参考 | `hard_derived_from_runtime` | `referenced` | 已进入第二只样本 runtime bundle |
| `ARTIFACT` | `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/watchlist_subset/601991_SH_1d.csv` | `historical_recovered_reference_only` | `historical_runtime_sample` | `CHZL_BSD` | 第二只样本现有输入数据参考 | `historical_recovered` | `referenced` | 已与 daily/weekly/auto series/seed/stub 输出完成绑定说明 |
| `ARTIFACT` | `02_runtime/butler_r0_ohlcv_object_cards/acceptance_outputs/chzl_bsd_300302_sz_semi_auto_output.json` | `historical_recovered_reference_only` | `run_chzl_bsd_sample_stub_v1.py` | `CHZL_BSD` | 第一只样本半自动输出参考 | `semi_auto_structure_with_seed_override` | `referenced` | 不是第二只样本输出 |
| `ARTIFACT` | `batch_148/00_raw_snapshot/CHZL_BSD_existing_second_sample_anchor__historical_recovered.md` | `batch_148/00_raw_snapshot/CHZL_BSD_existing_second_sample_anchor__historical_recovered.md` | `historical_recovered_runtime_reference` | `CHZL_BSD` | 批次内第二只样本锚点说明 | `historical_recovered` | `active` | 已补 seed 与 stub 校验，仍非完整结构真值 |
| `INDEX_NOTE` | `watchlist_subset/601991_SH_1d.csv + weekly_subset/601991_SH_1w.csv + auto_series/601991_SH_structure_series_v1.tsv + bundle_index_v1.tsv + 601991_SH_structure_seed_v1.tsv + chzl_bsd_601991_sh_semi_auto_output.json` | `batch_148/00_raw_snapshot/601991_SH_second_sample_input_binding_note__20260713.md` | `manual_batch_absorb_note` | `CHZL_BSD` | 第二只样本输入绑定说明 | `historical_recovered` | `active` | 已固化 daily/weekly/auto series/seed/stub 输出绑定 |
| `INDEX_NOTE` | `300302_SZ_structure_seed_v1.tsv + bundle_index_v1.tsv + sample_provenance_index_v1.tsv` | `batch_148/00_raw_snapshot/601991_SH_second_sample_seed_scaffold__20260713.md` | `manual_seed_scaffold_note` | `CHZL_BSD` | 第二只样本 seed 镜像脚手架说明 | `weak_manual_seed` | `active` | 已固定字段合同与落点镜像 |
| `ARTIFACT` | `manual_seed_from_601991_auto_series -> promoted_to_runtime_bundle` | `batch_148/00_raw_snapshot/601991_SH_structure_seed_v1.tsv` | `manual_sample_intake` | `CHZL_BSD` | 第二只样本最小 seed 行 | `weak_manual_seed` | `active` | 已补 `1-3` 行真实弱证据 seed，并已吸收到 runtime bundle |
| `INDEX_NOTE` | `acceptance_outputs/chzl_bsd_601991_sh_semi_auto_output.json` | `batch_148/00_raw_snapshot/601991_SH_second_sample_stub_validation_note__20260714.md` | `run_chzl_bsd_sample_stub_v1.py` | `CHZL_BSD` | 第二只样本半自动 stub 校验记录 | `semi_auto_structure_with_seed_override` | `active` | 已证明第二只样本可输出最小 JSON，但仍非完整结构真值 |
| `INDEX_NOTE` | `seed + runtime bundle + semi_auto_output + acceptance_flags` | `batch_148/00_raw_snapshot/601991_SH_second_sample_stronger_validation_record__20260715.md` | `manual_validation_rollup` | `CHZL_BSD` | 第二只样本更强校验记录，固定 `acceptance flags` 与 `degraded` 边界 | `stronger_validation_record` | `active` | 已明确不是缺 seed，而是仍缺完整结构真值或更强机器验收 |

## 当前说明

- 仓内已存在第二只样本的 auto series，且对应 seed 说明已正式落盘。
- 当前批次已补第二只样本输入绑定说明、seed 镜像脚手架、最小 seed 行、stub 校验记录与更强校验记录页。
- 当前运行侧也已补齐第二只样本 seed 落点、bundle 索引、provenance 索引与半自动输出。
- 当前仍不把这些最小 seed 行或 stub 输出写成完整真值或自动结构引擎完成。
