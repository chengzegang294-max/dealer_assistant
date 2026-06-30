# Volty Probe Result Intake v1

## 目的

- 这份文件用于收口 `Volty` 家族后续 probe 结果。
- 它不是字段草案的替代，而是字段草案之后的证据入口。

## 当前家族对象

- 家族：`VOLTY_STOP`
- 主要文件：
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\VoltyChannel_Stop_v2_1M.mq4`
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\VoltyChannel_Stop_v2_1M.ex4`
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\MT4Probe_Volty.mq4`
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\MT4Probe_Volty.ex4`
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\mt4probe_volty_portable.ini`

## 当前应收集的 probe 证据

- MT4 probe 输出至少要有：
  - `indicator_name`
  - `indicator_tf`
  - `mode`
  - `non_empty`
  - `err_count`
  - `first_valid`
  - `last_valid`
- 最好同时记录：
  - `Symbol`
  - `chart_tf`
  - `MaxModes`
  - `MaxShifts`
  - 使用的 `ini` 或参数快照

## 当前字段映射目标

- 如果 probe 正常，可优先对齐这些字段：
  - `volty_trend_state`
  - `volty_flip_signal`
  - `volty_up_stop`
  - `volty_dn_stop`
  - `volty_stop_distance_atr`
- 当前默认角色仍是：
  - `RISK / EXIT / DIAG`

## Intake 模板

- 证据批次：
  - `date_tag`
  - `platform`
  - `symbol`
  - `timeframe`
- 产物路径：
  - `csv`
  - `tester_report`
  - `log`
- probe 结论：
  - `mode_count`
  - `non_empty_modes`
  - `stable_modes`
  - `error_modes`
- 字段化裁决：
  - 哪些字段可升级到 `field_ready`
  - 哪些字段继续 `diag_only`

## 当前运行时落点

- 首批 probe 运行时批次：
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\`
- 本批执行卡：
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\BATCH_01_EXECUTION_CARD.md`
- 本批产物索引模板：
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\BATCH_01_ARTIFACT_INDEX_TEMPLATE.md`
- 首次实跑操作卡：
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\MT4_MT5_FIRST_RUN_PLAYBOOK.md`

## 当前状态

- 当前已经把一份历史 `Volty` probe 结果正式落回新仓库。
- 这份证据来自旧仓库已落盘产物回收，不是 `20260626` 在本机终端目录自动新扫出来的最新文件。
- `20260626` 已对本机 `MetaQuotes` 终端目录做过一次自动扫描：
  - `csv`: `not found`
  - 说明当前本机终端目录里还没有新的 `Volty csv`

## 第一份历史回收证据

- 证据批次：
  - `date_tag`: `20260626_backfill`
  - `platform`: `MT4`
  - `symbol`: `EURUSD`
  - `timeframe`: `H4`
  - `evidence_mode`: `historical_recovered`
- 产物路径：
  - `csv`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\volty\csv\MT4_probe_Volty_EURUSD_H4_20250102_000000.csv`
  - `tester_report`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\volty\tester_report\mt4probe_volty_portable.htm`
  - `log`: `pending`
- probe 结论：
  - `mode_count`: `8`
  - `non_empty_modes`: `1,4,5,6,7`
  - `stable_modes`: `1,4,5,6,7`
  - `error_modes`: `none`
  - `used_common`: `0`
  - `status_row`: `DONE`
- mode 摘要：
  - `mode 1`: `non_empty=50`, `first_valid=1.04579600`, `last_valid=1.04898000`
  - `mode 4`: `non_empty=50`, `first_valid=1.02399400`, `last_valid=1.02094000`
  - `mode 5`: `non_empty=50`, `first_valid=1.04579600`, `last_valid=1.04898000`
  - `mode 6`: `non_empty=50`, `first_valid=-1.00000000`, `last_valid=-1.00000000`
  - `mode 7`: `non_empty=50`, `first_valid=0.00000000`, `last_valid=0.00000000`
- `mode -> buffer` 参考映射（来自 `VoltyChannel_Stop_v2_1M.mq4` 的 `SetIndexBuffer` 顺序）：
  - `mode 0` -> `UpBuffer`（UpTrend）
  - `mode 1` -> `DnBuffer`（DnTrend）
  - `mode 2` -> `UpSignal`
  - `mode 3` -> `DnSignal`
  - `mode 4` -> `smin`（内部 stop 基线之一）
  - `mode 5` -> `smax`（内部 stop 基线之一）
  - `mode 6` -> `trend`（1 / -1）
  - `mode 7` -> `unknown_suspect_all_zero`（源码未设置 index=7，且全 0，先不当作有效 buffer）
- 字段化裁决：
  - `volty_up_stop / volty_dn_stop`：`field_ready_candidate`
  - `volty_trend_state`：`field_ready_candidate`
  - `volty_flip_signal`：`diag_only_until_mode_mapping_is_confirmed`
  - `volty_stop_distance_atr`：`needs_formula_side_rebuild_not_probe_only`
- 规范化输出（新仓库内脚本）：
  - `python 02_runtime\\mt_indicator_probes\\batch_01_volty_xbreaking\\probe_artifact_ingest_v1.py --family volty --kind csv --normalize-volty-summary`
  - `volty_trend_state=down|volty_dn_stop_last=1.048980|volty_lower_band_last=1.020940|volty_upper_band_last=1.048980`

## 下一步

1. 继续补 `Volty` 的明确 `tester log / journal`
2. 若本机 MT4 终端后续再跑出新 `csv`，把它和这份历史证据做一次前后对照
3. 结合 `mode 1/4/5/6/7` 的稳定性，复核字段草案里的 `mode -> field` 映射
4. 再决定哪些 `Volty` 字段可以升级到 `field_ready_v1`
