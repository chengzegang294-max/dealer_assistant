# Batch9 批次收口与四分流 v1

## 批次定义

- 批次：`Batch9 = 00_外部公开资料与方法论参考\\01_外部公开指标资料_Batch9`
- 当前定位：海外公开指标资料整理批，不直接改当前 `FX / index / commodity 1H` 主线执行链路
- 本批主线：先完成类型裁决，再做公开来源收集，再收成字段草案、统一索引、命名规范、落盘优先级与 `P0` 合约

## 目录摘要

- 本批已经从“资料收集轮”推进到“可落盘合约轮”
- 已形成三条已裁决类型主线：
  - `N01`：波动率状态机
  - `N02`：时段 / 开盘区间结构
  - `N03`：市场结构 / 突破质量（只保留定义层与审计边界）
- 已形成的统一产物包括：
  - 字段草案
  - 字段总表与统一字段索引
  - 命名规范与标准字段映射
  - 落盘优先级清单
  - `P0` 统一落盘总表
  - `CSV` 草案与程序接入空壳
- 当前结论：`Batch9` 已完成第一轮“全量吃透到合同层”的收口，但仍存在明确的未补齐证据缺口

## 代表文件

- 类型与来源入口：
  - `00_本批说明与多AI能力画像.md`
  - `Batch9_外部AI补源评估_v1.md`
  - `Batch9_待用户手动补网页清单_v1.md`
- 字段与合约主轴：
  - `Batch9_指标字段总表_v1.md`
  - `Batch9_统一字段索引表_v1.md`
  - `Batch9_统一字段命名规范_v1.md`
  - `Batch9_标准字段名到实际落盘名映射表_v1.md`
  - `Batch9_字段落盘优先级清单_v1.md`
- `P0` 落盘主轴：
  - `N01_P0_字段落盘草案_v1.md`
  - `N02_P0_字段落盘草案_v1.md`
  - `N03_P0_字段落盘草案_v1.md`
  - `Batch9_P0_统一落盘草案总表_v1.md`
  - `Batch9_P0_统一字段_CSV草案_v1.csv`
  - `Batch9_P0_统一字段_CSV样例空表_v1.csv`

## 当前已确认事实

- `N01 / N02 / N03` 都已从“纯资料收集”进入“字段与合约可映射”阶段
- `N02` 当前是三类里最稳的一组，已形成 `12` 个 `P0` 字段
- `N01` 已形成 `8` 个 `P0` 字段，但 `GainzAlgo / AG Pro` 仍有源码缺口
- `N03` 已形成 `11` 个 `P0` 字段，但只限定义层；审计层和复杂 confluence 继续隔离
- `Kimi` 二次整理稿已经完成“可吸收部分并入正式正文/字段草案/索引”的第一轮收口
- `N04 / N05 / N06` 并未删除，而是明确转入 `A股指标整理区` 后续整理

## 四分流

### 已吸收

- `N01` 的 `P0` 最小波动环境层：
  - `atr_value / atr_ratio / atr_percentile / atr_percentile_regime`
  - `squeeze_is_on / squeeze_tier / squeeze_fired`
  - `compression_quality_score`
- `N02` 的 `P0` 最小时段锚点层：
  - `session_id / session_timezone / opening_range_window_minutes`
  - `opening_range_high / low / mid / width / width_pct_open`
  - `session_open_price / opening_range_defined / first_break_direction / width_error_day`
- `N03` 的 `P0` 最小结构定义层：
  - `swing_mode / swing_left_bars / swing_right_bars`
  - `swing_high_confirmed / swing_low_confirmed`
  - `break_confirmation_mode / break_level_price`
  - `bos_event / choch_event / structure_direction / structure_event_bar_close_confirmed`
- Batch9 统一合同层：
  - 统一字段总表
  - 统一字段索引表
  - 命名规范
  - 标准字段映射表
  - 字段优先级清单
  - `P0` 统一总表
  - `CSV` 草案与程序空壳

### 可重开

- `REOPEN_B9_N02_SESSION_OR_P0`
  - 主题：`N02 P0` 时段 / 开盘区间锚点
  - 角色：首批量化重开优先项
  - 原因：定义最稳、共用价值最高、能为后续 `IB / acceptance / failed ORB` 提供锚点
- `REOPEN_B9_N01_VOL_STATE_P0`
  - 主题：`N01 P0` 波动环境与压缩状态锚点
  - 角色：首批量化重开优先项
  - 原因：能直接补当前主线的波动环境分桶，但仍需保留“未收集完全”备注
- `REOPEN_B9_N03_STRUCTURE_P0`
  - 主题：`N03 P0` 结构事件最小定义层
  - 角色：条件型可重开项
  - 原因：价值高，但必须等 `N02 / N01` 锚点先稳定，且不能混入审计层与 confluence

### future bucket

- `N04 liquidity / imbalance / FVG`
- `N05 VWAP / anchored VWAP / volume profile`
- `N06 breadth / relative strength / leadership`
- `N01` 条件字段：
  - `compression_state`
  - `vol_regime_code`
  - `vol_breakout_signal`
  - `trend_confirmation_after_vol_breakout`
- `N02` 条件字段：
  - `ib_high / ib_low / ib_range`
  - `ib_break_direction`
  - `ib_accept_2period`
  - `ib_regime_narrow_or_wide`
  - `ib_failed_breakout_event`
- `N03` 审计层 / 过滤层字段：
  - `pivot_confirm_delay_bars`
  - `confirmed_pivot_non_repaint`
  - `current_bar_visuals_mutable`
  - `extra_confluence_used`
  - `failed_breakout_event`

### 仅来源库保留

- `Batch9_待用户手动补网页清单_v1.md`
  - 作为补源协作文档保留，不等于已吸收证据
- `batch9_sources_kimi`
  - 作为外部 AI 二次整理稿暂存区保留，不等同于原始源码或原网页落盘
- 仍缺源码级补强的 page excerpt / page_only 资料：
  - `GainzAlgo Volatility Regimes`
  - `AG Pro ATR Compression Map`
  - `Initial Balance` 更强源码级证据
  - `Dots3Red / algo_aakash` 对象级更新时间与过滤层边界

## 本批建议的首批量化重开项

- 第一优先：`REOPEN_B9_N02_SESSION_OR_P0`
  - 理由：它是时段锚点层，最适合作为后续上下文字段底座
- 第二优先：`REOPEN_B9_N01_VOL_STATE_P0`
  - 理由：它是波动环境层，适合作为分桶与解释变量
- `N03` 暂不进入首批，只保留为：
  - `REOPEN_B9_N03_STRUCTURE_P0`
  - 条件：必须保持定义层，不引入复杂 SMC extras，不变成硬门控

## 与主线的关系

- `Batch9` 不是偏离主线，而是“全量吃透 -> 统一分流/重开清单”中的一批正式来源库
- 它当前已经完成：
  - 类型裁决
  - 资料收集
  - 字段化
  - 命名/映射/优先级收口
  - `P0` 合约化
- 它下一步不应再停留在“继续网页堆料”，而应进入：
  - 统一重开清单
  - 选 `1-2` 个首批量化重开项
  - 再决定何时回到组合优化主线

## 未收集完全备注

- 本批已完成“合同层收口”，不代表证据已收齐
- 当前最核心的未补齐缺口仍然是：
  - `GainzAlgo` 源码页
  - `AG Pro` 核心计算段源码
  - `Initial Balance` 源码级或更强定义证据
  - `N03` 对象级更新时间与过滤层边界
- 因此 `Batch9` 当前最准确的状态是：
  - 已收口
  - 可重开
  - 但仍未收集完全

## 源码级缺口备注收口

- 本轮已把 `batch9_sources_kimi` 的可用补强统一降格写入 `batch9_source_manifest.csv` 的 `notes`，统一标签为：
  - `secondary_structured_note`
  - `secondary_structured_note_conflict`
- 当前已按补强层吸收的对象：
  - `TTM Squeeze Pro`
  - `AG Pro ATR Compression Map`
  - `Initial Balance Breakout`
  - `Dots3Red Regime-Adaptive SMC`
  - `algo_aakash BOS/CHoCH`
- 当前只保留冲突线索、不得覆盖原证据的对象：
  - `Volatility Regimes | GainzAlgo`
- 当前口径固定为：
  - `manifest notes` 可以吸收二次整理稿
  - `source status` 不能因此冒充源码已补全
  - `batch9_sources_kimi` 继续只作补强层，不上升为原始真值层

## 下一步

- 先把 `Batch9` 的四分流与首批重开建议同步进主文档
- 再把 `REOPEN_B9_N02_SESSION_OR_P0`、`REOPEN_B9_N01_VOL_STATE_P0` 纳入统一重开清单入口
- 继续保持总主线顺序：
  - 全量扫库 / 吃透
  - 统一分流 / 重开清单
  - 再开稳定候选组合优化
