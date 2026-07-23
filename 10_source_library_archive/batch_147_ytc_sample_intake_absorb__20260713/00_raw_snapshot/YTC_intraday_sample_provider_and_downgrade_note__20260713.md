# YTC 分钟级样本 provider 与降级口径说明

更新时间：2026-07-13

## 文件类型

- `INDEX_NOTE`

## 原路径

- 仓内既有：
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/ytc_daily_weekly_sample_plan_v1.tsv`
  - `02_runtime/butler_r0_ohlcv_object_cards/acceptance_samples/sample_provenance_index_v1.tsv`

## 新路径

- `batch_147/00_raw_snapshot/YTC_intraday_sample_provider_and_downgrade_note__20260713.md`

## 生成入口

- `manual_batch_absorb_note`

## 适用对象

- `YTC`

## 当前作用

- 固定 `60m/5m` 样本当前为什么仍缺。
- 固定分钟级样本补采前的 provider 与降级口径。
- 避免后续把 `daily+weekly` 锚点误写成分钟级样本已完成。

## 证据强度

- `weak_evidence`

## 当前已确认事实

- 仓内 `YTC` 样本计划当前只有：
  - `daily_weekly_ready`
  - `optional_intraday = 60m_pending__5m_pending`
- 已确认样本：
  - `300302.SZ`
  - `300750.SZ`
  - `601991.SH`
  - `301666.SZ`
- 本轮全仓搜索未发现：
  - 可直接吸收的 `A股 60m` 样本
  - 可直接吸收的 `A股 5m` 样本

## 当前 provider 口径

- 当前仓内已稳定的 provider 只覆盖：
  - `1d`
  - `1w`
- 对 `60m/5m`：
  - 当前只能记为 `provider_not_yet_fixed`
  - 不冒充仓内已存在

## 当前推荐的分钟样本最小合同

- `symbol`
  - 优先沿已有 `YTC` 样本池：
    - `601991.SH`
    - 或 `300302.SZ`
- `timeframe`
  - `60m`
  - `5m`
- `fields`
  - `trade_date`
  - `open`
  - `high`
  - `low`
  - `close`
  - `volume`
- `scope`
  - 只要能支持最小对象验证即可
  - 当前不要求全市场或长期全量

## 当前降级口径

- 在没有 `60m/5m` 真样本前：
  - `YTC` 仍只能写成：
    - `daily_weekly_only`
- 当前允许：
  - 继续保留 `daily+weekly` 锚点作为对象存在性证据
- 当前不允许：
  - 把 `daily+weekly` 输出伪装成分钟级证据
  - 把别的对象的分钟样本借来冒充 `YTC` 真样本

## 下一刀

- 若继续推进本批次，优先补：
  - `601991.SH` 的 `60m` 最小样本
  - `601991.SH` 的 `5m` 最小样本
- 若短期仍拿不到：
  - 至少再补一页 provider 决策说明
  - 但状态仍只能保持 `partial`
