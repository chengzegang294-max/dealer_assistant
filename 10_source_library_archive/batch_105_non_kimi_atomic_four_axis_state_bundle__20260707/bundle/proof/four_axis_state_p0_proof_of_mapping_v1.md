# four_axis_state_p0_proof_of_mapping_v1

## 目标

- 证明“四轴状态模板”已经可以收成最小诊断对象，而不是只停留在文字入口卡。
- 当前 proof 只验证“字段冻结与样本可跑通”，不验证策略收益。

## 来源锚点

- 对象入口：
  - `10_source_library_archive/_raw_snapshot_batch09/10_来源库_SOURCE_LIBRARY/02_原子化拆解文件/趋势系统交易_四轴状态模板_后续对象定义入口_v1.md`
- 结构定义：
  - 四轴定义（Structure / Bias / Friction / Risk）
- 当前字段候选：
  - `trend_existence_state`
  - `breakout_validity_state`
  - `volatility_regime_state`
  - `crowd_extremity_state`
  - `transaction_cost_load_state`
  - `liquidity_adequacy_state`

## 映射规则

- Structure Axis
  - `trend_slope_20` -> `trend_existence_state`
  - `breakout_strength_20` -> `breakout_validity_state`
- Bias Axis
  - `crowd_extremity_z` -> `crowd_extremity_state`
- Friction Axis
  - `spread_bps` -> `transaction_cost_load_state`
  - `liquidity_depth_ratio` -> `liquidity_adequacy_state`
- Risk Axis
  - 第一版不单独输出新字段，先通过 `volatility_regime_state` 承接风险环境强弱

## 样本说明

- `proof_input_v1.csv`
  - 提供 3 行代理输入样本
- `proof_output_v1.csv`
  - 根据合同阈值给出 3 行冻结输出

## 当前裁决

- 本对象当前角色固定为 `DIAG_ONLY_OBJECT_CANDIDATE`
- proof 通过后，说明该对象已具备：
  - 最小输入
  - 最小输出
  - 最小可审计映射
- 仍不说明：
  - 已可驱动自动执行
  - 已可作为仓位引擎输入
