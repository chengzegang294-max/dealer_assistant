# KD MTF P0 对象与职责卡 v1

## 用途

- 这张卡只负责收口 `kd_mtf_p0_v1` 目录里的非 md 对象。
- 目标是让后续接手的人知道每个代码/合同/产物对象当前在做什么、哪些是当前主线对象、哪些只是历史遗留对象。
- 默认阅读顺序、停点和下一跳：
  - 以 `kd_mtf_p0_directory_index_card_v1.md` 为准

## 对象分组

### A. 代码对象

- `kd_mtf_p0_runtime_append_stub_v1.py`
  - 当前唯一可执行代码对象
  - 只负责：
    - 读取 `proof_output_csv`
    - 校验 runtime 表头
    - 去 placeholder
    - 把 proof 行写入 `kd_mtf_p0_fields_runtime_v1.csv`
  - 当前不负责：
    - 读取 broker 原始导出
    - 重建 `H1 -> 4h/day/week`
    - 直接从 bars 生成真实 runtime 字段
  - 当前角色：
    - append 末端工具
    - 不是 proof 生成器
    - 不是 ingest 入口

### B. 合同对象

- `kd_mtf_p0_runtime_params_template_v1.json`
  - 当前参数与枚举合同源
  - 固定：
    - `kd_length = 13`
    - `kd_smooth_k = 3`
    - `kd_smooth_d = 3`
    - `ma_type = sma`
    - `price_field = close_close`
    - `week_extreme_low = 20`
    - `week_extreme_high = 80`
  - 还固定了：
    - 输出文件路径
    - proof 输入/输出路径
    - 数据枚举范围
    - 执行边界
  - 当前不要误读成：
    - 已绑定真实 broker 源
    - 已能独立跑完整真实链路

- `kd_mtf_p0_fields_runtime_header_v1.txt`
  - 当前 runtime 表头合同
  - 固定字段：
    - `symbol,timeframe,bar_time,kd_week_bias,kd_day_signal,kd_4h_confirm,kd_alignment_tier,kd_direction_filter,kd_week_extreme_zone`
  - 当前角色：
    - append 前的硬校验锚点

### C. 当前 proof 产物

- `real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - 当前真实 proof 输入样本
  - 作用：
    - 保存 `week/day/4h` 中间列
    - 给 `proof_output` 派生提供直接输入
  - 当前内容：
    - `7` 行真实 `EURUSD H1` 样本
    - 已覆盖 `a / s / conflict`
    - 仍未覆盖 `b`

- `real_input_samples\kd_mtf_p0_proof_output_v1.csv`
  - 当前真实 proof 输出样本
  - 作用：
    - 保存 `6` 个 `KD P0` 输出字段
    - 作为 append stub 的输入来源
  - 当前内容：
    - `7` 行真实输出
    - 已覆盖 `a / s / conflict`
    - 仍未覆盖 `b`

### D. runtime 产物

- `kd_mtf_p0_fields_runtime_v1.csv`
  - 当前 runtime 落盘文件
  - 当前内容：
    - `5` 行历史手工 proof persist 样本
  - 当前重要备注：
    - 文件里确实有一条历史 `b` 行
    - 但这条 `b` 不是当前真实 proof 链跑出来的结果
    - 它只属于早先的手工 proof persist 历史
  - 当前不要误读成：
    - 已对应最新真实 `proof_output_v1.csv`
    - 已对应当前真实 `EURUSD H1` proof

## 当前对象状态总览

- 当前主线对象：
  - `kd_mtf_p0_runtime_params_template_v1.json`
  - `kd_mtf_p0_fields_runtime_header_v1.txt`
  - `real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - `real_input_samples\kd_mtf_p0_proof_output_v1.csv`
- 当前末端工具对象：
  - `kd_mtf_p0_runtime_append_stub_v1.py`
- 当前历史遗留对象：
  - `kd_mtf_p0_fields_runtime_v1.csv`
    - 只可作为“旧 persist 历史”读取
    - 不可作为“当前真实链路状态”读取

## 当前对象停点

- 当前对象层真正停在：
  - `proof_input_v1.csv`
  - `proof_output_v1.csv`
  - 以及 `b` 的阻塞说明
- 当前对象层不要停在：
  - `kd_mtf_p0_fields_runtime_v1.csv`
  - 因为它还是历史手工 persist 结果
