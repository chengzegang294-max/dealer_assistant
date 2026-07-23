# Batch 148 Execution Card

更新时间：2026-07-15

## 批次对象

- `CHZL_BSD`

## 当前目标

- 把“第二只带 seed 的结构样本”补采需求与仓内现有 auto series、第一只 seed 样本、半自动输出回链起来。

## 当前入口

- 本批次入口：`README.md`
- 样本需求：`CHZL_BSD_SAMPLE_REQUIREMENT_v1.tsv`
- 产物索引：`BATCH_148_ARTIFACT_INDEX_v1.md`

## 执行步骤

- 1. 先登记仓内已存在的 `601991_SH` auto series 与半自动结构线索。
- 2. 再补第二只样本的 seed 说明到本批次 `00_raw_snapshot/`。
- 3. 再把 seed、runtime bundle、semi-auto output 与 acceptance flags 串成更强校验记录。
- 4. 若后续产生新的半自动输出，再回写 artifact 索引。

## 当前状态

- 当前已完成：
  - 批次入口
  - provenance
  - manifest
  - 样本需求清单
  - 第二只样本的 seed 说明
  - 对应输入数据的正式归档
  - 更强校验记录页
- 当前未完成：
  - 更完整结构真值或更强机器验收
  - 后续是否继续降低人工 seed 依赖的判断说明

## 当前边界

- 当前不做：
  - 自动化 seed 生成
  - 新增规则实现
  - 回测产物生成
