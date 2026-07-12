# 原子方法对象孵化主题入口 v1

## 适用问题

- 想直接进入 `多周期KD / RSJ / 高频价量相关性 / 四轴状态 / VanTharp R` 这组原子方法对象束
- 想区分 `batch_101` 的边界批职责，和 `batch_102 ~ batch_106` 的对象束职责
- 想先看对象合同、proof、字段样例，而不是直接回 raw snapshot 根目录

## first-hop 入口

- `../batch_101_non_kimi_atomic_rules_boundary__20260707/README.md`

## 对象快入口

- `object_entry/kd_mtf_object_entry_v1.md`
- `object_entry/rsj_state_object_entry_v1.md`
- `object_entry/pv_corr_object_entry_v1.md`
- `object_entry/four_axis_state_object_entry_v1.md`
- `object_entry/vantharp_r_object_entry_v1.md`

## 最顺阅读顺序

- 第一步：
  - 先看 `../batch_101_non_kimi_atomic_rules_boundary__20260707/README.md`
  - 若想知道这组对象为什么从原子规则边界批中独立出来，再看 `../_raw_snapshot_batch09/10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/INDEX_phase1_v1.md`
- 第二步：
  - 按对象进入 `batch_102 ~ batch_106` 对应对象卡
- 第三步：
  - 在对应批次中继续下钻 `bundle/objects`、`bundle/contracts`、`bundle/proof`、`bundle/samples`

## 当前边界

- 当前主题入口主要服务：
  - 原子方法对象的 first-hop 导航
  - proof-ready / contract-frozen 小束的集中索引
  - 后续对象化与运行时接线前的来源层整理
- 当前不承担：
  - runtime 默认执行入口
  - 交易 gate 或仓位引擎的正式裁决

## 当前结论速记

- `batch_102 ~ batch_106` 已经不是纯边界批附件，而是可直接进入的对象束
- 当前统一口径仍是：
  - `diag-only`
  - `proof-ready`
  - `contract-frozen`

## 回链

- 来源库根入口：
  - `../README.md`
- 主题索引：
  - `topic_entry_index_v1.tsv`
