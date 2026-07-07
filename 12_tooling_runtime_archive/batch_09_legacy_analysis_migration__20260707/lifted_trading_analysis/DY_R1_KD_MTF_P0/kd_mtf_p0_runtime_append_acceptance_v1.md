# kd_mtf_p0_runtime_append_acceptance_v1

## 目的

- 记录 `多周期KD P0` 首批 `params template + append stub` 的 `dry-run + persist` 验收结论。
- 把“手工 proof 已存在”推进到“runtime csv 已有首批 persist proof 行”。

## 本次验收对象

- params 模板：
  - `kd_mtf_p0_runtime_params_template_v1.json`
- append stub：
  - `kd_mtf_p0_runtime_append_stub_v1.py`
- proof 输出：
  - `real_input_samples\kd_mtf_p0_proof_output_v1.csv`
- runtime csv：
  - `kd_mtf_p0_fields_runtime_v1.csv`

## 执行命令

- 仅作为历史复核样例；当前不要把下面命令当作默认续跑入口。

```bash
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\DY_R1_KD_MTF_P0\kd_mtf_p0_runtime_append_stub_v1.py
python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\DY_R1_KD_MTF_P0\kd_mtf_p0_runtime_append_stub_v1.py --persist
```

## dry-run 结果

- 已成功读取：
  - `kd_mtf_p0_runtime_params_template_v1.json`
  - `real_input_samples\kd_mtf_p0_proof_output_v1.csv`
- 已成功校验：
  - `kd_mtf_p0_fields_runtime_v1.csv` 表头与 `v1` 合同一致
- 已成功完成 dry-run 内存追加：
  - `rows_before_cleanup = 1`
  - `proof_rows_loaded = 3`
  - `rows_before_append = 0`
  - `rows_after_append = 3`
- 已确认：
  - 第一条 proof 行可被 stub 正常读取
  - `placeholder` 行在内存态会被清除
  - 默认 `dry_run_only = true`

## persist 结果

- 已成功执行：
  - `--persist`
- 已成功写回：
  - `kd_mtf_p0_fields_runtime_v1.csv`
- 已确认当前 runtime csv 为：
  - `EURUSD H1 2026-06-18T08:00:00Z`
  - `XAUUSD H1 2026-06-18T12:00:00Z`
  - `BTCUSD H1 2026-06-18T16:00:00Z`
- 已确认：
  - `__PLACEHOLDER__` 不再保留
  - 当前 runtime 行数 = `3`

## 历史第二批 proof dry-run 结果

- 已新增第二批 proof：
  - `GBPUSD H1 2026-06-19T04:00:00Z`
  - `USDJPY H1 2026-06-19T08:00:00Z`
- 第二批补样目标：
  - 补齐 `down + short_preferred` 的 `s` tier
  - 补一条 `a` tier（当前先写成 `week = unknown` 且 `day + 4h` 同向）
- 已再次执行 dry-run：
  - `python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\DY_R1_KD_MTF_P0\kd_mtf_p0_runtime_append_stub_v1.py`
- dry-run 输出：
  - `rows_before_cleanup = 3`
  - `proof_rows_loaded = 5`
  - `rows_before_append = 0`
  - `rows_after_append = 5`
- 当前确认：
  - 第二批样本已进入 `proof_input_v1.csv / proof_output_v1.csv`
  - append stub 能正常读取 `5` 行 proof
  - 该轮 dry-run 后已继续执行第二次 `--persist`

## 历史第二批 proof persist 结果

- 已执行：
  - `python .\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\DY_R1_KD_MTF_P0\kd_mtf_p0_runtime_append_stub_v1.py --persist`
- persist 输出：
  - `rows_before_cleanup = 3`
  - `proof_rows_loaded = 5`
  - `rows_before_append = 0`
  - `rows_after_append = 5`
- 已确认当前 runtime csv 为：
  - `EURUSD H1 2026-06-18T08:00:00Z`
  - `XAUUSD H1 2026-06-18T12:00:00Z`
  - `BTCUSD H1 2026-06-18T16:00:00Z`
  - `GBPUSD H1 2026-06-19T04:00:00Z`
  - `USDJPY H1 2026-06-19T08:00:00Z`
- 已确认：
  - 当前 runtime 行数 = `5`
  - 第二批 proof 已正式写回 runtime csv

## 当前与最新真实 proof 的关系

- 以上验收结论只对应：
  - 早先那批手工 proof 样本
  - 当时写回 `kd_mtf_p0_fields_runtime_v1.csv` 的 `5` 行历史 persist 结果
- 当前 `real_input_samples\kd_mtf_p0_proof_input_v1.csv / kd_mtf_p0_proof_output_v1.csv` 已替换为真实 `EURUSD H1` 驱动的 `7` 行 proof：
  - 新增 `a(down)`：`2025-01-29T00:00:00Z`
  - 新增 `a(up)`：`2025-02-13T04:00:00Z`
  - 保留 `s(up) / s(down) / conflict`
- 当前已重新执行：
  - 按这批最新真实 `7` 行 proof 的 dry-run
- 最新 dry-run 输出：
  - `stub_mode = dry_run`
  - `rows_before_cleanup = 5`
  - `proof_rows_loaded = 7`
  - `rows_before_append = 5`
  - `rows_after_append = 12`
  - `dry_run_only = true`
- 当前尚未执行：
  - 按这批最新真实 `7` 行 proof 重新 `--persist`
- 因此当前不能把本文件读成：
  - “最新真实 proof 已 append 完成”
  - “最新 runtime csv 已对应这批真实 `EURUSD H1` proof”

## 当前可接受结论

- `多周期KD` 已具备：
  - `params template`
  - `append stub`
  - `proof -> runtime` 的最小 dry-run 验证
  - `proof -> runtime` 的首批 persist 验证
  - 第二批 proof 的补样与 dry-run 复核
  - 第二批 proof 的 persist 验证
- 当前还不能宣称：
  - 已接入 broker 原始链路重建的真实 runtime 行
  - `week/day/4h` 重建逻辑已经过真实数据链路验证
  - 最新真实 `7` 行 proof 已正式写回 runtime csv

## 下一步

- 若继续推进同一条线，最顺动作是：
  - 先把这次最新真实 `7` 行 proof 的 dry-run 结果同步回长期文档
  - 再决定是否允许针对最新真实 proof 重新 `--persist`
