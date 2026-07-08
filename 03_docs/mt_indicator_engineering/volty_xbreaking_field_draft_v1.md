# Volty XBreaking Field Draft v1

## 目的

- 这份文件把 `Volty / XBreaking` 从“已归档的 MT 指标家族”继续推进到“可工程化字段草案 v0”。
- 当前只定义字段、角色和约束，不把它们直接接进默认交易门控。

## 证据基础

- 来源目录：
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\`
- 当前可直接使用的证据：
  - `VoltyChannel_Stop_v2_1M.mq4`
  - `MT4IndicatorProbe.mq4`
  - `XBreakingProbe.mq5`
  - `XBreaking.ex4`
  - `XBreaking.ex5`
- 当前边界：
  - `Volty` 有源码，可先做公式骨架和字段草案
  - `XBreaking` 当前只有 probe 和二进制本体，先做 probe 级字段草案
  - `Volty` 当前已补齐 `EURUSD/H1` fresh-run `DumpSeries` 证据，`series_row_count = 350`
  - `XBreaking` 当前已补齐 `EURUSD/H1` fresh-run `csv + tester report + tester log`

## Volty 家族

### 指标类型

- `MT4 / mq4 源码可读`

### 公式骨架

- 输入参数（源码）：
  - `MA_Price / MA_Length / MA_Mode / ATR_Length / Kv / MoneyRisk`
  - `usePrice_HiLoBreak`（默认 true）
  - `useMA_HiLoEnvelope`（默认 false）
- 基础价格（每根 bar 的 shift）：
  - 若 `useMA_HiLoEnvelope=true`：
    - `bprice = iMA(..., applied_price=2 /*High*/, shift)`
    - `sprice = iMA(..., applied_price=3 /*Low*/, shift)`
  - 否则：
    - `bprice = iMA(..., applied_price=MA_Price, shift)`
    - `sprice = iMA(..., applied_price=MA_Price, shift)`
- 通道边界（每根 bar 的 shift）：
  - `smax[shift] = bprice + Kv * iATR(..., ATR_Length, shift)`
  - `smin[shift] = sprice - Kv * iATR(..., ATR_Length, shift)`
- 趋势状态（每根 bar 的 shift，先继承上一根）：
  - `trend[shift] = trend[shift+1]`
  - 若 `usePrice_HiLoBreak=true`：
    - `High[shift] > smax[shift+1] -> trend=1`
    - `Low[shift]  < smin[shift+1] -> trend=-1`
  - 否则：
    - `bprice > smax[shift+1] -> trend=1`
    - `sprice < smin[shift+1] -> trend=-1`
- 上行分支（`trend>0`）：
  - `smin` 的单调约束：若 `smin[shift] < smin[shift+1]` 则置为 `smin[shift+1]`
  - `UpBuffer[shift] = smin[shift] - (MoneyRisk - 1) * iATR(..., ATR_Length, shift)`
  - `UpBuffer` 的单调约束：若 `UpBuffer[shift] < UpBuffer[shift+1] && UpBuffer[shift+1] != EMPTY_VALUE` 则置为 `UpBuffer[shift+1]`
  - 翻转信号：若 `trend[shift+1] != trend[shift]`，则 `UpSignal[shift] = UpBuffer[shift]`，否则 `EMPTY_VALUE`
- 下行分支（`trend<0`）：
  - `smax` 的单调约束：若 `smax[shift] > smax[shift+1]` 则置为 `smax[shift+1]`
  - `DnBuffer[shift] = smax[shift] + (MoneyRisk - 1) * iATR(..., ATR_Length, shift)`
  - `DnBuffer` 的单调约束：若 `DnBuffer[shift] > DnBuffer[shift+1]` 则置为 `DnBuffer[shift+1]`
  - 翻转信号：若 `trend[shift+1] != trend[shift]`，则 `DnSignal[shift] = DnBuffer[shift]`，否则 `EMPTY_VALUE`

### 字段草案 v0

- 连续值字段：
  - `volty_base_ma`
  - `volty_atr`
  - `volty_upper_band_raw`
  - `volty_lower_band_raw`
  - `volty_up_stop`
  - `volty_dn_stop`
  - `volty_stop_distance_atr`
- 离散值字段：
  - `volty_trend_state`
    - 值域：`up / down / unknown`
  - `volty_flip_signal`
    - 值域：`flip_up / flip_down / none`
  - `volty_break_basis`
    - 值域：`price_hilo_break / ma_envelope_break`
- 分桶候选字段：
  - `volty_stop_distance_atr_bucket`
    - 值域建议：`tight / medium / wide`
  - `volty_kv_bucket`
    - 值域建议：`kv_lt_2 / kv_2_to_4 / kv_gt_4`
  - `volty_moneyrisk_bucket`
    - 值域建议：`mr_eq_1 / mr_1_to_2 / mr_gt_2`

### Probe mode -> 字段映射（MT4 iCustom mode）

- 证据来源：
  - `VoltyChannel_Stop_v2_1M.mq4` 的 `SetIndexBuffer` 顺序
  - `MT4Probe_Volty` 的输出 `mode`（按 index 读取）
- 映射表：
  - `mode 0` -> `UpBuffer` -> `volty_up_stop`
  - `mode 1` -> `DnBuffer` -> `volty_dn_stop`
  - `mode 2` -> `UpSignal` -> `volty_flip_signal=flip_up`（当值非空且非 0）
  - `mode 3` -> `DnSignal` -> `volty_flip_signal=flip_down`（当值非空且非 0）
  - `mode 4` -> `smin` -> `volty_lower_band_raw`
  - `mode 5` -> `smax` -> `volty_upper_band_raw`
  - `mode 6` -> `trend` -> `volty_trend_state`（`>0 -> up`，`<0 -> down`）
  - `mode 7` -> `unknown_suspect_all_zero`
- 衍生连续字段建议：
  - `volty_stop_distance_atr = abs(volty_up_stop - close) / volty_atr`（up trend）
  - `volty_stop_distance_atr = abs(volty_dn_stop - close) / volty_atr`（down trend）
  - `volty_base_ma / volty_atr` 需在字段化时从同参数组的 `iMA / iATR` 同步计算或从外部补齐

### 当前角色

- `RISK / EXIT / DIAG`

### 约束条件

- 必须基于 bar close 确认，不使用未收盘浮动值做硬结论。
- 同一参数组下，`MA_Length / ATR_Length / Kv / MoneyRisk` 必须落盘。
- 在没有跨品种、跨窗口证据前，不把 `volty_flip_signal` 直接升级成 `ENTRY_FILTER`。
- probe mode 映射边界：
  - `mode 0..6` 可按 `SetIndexBuffer` 映射（Up/Dn/Signals/smin/smax/trend）
  - `mode 7` 若持续全 0，先视为 `unknown_suspect_all_zero`，不进入字段化

## XBreaking 家族

### 指标类型

- `MT4/MT5 二进制本体 + probe 可用`

### 当前可确认事实

- `MT5 probe` 已定义：
  - `handle`
  - `init_err`
  - `buffer copied`
  - `non_empty`
  - `first_valid`
  - `last_valid`
- 当前已观测到的 buffer 访问形态（首轮）：
  - `buffer_0` 可读：`copied=200|non_empty=200|first_valid=0|last_valid=0`
  - `buffer_1..7` 不可读：`copied=-1|err=4806`
- 当前第二轮 fresh-run 仍重复得到：
  - `handle=10`
  - `init_err=0`
  - `buffer_0 copied=200|non_empty=200|last_valid=0`
  - `buffer_1..7 copied=-1|err=4806`
- 当前第三轮 validation-matrix（`EURUSD / H4 / IndicatorTf=H4`）仍重复得到：
  - `chart_tf=PERIOD_H4`
  - `indicator_tf=PERIOD_H4`
  - `handle=10`
  - `init_err=0`
  - `buffer_0 copied=200|non_empty=200|last_valid=0`
  - `buffer_1..7 copied=-1|err=4806`
- 当前第四轮 validation-matrix（`GBPUSD / H4 / IndicatorTf=H4`）仍重复得到：
  - `chart_tf=PERIOD_H4`
  - `indicator_tf=PERIOD_H4`
  - `handle=10`
  - `init_err=0`
  - `buffer_0 copied=200|non_empty=200|last_valid=0`
  - `buffer_1..7 copied=-1|err=4806`
- 当前第五轮 validation-matrix（`USDJPY / H4 / IndicatorTf=H4`）仍重复得到：
  - `chart_tf=PERIOD_H4`
  - `indicator_tf=PERIOD_H4`
  - `handle=10`
  - `init_err=0`
  - `buffer_0 copied=200|non_empty=200|last_valid=0`
  - `buffer_1..7 copied=-1|err=4806`
- 当前第六轮 validation-matrix（`USDJPY / H1 / IndicatorTf=H1`）仍重复得到：
  - `chart_tf=PERIOD_H1`
  - `indicator_tf=PERIOD_H1`
  - `handle=10`
  - `init_err=0`
  - `buffer_0 copied=200|non_empty=200|last_valid=0`
  - `buffer_1..7 copied=-1|err=4806`
- 当前第七轮 validation-matrix（`XAUUSD / H4 / IndicatorTf=H4`）仍重复得到：
  - `chart_tf=PERIOD_H4`
  - `indicator_tf=PERIOD_H4`
  - `handle=10`
  - `init_err=0`
  - `buffer_0 copied=200|non_empty=200|last_valid=0`
  - `buffer_1..7 copied=-1|err=4806`
- 当前第八轮 validation-matrix（`US30 / H4 / IndicatorTf=H4`）仍重复得到：
  - `chart_tf=PERIOD_H4`
  - `indicator_tf=PERIOD_H4`
  - `handle=10`
  - `init_err=0`
  - `buffer_0 copied=200|non_empty=200|last_valid=0`
  - `buffer_1..7 copied=-1|err=4806`
- 当前第九至第十二轮 validation-matrix（`EURUSD / H4` 与 `XAUUSD / H4`，窗口分别为 `2025.01.03~2025.01.10`、`2025.01.07~2025.01.14`）仍重复得到：
  - `chart_tf=PERIOD_H4`
  - `indicator_tf=PERIOD_H4`
  - `handle=10`
  - `init_err=0`
  - `buffer_0 copied=200|non_empty=200|last_valid=0`
  - `buffer_1..7 copied=-1|err=4806`
- 当前已补充强相关运行佐证：
  - `tester report = xbreaking_probe_portable.htm`
  - `tester log = 20260701_20260701T041405.log`
- 当前不能确认：
  - 每个 buffer 的交易语义
  - 最终突破判定公式
  - 是否存在重绘或确认时点后移

### 字段草案 v0

- 连续值字段：
  - `xbreaking_buffer_0_last_valid`
  - `xbreaking_buffer_1_last_valid`
  - `xbreaking_buffer_2_last_valid`
  - `xbreaking_buffer_3_last_valid`
- 离散值字段：
  - `xbreaking_probe_status`
    - 值域：`handle_ok / invalid_handle / partial_buffers / no_signal`
  - `xbreaking_buffer_activity_profile`
    - 值域：`single_buffer / multi_buffer / sparse / empty`
  - `xbreaking_platform_type`
    - 值域：`mt4 / mt5`
- 分桶候选字段：
  - `xbreaking_non_empty_count_bucket`
    - 值域建议：`0 / 1_to_5 / 6_to_20 / gt_20`
  - `xbreaking_init_err_bucket`
    - 值域建议：`ok / recoverable / fatal`

### 当前角色

- `NEED_PROBE / DIAG`

### 约束条件

- 当前不把任何 `XBreaking buffer` 直接解释成买卖信号。
- 在未拿到源码、公式说明或稳定 buffer 语义前，只允许保留 probe 级字段。
- 允许后续通过仓库外、合规、可审计途径取得源码或说明，再回补正式字段语义。

## 当前裁决

- `Volty`
  - 已达到“字段草案 + series 级证据闭环”的程度
  - `mode 0..6` 当前已拿到 `H1 DumpSeries` 行级证据，可继续升级 `field_ready_v1`
- `XBreaking`
  - 已达到“probe + report + journal 证据闭环”的程度
  - 已额外通过 `EURUSD / H4` 与 `GBPUSD / H4` validation-matrix 复核 `buffer0_only`
  - 已额外通过 `USDJPY / H4` validation-matrix 复核 `buffer0_only`
  - 已额外通过 `USDJPY / H1` validation-matrix 复核 `buffer0_only`
  - 已额外通过 `XAUUSD / H4` 与 `US30 / H4` validation-matrix 复核 `buffer0_only`
  - 已额外通过两组日期窗口（`2025.01.03~2025.01.10`、`2025.01.07~2025.01.14`）复核 `buffer0_only`
  - 当前这些验证仍集中在单一 `MT5` 环境：`ICMarketsSC-Demo__52886989`
- 当前 rerun 入口已支持 `DataRootOverride`，为第二环境接入预留了显式 data root 选择能力
- 当前 rerun / matrix 入口已支持 `EnvironmentInventoryJson + EnvironmentSelector`，可直接按 `environment_label / data_root_hash / server / login` 从环境快照选择目标 `MT5` 环境
  - 仍保留为 `probe-first` 家族
  - 下一步更适合做 `buffer 语义验证`，不是继续补 report，也不是直接接策略

## 下一步建议

1. 用 `Volty` 最新 `H1 DumpSeries` 行级证据复核 `mode 0..6 -> field` 映射
2. 用 `XBreaking` 已补齐的 `EURUSD/H1 + EURUSD/H4 + GBPUSD/H4 + USDJPY/H4 + USDJPY/H1 + XAUUSD/H4 + US30/H4 + 两组日期窗口样本` 结果继续复核 `buffer0_only` 是否稳定
3. 下一轮优先改 broker/demo 环境或补更远日期段，再判断 `buffer0_only` 是否可升为更稳定的平台特征
4. 若未来通过外部途径拿到 `XBreaking` 源码或公式说明，再升级 `XBreaking` 字段草案到 v1
