# Batch9 P0 统一落盘草案总表 v1

## 目标

- 把 `N01 / N02 / N03` 三份 `P0` 字段落盘草案收成一张统一总表。
- 这张表优先回答四个问题：
  - 字段属于哪一类
  - 当前是否 ready for landing
  - 默认值和空值规则是什么
  - 还缺什么证据
- 当前结论：三类都已经具备 `P0` 最小落盘层，但都**仍未收集完全**。

## 统一列说明

- `type_id`
  - 所属类型：`N01 / N02 / N03`
- `field_name`
  - 标准字段名
- `field_type`
  - 建议类型：`int / float / string`
- `null_allowed`
  - 是否允许空值
- `recommended_default`
  - 推荐默认值
- `landing_status`
  - 当前是否可准备落盘
- `evidence_status`
  - `strong_enough_for_p0` / `usable_but_incomplete`
- `main_gap`
  - 当前主要缺口

## 统一总表

| type_id | field_name | field_type | null_allowed | recommended_default | landing_status | evidence_status | main_gap |
|---|---|---|---|---|---|---|---|
| N01 | `atr_value` | float | yes | `na` | ready_for_landing | strong_enough_for_p0 | 仍缺不同来源 ATR 窗口统一口径 |
| N01 | `atr_ratio` | float | yes | `na` | ready_for_landing | usable_but_incomplete | 仍缺 GainzAlgo 源码级基线 ATR 细节 |
| N01 | `atr_percentile` | float | yes | `na` | ready_for_landing | strong_enough_for_p0 | 仍缺更多窗口样本 |
| N01 | `atr_percentile_regime` | string | no | `unknown` | ready_for_landing | strong_enough_for_p0 | 仍缺 CHE panel/table 字段名 |
| N01 | `squeeze_is_on` | int | no | `0` | ready_for_landing | strong_enough_for_p0 | 仍缺更多跨实现对照 |
| N01 | `squeeze_tier` | string | no | `off` | ready_for_landing | strong_enough_for_p0 | 已补到 Beardy_Fred 版本 `1.0/1.5/2.0 ATR KC`，仍缺更多跨实现对照 |
| N01 | `squeeze_fired` | int | no | `0` | ready_for_landing | strong_enough_for_p0 | 已补到 `NoSqz and not NoSqz[1]`，仍缺对象级触发时点补强 |
| N01 | `compression_quality_score` | float | yes | `na` | ready_for_landing | usable_but_incomplete | 已补到 AG Pro 权重/阈值骨架，仍缺核心计算段源码 |
| N02 | `session_id` | string | no | `unknown_session` | ready_for_landing | strong_enough_for_p0 | 仍缺更多市场 session 样本 |
| N02 | `session_timezone` | string | no | `UTC` | ready_for_landing | strong_enough_for_p0 | 仍缺 DST/多市场样本补强 |
| N02 | `opening_range_window_minutes` | int | no | `30` | ready_for_landing | strong_enough_for_p0 | 仍缺更广窗口样本 |
| N02 | `opening_range_high` | float | yes | `na` | ready_for_landing | strong_enough_for_p0 | 仍缺更多来源交叉验证 |
| N02 | `opening_range_low` | float | yes | `na` | ready_for_landing | strong_enough_for_p0 | 仍缺更多来源交叉验证 |
| N02 | `opening_range_mid` | float | yes | `na` | ready_for_landing | strong_enough_for_p0 | 主要依赖 OR high/low 派生 |
| N02 | `opening_range_width` | float | yes | `na` | ready_for_landing | strong_enough_for_p0 | 主要依赖 OR high/low 派生 |
| N02 | `opening_range_width_pct_open` | float | yes | `na` | ready_for_landing | strong_enough_for_p0 | 仍缺 open 异常值处理样本 |
| N02 | `session_open_price` | float | yes | `na` | ready_for_landing | strong_enough_for_p0 | 仍缺不同市场 session 开盘定义补强 |
| N02 | `opening_range_defined` | int | no | `0` | ready_for_landing | strong_enough_for_p0 | 仍缺跨实现定义差异补强 |
| N02 | `first_break_direction` | string | no | `none` | ready_for_landing | strong_enough_for_p0 | 仍缺 `close` vs `wick` 进一步切分 |
| N02 | `width_error_day` | int | no | `0` | ready_for_landing | usable_but_incomplete | 阈值仍主要来自 joveteo 系 |
| N03 | `swing_mode` | string | no | `unknown` | ready_for_landing | strong_enough_for_p0 | 仍缺更多 custom mode 实例 |
| N03 | `swing_left_bars` | int | yes | `na` | ready_for_landing | usable_but_incomplete | 并非所有来源都显式暴露 |
| N03 | `swing_right_bars` | int | yes | `na` | ready_for_landing | usable_but_incomplete | 并非所有来源都显式暴露 |
| N03 | `swing_high_confirmed` | int | no | `0` | ready_for_landing | strong_enough_for_p0 | 仍缺 live 未确认对象的统一对照 |
| N03 | `swing_low_confirmed` | int | no | `0` | ready_for_landing | strong_enough_for_p0 | 仍缺 live 未确认对象的统一对照 |
| N03 | `break_confirmation_mode` | string | no | `close` | ready_for_landing | usable_but_incomplete | 仍缺更多源码级 `close/wick` 实现核验 |
| N03 | `break_level_price` | float | yes | `na` | ready_for_landing | usable_but_incomplete | 仍缺对象级 tracked level 暴露一致性 |
| N03 | `bos_event` | int | no | `0` | ready_for_landing | strong_enough_for_p0 | 仍缺更多最小实现对照样本 |
| N03 | `choch_event` | int | no | `0` | ready_for_landing | strong_enough_for_p0 | 仍缺更多最小实现对照样本 |
| N03 | `structure_direction` | string | no | `neutral` | ready_for_landing | strong_enough_for_p0 | 仍缺方向初始化口径统一 |
| N03 | `structure_event_bar_close_confirmed` | int | no | `1` | ready_for_landing | usable_but_incomplete | 仍缺对象级 close confirm 落点核验 |

## 按类型汇总

### N01

- P0 共 `8` 个字段
- 更稳的锚点：
  - `atr_percentile_regime`
  - `squeeze_is_on`
  - `squeeze_tier`
- 仍较依赖补网页的字段：
  - `atr_ratio`
  - `compression_quality_score`

### N02

- P0 共 `12` 个字段
- 当前最稳的一组
- 主要缺口不在 P0 本身，而在：
  - `IB`
  - `acceptance`
  - `failed ORB`

### N03

- P0 共 `11` 个字段
- 当前只保留定义层，不混入审计层
- 主要缺口集中在：
  - `close` vs `wick`
  - pivot 固化时机
  - tracked level 的对象级实现

## 当前执行建议

- 若真开始接“实际落盘字段”，建议顺序仍然保持：
  1. `N02 P0`
  2. `N01 P0`
  3. `N03 P0`
- 理由：
  - N02 是时段锚点
  - N01 是波动环境锚点
  - N03 是结构事件锚点

## 未收集完全总备注

- 这张统一总表只是把三份 `P0` 草案合并，不代表证据已经收齐。
- 当前最明显的未补完缺口仍然是：
  - `GainzAlgo Volatility Regimes` 源码页
  - `AG Pro ATR Compression Map` 核心计算段源码与原始 Pine Editor 导出
  - `Initial Balance` 源码级或更强定义证据
  - `Dots3Red / algo_aakash` 的对象级更新时间与过滤层边界
- 本轮虽已把 `compression_state`、`ib_failed_breakout_event` 的命名和标准层收稳，但它们仍不进入当前 `P0` 统一落盘层。

## 对应文件

- [N01_P0_字段落盘草案_v1.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/N01_波动率状态机/N01_P0_字段落盘草案_v1.md#L1-L187)
- [N02_P0_字段落盘草案_v1.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/N02_时段_开盘区间结构/N02_P0_字段落盘草案_v1.md#L1-L163)
- [N03_P0_字段落盘草案_v1.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/N03_市场结构_突破质量_条件收集/N03_P0_字段落盘草案_v1.md#L1-L199)
- [Batch9_P0_统一字段_CSV草案_v1.csv](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/Batch9_P0_统一字段_CSV草案_v1.csv)
- [Batch9_P0_统一字段_CSV样例空表_v1.csv](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/Batch9_P0_统一字段_CSV样例空表_v1.csv)
