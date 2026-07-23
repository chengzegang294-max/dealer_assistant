# 601991_SH 第二只样本输入绑定说明

更新时间：2026-07-14

## 文件类型

- `INDEX_NOTE`

## 原路径

- `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/watchlist_subset/601991_SH_1d.csv`
- `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/weekly_subset/601991_SH_1w.csv`
- `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/chzl_bsd_structure_bundle/auto_series/601991_SH_structure_series_v1.tsv`
- `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/chzl_bsd_structure_bundle/bundle_index_v1.tsv`
- `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/chzl_bsd_structure_bundle/601991_SH_structure_seed_v1.tsv`
- `02_runtime/butler_r0_ohlcv_object_cards/acceptance_outputs/chzl_bsd_601991_sh_semi_auto_output.json`

## 新路径

- `batch_148/00_raw_snapshot/601991_SH_second_sample_input_binding_note__20260713.md`

## 生成入口

- `manual_batch_absorb_note`

## 适用对象

- `CHZL_BSD`

## 当前作用

- 把第二只样本的 `daily / weekly / auto series` 正式绑定进本批次。
- 说明当前第二只样本为什么已经具备输入基座，并已进入 runtime seed/stub 校验链。

## 证据强度

- `historical_recovered`

## 当前已绑定输入

- `daily_sample`
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/watchlist_subset/601991_SH_1d.csv`
- `weekly_sample`
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/weekly_subset/601991_SH_1w.csv`
- `auto_structure_series`
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/chzl_bsd_structure_bundle/auto_series/601991_SH_structure_series_v1.tsv`
- `annotation_seed`
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/chzl_bsd_structure_bundle/601991_SH_structure_seed_v1.tsv`

## bundle 绑定事实

- `bundle_index_v1.tsv` 已记录：
  - `CHZL_BSD__601991_SH__bundle_v1`
- 当前 bundle 状态：
  - `semi_auto_series_ready`
- 当前已补齐：
  - `annotation_seed`
- 当前已形成：
  - `semi_auto_structure_with_seed_override` 的最小 stub 输出

## 当前结论

- 第二只样本输入基座已经存在：
  - `1d` 日线
  - `1w` 周线
  - `auto series`
- 第二只样本运行侧最小绑定也已存在：
  - `annotation_seed`
  - `semi_auto_output`
- 因而当前不再把：
  - `CHZL_S001`
  写成完全 `missing`
- 但当前仍不能写成：
  - `second sample fully ready`
- 原因是：
  - 当前只完成半自动 stub 级验证，仍不是完整结构真值

## 下一刀

- 继续补：
  - 更强校验记录或后续结构真值增强
- 当前最小目标：
  - 保持 `seed + auto_series + stub_output` 三件套回链稳定
