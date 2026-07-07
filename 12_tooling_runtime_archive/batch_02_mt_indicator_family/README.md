# MT Indicator Family Batch 02

## 用途

- 这里放 `02_MT指标家族_源码与探针` 的最小工程家族集。

## 当前包含

- 通用 probe：
  - `MT4IndicatorProbe.*`
  - `MT4Probe_Volty.*`
  - `XBreakingProbe.*`
- 指标家族：
  - `VoltyChannel_Stop_v2_1M.*`
  - `XBreaking.ex4/ex5`
  - `交易盈亏统计.ex4`
  - `0_Harmony_06.*`
  - `a_ZZ.*`
  - `ZUP_v15[1][1].1.*`

## 当前裁决

- 这批文件用于保留 MT 指标工程化入口。
- 其中源码可读的家族优先用于公式/机制抽取。
- 二进制文件只作为 probe 对象，不承诺反编译。

## 配置口径

- `mt4probe_volty_portable.ini`
  - 采用终端内相对路径口径，可作为 `MT4` 便携探针参考模板。
- `XBreakingProbe.ini`
  - 已改为终端内相对 `Report=` 路径，不再默认依赖旧仓库 `backtest_out`。
- `MT4Probe_XBreaking.ini`
  - 已改为 `Probe\MT4IndicatorProbe` + 终端内相对 `TestReport=` 路径，不再默认依赖旧仓库绝对地址。
- `交易盈亏统计.ex4`
  - 当前仅作为 `binary_only archive placeholder` 保留，不接入本轮 probe 主线。
- 这些 `ini` 仍属于工程模板层：
  - 当前默认产物回收根仍是 `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\...`
  - tester 实跑后仍应通过 `probe_artifact_ingest_v1.py` 或手工复制回新仓库运行时批次
