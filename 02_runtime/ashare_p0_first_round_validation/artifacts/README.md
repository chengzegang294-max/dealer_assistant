# AShare P0 First Round Validation Artifacts

更新时间：2026-07-12

## 用途

- 这里放 A 股 P0 首轮离线验证的统计表、日志、导出表和后续批次归档说明。
- 当前只建立边界说明，不预创建大体量空目录树。

## 计划承接的产物

- `csv`
  - 统计摘要
  - 抽样明细
- `tsv`
  - 汇总对照表
- `log`
  - 运行日志
- `json`
  - 若后续需要结构化摘要，可在本层承接

## 当前规则

- 新跑出的结果优先按批次放在本层。
- 大体量或历史回收结果，必要时同步归档到：
  - `12_tooling_runtime_archive/<validation_batch>/`
- 每批产物至少要写清：
  - `producer`
  - `scope`
  - `status`
  - `evidence_mode`

## 当前回链

- runtime 执行卡：
  - `02_runtime/ashare_p0_first_round_validation/runtime_execution_card_v1.md`
- repo 级产出落点说明：
  - `00_entry/A股_P0_离线验证产出落点说明__20260712.md`
