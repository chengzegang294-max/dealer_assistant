# kd_mtf_p0_runtime_notes_v1

## 角色

- 这份文件属于 `trading_assistant` 下的 `DY-R1 / KD_MTF_P0` 运行时层。
- 作用是记录当前运行时真实状态。

## 当前状态

- 当前运行时目录：
  - `02_runtime\dy_r1_kd_mtf_p0`
- 当前已具备：
  - `kd_mtf_p0_runtime_append_stub_v1.py`
  - `kd_mtf_p0_proof_builder_v1.py`
  - `kd_mtf_p0_runtime_params_template_v1.json`
  - `kd_mtf_p0_fields_runtime_header_v1.txt`
  - `kd_mtf_p0_fields_runtime_v1.csv`
  - `real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - `real_input_samples\kd_mtf_p0_proof_output_v1.csv`
  - `upstream_samples\n01_first_real_input_bars_v1.csv`
- 当前 proof 样本状态：
  - `8` 行真实 `EURUSD H1` proof 已在本运行时层落地
  - 当前真实覆盖：
    - `a(up) / a(down) / s(up) / s(down) / conflict / b(down)`
  - 当前首条真实 `b`：
    - `EURUSD H1 2026-03-27T16:00:00Z`
- append 当前状态：
  - 最新真实 `8` 行 proof 已在当前运行时层完成一次 `--persist`
  - 当前 runtime csv 行数：
    - `13`
  - 当前 `13` 行由：
    - 历史 `5` 行手工 persist 样本
    - 最新真实 `8` 行 proof
    - 共同组成
- proof builder 当前状态：
  - 已可从本地 `n01_first_real_input_bars_v1.csv` 重建当前 `8` 行 `proof_input / proof_output`
  - 当前冻结参数：
    - `h4_confirm_tie_epsilon = 0.01`
  - `dry-run` 对照结果：
    - `proof_input_matches_existing = true`
    - `proof_output_matches_existing = true`
  - 已支持：
    - `--target-bar-time`
    - 可按显式目标 `bar_time` 列表生成新的 proof 行
    - `--scan-b` / `--extend-proof-with-first-b`

## 当前可宣称

- 已完成运行时层的最小迁入
- 已完成本运行时层一次可复现 `--persist`
- 已完成 proof 到 runtime 的最小独立闭环
- 已完成本地 `H1 bars -> proof_input / proof_output` 的最小可复现脚本化

## 当前不可宣称

- 不可宣称已接入 broker 原始链路重建的真实 runtime 数据

## 当前额外备注

- 第一份完整 canonical H1 bars 大样本已正式导入本运行时层。
- 当前 append 独立性继续成立，因为 `append stub` 只读取本地 `proof_output_v1.csv`。
- 后续可以直接在新目录里继续 proof 重建，不再依赖旧仓库中的同名上游样本文件。
