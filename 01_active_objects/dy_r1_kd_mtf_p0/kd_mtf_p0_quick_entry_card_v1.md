# KD MTF P0 简明执行入口卡 v1

## 用途

- 这是一张给 `DY-R1 / KD_MTF_P0` 在新目录里直接续跑时使用的短入口卡。
- 目标不是重复长文，而是把最关键的口径、路径和下一步动作压成最短清单。

## 当前不变量

- 不改 `DY-R1` 逻辑
- 不碰策略门控
- 只在 `trading_assistant` 的新对象包里继续维护

## 当前运行时位置

- 运行时目录：
  - `..\..\02_runtime\dy_r1_kd_mtf_p0\`
- 上游主样本：
  - `..\..\02_runtime\dy_r1_kd_mtf_p0\upstream_samples\n01_first_real_input_bars_v1.csv`
- 当前 proof 样本：
  - `..\..\02_runtime\dy_r1_kd_mtf_p0\real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - `..\..\02_runtime\dy_r1_kd_mtf_p0\real_input_samples\kd_mtf_p0_proof_output_v1.csv`

## 当前覆盖

- 已补出：
  - `a(up)`
  - `a(down)`
  - `s(up)`
  - `s(down)`
  - `conflict`
- 当前仍缺：
  - `b`

## 当前执行状态

- append stub 已在新运行时层完成一次 `--persist`
- 当前 runtime csv 行数：
  - `12`
- 当前仍不能宣称：
  - 已接入 broker 原始链路重建脚本
  - 已补出第一条真实 `b`
  - broker 原始链路重建脚本已经在新目录实现

## 当前硬结论

- 当前主样本总扫描统计：
  - `s=3587 / a=1856 / b=0 / conflict=8318 / unknown=73438`
- 当前 `b` 长期为 `0` 的直接工程原因：
  - `h4_confirm = none` 只会落在 `h4_k == h4_d`
  - 当前已扫真实浮点样本里没有自然出现这种精确相等

## 下一跳

- 若继续扫样本：
  - 先看 `..\..\03_docs\dy_r1_kd_mtf_p0\kd_mtf_p0_b_blocker_note_v1.md`
- 若继续更新 proof：
  - 先看 `..\..\03_docs\dy_r1_kd_mtf_p0\kd_mtf_p0_real_input_mapping_draft_v1.md`
- 若准备继续碰 append：
  - 先看 `..\..\02_runtime\dy_r1_kd_mtf_p0\kd_mtf_p0_runtime_append_protocol_v1.md`
