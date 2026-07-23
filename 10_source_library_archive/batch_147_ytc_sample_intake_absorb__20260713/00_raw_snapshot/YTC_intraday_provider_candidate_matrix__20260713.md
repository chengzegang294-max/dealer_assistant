# YTC 分钟样本 provider 候选矩阵

更新时间：2026-07-13

## 作用

- 这页只负责回答：
  - `YTC 60m/5m` 真样本后续应该优先从哪里补。
- 当前不是执行页，而是 provider 候选裁决页。

## 当前已确认 runtime 侧 provider 现状

- 已有稳定日线入口：
  - `BaoStock daily fetch`
  - `BaoStock daily probe`
  - `AkShare daily probe`
  - `Tushare daily probe`
- 当前未见 A 股分钟级正式入口：
  - `60m`
  - `5m`

## 候选矩阵

| 候选 provider | 当前仓内状态 | 是否已有脚本 | 是否适合直接补 `YTC` | 当前裁决 | 备注 |
|---|---|---|---|---|---|
| `BaoStock` | `daily_ready` | `yes`，但仅日线 | `no` | `not_first_choice` | 当前仓内只证明了日线 fetch/probe |
| `AkShare` | `daily_probe_ready` | `yes`，但仅日线 | `partial` | `candidate` | 若后续补分钟级，最像可扩成新 probe |
| `Tushare` | `daily_probe_ready` | `yes`，但仅日线 | `partial` | `candidate` | 若 token/接口允许，可作为分钟级正式候选 |
| `legacy FX minute scripts` | `archive_only` | `yes` | `no` | `reference_only` | 只能借鉴字段与聚合路径，不可冒充 A 股样本 |
| `unknown external manual file` | `not_ingested` | `no` | `partial` | `last_resort` | 只能作为临时补位，仍需 provenance |

## 当前主裁决

- 如果后续要给 `YTC` 补 A 股 `60m/5m`：
  - 第一顺位先看：
    - `Tushare`
    - `AkShare`
- 不优先选：
  - `BaoStock`
- 原因：
  - 当前仓内只确认了它的日线入口
  - 没有分钟级成功记录

## 为什么不直接拿 legacy 分钟脚本顶上

- 当前 legacy 里的分钟脚本属于：
  - `FX`
  - `subhour`
  - `proof-of-mapping`
- 它们可以提供：
  - 文件命名参考
  - `m5` 聚合思路
  - real-input proof 组织方式
- 但当前不能直接提供：
  - `A股 60m/5m OHLCV` 真样本

## 当前最小 provider 裁决

- `60m`
  - 推荐先补：
    - `Tushare` 或 `AkShare`
- `5m`
  - 推荐先补：
    - `Tushare` 或 `AkShare`
- 若都不可用：
  - 允许短期用：
    - `unknown external manual file`
  - 但必须补：
    - provenance
    - source note
    - evidence mode

## 当前不允许的写法

- 不把 `daily probe` 写成 `intraday provider ready`
- 不把 `legacy FX minute file` 写成 `A股分钟样本`
- 不把外部临时手工文件写成默认真源

## 下一刀

- 继续补：
  - `YTC` 最小分钟样本补采路径
