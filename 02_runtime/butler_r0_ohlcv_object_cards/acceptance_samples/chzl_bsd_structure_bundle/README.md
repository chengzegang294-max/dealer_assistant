# CHZL_BSD Structure Bundle

## 用途

- 为 `CHZL_BSD_P0_E` 准备最小结构样本包。
- 当前阶段只落：
  - 来源样本绑定
  - 结构标注模板
  - bundle 索引
- 当前**不伪造**分型、笔、中枢、背驰标签；真实标注后再进入 runner。

## 组成

- `bundle_index_v1.tsv`
  - 记录每个结构样本包绑定哪份 `1d` 样本、哪份 `1w` 样本、使用哪个模板
- `structure_annotation_template_v1.tsv`
  - 统一结构标注字段模板
- `300302_SZ_structure_seed_v1.tsv`
  - 基于真实日线窗口做的最小人工 seed 标注，只作为 stub 验证输入，不冒充完整真值

## 当前口径

- `daily_sample` 是主样本基座。
- `weekly_sample` 是辅助的大周期结构上下文。
- `annotation_template` 目前只有模板，没有伪造结构标签。
- `annotation_seed` 若存在，只代表最小人工 seed，用于验证字段合同、索引回链和 stub 输出格式。
- 若 `chanlun_strokes_zs / chanlun_divergence` 仍缺失，则 `CHZL_BSD` 不得冒充为可跑完成态，只能保留为 `sample_bundle_ready`。

## 后续动作

- 先选 1-2 只代表性标的，人工或 AI 辅助标注少量结构片段。
- 标注完成后，再决定是否补 `run_chzl_bsd_on_sample.py` 或并入统一 runner。
