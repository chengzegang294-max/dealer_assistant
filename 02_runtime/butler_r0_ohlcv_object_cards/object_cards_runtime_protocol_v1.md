# Object Cards Runtime Protocol v1

## 输入

- 单标的 OHLCV CSV
- 至少包含字段：`date, open, high, low, close, volume`
- 默认编码：UTF-8

## 运行方式（最小目标）

- 单文件 Runner 接受：
  - `--object-card`：`VOLFAC_P0_A / BPB_P0_E / VP_P0_E / TKR7_P0_E`
  - `--input-csv`
  - `--output-json`

## 输出

- JSON 必须包含：
  - `object_id`
  - `input_rows`
  - `as_of_date`
  - `signal_payload`
  - `acceptance_flags`

## 最小验收

- `input_rows` 与样本约束一致
- `signal_payload` 至少包含该对象卡字段合同中的必填字段
- 缺数据时必须显式输出 `degrade_reason`，不允许 silent failure

