# T02 真实宽表拼接说明 v1

更新时间：2026-07-12

## 用途

- 说明 `T02` 首份真实资金宽表应该由哪些源表拼出来。
- 固定 join key、字段来源和允许留空的边界，避免真实数据一到手又重新临时定口径。

## 最小主键

- 当前统一主键：
  - `trade_date`
  - `symbol`

## 字段来源建议

- 底表 `base_ohlcv`
  - 提供：
    - `trade_date`
    - `symbol`
    - `symbol_name`
    - `open`
    - `high`
    - `low`
    - `close`
    - `prev_close`
    - `volume`
    - `amount`
- 主力资金表 `moneyflow`
  - 提供：
    - `main_fund_net_inflow`
    - `main_fund_net_inflow_ratio`
- 北向表 `northbound`
  - 提供：
    - `northbound_net_inflow`
    - `northbound_holding_change`
- 市场阶段表 `regime`
  - 提供：
    - `market_regime_label`
- 行业映射表 `industry`
  - 提供：
    - `industry_code`
    - `industry_name`
- 元信息
  - 统一补：
    - `data_source`
    - `asof_date`
    - `notes`

## Join 规则

- `moneyflow`
  - 默认按 `trade_date + symbol` 左连接
- `northbound`
  - 默认按 `trade_date + symbol` 左连接
- `regime`
  - 优先按 `trade_date + symbol` 左连接
  - 若只有 `trade_date` 级别，先扩成可消费结构，再进入拼接脚本
- `industry`
  - 默认按 `symbol` 左连接

## 允许留空

- 当前可留空：
  - `northbound_net_inflow`
  - `northbound_holding_change`
  - `market_regime_label`
  - `industry_code`
  - `industry_name`
- 当前不应留空：
  - `trade_date`
  - `symbol`
  - `main_fund_net_inflow`
  - `main_fund_net_inflow_ratio`

## 当前运行入口

- 拼接脚本：
  - `02_runtime/ashare_p0_first_round_validation/build_t02_real_input_v1.py`
- 源表 manifest：
  - `02_runtime/ashare_p0_first_round_validation/data/t02_real_input_sources_manifest_v1.tsv`
- 当前模板输入：
  - `02_runtime/ashare_p0_first_round_validation/artifacts/t02_input_prepare/t02_fund_flow_input_normalized_latest.csv`

## 当前回链

- `00_entry/A股_P0_首轮数据字段清单__20260712.md`
- `00_entry/A股_P0_离线验证执行卡__20260712.md`
- `02_runtime/ashare_p0_first_round_validation/runtime_execution_card_v1.md`
