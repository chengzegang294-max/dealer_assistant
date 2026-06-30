# kd_mtf_p0_runtime_gaps_v1

## 目的

- 记录 `DY-R1 / KD_MTF_P0` 在新运行时层当前还没做的内容。

## 当前缺口清单

### 1. 原始链路缺口

- 还没有把 `proof builder` 再扩成可接多样本批次的正式入口
- 还没有真实 `week/day/4h` 的单独审计记录

### 2. 样本覆盖缺口

- 当前真实样本已补出 `a / s / conflict / b`
- 首条真实 `b`：
  - `EURUSD H1 2026-03-27T16:00:00Z`
- 当前口径依赖：
  - `h4_confirm_tie_epsilon = 0.01`
- 当前主样本扫描统计（在上述 epsilon 下）：
  - `s=368 / a=216 / b=4 / conflict=1452 / unknown=6936`

### 3. 来源证据缺口

- `kd_week_extreme_zone` 仍使用 `20/80` 保守阈值
- `week/day/4h` 仍缺单独来源级更强证据

## 当前明确不补

- 当前不继续扩大 `h4_confirm_tie_epsilon` 的默认值
- 当前不补 `month / 1h / divergence` 扩展字段

## 当前结论

- 当前已到：
  - `runtime-ready`
  - `append-ready`
-  `proof-builder-ready`
- 当前仍不能写成：
  - `runtime-verified`
