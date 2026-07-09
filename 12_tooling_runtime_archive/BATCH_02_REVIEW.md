# Tooling Runtime 归档批次 02 审查

## 批次结论

- 本批已完成 `12_tooling_runtime_archive` 第二批迁入。
- 当前已迁入新仓库的是一组 `MT 指标家族最小工程集`，位置：
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\`
- 这批材料覆盖了：
  - 通用 probe
  - Volty 通道止损
  - XBreaking 突破探针
  - Harmony 谐波
  - ZigZag / ZUP 家族

## 本批迁入文件

- probe 层
  - `MT4IndicatorProbe.ex4`
  - `MT4IndicatorProbe.mq4`
  - `MT4Probe_Volty.ex4`
  - `MT4Probe_Volty.mq4`
  - `MT4Probe_XBreaking.ini`
  - `mt4probe_volty_portable.ini`
- Volty 家族
  - `VoltyChannel_Stop_v2_1M.ex4`
  - `VoltyChannel_Stop_v2_1M.mq4`
- XBreaking 家族
  - `XBreaking.ex4`
  - `XBreaking.ex5`
  - `XBreakingProbe.ex5`
  - `XBreakingProbe.ini`
  - `XBreakingProbe.mq5`
- binary-only 占位
  - `交易盈亏统计.ex4`
- Harmony / ZigZag 家族
  - `0_Harmony_06.ex4`
  - `0_Harmony_06.mq4`
  - `a_ZZ.ex4`
  - `a_ZZ.mq4`
  - `ZUP_v15[1][1].1.ex4`
  - `ZUP_v15[1][1].1.mq4`

## 为什么这批先进

- `MT4IndicatorProbe.mq4`
  - 给出 `mode / non_empty / err_count / first_valid / last_valid`
- `XBreakingProbe.mq5`
  - 给出 `handle / init_err / CopyBuffer` 级 probe 能力
- `VoltyChannel_Stop_v2_1M.mq4`
  - 源码可读，核心是 `MA + Kv * ATR` 的通道止损与翻转信号
- `0_Harmony_06.mq4`
  - 源码可读，体现谐波模式识别与比例校验
- `a_ZZ.mq4` 与 `ZUP_v15[1][1].1.mq4`
  - 源码可读，代表 ZigZag / Fibo / Gartley 家族
- `XBreaking.ex4 / ex5`
  - 二进制本体可作为 probe 对象，但不承诺反编译
- `交易盈亏统计.ex4`
  - 当前仅保留为 `binary_only archive placeholder`，不纳入本轮 probe 主线

## 家族映射裁决

- `PROBE_GENERIC`
  - 文件：`MT4IndicatorProbe.*`、`MT4Probe_Volty.*`、`XBreakingProbe.*`
  - 当前角色：`NEED_PROBE / DIAG`
  - 工程优先级：`P0`
- `VOLTY_STOP`
  - 文件：`VoltyChannel_Stop_v2_1M.*`
  - 家族本质：`ATR 通道止损 / 趋势翻转`
  - 当前角色：`RISK / EXIT / DIAG`
  - 工程优先级：`P1`
- `XBREAKING`
  - 文件：`XBreaking.ex4/ex5`
  - 家族本质：`突破类二进制指标`
  - 当前角色：`NEED_PROBE`
  - 工程优先级：`P1`
- `HARMONY_PATTERN`
  - 文件：`0_Harmony_06.*`
  - 家族本质：`谐波形态识别`
  - 当前角色：`SOURCE_LIBRARY / DIAG`
  - 工程优先级：`P2`
- `ZZ_GARTLEY_FIBO`
  - 文件：`a_ZZ.*`、`ZUP_v15[1][1].1.*`
  - 家族本质：`ZigZag + 比例结构 + Gartley/Fibo`
  - 当前角色：`SOURCE_LIBRARY / NEED_PROBE`
  - 工程优先级：`P2`
- `PNL_STATS_BINARY_ONLY`
  - 文件：`交易盈亏统计.ex4`
  - 家族本质：`binary_only utility indicator`
  - 当前角色：`ARCHIVE_ONLY / UNKNOWN_FORMULA`
  - 工程优先级：`P3`

## 风险与限制

- 不承诺反编译 `ex4/ex5`。
- 允许后续通过仓库外、合规、可审计的方式取得 `ex4/ex5` 对应源码、公式说明或厂商文档；若未来拿到，再回补到新仓库，但当前批次不把这件事写成“已具备源码”。
- 谐波 / ZigZag / ZUP 当前不能直接写成硬交易门控。
- 本批完成的是“家族锚点迁入”，不是“平台 probe 已全部跑完”。

## 验收校验

- 文件集合与 `sha256` 校验见：
  - `BATCH_02_ACCEPTANCE_CHECK.md`
- 当前结论：
  - `20/20` 旧源文件已在新仓对齐
  - `18` 个文件哈希一致
  - `2` 个 `ini` 存在受控差异，原因是主动去旧仓绝对路径依赖

## 下一步建议

1. 单开 `03_MT4便携探针实例` 批次
2. 或直接为 `Volty / XBreaking` 在新仓库写字段草案与 probe 结果入口
