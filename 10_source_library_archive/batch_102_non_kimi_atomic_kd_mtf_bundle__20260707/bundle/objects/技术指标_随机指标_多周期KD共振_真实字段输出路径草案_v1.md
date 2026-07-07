# 技术指标_随机指标_多周期KD共振_真实字段输出路径草案_v1

## 目标

- 把 `多周期KD P0` 从“样本/合同层”推进到“真实字段输出路径已定义”。
- 先固定第一版真实产物应放哪里、叫什么、各文件承担什么角色。
- 这一步仍然不接入真实计算脚本，只收口运行时目录与文件合同。

## 不变量

- 只覆盖 `KD P0` 的 `6` 个字段：
  - `kd_week_bias`
  - `kd_day_signal`
  - `kd_4h_confirm`
  - `kd_alignment_tier`
  - `kd_direction_filter`
  - `kd_week_extreme_zone`
- 不提前混入：
  - `kd_month_bias`
  - `kd_1h_entry_refine`
  - `kd_divergence_flag`
  - `kd_perfect_state_flag`
  - `kd_dispersion_state`
  - 仓位倍率字段
- 不把样本文件误记成真实运行产物。
- 第一版仍然是：
  - `diagnostic/filter layer`
  - 不是策略门控
  - 不是执行产物

## 第一版真实产物建议目录

- 建议以 `12_工具运行时_TOOLING_RUNTIME` 作为未来真实输出根目录。
- 第一版建议路径：
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\`

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
  - `技术指标_随机指标_多周期KD共振_P0_最小实施草案_v1.md`

## 第一版真实产物清单

### 1. 主产物

- `kd_mtf_p0_fields_runtime_v1.csv`
- 角色：
  - `bar-level` 真实字段输出
- 说明：
  - 每一行对应一个 bar
  - 用于后续和 `event / entry / state` 层做 join

### 2. 表头冻结文件

- `kd_mtf_p0_fields_runtime_header_v1.txt`
- 角色：
  - 冻结真实输出的当前表头
- 说明：
  - 若未来升级为 `v2`，旧版 header 不覆盖

### 3. 运行说明

- `kd_mtf_p0_runtime_notes_v1.md`
- 角色：
  - 记录 KD 参数、周期映射、空值口径、当前未实现内容
- 说明：
  - 这里写“运行口径”
  - 不重复大段字段定义

### 4. 缺口与审计说明

- `kd_mtf_p0_runtime_gaps_v1.md`
- 角色：
  - 记录当前没做什么，以及为什么没做
- 说明：
  - 要明确：
    - `month bias` 未接入
    - `1h refine` 未接入
    - `背离 / 离散 / 完美` 未接入

### 5. 追加协议

- `kd_mtf_p0_runtime_append_protocol_v1.md`
- 角色：
  - 约束第一批真实数据行怎样从占位状态过渡到真实追加
- 说明：
  - 明确是否删除占位样本行
  - 明确何时需要起 `v2`

## 最小输入 / 输出 / 证据落点

- 最小输入：
  - `symbol`
  - `timeframe`
  - `bar_time`
  - `open`
  - `high`
  - `low`
  - `close`
  - `kd_length = 13`
  - `kd_smooth_k = 3`
  - `kd_smooth_d = 3`
- 最小输出：
  - `kd_week_bias`
  - `kd_day_signal`
  - `kd_4h_confirm`
  - `kd_alignment_tier`
  - `kd_direction_filter`
  - `kd_week_extreme_zone`
- 合同证据：
  - `kd_mtf_p0_contract_notes_v1.md`
  - `kd_mtf_p0_field_header_v1.txt`
  - `kd_mtf_p0_field_sample_v1.csv`
- 运行时证据：
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_fields_runtime_v1.csv`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_fields_runtime_header_v1.txt`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_runtime_notes_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_runtime_gaps_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_runtime_append_protocol_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_runtime_append_stub_v1.py`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_runtime_params_template_v1.json`
- proof 证据：
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\kd_mtf_p0_real_input_mapping_draft_v1.md`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - `12_工具运行时_TOOLING_RUNTIME\kd_mtf_p0_v1\real_input_samples\kd_mtf_p0_proof_output_v1.csv`

## 文件命名规则

- 统一小写下划线风格，不混中文文件名到运行产物目录。
- 固定前缀：
  - `kd_mtf_p0_`
- 版本号固定放文件名末尾：
  - `_v1`
- 不在文件名里携带：
  - `date_tag`
  - `symbol`
  - `timeframe`
- 这些运行维度应体现在文件内容列里，而不是拆成大量碎文件。

## 真实输出表头

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

## 产物职责分层

- `sample / header / notes`
  - 现在先在来源库合同层落地
  - 用于合同演示和表头冻结
- `runtime csv / header / notes / gaps / append_protocol`
  - 当前已进入工具运行时目录空壳
  - 用于真实脚本输出与审计

## 第一版验收口径

- 真实输出目录已固定，后续不再来回改名。
- 主 CSV 表头必须和当前样本表头一致。
- 运行说明必须写清：
  - 默认 `kd_length`
  - 默认 `kd_smooth_k`
  - 默认 `kd_smooth_d`
  - 默认周期集合（`week/day/4h`）
- 缺口文件必须写清：
  - 还未做 `month bias`
  - 还未做 `1h refine`
  - 还未做 `背离 / 离散 / 完美`

## 当前不做

- 不拆 `symbol` 单文件输出
- 不拆 `timeframe` 单文件输出
- 不加 `trade_id`
- 不加 `entry_id`
- 不加 `signal_id`
- 不加 `month bias`
- 不加 `1h refine`
- 不加高阶形态解释字段

## 下一步

- 按本路径草案，把 `多周期KD P0` 的下一阶段定义为：
  - 真实字段输出文件路径已固定
  - 运行时目录合同已固定
  - `runtime csv / header / notes / gaps / append_protocol / real_input_mapping_draft` 已落空壳
  - 后续若继续推进，优先补：
    - 第一份真实 proof 输入
    - 第一份真实 proof 输出
    - `runtime params template / append stub` 是否值得进入 v1
