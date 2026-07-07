# Batch9 统一字段索引表 v1

## 说明

- 目标：把 `N01 / N02 / N03` 的字段拉成一张逐行索引表。
- 用途：后续查询“某字段属于哪类、当前完整度如何、还缺什么证据”时，优先看这张表。
- 这张表是索引层，不替代各自的字段草案。
- 当前结论：三类都已可做 v1 索引，但**仍未收集完全**。

## 完整度等级

- `L3-ready`：定义清楚，可先做研究侧/诊断字段
- `L2-conditional`：有证据，但还缺源码/阈值/对象级时序核验
- `L1-context-only`：只作背景或越界说明，不进当前最小字段层

## 字段索引

| field_name | type_id | layer | data_type | completeness | current_status | key_gap_or_note |
|---|---|---|---|---|---|---|
| `atr_value` | N01 | A | float | L3-ready | 可先落诊断字段 | 默认长度不写死到单一来源 |
| `atr_baseline_value` | N01 | A | float | L3-ready | 可先落诊断字段 | 长窗基线来源仍偏 GainzAlgo |
| `atr_ratio` | N01 | A | float | L3-ready | 可先落诊断字段 | regime 主轴变量 |
| `atr_percentile` | N01 | A | float | L3-ready | 可先落诊断字段 | 0-100 标准化 |
| `atr_percentile_regime` | N01 | A | string | L3-ready | 可先落诊断字段 | 五档阈值已清楚 |
| `atr_regime_is_extreme` | N01 | A | int | L3-ready | 可先落诊断字段 | 先按 percentile > 90 草案 |
| `atr_regime_is_squeeze` | N01 | A | int | L3-ready | 可先落诊断字段 | 先按 percentile < 10 草案 |
| `squeeze_is_on` | N01 | A | int | L3-ready | 可先落诊断字段 | BB inside KC 压缩态 |
| `squeeze_tier` | N01 | A | string | L3-ready | 可先落诊断字段 | Beardy_Fred 版本已补到 `1.0/1.5/2.0 ATR KC` 三档 |
| `squeeze_fired` | N01 | A | int | L3-ready | 可先落诊断字段 | Beardy_Fred 版本已补到 `NoSqz and not NoSqz[1]` |
| `squeeze_momentum_sign` | N01 | A | int | L3-ready | 可先落诊断字段 | 方向层，不等于压缩层 |
| `compression_quality_score` | N01 | A | float | L3-ready | 可先落诊断字段 | 已补到 `30/30/20/20` 权重与 `62/80` 阈值骨架 |
| `atr_contraction_score` | N01 | A | float | L3-ready | 可先落诊断字段 | AG Pro 四维评分子项之一 |
| `range_tightness_score` | N01 | A | float | L3-ready | 可先落诊断字段 | AG Pro 四维评分子项之一 |
| `noise_cleanliness_score` | N01 | A | float | L3-ready | 可先落诊断字段 | AG Pro 四维评分子项之一 |
| `containment_score` | N01 | A | float | L3-ready | 可先落诊断字段 | AG Pro 四维评分子项之一 |
| `compression_state` | N01 | B | string | L2-conditional | 条件字段 | 可优先对齐 `Loose/Building/Tight/Mature`，仍缺原始源码页复核 |
| `vol_regime_code` | N01 | B | string | L2-conditional | 条件字段 | GainzAlgo 仍缺源码级证据 |
| `vol_breakout_signal` | N01 | B | int | L2-conditional | 条件字段 | breakout 阈值与确认时机未稳 |
| `trend_confirmation_after_vol_breakout` | N01 | B | int | L2-conditional | 条件字段 | Step1/Step2 对象级逻辑未核 |
| `squeeze_momentum_accel` | N01 | B | float | L2-conditional | 条件字段 | 各实现差异较大 |
| `atr_percentile_window` | N01 | B | int | L2-conditional | 条件字段 | 窗口默认值未统一 |
| `position_size_calculator` | N01 | C | context | L1-context-only | 不进当前字段 | 执行/风控说明 |
| `dynamic_stop_loss` | N01 | C | context | L1-context-only | 不进当前字段 | 执行/风控说明 |
| `take_profit_scaling` | N01 | C | context | L1-context-only | 不进当前字段 | 执行/风控说明 |
| `integrated_risk_management` | N01 | C | context | L1-context-only | 不进当前字段 | 越出最小状态机范围 |
| `session_id` | N02 | A | string | L3-ready | 可先落诊断字段 | 伦敦/纽约/自定义窗口 |
| `session_timezone` | N02 | A | string | L3-ready | 可先落诊断字段 | 必须显式保留，防 DST 漂移 |
| `opening_range_window_minutes` | N02 | A | int | L3-ready | 可先落诊断字段 | 30/60/90/120m 等 |
| `opening_range_high` | N02 | A | float | L3-ready | 可先落诊断字段 | OR 窗口高点 |
| `opening_range_low` | N02 | A | float | L3-ready | 可先落诊断字段 | OR 窗口低点 |
| `opening_range_mid` | N02 | A | float | L3-ready | 可先落诊断字段 | `(ORH + ORL)/2` |
| `opening_range_width` | N02 | A | float | L3-ready | 可先落诊断字段 | `abs(ORH - ORL)` |
| `opening_range_width_pct_open` | N02 | A | float | L3-ready | 可先落诊断字段 | 可交易性辅助字段 |
| `session_open_price` | N02 | A | float | L3-ready | 可先落诊断字段 | width threshold 基准 |
| `opening_range_defined` | N02 | A | int | L3-ready | 可先落诊断字段 | OR 完成建立后固定 |
| `or_break_high` | N02 | A | int | L3-ready | 可先落诊断字段 | OR 上破事件 |
| `or_break_low` | N02 | A | int | L3-ready | 可先落诊断字段 | OR 下破事件 |
| `first_break_direction` | N02 | A | string | L3-ready | 可先落诊断字段 | `up/down/none` |
| `target_trigger_source` | N02 | A | string | L3-ready | 可先落诊断字段 | `close/high_low` |
| `width_error_day` | N02 | A | int | L3-ready | 可先落诊断字段 | 当前样本为 `<0.2% of open` |
| `session_bias` | N02 | B | string | L2-conditional | 条件字段 | 依赖实现细节，定义未统一 |
| `ib_high` | N02 | B | float | L2-conditional | 条件字段 | IB 仍主要来自定义文章 |
| `ib_low` | N02 | B | float | L2-conditional | 条件字段 | 同上 |
| `ib_range` | N02 | B | float | L2-conditional | 条件字段 | 同上 |
| `ib_break_direction` | N02 | B | string | L2-conditional | 条件字段 | 需与 OR 事件分离 |
| `ib_accept_2period` | N02 | B | int | L2-conditional | 条件字段 | 文章在多个 breakout 场景中重复强调，仍缺源码级证据 |
| `ib_regime_narrow_or_wide` | N02 | B | string | L2-conditional | 条件字段 | 语义已较清楚，但仍缺统一阈值 |
| `ib_failed_breakout_event` | N02 | B | int | L2-conditional | 条件字段 | 已补到 `price returns into IB` 定义，仍非源码实现 |
| `custom_session_used` | N02 | B | int | L2-conditional | 条件字段 | 偏配置元数据 |
| `session_ma_bias` | N02 | B | string | L2-conditional | 条件字段 | 混有可视趋势层 |
| `profit_days` | N02 | C | context | L1-context-only | 不进当前字段 | 统计面板结果 |
| `loss_days` | N02 | C | context | L1-context-only | 不进当前字段 | 统计面板结果 |
| `error_days` | N02 | C | context | L1-context-only | 不进当前字段 | 统计面板结果 |
| `options_premium_decay_logic` | N02 | C | context | L1-context-only | 不进当前字段 | 策略应用层 |
| `swing_mode` | N03 | A | string | L3-ready | 可先落诊断字段 | `pivot/fractal/custom` |
| `swing_left_bars` | N03 | A | int | L3-ready | 可先落诊断字段 | 左侧确认根数 |
| `swing_right_bars` | N03 | A | int | L3-ready | 可先落诊断字段 | 右侧确认根数 |
| `swing_high_confirmed` | N03 | A | int | L3-ready | 可先落诊断字段 | 只认确认后摆点 |
| `swing_low_confirmed` | N03 | A | int | L3-ready | 可先落诊断字段 | 只认确认后摆点 |
| `break_confirmation_mode` | N03 | A | string | L3-ready | 可先落诊断字段 | `close` 或 `wick`；已补到 Dots3Red `conf_mode="Close"` 样本 |
| `break_level_price` | N03 | A | float | L3-ready | 可先落诊断字段 | 被突破结构价位 |
| `bos_event` | N03 | A | int | L3-ready | 可先落诊断字段 | 同向结构突破 |
| `choch_event` | N03 | A | int | L3-ready | 可先落诊断字段 | 反向结构切换 |
| `structure_direction` | N03 | A | string | L3-ready | 可先落诊断字段 | `bullish/bearish/neutral` |
| `structure_event_bar_close_confirmed` | N03 | A | int | L3-ready | 可先落诊断字段 | 是否要求收盘确认 |
| `pivot_confirm_delay_bars` | N03 | B | int | L2-conditional | 条件字段 | 当前已有 `pivot_len=7` 与 `swingLen=10` 样本，仍需更细延迟表 |
| `confirmed_pivot_non_repaint` | N03 | B | int | L2-conditional | 条件字段 | 仍缺源码级更新时机核验 |
| `structure_label_inherits_pivot_delay` | N03 | B | int | L2-conditional | 条件字段 | 多数 pivot-based 为 1 |
| `current_bar_visuals_mutable` | N03 | B | int | L2-conditional | 条件字段 | live bar 行为仍缺源码核验 |
| `close_vs_wick_risk_note` | N03 | B | string | L2-conditional | 条件字段 | 审计说明字段 |
| `future_leak_risk_flag` | N03 | B | int | L2-conditional | 条件字段 | 不确定时先标 1 |
| `extra_confluence_used` | N03 | B | string | L2-conditional | 条件字段 | algo_aakash 已补到 4 因子样本；仅作审计层 |
| `source_complexity_tier` | N03 | B | string | L2-conditional | 条件字段 | `minimal/medium/complex` |
| `failed_breakout_event` | N03 | B | int | L2-conditional | 暂未纳入 v1 | 对象级字段仍未系统补齐 |
| `FVG` | N03 | C | context | L1-context-only | 不进当前字段 | 本轮越界内容 |
| `order_block` | N03 | C | context | L1-context-only | 不进当前字段 | 本轮越界内容 |
| `premium_discount` | N03 | C | context | L1-context-only | 不进当前字段 | 本轮越界内容 |
| `Fib` | N03 | C | context | L1-context-only | 不进当前字段 | 本轮越界内容 |
| `regime_adaptation` | N03 | C | context | L1-context-only | 不进当前字段 | 本轮越界内容 |
| `HTF_overlay` | N03 | C | context | L1-context-only | 不进当前字段 | 本轮越界内容 |
| `volume_scoring` | N03 | C | context | L1-context-only | 不进当前字段 | 本轮越界内容 |
| `EMA_momentum_confirmation` | N03 | C | context | L1-context-only | 不进当前字段 | 本轮越界内容 |

## 当前裁决

- 若要开始真正做“研究侧字段索引”或“统一字段命名”，优先从 `L3-ready` 字段开工。
- `L2-conditional` 字段必须保留缺口说明，不能伪装成已收全。
- `L1-context-only` 继续留在来源说明层，不进入当前最小实现。

## 当前重开进度补记

- `N01`
  - 已新增：
    - `n01_p0_field_sample_v1.csv`
    - `n01_p0_field_header_v1.txt`
    - `n01_p0_contract_notes_v1.md`
    - `REOPEN_B9_N01_VOL_STATE_P0_真实字段输出路径草案_v1.md`
    - `REOPEN_B9_N01_VOL_STATE_P0_批次推进记录_v1.md`
    - `n01_p0_runtime_params_template_v1.json`
    - `n01_p0_runtime_append_stub_v1.py`
  - 当前状态：
    - `REOPEN_B9_N01_VOL_STATE_P0 = in_progress`
    - 已从字段合同层推进到第一版样本证据、运行时空壳与 persist 示例行验证
- `N02`
  - 已验证：
    - `n02_p0_runtime_append_stub_v1.py` 的 `dry-run`
    - `n02_p0_runtime_append_stub_v1.py --persist`
  - 当前状态：
    - `REOPEN_B9_N02_SESSION_OR_P0 = in_progress`
    - 运行时 CSV 中当前是 `1` 条示例行，不是实盘/回测真实输出

## 对应草案

- [N01_字段草案_v1.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/N01_波动率状态机/N01_字段草案_v1.md#L1-L94)
- [N02_字段草案_v1.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/N02_时段_开盘区间结构/N02_字段草案_v1.md#L1-L97)
- [N03_字段草案_v1.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/N03_市场结构_突破质量_条件收集/N03_字段草案_v1.md#L1-L90)
- [Batch9_指标字段总表_v1.md](file:///d:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_外部公开资料与方法论参考/01_外部公开指标资料_Batch9/Batch9_指标字段总表_v1.md#L1-L98)
