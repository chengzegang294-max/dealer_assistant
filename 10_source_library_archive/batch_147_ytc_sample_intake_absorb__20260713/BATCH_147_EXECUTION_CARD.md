# Batch 147 Execution Card

更新时间：2026-07-14

## 批次对象

- `YTC`

## 当前目标

- 把 `60m/5m` 样本补采需求与仓内现有 `1d/1w` 降级样本、最小运行输出回链起来。

## 当前入口

- 本批次入口：`README.md`
- 样本需求：`YTC_SAMPLE_REQUIREMENT_v1.tsv`
- 产物索引：`BATCH_147_ARTIFACT_INDEX_v1.md`

## 执行步骤

- 1. 先登记仓内已存在的 `1d/1w` 样本与 YTC 最小运行输出。
- 2. 再看仓内搜索状态与 provider 候选矩阵，确认当前阻塞点不是“没搜过”。
- 3. 按最小补采路径把 `60m/5m` 小样本补到本批次 `00_raw_snapshot/`。
- 4. 按接收合同与 provenance 模板补说明。
- 5. 若拿不到 `5m`，在 provenance 与索引里明确降级口径。
- 6. 若使用外部历史分钟包吸收，也必须把包路径、包内条目与本地聚合关系写入 provenance。

## 当前状态

- 当前已完成：
  - 批次入口
  - provenance
  - manifest
  - 样本需求清单
  - 仓内搜索状态
  - provider 候选矩阵
  - 最小补采路径
  - 接收合同与 provenance 模板
  - `601991_SH_5m.csv`
  - `601991_SH_60m.csv`
  - 两份样本 provenance 实填页
- 当前未完成：
  - 外部卖家元信息补录（若后续能确认）

## 当前边界

- 当前不做：
  - 新增指标实现
  - 扩展执行链
  - 回测产物生成
