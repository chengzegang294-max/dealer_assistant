# YTC 分钟样本接收合同

更新时间：2026-07-13

## 作用

- 固定 `YTC 60m/5m` 样本进入 `batch_147` 前至少要满足什么。
- 防止后续拿到一个分钟文件就直接吸收，结果字段、时间范围、来源说明都不完整。

## 最小接收条件

### 1. 文件本体

- 至少满足其一：
  - `601991_SH_60m.csv`
  - `601991_SH_5m.csv`
- 若不是 `601991.SH`：
  - 必须先在 note 里说明为什么换 symbol

### 2. 最小字段

- 必须至少有：
  - `trade_date`
  - `open`
  - `high`
  - `low`
  - `close`
  - `volume`

### 3. 时间范围

- 不要求长窗口全量。
- 但至少要能支持：
  - 一轮最小对象验证
  - 一页 provenance note

### 4. 来源说明

- 必须同时写清：
  - `source_path` 或 provider
  - `producer`
  - `symbol`
  - `timeframe`
  - `evidence_mode`
  - `status`

## 当前接收后必须同步的文件

- `BATCH_147_ARTIFACT_INDEX_v1.md`
- `YTC_SAMPLE_REQUIREMENT_v1.tsv`
- `provenance.md`
- `00_raw_snapshot/README.md`
- 若状态发生变化，再同步：
  - `archive_batch_index_v1.tsv`
  - `全库资料整理总台账__20260713.md`

## 当前通过标准

- `60m`
  - 一旦有真实文件本体 + provenance note
  - 就可以把：
    - `YTC_S001`
    - 从 `partial`
    - 提到 `active`
- `5m`
  - 一旦有真实文件本体 + provenance note
  - 就可以把：
    - `YTC_S002`
    - 从 `partial`
    - 提到 `active`

## 当前不通过标准

- 只有截图，没有 csv
- 只有口头来源，没有 provenance
- 只有 `1d/1w` 文件改名
- 只有 legacy FX `m5` 文件镜像

## 当前结论

- `batch_147` 现在缺的已经不是“接收规则”。
- 后续只要样本文件满足本合同，就能直接纳入。
