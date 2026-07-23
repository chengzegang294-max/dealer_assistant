# Batch 148 CHZL_BSD Sample Intake Absorb

更新时间：2026-07-15

## 批次目标

- 为 `CHZL_BSD` 补齐“第二只带 seed 的结构样本”，用于判断能否继续降低人工 seed 依赖。
- 当前阶段只做资料整理，不扩成自动化执行逻辑。

## 已知仓内入口

- 运行侧样本 stub：
  - `02_runtime/butler_r0_ohlcv_object_cards/run_chzl_bsd_sample_stub_v1.py`
- 运行侧结构序列构建：
  - `02_runtime/butler_r0_ohlcv_object_cards/build_chzl_structure_series_v1.py`
- 现有样本包：
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/chzl_bsd_structure_bundle/README.md`

## 当前产物

- `manifest_v1.tsv`
- `provenance.md`
- `CHZL_BSD_SAMPLE_REQUIREMENT_v1.tsv`
- `BATCH_148_EXECUTION_CARD.md`
- `BATCH_148_ARTIFACT_INDEX_v1.md`
- `00_raw_snapshot/CHZL_BSD_existing_second_sample_anchor__historical_recovered.md`
- `00_raw_snapshot/601991_SH_second_sample_input_binding_note__20260713.md`
- `00_raw_snapshot/601991_SH_second_sample_seed_scaffold__20260713.md`
- `00_raw_snapshot/601991_SH_structure_seed_v1.tsv`
- `00_raw_snapshot/601991_SH_second_sample_stub_validation_note__20260714.md`
- `00_raw_snapshot/601991_SH_second_sample_stronger_validation_record__20260715.md`

## 默认阅读顺序

- 1. 先看本 README
- 2. 再看 `CHZL_BSD_SAMPLE_REQUIREMENT_v1.tsv`
- 3. 再按该表落样本并补 provenance

## 当前边界

- 本批次只负责样本补采与追溯，不负责：
  - 自动化 seed 生成
  - 新增规则实现
  - 回测产物生成

## 当前进展

- 第二只样本 `601991.SH` 当前已具备：
  - `daily + weekly + auto_series + seed`
- 并已在 runtime 侧成功生成：
  - `chzl_bsd_601991_sh_semi_auto_output.json`
- 当前因此不再把本批次写成“仍缺第二只 seed”。
- 当前更准确口径是：
  - 第二只样本已完成 `semi_auto seed bound + stub validated`
  - 并已补出正式的更强校验记录页，固定 `acceptance flags` 与 `degraded` 边界
  - 但仍不是完整结构真值或自动结构引擎完成
