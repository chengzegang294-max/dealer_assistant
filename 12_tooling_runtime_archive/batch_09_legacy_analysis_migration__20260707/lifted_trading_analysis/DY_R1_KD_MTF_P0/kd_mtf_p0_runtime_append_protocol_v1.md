# KD MTF P0 运行追加协议 v1

## 目的

- 规定未来脚本向 `kd_mtf_p0_fields_runtime_v1.csv` 追加第一批真实数据时应遵守的最小流程。
- 避免把占位样本行、真实 proof 行和未来版本升级混在一起。

## 当前前提

- 当前 CSV 已有：
  - `1` 行表头
  - `5` 行历史手工 proof persist 样本
- 当前运行时目录还已新增：
  - `kd_mtf_p0_runtime_notes_v1.md`
  - `kd_mtf_p0_runtime_gaps_v1.md`
  - `kd_mtf_p0_real_input_mapping_draft_v1.md`
- 当前 proof 样本还已新增：
  - `real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - `real_input_samples\kd_mtf_p0_proof_output_v1.csv`
  - 且当前这两份文件已替换为真实 `EURUSD H1` 驱动的首批 `7` 行 proof

## 追加真实数据前先做什么

1. 检查表头是否仍与 `kd_mtf_p0_fields_runtime_header_v1.txt` 一致
2. 检查本次仍只输出 `KD P0` 的 `6` 个字段
3. 确认当前 runtime csv 中不存在 `__PLACEHOLDER__` 行；若仍残留则先删除
4. 在 `kd_mtf_p0_runtime_notes_v1.md` 记录本次参数来源
5. 先固定：
   - `kd_length`
   - `kd_smooth_k`
   - `kd_smooth_d`
   - `ma_type`
   - `price_field`
6. 再确认本次 proof 只覆盖：
   - `week/day/4h`
7. 再核对真实输入是否符合：
   - `kd_mtf_p0_real_input_mapping_draft_v1.md`
8. 若本次先使用手工 proof 样本：
   - 不得把 `proof_output_v1.csv` 直接当作已 append runtime 行
   - 只能把它当作字段映射核对证据

## append stub 当前使用边界

- `kd_mtf_p0_runtime_append_stub_v1.py` 当前只负责：
  - 读取 `proof_output_csv`
  - 校验 runtime 表头
  - 去掉 `__PLACEHOLDER__`
  - 把 proof 行写入 `kd_mtf_p0_fields_runtime_v1.csv`
- 当前不负责：
  - 读取 broker 原始导出
  - 时区归一化
  - 从 bar 数据重建 `week/day/4h`
  - 直接把原始 bar 算成 KD 字段
- 因此第一份真实 bar 输入的顺序必须是：
  - `broker export -> canonical real_input_bars csv -> proof_input/proof_output -> append stub`
  - 不是 `broker export -> append stub`
- 当前已固定的 `canonical real_input_bars csv`：
  - `upstream_samples\n01_first_real_input_bars_v1.csv`
- 当前策略：
  - 先引用独立包内这份已复制的 canonical H1 bars
  - 不再依赖旧目录的上游样本路径
  - 若后续需要再次升级命名，再单独落 `kd_mtf_p0_first_real_input_bars_v1.csv`

## params template 当前使用边界

- `kd_mtf_p0_runtime_params_template_v1.json` 当前角色是：
  - `v1` 运行时合同冻结
  - 默认参数与枚举约束说明
  - 产物路径集中配置
- 当前不应把它理解成：
  - 已绑定真实 broker 源
  - 已覆盖完整计算链
  - 已可独立跑出真实 KD runtime
- 当前最正确用法：
  - 给 proof/runtime 目录与字段枚举提供统一口径
  - 等第一份真实 `bar` 输入接入后，再决定是否需要新增“source ingest params”或继续复用本文件

## 第一批真实数据最小要求

- 至少有：
  - `symbol`
  - `timeframe`
  - `bar_time`
  - `kd_week_bias`
  - `kd_day_signal`
  - `kd_4h_confirm`
  - `kd_alignment_tier`
  - `kd_direction_filter`
  - `kd_week_extreme_zone`
- 对历史不足或条件不足的 bar：
  - 允许关键字段写 `unknown`
  - 不允许伪造非空值

## proof_input 生成前的高周期约束

- `proof_input_v1.csv` 生成时必须先满足：
  - `week/day/4h` 都来自同一份 canonical H1 bars
  - 都只使用目标 `bar_time` 之前最近的**已闭合**高周期
  - `day_k_prev/day_d_prev` 必须来自当前 `day_k/day_d` 的前一根已闭合日线
  - `bar_time` 当前按 H1 bar 的起始时点理解
  - `4h/day/week` 当前按 `UTC` 分桶重建
- 不允许：
  - 用未闭合的当日 / 当周 / 当前 4h 状态
  - 用 H1 当前值直接冒充 `day` 或 `week`
  - 先算出 `proof_output` 再反推 `proof_input`

## 不允许

- 不允许保留 `__PLACEHOLDER__` 并同时写入真实数据
- 不允许偷偷加入：
  - `kd_month_bias`
  - `kd_1h_entry_refine`
  - `kd_divergence_flag`
  - `kd_perfect_state_flag`
  - `kd_dispersion_state`
  - `kd_position_size_multiplier`
- 不允许改表头却还沿用 `v1` 文件名
- 不允许对同一个 `kd_mtf_p0_fields_runtime_v1.csv` 做并发 append
- 不允许把 proof 文件的更新写成“真实 runtime append 已完成”；append 必须单独执行并记录

## 若需要升级到 v2

- 触发条件示例：
  - 表头变更
  - 新增运行时主键列
  - 新增经过正式裁决的字段
- 升级动作：
  - 新建 `kd_mtf_p0_fields_runtime_v2.csv`
  - 新建对应 `header / notes / gaps / append_protocol`
  - 保留 `v1` 不覆盖

## 当前结论

- 这份协议落地后，`多周期KD P0` 已不仅有运行时空壳，还具备了“如何从占位过渡到真实追加”的最小执行约束。
- 当前若重新回到 append 线，最顺动作不是改协议，而是：
  - 已先对最新真实 `7` 行 proof 完成一次 dry-run
  - 下一步只剩决定是否允许新一轮 `--persist`
