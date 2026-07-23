# 601991_SH 第二只样本更强校验记录

更新时间：2026-07-15

## 文件类型

- `INDEX_NOTE`

## 原路径

- `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/chzl_bsd_structure_bundle/601991_SH_structure_seed_v1.tsv`
- `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/chzl_bsd_structure_bundle/auto_series/601991_SH_structure_series_v1.tsv`
- `02_runtime/butler_r0_ohlcv_object_cards/acceptance_outputs/chzl_bsd_601991_sh_semi_auto_output.json`
- `batch_148/00_raw_snapshot/601991_SH_second_sample_input_binding_note__20260713.md`
- `batch_148/00_raw_snapshot/601991_SH_second_sample_stub_validation_note__20260714.md`

## 新路径

- `batch_148/00_raw_snapshot/601991_SH_second_sample_stronger_validation_record__20260715.md`

## 生成入口

- `manual_validation_rollup`

## 当前作用

- 把第二只样本 `601991.SH` 的 seed、runtime bundle、semi-auto output、acceptance flags 一次串成正式校验闭环。
- 让本批次不再残留“还缺第二只样本 seed 说明”的旧口径。

## 校验链闭环

- `seed 已落盘`
  - `batch_148/00_raw_snapshot/601991_SH_structure_seed_v1.tsv`
  - `02_runtime/.../chzl_bsd_structure_bundle/601991_SH_structure_seed_v1.tsv`
- `runtime bundle 已登记`
  - `CHZL_BSD__601991_SH__bundle_v1`
  - `status = semi_auto_series_ready`
- `semi-auto output 已生成`
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_outputs/chzl_bsd_601991_sh_semi_auto_output.json`
- `stub validation 已落盘`
  - `batch_148/00_raw_snapshot/601991_SH_second_sample_stub_validation_note__20260714.md`

## 当前硬事实

- 输入规模：
  - `daily = 1538`
  - `weekly = 326`
  - `structure_series_rows = 179`
  - `annotation_rows = 3`
- `evidence_mode`
  - `semi_auto_structure_with_seed_override`
- 关键输出：
  - `chzl_bsd_type = 1B`
  - `chzl_filter_action = APPROVE`
  - `chzl_risk_action = HALF_SIZE`
  - `chzl_size_scalar = 0.5`
- acceptance flags：
  - `passed_annotation_binding = true`
  - `passed_auto_structure_binding = true`
  - `degraded = true`
  - `degrade_reason = semi_auto_structure_series_with_manual_seed_override`

## 当前结论

- 第二只样本当前已正式达到：
  - `semi_auto seed bound + stub validated + acceptance flags fixed`
- 当前不再允许写成：
  - `仍缺第二只样本 seed 说明`
- 当前仍必须保留：
  - `degraded = true`
  - 这不是完整结构真值
  - 这不是完整自动结构引擎完成

## 对 batch_148 的当前意义

- 这条线当前真正缺的不是原始样本材料。
- 当前真正缺的是：
  - 更强校验记录已补后，只剩后续是否继续降低人工 seed 依赖的判断说明
  - 若再提升证据强度，需要新增更完整结构真值或更强机器验收，而不是重复补 seed
