# n02_p0_real_input_mapping_draft v1

## 目的

- 给 `REOPEN_B9_N02_SESSION_OR_P0` 第一份真实 runtime 数据接入前提供最小输入映射草案。
- 只解决“真实输入从哪里来、如何映射到当前 v1 字段”，不扩到 `IB / acceptance / failed breakout`。

## 当前目标输出

- `session_id`
- `session_timezone`
- `opening_range_window_minutes`
- `opening_range_high`
- `opening_range_low`
- `opening_range_mid`
- `opening_range_width`
- `opening_range_width_pct_open`
- `session_open_price`
- `opening_range_defined`
- `first_break_direction`
- `width_error_day`

## 最小真实输入

### 行情主输入

- `symbol`
- `timeframe`
- `bar_time`
- `open`
- `high`
- `low`
- `close`

### 配置主输入

- `session_binding_registry`
  - `session_id`
  - `session_timezone`
  - `calendar_basis`
  - `dst_handling`
- `opening_range_window_minutes = 30`

## 输入到输出映射

### 1. 直接透传

- `symbol <- symbol`
- `timeframe <- timeframe`
- `bar_time <- bar_time`

### 2. session 映射

- `session_id`
  - 不是从 bar 本身直接读取
  - 而是根据：
    - 品种/运行模板
    - 本地日期解释
    - `session_binding_registry`
    进行归属
- `session_timezone`
  - 由 `session_id` 命中 registry 后派生
  - 不允许手写与 registry 不一致的值

### 3. OR 窗口定义

- `opening_range_window_minutes`
  - 当前固定读取参数模板中的 `30`
- OR 窗口起点
  - 必须从 session 本地开盘时刻推导
  - 不能直接写死 UTC 偏移

### 4. OR 字段派生

- `session_open_price`
  - 当前 session 第一根有效 bar 的 `open`
- `opening_range_high`
  - OR 窗口内所有 bar 的最高 `high`
- `opening_range_low`
  - OR 窗口内所有 bar 的最低 `low`
- `opening_range_mid`
  - `(opening_range_high + opening_range_low) / 2`
- `opening_range_width`
  - `opening_range_high - opening_range_low`
- `opening_range_width_pct_open`
  - `opening_range_width / session_open_price`
  - 若 `session_open_price <= 0`，则保留 `na`
- `opening_range_defined`
  - OR 窗口完成前 = `0`
  - OR 窗口完成后 = `1`

### 5. OR 完成后的事件位

- `first_break_direction`
  - 仅在 `opening_range_defined = 1` 后检查
  - 当前只允许：
    - `up`
    - `down`
    - `none`
  - 当前不拆 `close` vs `wick`
- `width_error_day`
  - 当前只保留 `0/1`
  - 阈值逻辑仍保持运行时诊断层，不写入字段名

## 第一份真实数据的最小来源候选

- 候选 A：
  - MT5 / broker bar export
  - 优点：最接近未来实际接入
  - 风险：session 本地时间与 DST 解释必须先验清
- 候选 B：
  - 手工整理的 bar-level CSV
  - 优点：最容易先做 proof-of-mapping
  - 风险：容易把 timezone 与 local date 写错

## 第一份真实数据建议最小样本

- `london` 1 组
  - OR 未定义样本 1 条
  - OR 已定义样本 1 条
- `new_york` 1 组
  - OR 未定义样本 1 条
  - OR 已定义样本 1 条

## 当前不做

- 不做 `IB`
- 不做 `acceptance`
- 不做 `failed breakout`
- 不把财经新闻/宏观事件直接并入当前 P0 字段

## 接入前必须联动

- `n02_p0_runtime_session_calendar_dst_checklist_v1.md`
- `n02_p0_runtime_append_protocol_v1.md`
