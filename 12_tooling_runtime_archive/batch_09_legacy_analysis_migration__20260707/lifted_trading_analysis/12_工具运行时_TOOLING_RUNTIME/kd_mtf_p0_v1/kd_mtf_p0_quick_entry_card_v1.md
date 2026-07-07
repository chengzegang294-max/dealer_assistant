# KD MTF P0 历史入口卡镜像 v1

- ARCHIVE_ONLY_RUNTIME_MIRROR: 本文件只保留旧 `kd_mtf_p0_v1` 的历史短入口语义，不作为当前默认续跑入口。
- 当前 repo-first 入口先看：
  - `d:\Stock\trading_assistant\01_active_objects\`
  - `d:\Stock\trading_assistant\02_runtime\`
  - `d:\Stock\trading_assistant\04_active_main_docs\`

## 用途

- 这是一张旧 `DY-R1 / KD_MTF_P0` 运行时镜像的短入口卡。
- 目标是保留历史入口语义供追溯，不再把本文件当成当前最短续跑入口。

## 入口关系

- 默认阅读顺序与覆盖关系：
  - 先看 `kd_mtf_p0_directory_index_card_v1.md`
- 当前对象层职责：
  - 再看 `kd_mtf_p0_object_responsibility_card_v1.md`
- 本文件只负责：
  - 当前 proof 输入链的最短续跑口径

## 当前不变量

- 不改 `DY-R1` 逻辑。
- 不碰策略门控。
- 不做 runtime append。
- 只处理真实 proof 输入链、证据和文档收口。

## 当前上游输入

- 当前固定主样本：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_first_real_input_bars_v1.csv`
- 当前 proof 样本：
  - `real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - `real_input_samples\kd_mtf_p0_proof_output_v1.csv`

## 当前三层状态

- `week_k / week_d`
  - 已能按 `UTC week` 从同一份 `H1` canonical bars 稳定重建
  - 历史不足时自然落 `unknown`
- `day_k_prev / day_d_prev / day_k / day_d`
  - 已能稳定落出 `golden_cross / death_cross / none / unknown`
- `h4_k / h4_d`
  - 已能稳定落出 `confirm_up / confirm_down / unknown`
  - 当前真实样本还没自然落出 `none`

## 当前真实覆盖

- 已补出：
  - `a(up)`
  - `a(down)`
  - `s(up)`
  - `s(down)`
  - `conflict`
- 当前仍缺：
  - `b`

## 当前硬结论

- 当前主样本总扫描统计：
  - `s=3587 / a=1856 / b=0 / conflict=8318 / unknown=73438`
- 当前 `b` 长期为 `0` 的直接工程原因：
  - 现行 `h4_confirm = none` 只会落在 `h4_k == h4_d`
  - 当前已扫真实浮点样本里，没有自然出现这种精确相等
- 当前仓库内外扩搜状态：
  - 仓库内现有主样本池已扫尽
  - `d:\Stock` 范围内未发现新的更长 `M1/M15` 连续窗口

## 新样本到位后怎么续跑

- 第一步：
  - 确认新样本仍满足 `symbol,timeframe,bar_time,open,high,low,close`
- 第二步：
  - 若是 `M1/M15`，先上卷成 `H1`
- 第三步：
  - 固定 `UTC` 分桶重建 `4h/day/week`
- 第四步：
  - 固定 `13,3,3 + sma + close_close`
- 第五步：
  - 固定“只取目标 `bar_time` 之前最近的已闭合高周期”
- 第六步：
  - 先扫是否自然出现 `h4_k == h4_d`
- 第七步：
  - 只有自然出现 `h4_confirm = none` 后，才继续找第一条真实 `b`

## 当前不要做

- 不为了补 `b` 去改 `h4_confirm` 定义。
- 不为了补 `b` 去放宽 tier 规则。
- 不把 proof 更新误写成 append 已完成。

## 下一跳

- 若继续扫样本：
  - 先看 `kd_mtf_p0_b_blocker_note_v1.md`
- 若继续更新 proof：
  - 先看 `kd_mtf_p0_real_input_mapping_draft_v1.md`
- 若准备碰 append：
  - 先看 `kd_mtf_p0_runtime_append_protocol_v1.md`
