# Crypto Exchange Data Onramp Plan V1

## 用途

- 记录“如果后续把当前 `XBreaking / 旧仓标准化` 主线扩展到币圈数据，应该怎么接”的最小可实施方案。
- 当前角色是 `INDEX_NOTE`，用于先固定入口、边界、字段契约与优先级，不直接改变现有 `MT5 / XBreaking` 默认执行链路。
- 当前优先使用用户已具备账户的 `Binance` 与 `OKX` 作为候选交易所入口；后续若要真实落地，再决定先接一家还是两家并跑首批样本。

## 当前裁决

- 当前主线仍是 `MT5 / XBreaking / 旧仓已购数据迁移`，币圈接入暂不抢占默认执行链路。
- 当前先记录一套“好实现就直接接，不好实现也能落档”的方案，避免未来重开题时再次从零讨论。
- 当前不建议把币圈数据先硬塞进 `MT5 broker symbol` 口径；优先走交易所原生数据，再做新仓标准化契约。

## 为什么需要单独渠道

- `MT5 / CFD` 口径通常不是交易所原生数据，`symbol` 命名、成交量含义与历史稳定性都容易漂移。
- 币圈常见增强字段如 `funding_rate / open_interest / trade_count / taker volume`，在 `MT5` 口径里往往不全。
- 币圈是 `24/7` 连续交易，时间对齐、周末处理和缺口判断都不同于当前外汇/股指/黄金链路。

## 推荐接法

### 第一优先

- `Binance`
  - 优点：资料最多、样本最常见、社区生态成熟，适合作为首条最小实现链路。
  - 适用：`spot klines`、`perpetual futures klines`、后续的 `funding rate / open interest`。
- `OKX`
  - 优点：可作为第二条交易所对照链，帮助验证“交易所差异”而不是只验证单一源。
  - 适用：首批做 `spot / swap` 的对照样本，不急着全量覆盖。

### 渠道可靠性建议

- 历史 `OHLCV` 优先走交易所官方 `REST API`。
- 增量实时数据若以后需要，再补 `WebSocket`。
- 首阶段不依赖私有账户权限就能做：
  - `public market data`
  - `klines/candles`
  - `funding/open interest` 的公开接口
- 私有 `API Key` 只在后续确实要接账户维度数据、或需要更高额度时再接入。

## 分阶段落地

### P0 记录阶段

- 当前已完成本方案文档落盘。
- 当前目标是把数据源、字段契约、目录结构和首批样本一次写清楚。

### P1 最小数据层

- 只做 `OHLCV` 标准化，不碰账户、下单、仓位、链上数据。
- 首批交易所：
  - `Binance`
  - `OKX`
- 首批市场：
  - `spot`
  - `perpetual/swap`
- 首批标的：
  - `BTCUSDT`
  - `ETHUSDT`
  - 可选补一条 `SOLUSDT`
- 首批周期：
  - `1h`
  - `4h`
- 首批目标：
  - 在 repo 内形成 `raw -> normalized -> manifest -> docs` 的闭环
  - 先让币圈数据接入方式和当前 `legacy csv` 标准化主线长得一致

### P2 增强字段

- 在 `P1` 跑稳后，再补：
  - `funding_rate`
  - `open_interest`
  - `trade_count`
  - `taker_buy_base_volume / taker_buy_quote_volume`
- 这一步才开始真正体现“币圈不是只多一份 K 线”的差异。

### P3 交易所对照与研究扩展

- 做 `Binance <-> OKX` 的同 symbol / timeframe 对照。
- 若后续策略需要，再考虑：
  - `liquidation`
  - `order book`
  - `on-chain`

## 字段契约建议

### P1 最小契约

- `bar_time_utc`
- `exchange`
- `market_type`
- `symbol`
- `base_asset`
- `quote_asset`
- `open`
- `high`
- `low`
- `close`
- `volume_base`
- `volume_quote`
- `trade_count`
- `source_path`
- `source_row_number`
- `contract_version`

### P2 扩展契约

- `funding_rate`
- `open_interest`
- `taker_buy_base_volume`
- `taker_buy_quote_volume`

## 目录建议

- 原始抓取：
  - `02_runtime\exchange_market_data\raw\binance\...`
  - `02_runtime\exchange_market_data\raw\okx\...`
- 标准化输出：
  - `02_runtime\exchange_market_data\normalized\crypto_contract_v1\...`
- 运行摘要：
  - `02_runtime\exchange_market_data\artifacts\crypto_contract_preview\<archive_tag>\run_summary.json`
  - `02_runtime\exchange_market_data\artifacts\crypto_contract_preview\<archive_tag>\ingest_manifest.json`

## 与当前主线怎么接

- 接入方式优先模仿 `normalize_purchased_csv_contract_v1.py` 的闭环，而不是模仿 `MT5 tester`。
- 目标不是立刻让 `XBreaking` 直接跑币圈，而是先把“数据标准化入口”做好。
- 当 `P1` 标准化层稳定后，再决定：
  - 是否做新的消费者脚本
  - 是否需要为币圈单独做 `validation matrix`
  - 是否需要单独 acceptance 项

## 实现优先级

- 最顺手实现：
  - `Binance public klines -> standardized contract`
- 第二顺手实现：
  - `OKX public candles -> standardized contract`
- 先不做：
  - 账户私有接口
  - 实盘交易
  - 全量链上数据
  - 订单簿全深度历史

## 可靠性建议

- 首批只用官方接口，不先引第三方聚合商。
- 所有时间统一转成 `UTC`。
- 每条标准化样本都写 `exchange + market_type + source_path + contract_version`。
- 所有首批归档都要沿用当前主线收口规则：
  - `run_summary`
  - `ingest_manifest`
  - `README / EXECUTION_CARD` 同步

## 当前结论

- 用户已具备 `Binance` 与 `OKX` 账户，因此未来如果要做币圈数据扩展，优先走这两条链路即可，不需要先找新的交易账户。
- 真正需要额外补的是“交易所原生数据入口”，不是先补另一套 `MT5 broker`。
- 当前最推荐的实现起点是：
  - `Binance`
  - `spot + perpetual`
  - `BTCUSDT / ETHUSDT`
  - `1h / 4h`
  - `public REST -> standardized contract`
