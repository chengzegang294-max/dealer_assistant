# 601991_SH 第二只样本 seed 脚手架说明

更新时间：2026-07-14

## 文件类型

- `INDEX_NOTE`

## 原路径

- 参考物：
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/chzl_bsd_structure_bundle/300302_SZ_structure_seed_v1.tsv`
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/chzl_bsd_structure_bundle/bundle_index_v1.tsv`
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/sample_provenance_index_v1.tsv`

## 新路径

- `batch_148/00_raw_snapshot/601991_SH_second_sample_seed_scaffold__20260713.md`

## 生成入口

- `manual_seed_scaffold_note`

## 适用对象

- `CHZL_BSD`

## 当前作用

- 固定第二只样本 `601991.SH` 的 seed 字段合同与镜像来源。
- 说明为什么当前仍不能把第二只 seed 写成完整结构真值。
- 作为已落 `601991_SH_structure_seed_v1.tsv` 的镜像脚手架说明与回链页。

## 证据强度

- `weak_manual_seed`

## 当前已确认事实

- `300302_SZ_structure_seed_v1.tsv` 已存在，可作为第一只样本 seed 镜像参考。
- `601991_SH_structure_series_v1.tsv` 已存在，可作为第二只样本 auto series 参考。
- `bundle_index_v1.tsv` 已确认：
  - `CHZL_BSD__601991_SH__bundle_v1`
  - 已绑定：
    - `daily_sample`
    - `weekly_sample`
    - `auto_structure_series`
    - `annotation_seed`
- `sample_provenance_index_v1.tsv` 已登记：
  - `601991_SH_structure_seed_v1.tsv`
- `run_chzl_bsd_sample_stub_v1.py` 已输出：
  - `chzl_bsd_601991_sh_semi_auto_output.json`

## 第一只样本的可镜像字段

- `symbol`
- `timeframe`
- `bar_date`
- `fractal_type`
- `bi_direction`
- `zs_state`
- `zs_zg`
- `zs_zd`
- `divergence_flag`
- `bsd_type`
- `stop_logic`
- `note`

## 第二只样本当前脚手架口径

- 标的：
  - `601991.SH`
- 周期：
  - `1d`
- 角色：
  - `manual seed only`
- 当前目标：
  - 保持 `1-3` 行最小人工 seed
  - 只用于验证字段合同、stub 输入、索引回链和半自动输出
- 当前不扩成：
  - 完整 chanlun 真值
  - 自动结构引擎
  - 回测结论

## 推荐的最小 seed 填写方式

- 先从 `601991_SH_structure_series_v1.tsv` 里挑：
  - 一个更像底分型或 `1B/2B` 候选的位置
  - 最多再补 `1-2` 个连接点
- 然后仿照 `300302_SZ_structure_seed_v1.tsv` 只写最少几行：
  - `bottom candidate`
  - `top connector`
  - `2B candidate` 或等价结构点

## 当前不能直接判已完成的原因

- 目前还没有：
  - 完整 chanlun 结构真值
  - 自动结构引擎级别的稳定输出
- 因而当前可以写成：
  - `seed ready`
  - `semi_auto_stub_validated`
- 但仍不能写成：
  - `full_structure_truth_ready`

## 下一刀

- 若继续推进本批次，下一刀不再是新建 seed 文件，而是：
  - 补更强校验记录
  - 或继续增强结构真值说明
