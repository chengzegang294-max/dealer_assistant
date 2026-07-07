# 技术指标_随机指标_多周期KD共振_后续对象定义入口_v1

## 作用

- 把 `技术指标_随机指标_多周期KD共振与过滤规则.md` 从“原子规则条目”推进到更明确的后续对象入口。
- 当前目标不是直接把它变成交易门控，而是先固定：
  - 进入条件
  - 最小输入
  - 最小输出
  - 与现有来源层/字段层的衔接关系
  - 后续验收边界

## 当前定位

- 层级：
  - `02_原子化拆解文件` 后续对象层
- 当前角色：
  - `next_object_entry`
- 不是：
  - 当前已接入的真实字段
  - 当前硬门控
  - 当前自动执行入口

## 为什么先从多周期KD开

- 它已经具备“最小实现入口”最需要的三件事：
  - 多周期层级清楚
  - 过滤逻辑清楚
  - 可先做诊断层，不必直接碰执行层
- 相比 `B转A失败`、`周期状态机`：
  - 主观图感更少
  - 周期约束更容易写成字段
  - 更适合先做 `diag-only / filter-layer`
- 相比 `Spring/UT`：
  - 它不是单一形态事件，而是可复用的上游过滤层
  - 更适合作为后续 entry/shape/event 对象的共用上下文

## 来源锚点

- 主来源：
  - `技术指标_随机指标_多周期KD共振与过滤规则.md`
- 补充来源：
  - `00_大隐体系\大隐体系_一级索引与可重开候选_v1.md`
  - `00_大隐体系\0)stochastic oscillator指标组的各种讲解\0.stochastic oscillator指标组实战应用详细讲解.mp4.md`
  - `00_大隐体系\0)stochastic oscillator指标组的各种讲解\1.[专业技术课]stochastic oscillator指标组的深入讲解.mp4.md`
  - `00_大隐体系\0)stochastic oscillator指标组的各种讲解\3.[精华尽出]stochastic oscillator指标组设计思想、应用方法详解.mp4.md`
  - `00_大隐体系\0)stochastic oscillator指标组的各种讲解\4.stochastic oscillator指标组钝化后涨跌判断诀窍.mp4.md`
  - `00_大隐体系\0)stochastic oscillator指标组的各种讲解\5.如何在MT4软件上,建立和设置stochastic oscillator(KD)指标和指标模板.mp4.md`
  - `00_大隐体系\0)stochastic oscillator指标组的各种讲解\9.指标组口诀的视频教学课程.mp4.md`
- 当前承接方式：
  - 以 `原子规则` 为合同主源
  - 以 `大隐 stochastic 指标组` 作为多周期组织方式与默认参数的补强说明

## 回链到当前 KD 一组文件

- 对象入口：
  - `技术指标_随机指标_多周期KD共振_后续对象定义入口_v1.md`
- 最小实施草案：
  - `技术指标_随机指标_多周期KD共振_P0_最小实施草案_v1.md`
- 真实字段输出路径草案：
  - `技术指标_随机指标_多周期KD共振_真实字段输出路径草案_v1.md`
- 合同层：
  - `kd_mtf_p0_contract_notes_v1.md`
  - `kd_mtf_p0_field_header_v1.txt`
  - `kd_mtf_p0_field_sample_v1.csv`

## 最小输入

- 基础行情：
  - `symbol`
  - `timeframe`
  - `bar_time`
  - `open`
  - `high`
  - `low`
  - `close`
- 至少可重建以下周期的 K 线：
  - `week`
  - `day`
  - `4h`
- 第一版不强求：
  - `1h`
  - `month` 的完整事件位
- 第一版默认参数建议：
  - `kd_length = 13`
  - `kd_smooth_k = 3`
  - `kd_smooth_d = 3`
  - `ma_type = sma`
  - `price_field = close_close`

## 最小输出

- `kd_week_bias`
  - `up / down / unknown`
- `kd_day_signal`
  - `golden_cross / death_cross / none / unknown`
- `kd_4h_confirm`
  - `confirm_up / confirm_down / none / unknown`
- `kd_alignment_tier`
  - `s / a / b / conflict / unknown`
- `kd_direction_filter`
  - `long_preferred / short_preferred / wait / unknown`
- `kd_week_extreme_zone`
  - `overbought / oversold / normal / unknown`

## 建议的派生输出（先占位，不进第一版最小合同）

- `kd_month_bias`
- `kd_1h_entry_refine`
- `kd_cross_age_bars`
- `kd_divergence_flag`
- `kd_perfect_state_flag`
- `kd_dispersion_state`

## 最小证据落点

- 来源回链：
  - `00_大隐体系\大隐体系_一级索引与可重开候选_v1.md`
  - `00_大隐体系\0)stochastic oscillator指标组的各种讲解\`
- 合同证据：
  - `kd_mtf_p0_contract_notes_v1.md`
  - `kd_mtf_p0_field_header_v1.txt`
  - `kd_mtf_p0_field_sample_v1.csv`
- 运行时证据：
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_fields_runtime_v1.csv`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_runtime_notes_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_real_input_mapping_draft_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\real_input_samples\kd_mtf_p0_proof_output_v1.csv`

## 对齐逻辑

- `week`
  - 当前先承担中期方向角色
- `day`
  - 当前先承担主信号角色
- `4h`
  - 当前先承担确认角色
- 第一版更稳的 tier 划分：
  - `s`
    - `week up/down` 明确
    - `day` 出现同向主信号
    - `4h` 同向确认
  - `a`
    - `day + 4h` 同向
    - 但 `week` 未冲突或仍可接受
  - `b`
    - 仅 `day` 有信号
  - `conflict`
    - `week` 与 `day` 冲突

## 最小验收定义

- 有一份对象合同草案：
  - 输入/输出/默认参数明确
- 有一份最小实施草案：
  - 只做诊断层字段
- 有一份当前角色裁决：
  - `DIAG_ONLY_OBJECT_CANDIDATE`
  - 或 `next_object_entry`
- 不得提前宣称：
  - 已接入主交易链路
  - 已成为硬门控
  - 已实现 `1h` 精细入场
  - 已实现 `month/week/day/4h/1h` 全层完备共振引擎

## 当前 gaps

- 原子规则文档没有给出一套完全冻结的 KD 参数，当前需要借助 `大隐 stochastic` 资料补默认值。
- `month` 层更适合作大方向约束，但第一版先不把它塞进最小合同。
- `背离 / 离散 / 完美` 这些高阶概念已存在来源支撑，但当前不直接进入 v1 落地字段。
- 当前不应把“仓位倍率建议”直接写成实现字段。

## 当前裁决

- `多周期KD` 已不再只是“可重开题材”，而应固定为：
  - `02_原子化拆解文件` 的首批后续对象入口之一
  - 优先角色是 `多周期过滤层`
  - 先落 `diag-only / filter-layer`
- 同时保持边界：
  - 不反向污染当前主线默认行为
  - 不提前宣称它已具备真实策略门控资格

## 下一步

- 若继续推进同一条线，优先顺序应为：
  - 先补 `多周期KD P0 最小实施草案`
  - 再固定 `运行时输出路径`
  - 再补 `header / contract notes / field sample`
  - 再补 `proof-of-mapping + runtime notes / gaps / append_protocol`
