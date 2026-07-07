# REOPEN_B9_N01_VOL_STATE_P0 最小实施草案 v1

## 目标

- 把 `Batch9 / N01` 从“P0 字段合同层”推进到“首批量化重开最小实施层”。
- 第一版只实现波动环境与压缩状态的 `P0` 诊断字段落盘，不进入策略 gate，不改当前默认执行链路。
- 这一步的作用是给后续分桶、解释变量和环境过滤研究提供统一波动状态底座。

## 不变量

- 只做 `N01 P0` 的 `8` 个字段，不提前混入：
  - `atr_baseline_value`
  - `squeeze_momentum_sign`
  - `compression_state`
  - `vol_regime_code`
  - `vol_breakout_signal`
  - `trend_confirmation_after_vol_breakout`
  - 四项 compression 子评分
- 默认角色保持：
  - `diagnostic/state layer`
  - 不是硬门控
  - 不是自动执行入口
- 字段名、默认值、空值规则，严格对齐现有：
  - `N01_P0_字段落盘草案_v1.md`
  - `Batch9_P0_统一字段_CSV草案_v1.csv`

## 实施范围

### 第一版必做字段

- `atr_value`
- `atr_ratio`
- `atr_percentile`
- `atr_percentile_regime`
- `squeeze_is_on`
- `squeeze_tier`
- `squeeze_fired`
- `compression_quality_score`

### 第一版明确不做

- `atr_baseline_value`
- `atr_regime_is_extreme`
- `atr_regime_is_squeeze`
- `squeeze_momentum_sign`
- `atr_contraction_score`
- `range_tightness_score`
- `noise_cleanliness_score`
- `containment_score`
- `compression_state`
- `vol_regime_code`
- `vol_breakout_signal`
- `trend_confirmation_after_vol_breakout`

## 最小输入

- `bar_time`
- `open`
- `high`
- `low`
- `close`
- `symbol`
- `timeframe`
- 一组可配置但默认固定的波动参数：
  - `atr_length`
  - `atr_baseline_length`
  - `atr_percentile_window`
  - `squeeze_mode`

## 最小输出

- 第一版建议只落一张波动状态诊断字段表
- 建议文件角色：
  - `bar-level diagnostic csv`
- 最小列：
  - 运行时主键列：
    - `symbol`
    - `timeframe`
    - `bar_time`
  - `N01 P0` 字段列：
    - `atr_value`
    - `atr_ratio`
    - `atr_percentile`
    - `atr_percentile_regime`
    - `squeeze_is_on`
    - `squeeze_tier`
    - `squeeze_fired`
    - `compression_quality_score`

## 计算顺序

1. 先计算 `atr_value`
2. 若有基线 ATR，则计算 `atr_ratio`
3. 若有足够回看窗口，则计算 `atr_percentile`
4. 基于 percentile 派生 `atr_percentile_regime`
5. 并行记录：
   - `squeeze_is_on`
   - `squeeze_tier`
   - `squeeze_fired`
6. 最后补：
   - `compression_quality_score`

## 字段级口径

- `atr_percentile`
  - 第一版保持 `0-100`
  - 不切换成 `0-1`
- `atr_percentile_regime`
  - 第一版只允许：
    - `extreme`
    - `elevated`
    - `normal`
    - `calm`
    - `squeeze`
    - `unknown`
- `squeeze_tier`
  - 第一版只允许：
    - `high`
    - `medium`
    - `low`
    - `off`
- `squeeze_fired`
  - 第一版只保留事件位 `0/1`
  - 不记录方向
- `compression_quality_score`
  - 第一版允许 `na`
  - 不离散成状态枚举

## 第一版验收

### 合同验收

- 产出列名与 `Batch9_P0_统一字段_CSV草案_v1.csv` 中 `N01` 的 `actual_landing_name_v1` 一致
- 不出现任何 `compression_state / vol_regime_code / breakout` 字段
- `atr_percentile` 若存在，必须保持 `0-100`

### 最小证据

- 至少留下一份字段样本输出
- 至少留下一份表头证据
- 至少留下一份字段缺口说明，明确：
  - 还没做 `compression_state`
  - 还没做 `vol_regime_code`
  - 还没做四项子评分

### 当前角色验收

- 只能宣称：
  - `N01 P0 diagnostic/state fields implemented`
- 不能宣称：
  - `完整 vol regime engine 已实现`
  - `compression state 已实现`
  - `breakout gate 已实现`

## 推荐落地产物

- 第一版最小产物建议：
  - `n01_p0_field_sample_v1.csv`
  - `n01_p0_field_header_v1.txt`
  - `n01_p0_contract_notes_v1.md`

## 风险与缺口

- `GainzAlgo` 源码页仍未拿到
- `AG Pro` 核心计算段源码仍未拿到
- `compression_quality_score` 目前还不是全量源码口径
- `squeeze_tier` 不同 TTM 变体实现差异仍存在

## 回滚方式

- 若第一版实现不稳，直接退回到：
  - 只保留 `atr_value / atr_percentile / atr_percentile_regime`
  - 暂不输出 `squeeze_fired / compression_quality_score`
- 若后续字段口径漂移：
  - 先冻结 `v1`
  - 再单独起 `v2`
  - 不覆盖 `v1`

## 当前结论

- `REOPEN_B9_N01_VOL_STATE_P0` 现在可以正式从：
  - `candidate`
  - 进入
  - `in_progress（最小实施草案已落地）`
- 下一步不是继续讨论要不要做，而是按这份草案去落第一版字段样本证据。
