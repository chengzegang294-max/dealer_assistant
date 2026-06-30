# Probe Batch 01 Execution Card

## 目标

- 把 `Volty / XBreaking` 从“只有模板”推进到“有统一落盘口径的首批 probe 批次”。
- 当前批次只收集平台可用性与 buffer 观察证据，不改默认执行链路。

## 对象范围

- `Volty`
  - 平台：`MT4`
  - 入口：`MT4Probe_Volty.mq4`
  - 指标本体：`VoltyChannel_Stop_v2_1M.mq4/.ex4`
- `XBreaking`
  - 平台：`MT5`
  - 入口：`XBreakingProbe.mq5`
  - 指标本体：`XBreaking.ex4/.ex5`

## 源锚点

- 代码锚点：
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\MT4Probe_Volty.mq4`
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreakingProbe.mq5`
- 文档锚点：
  - `03_docs\mt_indicator_engineering\volty_probe_result_intake_v1.md`
  - `03_docs\mt_indicator_engineering\xbreaking_buffer_semantics_log_v1.md`

## 建议产物目录

- `artifacts\volty\csv`
- `artifacts\volty\log`
- `artifacts\volty\tester_report`
- `artifacts\xbreaking\csv`
- `artifacts\xbreaking\log`
- `artifacts\xbreaking\tester_report`
- 以上目录已在新仓库创建，可直接回收第一批实跑产物

## 首次实跑操作卡

- 参考：
  - `MT4_MT5_FIRST_RUN_PLAYBOOK.md`
- 辅助脚本：
  - `probe_artifact_ingest_v1.py`
- 当前口径：
  - 旧批次 `ini` 只作为字段与参数范围参考
  - 新仓库默认以本批目录为产物回收根

## 证据合同

- `Volty` 最少记录：
  - `symbol`
  - `chart_tf`
  - `indicator_tf`
  - `indicator_name`
  - `max_modes`
  - `max_shifts`
  - `used_common`
  - 每个 `mode` 的 `non_empty / err_count / first_valid / last_valid`
  - 规范化输出（新仓库内）：
    - `python probe_artifact_ingest_v1.py --family volty --kind csv --normalize-volty-summary`
  - series 输出（若开启 `DumpSeries`）：
    - `python probe_artifact_ingest_v1.py --family volty --kind csv --normalize-volty-series`
- `XBreaking` 最少记录：
  - `symbol`
  - `chart_tf`
  - `indicator_tf`
  - `indicator_name`
  - `bars_to_probe`
  - `max_buffers`
  - `handle`
  - `init_err`
  - 每个 `buffer` 的 `copied / err / non_empty / first_valid / last_valid`

## 文件命名口径

- `Volty CSV`
  - `MT4_probe_Volty_<SYMBOL>_<TF>_<STAMP>.csv`
- `XBreaking CSV`
  - `XBreaking_probe_<SYMBOL>_<TF>_<STAMP>.csv`
- `STAMP`
  - 使用平台脚本默认输出的时间戳，不手工改名

## 当前执行状态

- `Volty`
  - `status`: `historical_first_csv_recovered`
  - `note`: 已从旧仓库回收 `MT4_probe_Volty_EURUSD_H4_20250102_000000.csv` 与 `mt4probe_volty_portable.htm`，本机终端目录仍未发现新的 `csv`
- `XBreaking`
  - `status`: `first_csv_ingested`
  - `note`: 已回收 `XBreaking_probe_EURUSD_H1_20250101_220500.csv`，第一轮 semantics 已开始落盘

## 收口规则

- 第一批实际产物落盘后：
  1. 先更新本目录的产物索引
  2. 再回写 `03_docs\mt_indicator_engineering` 对应 intake 文档
  3. 最后决定哪些字段可从 `template_only` 升到 `field_ready`

## 禁止事项

- 不把 `Volty` probe 直接写成默认入场门控
- 不把 `XBreaking` 任一 buffer 未验证前直接标成买卖信号
- 不把 `ex4/ex5` 二进制存在，误写成“已拿到源码”
