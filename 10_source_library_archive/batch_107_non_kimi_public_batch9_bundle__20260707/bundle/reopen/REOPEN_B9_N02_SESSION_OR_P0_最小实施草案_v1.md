# REOPEN_B9_N02_SESSION_OR_P0 最小实施草案 v1

## 目标

- 把 `Batch9 / N02` 从“字段合同层”推进到“首批量化重开最小实施层”。
- 第一版只实现 `session / opening range` 的 `P0` 诊断字段落盘，不进入策略 gate，不改默认执行链路。
- 这一步的作用是给后续 `IB / acceptance / failed ORB` 提供统一时段锚点，而不是直接复刻完整 ORB 策略。

## 不变量

- 只做 `N02 P0` 的 `12` 个字段，不提前混入：
  - `IB`
  - `acceptance`
  - `ib_failed_breakout_event`
  - `session_bias`
  - `or_break_high / or_break_low / target_trigger_source`
- 默认角色保持：
  - `diagnostic/context layer`
  - 不是硬门控
  - 不是自动执行入口
- 字段名、默认值、空值规则，严格对齐现有：
  - `N02_P0_字段落盘草案_v1.md`
  - `Batch9_P0_统一字段_CSV草案_v1.csv`

## 实施范围

### 第一版必做字段

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

### 第一版明确不做

- `or_break_high`
- `or_break_low`
- `target_trigger_source`
- `ib_high`
- `ib_low`
- `ib_range`
- `ib_break_direction`
- `ib_accept_2period`
- `ib_regime_narrow_or_wide`
- `ib_failed_breakout_event`
- `session_bias`
- `custom_session_used`
- `session_ma_bias`

## 最小输入

- `bar_time`
- `open`
- `high`
- `low`
- `close`
- `symbol`
- `timeframe`
- 一组可配置但默认固定的 session 参数：
  - `session_id`
  - `session_timezone`
  - `opening_range_window_minutes`

## 最小输出

- 第一版建议只落一张诊断字段表
- 建议文件角色：
  - `trade/bar-level diagnostic csv`
- 最小列：
  - 运行时主键列：
    - `symbol`
    - `timeframe`
    - `bar_time`
  - `N02 P0` 字段列：
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

## 计算顺序

1. 先确定当前 bar 所属 `session_id / session_timezone`
2. 记录当前 session 的 `session_open_price`
3. 在 `opening_range_window_minutes` 窗口内累计：
   - `opening_range_high`
   - `opening_range_low`
4. 窗口结束后派生：
   - `opening_range_mid`
   - `opening_range_width`
   - `opening_range_width_pct_open`
   - `opening_range_defined = 1`
5. 在 OR 已定义后，再判断：
   - `first_break_direction`
   - `width_error_day`

## 字段级口径

- `opening_range_defined`
  - OR 未完成前固定为 `0`
  - OR 窗口完成后固定为 `1`
- `opening_range_high / low / mid / width`
  - 仅在 `opening_range_defined = 1` 后视为稳定值
- `opening_range_width_pct_open`
  - 仅在 `session_open_price > 0` 时计算
  - 否则保留 `na`
- `first_break_direction`
  - 第一版只允许：
    - `up`
    - `down`
    - `none`
  - 不切分 `close` vs `wick`
- `width_error_day`
  - 第一版只保留结果标记 `0/1`
  - 不把阈值直接硬编码到字段名和输出列

## 第一版验收

### 合同验收

- 产出列名与 [Batch9_P0_统一字段_CSV草案_v1.csv](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/Batch9_P0_统一字段_CSV草案_v1.csv#L1-L13) 中 `N02` 的 `actual_landing_name_v1` 一致
- 不出现任何 `IB`、`acceptance`、`failed breakout` 字段
- `opening_range_defined = 0` 时，允许 OR 价格类列为空

### 最小证据

- 至少留下一份字段样本输出
- 至少留下一份表头证据
- 至少留下一份字段缺口说明，明确：
  - 还没做 `IB`
  - 还没做 `target_trigger_source`
  - 还没做 `close` vs `wick`

### 当前角色验收

- 只能宣称：
  - `N02 P0 diagnostic/context fields implemented`
- 不能宣称：
  - `完整 ORB 策略已实现`
  - `IB acceptance 已实现`
  - `failed ORB 已实现`

## 推荐落地产物

- 第一版最小产物建议：
  - `n02_p0_field_sample_v1.csv`
  - `n02_p0_field_header_v1.txt`
  - `n02_p0_contract_notes_v1.md`
- 若后续接到统一审计目录，再统一改名，不在这一步先扩工程

## 风险与缺口

- `session_id` 的跨市场样本仍偏少
- `session_timezone` 仍缺 DST 与 overlap 样本补强
- `width_error_day` 阈值目前仍主要来自 `joveteo`
- `first_break_direction` 还未拆 `close` vs `wick`
- `IB` 相关文章已补强，但仍不能提前并入本次最小实施

## 回滚方式

- 若第一版实现不稳，直接退回到：
  - 只保留 `session_id / session_timezone / opening_range_window_minutes`
  - 暂不输出 `first_break_direction / width_error_day`
- 若后续发现 session 口径漂移：
  - 先冻结旧表头
  - 再单独起 `v2`
  - 不覆盖 `v1`

## 当前结论

- `REOPEN_B9_N02_SESSION_OR_P0` 现在可以正式从：
  - `candidate`
  - 进入
  - `in_progress（最小实施草案已落地）`
- 下一步不是继续讨论方向，而是按这份草案去落第一版字段输出证据。

## 对应文件

- [N02_P0_字段落盘草案_v1.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/N02_时段_开盘区间结构/N02_P0_字段落盘草案_v1.md#L1-L163)
- [Batch9_P0_统一字段_CSV草案_v1.csv](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/Batch9_P0_统一字段_CSV草案_v1.csv#L1-L13)
- [Batch9_批次收口与四分流_v1.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/Batch9_批次收口与四分流_v1.md#L80-L138)
