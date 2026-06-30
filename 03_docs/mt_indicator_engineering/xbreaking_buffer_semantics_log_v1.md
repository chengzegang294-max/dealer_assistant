# XBreaking Buffer Semantics Log v1

## 目的

- 这份文件用于持续记录 `XBreaking` 各 buffer 的语义假设、probe 结果和验证结论。
- 当前先做语义日志，不把 `XBreaking` 直接接成交易信号。

## 当前家族对象

- 家族：`XBREAKING`
- 主要文件：
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreaking.ex4`
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreaking.ex5`
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreakingProbe.mq5`
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreakingProbe.ex5`
  - `12_tooling_runtime_archive\batch_02_mt_indicator_family\XBreakingProbe.ini`

## 当前已知 probe 字段

- `handle`
- `init_err`
- `buffer`
- `copied`
- `err`
- `non_empty`
- `first_valid`
- `last_valid`

## 语义日志模板

- 批次信息：
  - `date_tag`
  - `platform`
  - `symbol`
  - `indicator_tf`
  - `bars_to_probe`
- buffer 观察：
  - `buffer_id`
  - `copied`
  - `non_empty`
  - `first_valid`
  - `last_valid`
  - `suspected_role`
  - `confidence`
- 语义裁决：
  - `unknown`
  - `candidate_level`
  - `candidate_direction`
  - `candidate_state`
  - `rejected_guess`

## 当前允许的语义状态

- 当前只允许写：
  - `unknown`
  - `candidate`
  - `rejected`
- 当前不允许直接写：
  - `buy_signal`
  - `sell_signal`
  - `hard_gate_ready`

## 当前 future 路径

- 如果后续通过仓库外、合规、可审计途径拿到：
  - 源码
  - 公式说明
  - 厂商文档
- 可以回补：
  - buffer 语义
  - 公式骨架
  - 正式字段定义

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

- 当前 `XBreaking` 仍停在 `probe-first / semantics log first` 阶段。
- 但新仓库已经补好首批 runtime batch 路径和产物索引模板。

## 第一轮实际记录

- 批次信息：
  - `date_tag`: `20260626`
  - `platform`: `MT5`
  - `symbol`: `EURUSD`
  - `indicator_tf`: `PERIOD_H1`
  - `bars_to_probe`: `200`
  - `csv`: `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\csv\XBreaking_probe_EURUSD_H1_20250101_220500.csv`
- probe 总结：
  - `handle`: `10`
  - `init_err`: `0`
  - `status`: `DONE`
  - 解释：指标句柄成功建立，说明 `iCustom` 初始化链路可用。

## 第一轮 buffer 观察

- `buffer_id=0`
  - `copied`: `200`
  - `non_empty`: `200`
  - `first_valid`: `0.00000000`
  - `last_valid`: `0.00000000`
  - `suspected_role`: `candidate_state_or_placeholder`
  - `confidence`: `low`
  - `semantics_status`: `candidate`
  - 说明：当前只能确认 `buffer 0` 可稳定复制；但全窗口值均为 `0`，还不能把它解释成方向、价位或离散信号。
- `buffer_id=1..7`
  - `copied`: `-1`
  - `err`: `4806`
  - `non_empty`: `0`
  - `suspected_role`: `not_exposed_or_invalid_buffer_index`
  - `confidence`: `medium`
  - `semantics_status`: `rejected`
  - 说明：本轮更像是 probe 读取到了不存在或未暴露的 buffer，而不是“这些 buffer 只是暂时没信号”。

## 第一轮语义裁决

- 当前可确认：
  - `handle_ok`
  - `single_buffer_access_pattern`
  - `buffer_0_readable`
- 当前不能确认：
  - `buffer_0 = buy_signal`
  - `buffer_0 = sell_signal`
  - `buffer_0 = breakout_level`
  - `buffer_0 = hard_gate_ready`
- 当前记录的 `buffer_activity_profile` 可暂记为：
  - `single_buffer`

## 日志补证状态

- 已回收：
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\log\20260609.log`
  - `02_runtime\mt_indicator_probes\batch_01_volty_xbreaking\artifacts\xbreaking\log\20260609__excerpt.txt`
- 当前判断：
  - 当前 `20260609.log` 片段更像通用迁移日志，未检出 `XBreaking / XBreakingProbe / tester` 关键词，因此不能作为强相关 `XBreakingProbe tester journal` 的硬证据
  - `csv` 仍是主证据；在补齐 `tester report / tester journal` 前不升级任何 buffer 语义

## 下一步

1. 继续补 `XBreaking` 的 `log / tester_report`
2. 在不同 `symbol / timeframe` 下复核 `buffer 0` 是否仍全为 `0`
3. 若后续仍只暴露 `buffer 0`，可把 `single_buffer` 写进字段草案复核
4. 只在多轮验证稳定后，才升级 `XBreaking` 字段草案版本
