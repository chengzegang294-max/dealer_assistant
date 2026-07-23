# YTC 分钟样本最小补采路径

更新时间：2026-07-13

## 作用

- 把 `YTC 60m/5m` 真样本补采压成最小路径。
- 让后续补样本的人不需要再重新判断格式、命名和入档位置。

## 当前目标

- 至少补一只 A 股样本：
  - `601991.SH`
- 两个周期：
  - `60m`
  - `5m`

## 最小补采合同

- 文件命名建议：
  - `601991_SH_60m.csv`
  - `601991_SH_5m.csv`
- 推荐落点：
  - `10_source_library_archive/batch_147_ytc_sample_intake_absorb__20260713/00_raw_snapshot/`
- 最小字段：
  - `trade_date`
  - `open`
  - `high`
  - `low`
  - `close`
  - `volume`

## 最小备注合同

- 必须补一页来源说明，至少写清：
  - `source_path` 或 provider
  - `producer`
  - `timeframe`
  - `symbol`
  - `evidence_mode`
  - `status`
- 若来自 API 拉取：
  - 写清脚本名
- 若来自人工导出：
  - 写清导出来源与日期

## 当前推荐顺序

- 1. 先补 `601991_SH_60m.csv`
- 2. 再补 `601991_SH_5m.csv`
- 3. 再补对应 provenance note
- 4. 最后把 `YTC_SAMPLE_REQUIREMENT_v1.tsv` 改成 `active`

## 为什么先补 `60m`

- `60m` 更接近日线/周线框架的第一层下钻。
- 它比 `5m` 更像 `YTC` 当前降级链条的自然下一步。
- 先补 `60m` 能更快结束“完全没有分钟级样本”的状态。

## 当前最小可交付定义

- 若本批次只拿到：
  - `601991_SH_60m.csv`
- 当前也可以先把：
  - `YTC_S001`
  提升为：
    - `active`
- 但：
  - `YTC_S002`
  仍保持：
    - `partial`

## 当前不允许的偷换

- 不把 `1d/1w` 聚合结果改名冒充 `60m/5m`
- 不把 FX `m5` 样本镜像成 A 股样本
- 不把无来源的手工文件当正式分钟样本

## 下一刀

- 一旦分钟样本实物到位，马上同步更新：
  - `BATCH_147_ARTIFACT_INDEX_v1.md`
  - `YTC_SAMPLE_REQUIREMENT_v1.tsv`
  - `provenance.md`
  - `archive_batch_index_v1.tsv`
  - repo-global 总台账
