# KD MTF P0 对象与职责卡 v1

## 用途

- 这张卡只负责收口 `DY-R1 / KD_MTF_P0` 在新目录里的非长文对象。
- 默认阅读顺序、停点和下一跳：
  - 以 `kd_mtf_p0_directory_index_card_v1.md` 为准

## 代码对象

- `..\..\02_runtime\dy_r1_kd_mtf_p0\kd_mtf_p0_runtime_append_stub_v1.py`
  - 当前唯一可执行代码对象
  - 只负责：
    - 读取 `proof_output_csv`
    - 校验 runtime 表头
    - 去掉重复 proof 主键
    - 把 proof 行写入 `kd_mtf_p0_fields_runtime_v1.csv`
  - 当前不负责：
    - 读取 broker 原始导出
    - 重建 `H1 -> 4h/day/week`
    - 直接从 bars 生成真实 runtime 字段

- `..\..\02_runtime\dy_r1_kd_mtf_p0\kd_mtf_p0_proof_builder_v1.py`
  - 当前 proof 生成器
  - 负责：
    - 读取本地 `n01_first_real_input_bars_v1.csv`
    - 按 `UTC` 分桶重建 `4h / day / week`
    - 按 `13,3,3 + sma + close_close` 生成 `proof_input / proof_output`
    - 默认只做对照，`--persist` 时才回写 proof 文件

## 合同对象

- `..\..\02_runtime\dy_r1_kd_mtf_p0\kd_mtf_p0_runtime_params_template_v1.json`
  - 当前参数与枚举合同源
  - 固定：
    - `kd_length = 13`
    - `kd_smooth_k = 3`
    - `kd_smooth_d = 3`
    - `ma_type = sma`
    - `price_field = close_close`
    - `week_extreme_low = 20`
    - `week_extreme_high = 80`
- `..\..\02_runtime\dy_r1_kd_mtf_p0\kd_mtf_p0_fields_runtime_header_v1.txt`
  - 当前 runtime 表头合同
  - 当前角色：
    - append 前的硬校验锚点

## proof 对象

- `..\..\02_runtime\dy_r1_kd_mtf_p0\real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - 当前真实 proof 输入样本
  - 当前内容：
    - `7` 行真实 `EURUSD H1` 样本
    - 已覆盖 `a / s / conflict`
    - 仍未覆盖 `b`
- `..\..\02_runtime\dy_r1_kd_mtf_p0\real_input_samples\kd_mtf_p0_proof_output_v1.csv`
  - 当前真实 proof 输出样本
  - 当前内容：
    - `7` 行真实输出
    - 已覆盖 `a / s / conflict`
    - 仍未覆盖 `b`

## runtime 对象

- `..\..\02_runtime\dy_r1_kd_mtf_p0\kd_mtf_p0_fields_runtime_v1.csv`
  - 当前 runtime 落盘文件
  - 当前内容：
    - `12` 行
    - 由历史 `5` 行手工 persist 样本加最新真实 `7` 行 proof 组成
  - 当前不要误读成：
    - broker 原始链路已经完整接入

## 当前对象状态总览

- 当前主线对象：
  - `params`
  - `header`
  - `proof_input`
  - `proof_output`
  - `runtime csv`
- 当前末端工具对象：
  - `append stub`
- 当前 proof 生成对象：
  - `proof builder`
- 当前仍未闭环对象：
  - 真实 `b` 样本

## 当前对象停点

- 当前对象层真正停在：
  - `proof_input_v1.csv`
  - `proof_output_v1.csv`
  - `runtime csv`
  - `b` 的阻塞说明
- 当前对象层不要停在：
  - 旧仓库中的同名目录
  - 因为活跃维护位置已经转向 `trading_assistant`
