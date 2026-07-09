# KD MTF P0 运行缺口 v1

## 目的

- 记录 `多周期KD P0` 当前运行时层面还没做的内容。
- 默认阅读顺序、覆盖关系、停点与下一跳：
  - 以 `kd_mtf_p0_directory_index_card_v1.md` 为准

## 当前缺口清单

### 1. 真实链路缺口

- 还没有 broker 原始输入到 `week/day/4h` 的 repo 内正式重建脚本。
- 还没有真实 runtime 参数落盘样例。
- 还没有真实 `week/day/4h` 周期重建审计记录。
- 当前 `kd_mtf_p0_fields_runtime_v1.csv` 虽已有 `5` 行历史 proof persist，但仍不是 broker 原始链路重建行。

### 2. proof 到 runtime 的衔接缺口

- 当前虽已真实生成：
  - `real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - `real_input_samples\kd_mtf_p0_proof_output_v1.csv`
- 但当前仍缺：
  - 把最新真实 `proof_output_v1.csv` 单独 append 到 runtime csv 的刷新记录
  - 一份 repo 内正式脚本化的 `H1 -> week/day/4h -> proof_input/proof_output` 实现

### 3. `b` 真实样本缺口

- 当前真实样本已补出 `a / s / conflict`，但仍未补出第一条真实 `b`。
- 当前主样本总扫描统计仍是：
  - `s=3587 / a=1856 / b=0 / conflict=8318 / unknown=73438`
- 当前直接阻塞仍是：
  - `h4_confirm = none` 在现行实现下只会落在 `h4_k == h4_d`
  - 当前已扫真实浮点样本中没有自然出现这种精确相等
- 当前若继续补 `b`，前提仍是：
  - 先拿到新的真实 `M1/M15` 长窗口
- 当前阻塞详见：
  - `kd_mtf_p0_b_blocker_note_v1.md`

### 4. 审计与来源证据缺口

- `kd_week_extreme_zone` 当前仍使用 `20/80` 保守阈值，仍缺来源级更强证据。
- `week/day/4h` 的最小审计证据仍未形成单独审计记录。

## 当前明确不补

- 当前不为了补 `b` 去修改 tier 规则。
- 当前不为了补 `b` 去修改 `h4_confirm` 定义。
- 当前不补 `month / 1h / divergence` 扩展字段。
- 当前不拆新的 `append_from_proof` 独立脚本。

## 当前结论

- `多周期KD` 当前已到：
  - `runtime-prep`
  - `proof-ready`
- 当前仍不能写成：
  - `runtime-verified`
