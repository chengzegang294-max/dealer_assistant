# Batch 140 Tushare TDX Data Source Absorb

更新时间：2026-07-12

## 批次目标

- 把用户临时放在 `暂时存放/` 的两篇 A 股量化数据源教程纳入仓库可追溯链路。
- 同时完成三层收口：
  - `00_raw_snapshot/`：保留原始导出稿快照
  - `02_absorb_index/tushare_tdx_tutorial_core_digest_v1.md`：提炼教程核心
  - `02_absorb_index/ashare_p0_data_source_decision_v1.md`：给出当前项目的充值与使用裁决

## 收口裁决

- 当前两篇教程都不是仓库默认真值合同，只作为：
  - 外部公开资料
  - 当前 A 股 P0 数据源决策的参考证据
- 当前主负责人裁决：
  - 对本项目 A 股 P0，`Tushare` 不适合做“大而全预付费”
  - 但若目标是尽快打通当前 `T02 moneyflow`，则值得补最小 `2000` 积分层级
  - `通达信 + AKShare/雪球` 适合作为分层替代，不适合当前就宣称“完全等价替代 Tushare`

## 批次结构

- `00_raw_snapshot/`
  - 从 `暂时存放/` 复制进来的原始导出稿快照
- `02_absorb_index/`
  - 教程内化摘要
  - 当前项目数据源裁决

## 当前入口

- `manifest_v1.tsv`
- `provenance.md`
- `02_absorb_index/tushare_tdx_tutorial_core_digest_v1.md`
- `02_absorb_index/ashare_p0_data_source_decision_v1.md`
