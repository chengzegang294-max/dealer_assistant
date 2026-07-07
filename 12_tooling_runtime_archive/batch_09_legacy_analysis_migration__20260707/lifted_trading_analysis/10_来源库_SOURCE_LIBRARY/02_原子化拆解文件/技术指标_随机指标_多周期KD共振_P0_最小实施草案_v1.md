# 技术指标_随机指标_多周期KD共振_P0_最小实施草案_v1

## 目标

- 把 `多周期KD共振` 从“对象定义入口”推进到“首批最小实施层”。
- 第一版只实现 `diagnostic/filter layer` 字段落盘，不进入策略 gate，不改默认执行链路。
- 这一步的作用是给后续 `event / entry / A股状态 / 盘面面板` 提供统一的多周期方向过滤底座。

## 不变量

- 第一版只覆盖以下 `6` 个字段：
  - `kd_week_bias`
  - `kd_day_signal`
  - `kd_4h_confirm`
  - `kd_alignment_tier`
  - `kd_direction_filter`
  - `kd_week_extreme_zone`
- 第一版明确不做：
  - `kd_month_bias`
  - `kd_1h_entry_refine`
  - `kd_divergence_flag`
  - `kd_perfect_state_flag`
  - `kd_dispersion_state`
  - 任何仓位倍率落盘
- 默认角色保持：
  - `diagnostic/filter layer`
  - 不是硬门控
  - 不是自动执行入口

## 实施范围

### 第一版必做字段

- `kd_week_bias`
- `kd_day_signal`
- `kd_4h_confirm`
- `kd_alignment_tier`
- `kd_direction_filter`
- `kd_week_extreme_zone`

### 第一版明确不做

- `kd_month_bias`
- `kd_1h_entry_refine`
- `kd_cross_age_bars`
- `kd_divergence_flag`
- `kd_perfect_state_flag`
- `kd_dispersion_state`
- `kd_position_size_multiplier`

## 最小输入

- `symbol`
- `timeframe`
- `bar_time`
- `open`
- `high`
- `low`
- `close`
- 需要能重建或直接提供：
  - `week`
  - `day`
  - `4h`
- 默认参数建议：
  - `kd_length = 13`
  - `kd_smooth_k = 3`
  - `kd_smooth_d = 3`
  - `ma_type = sma`
  - `price_field = close_close`

## 来源回链

- 一级来源索引：
  - `10_来源库_SOURCE_LIBRARY\00_大隐体系\大隐体系_一级索引与可重开候选_v1.md`
- Family 0 来源：
  - `10_来源库_SOURCE_LIBRARY\00_大隐体系\0)stochastic oscillator指标组的各种讲解\0.stochastic oscillator指标组实战应用详细讲解.mp4.md`
  - `10_来源库_SOURCE_LIBRARY\00_大隐体系\0)stochastic oscillator指标组的各种讲解\1.[专业技术课]stochastic oscillator指标组的深入讲解.mp4.md`
  - `10_来源库_SOURCE_LIBRARY\00_大隐体系\0)stochastic oscillator指标组的各种讲解\3.[精华尽出]stochastic oscillator指标组设计思想、应用方法详解.mp4.md`
  - `10_来源库_SOURCE_LIBRARY\00_大隐体系\0)stochastic oscillator指标组的各种讲解\4.stochastic oscillator指标组钝化后涨跌判断诀窍.mp4.md`
  - `10_来源库_SOURCE_LIBRARY\00_大隐体系\0)stochastic oscillator指标组的各种讲解\5.如何在MT4软件上,建立和设置stochastic oscillator(KD)指标和指标模板.mp4.md`
  - `10_来源库_SOURCE_LIBRARY\00_大隐体系\0)stochastic oscillator指标组的各种讲解\9.指标组口诀的视频教学课程.mp4.md`
- 当前承接文件：
  - `技术指标_随机指标_多周期KD共振_后续对象定义入口_v1.md`
  - `技术指标_随机指标_多周期KD共振_真实字段输出路径草案_v1.md`

## 最小输出

- 第一版建议只落一张多周期 KD 诊断字段表
- 建议文件角色：
  - `bar-level diagnostic csv`
- 最小列：
  - 运行时主键列：
    - `symbol`
    - `timeframe`
    - `bar_time`
  - `KD P0` 字段列：
    - `kd_week_bias`
    - `kd_day_signal`
    - `kd_4h_confirm`
    - `kd_alignment_tier`
    - `kd_direction_filter`
    - `kd_week_extreme_zone`

## 最小证据落点

- 合同层：
  - `kd_mtf_p0_contract_notes_v1.md`
  - `kd_mtf_p0_field_header_v1.txt`
  - `kd_mtf_p0_field_sample_v1.csv`
- 运行时层：
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_fields_runtime_v1.csv`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_fields_runtime_header_v1.txt`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_runtime_notes_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_runtime_gaps_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_runtime_append_protocol_v1.md`
- proof-of-mapping：
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_real_input_mapping_draft_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\real_input_samples\kd_mtf_p0_proof_output_v1.csv`

## 计算顺序

1. 先重建 `week / day / 4h` 的 K/D 状态
2. 先派生 `kd_week_bias`
3. 再派生 `kd_day_signal`
4. 再派生 `kd_4h_confirm`
5. 再根据三者关系确定：
   - `kd_alignment_tier`
   - `kd_direction_filter`
6. 最后补：
   - `kd_week_extreme_zone`

## 字段级口径

- `kd_week_bias`
  - 第一版只允许：
    - `up`
    - `down`
    - `unknown`
- `kd_day_signal`
  - 第一版只允许：
    - `golden_cross`
    - `death_cross`
    - `none`
    - `unknown`
- `kd_4h_confirm`
  - 第一版只允许：
    - `confirm_up`
    - `confirm_down`
    - `none`
    - `unknown`
- `kd_alignment_tier`
  - 第一版只允许：
    - `s`
    - `a`
    - `b`
    - `conflict`
    - `unknown`
- `kd_direction_filter`
  - 第一版只允许：
    - `long_preferred`
    - `short_preferred`
    - `wait`
    - `unknown`
- `kd_week_extreme_zone`
  - 第一版只允许：
    - `overbought`
    - `oversold`
    - `normal`
    - `unknown`

## tier 口径

- `s`
  - `week up + day golden_cross + 4h confirm_up`
  - 或 `week down + day death_cross + 4h confirm_down`
- `a`
  - `day + 4h` 同向
  - 且 `week` 不冲突
- `b`
  - 仅 `day` 有主信号
  - `4h` 未明确确认
- `conflict`
  - `week` 与 `day` 方向冲突
- `unknown`
  - 任一关键周期无法可靠计算

## 第一版验收

### 合同验收

- 主 CSV 表头只包含 `6` 个 KD 字段，不出现高阶概念位。
- `kd_alignment_tier` 不允许出现 `s/a/b/conflict/unknown` 之外的值。
- `kd_direction_filter` 不允许落成仓位倍率或执行命令。

### 最小证据

- 至少留下一份字段样本输出
- 至少留下一份表头证据
- 至少留下一份字段缺口说明，明确：
  - 还没做 `month bias`
  - 还没做 `1h refine`
  - 还没做 `背离 / 离散 / 完美`

### 当前角色验收

- 只能宣称：
  - `KD multi-timeframe diagnostic/filter fields defined`
- 不能宣称：
  - `KD execution gate 已实现`
  - `KD sizing engine 已实现`
  - `大隐 stochastic 高阶体系已实现`

## 推荐落地产物

- 第一版最小产物建议：
  - `kd_mtf_p0_field_sample_v1.csv`
  - `kd_mtf_p0_field_header_v1.txt`
  - `kd_mtf_p0_contract_notes_v1.md`

## 风险与缺口

- `多周期KD` 的参数来自通用原子规则 + `大隐 stochastic` 补充，第一版仍属于保守默认值。
- `month` 层约束在概念上有价值，但现在先不进入 P0，避免把对象做重。
- `背离 / 离散 / 完美` 很重要，但当前更适合作 `P1/P2` 的高阶层，不应顺手混进 P0。
- `week/day/4h` 的状态重建口径若后续漂移，应冻结 `v1` 后再起 `v2`。

## 回滚方式

- 若第一版实施不稳，直接退回到：
  - 只保留 `kd_week_bias`
  - `kd_day_signal`
  - `kd_alignment_tier`
- 若后续字段口径漂移：
  - 先冻结 `v1`
  - 再单独起 `v2`
  - 不覆盖 `v1`

## 当前结论

- `多周期KD` 现在可以正式从：
  - `candidate`
  - 进入
  - `in_progress（最小实施草案已落地）`
- 当前已继续推进到：
  - 样本表头已落
  - contract notes 已落
  - field sample 已落
  - runtime 空壳已落
  - proof-of-mapping 草案已落
- 下一步不是继续讨论“值不值得做”，而是：
  - 先补第一份真实 proof 输入/输出
  - 再决定是否值得接 append stub 或 params template
