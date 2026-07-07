# kd_mtf_p0_real_input_mapping_draft_v1

## 目的

- 给 `多周期KD P0` 第一份真实 runtime 数据接入前提供最小输入映射草案。
- 只解决 `week/day/4h` 三层 KD 状态如何映射到当前 `6` 个输出字段。
- 默认阅读顺序、停点与覆盖关系：
  - 以 `kd_mtf_p0_directory_index_card_v1.md` 为准
- 不扩到：
  - `month bias`
  - `1h refine`
  - `背离 / 离散 / 完美`
  - 仓位倍率

## 当前目标输出

- `kd_week_bias`
- `kd_day_signal`
- `kd_4h_confirm`
- `kd_alignment_tier`
- `kd_direction_filter`
- `kd_week_extreme_zone`

## 最小真实输入

### 行情主输入

- `symbol`
- `timeframe`
- `bar_time`
- `open`
- `high`
- `low`
- `close`

### 配置主输入

- `kd_length = 13`
- `kd_smooth_k = 3`
- `kd_smooth_d = 3`
- `ma_type = sma`
- `price_field = close_close`

## 输入到输出映射

### 1. 直接透传

- `symbol <- symbol`
- `timeframe <- timeframe`
- `bar_time <- bar_time`

### 2. 周期状态重建

- `week_k / week_d`
  - 来源：
    - 由同一品种的周线 OHLC 重建
- `day_k / day_d`
  - 来源：
    - 由同一品种的日线 OHLC 重建
- `h4_k / h4_d`
  - 来源：
    - 由同一品种的 `4h` OHLC 重建
- 当前 v1 约束：
  - 不允许不同品种或不同 session 的 bar 串用
  - 不允许拿当前 `timeframe` 直接冒充更高周期状态

### 3. `kd_week_bias`

- 派生逻辑：
  - 若 `week_k > week_d`，则 `up`
  - 若 `week_k < week_d`，则 `down`
  - 若关键值不可算，则 `unknown`

### 4. `kd_day_signal`

- 派生逻辑：
  - 若 `day_k` 上穿 `day_d`，则 `golden_cross`
  - 若 `day_k` 下穿 `day_d`，则 `death_cross`
  - 若仅保持同向但本 bar 无新交叉，则 `none`
  - 若关键值不可算，则 `unknown`

### 5. `kd_4h_confirm`

- 派生逻辑：
  - 若 `h4_k > h4_d`，则可作为 `confirm_up`
  - 若 `h4_k < h4_d`，则可作为 `confirm_down`
  - 若未形成可读方向，则 `none`
  - 若关键值不可算，则 `unknown`

### 6. `kd_alignment_tier`

- `s`
  - `week_bias` 明确
  - `day_signal` 为同向主信号
  - `4h_confirm` 同向确认
- `a`
  - `day_signal + 4h_confirm` 同向
  - `week_bias` 不冲突
- `b`
  - 仅 `day_signal` 有主信号
  - `4h_confirm = none`
- `conflict`
  - `week_bias` 与 `day_signal` 冲突
- `unknown`
  - 任一关键周期无法可靠计算

### 7. `kd_direction_filter`

- 派生逻辑：
  - 若 `kd_alignment_tier = s` 且方向向上，则 `long_preferred`
  - 若 `kd_alignment_tier = s` 且方向向下，则 `short_preferred`
  - 若 `kd_alignment_tier = a` 且方向清晰，也允许保留同向 `preferred`
  - 若 `b/conflict/unknown`，则默认 `wait/unknown`

### 8. `kd_week_extreme_zone`

- 当前 v1 保守定义：
  - 若 `week_k >= 80` 且 `week_d >= 80`，则 `overbought`
  - 若 `week_k <= 20` 且 `week_d <= 20`，则 `oversold`
  - 若关键值可算但不处于极值带，则 `normal`
  - 若关键值不可算，则 `unknown`

## 第一份真实 bar 输入怎么接

- 当前固定策略：
  - 先只接 `1` 个品种、`1` 个基础周期
  - 当前固定基础周期为 `H1`
  - 当前直接引用既有 canonical bars，不再新建重复 bars 文件
- 当前不建议：
  - 直接拿 `proof_input_v1.csv` 冒充真实 bar 输入
  - 直接把 broker 原始导出不经标准化就喂给 append stub

## 当前已固定的第一份真实输入源

- 当前先不新建第二份重复 bars 文件。
- `DY-R1` 当前固定引用：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_first_real_input_bars_v1.csv`
- 当前已核对：
  - `rows = 8976`
  - `symbol = EURUSD`
  - `timeframe = H1`
  - `first_bar_time = 2025-01-02T00:00:00Z`
  - `last_bar_time = 2026-06-12T00:00:00Z`
- 当前角色：
  - `DY-R1` 的第一份上游 canonical real_input_bars
  - 先作为 proof 输入源引用
  - 当前不复制、不改名、不重切目录

## 从 H1 bars 到 proof_input 的最小转换口径

- 当前目标不是直接从 H1 bars 生成 runtime csv。
- 当前最小目标只到：
  - `H1 canonical bars -> proof_input_v1.csv -> proof_output_v1.csv`
- `proof_input_v1.csv` 当前固定列：
  - `symbol`
  - `timeframe`
  - `bar_time`
  - `week_k`
  - `week_d`
  - `day_k_prev`
  - `day_d_prev`
  - `day_k`
  - `day_d`
  - `h4_k`
  - `h4_d`
  - `input_note`

## 最小转换步骤

1. 从 canonical H1 bars 读取单一 `symbol + H1` 序列
2. 以同一份 H1 bars 重建：
   - `4h` OHLC
   - `day` OHLC
   - `week` OHLC
3. 按 `13,3,3 + sma` 计算：
   - `week_k / week_d`
   - `day_k / day_d`
   - `h4_k / h4_d`
4. 对每个目标 `bar_time` 只取“该时点之前已经闭合”的高周期状态
5. 把这些状态写入 `proof_input_v1.csv`
6. 再由 `proof_input_v1.csv` 派生 `proof_output_v1.csv`

## 已闭合周期边界

- `week_k / week_d`
  - 只能来自目标 `bar_time` 之前最近一根**已闭合**周线
- `day_k / day_d`
  - 只能来自目标 `bar_time` 之前最近一根**已闭合**日线
- `day_k_prev / day_d_prev`
  - 只能来自 `day_k / day_d` 的前一根**已闭合**日线
- `h4_k / h4_d`
  - 只能来自目标 `bar_time` 之前最近一根**已闭合** 4 小时线
- 当前禁止：
  - 使用尚未闭合的 `day / week / 4h`
  - 用目标 H1 所在的未完成高周期去推当前状态
  - 任何形式的 lookahead

## prev / current 的最小定义

- `day_k_prev / day_d_prev`
  - 用于判断“本次 `day` 是否出现新交叉”
  - 表示目标 `bar_time` 所参考的当前日线状态之前一根已闭合日线状态
- `day_k / day_d`
  - 表示目标 `bar_time` 所参考的最近一根已闭合日线状态
- 第一版判断规则因此固定为：
  - 先比较 `day_k_prev/day_d_prev`
  - 再比较 `day_k/day_d`
  - 只在“前后关系发生穿越”时落 `golden_cross / death_cross`
  - 若只是旧方向延续，则落 `none`

## 当前 proof_input 的角色边界

- `proof_input_v1.csv` 是：
  - 从真实 H1 bars 重建出的高周期状态中间层
  - 用于验证字段映射
- `proof_input_v1.csv` 不是：
  - broker 原始 bar 输入
  - 最终 runtime csv
  - 策略信号表

## 第一份真实 bar 输入标准化口径

- 外部导出列名可以不同，但收进仓库后的 canonical 列先固定为：
  - `symbol`
  - `timeframe`
  - `bar_time`
  - `open`
  - `high`
  - `low`
  - `close`
- `bar_time` 当前统一要求：
  - `UTC`
  - ISO8601，例如 `2026-06-18T08:00:00Z`
- 同一份输入内必须保持：
  - 单一 `symbol`
  - 单一基础 `timeframe`
  - 时间严格递增
  - 无重复 `bar_time`
- 若原始导出来自 broker 时区：
  - 先做时区归一化
  - 再落到 canonical CSV

## `bar_time` 语义与 UTC 分桶

- 当前 `DY-R1` 先沿现有 MT5 canonical bars 口径理解：
  - `bar_time` 表示该根 H1 bar 的**起始时点**
  - 例如 `2025-01-02T08:00:00Z` 表示区间 `[08:00, 09:00)`
- 第一版高周期重建固定按 `UTC` 分桶：
  - `4h`
    - 分桶起点：`00:00 / 04:00 / 08:00 / 12:00 / 16:00 / 20:00`
  - `day`
    - 分桶起点：每日 `00:00`
  - `week`
    - 分桶起点：每周一 `00:00`
- 当前若后续发现某份外部源不是“bar 起始时点”口径：
  - 不直接改写 `v1`
  - 必须在接入说明里单独声明并起新版本

## 第一份真实 bar 输入与 proof 样本的关系

- `real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - 当前是“高周期 KD 状态输入样本”
  - 不是 broker bar 真实输入
- `real_input_samples\kd_mtf_p0_first_real_input_bars_v1.csv`
  - 当前只是保留命名位
  - 本轮不强制创建
- 当前实际采用的第一份真实 bar 输入：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_first_real_input_bars_v1.csv`
- 推荐顺序：
  1. 先引用已存在的 canonical `n01_first_real_input_bars_v1.csv`
  2. 若未来需要完全解耦，再落本目录自己的 `kd_mtf_p0_first_real_input_bars_v1.csv`
  3. 再根据真实 bar 输入重建 `week/day/4h` 状态
  4. 再生成新的 proof 输入/输出
  5. 最后再考虑 runtime append

## 第一版真实 `proof_input_v1.csv` 生成步骤

1. 读取 `n01_first_real_input_bars_v1.csv`
2. 断言输入仍满足：
   - 单一 `symbol`
   - 单一 `timeframe = H1`
   - `bar_time` 严格递增
   - 无重复 `bar_time`
3. 以 `UTC` 分桶从同一份 H1 bars 重建：
   - `4h` OHLC
   - `day` OHLC
   - `week` OHLC
4. 按 `13,3,3 + sma + close_close` 计算三组状态：
   - `week_k / week_d`
   - `day_k / day_d`
   - `h4_k / h4_d`
5. 选择目标 `bar_time`
6. 对每个目标 `bar_time = t`，只取：
   - `t` 之前最近一根已闭合 `week`
   - `t` 之前最近一根已闭合 `day`
   - `t` 之前最近一根已闭合 `4h`
7. 额外回取一根前序已闭合日线，填入：
   - `day_k_prev`
   - `day_d_prev`
8. 生成 `proof_input_v1.csv`
9. 再由 `proof_input_v1.csv` 派生 `proof_output_v1.csv`

## 目标 `bar_time` 的选择规则

- 第一版不要求把全部 `8976` 根 H1 都写进 `proof_input_v1.csv`
- 当前推荐先做“代表性 proof 行”而不是全量展开：
  - 每次先选 `3-5` 个目标 `bar_time`
  - 目标是覆盖 `s / conflict / b`，若可能再补 `a`
- 目标 `bar_time` 选择时必须满足：
  - 该时点之前已有足够 H1 历史去重建 `week/day/4h`
  - 对应高周期都已经闭合
  - 不用未闭合日线/周线/4h 去填当前状态
- 第一版不建议：
  - 从样本最开头就取 proof 行
  - 在历史不足的区段硬凑 `week_k/week_d`

## 第一份真实数据建议最小样本

- 至少准备：
  - `1` 组 `s` tier 样本
  - `1` 组 `conflict` 样本
  - `1` 组 `a` 或 `b` 样本
- 若后续继续扩真实样本，再优先补：
  - 第一条真实 `b`
  - `week extreme normal / overbought / oversold`

## 历史长度最低要求

- 若只验证 `4h`：
  - 至少足够算出 `13,3,3` 的 `4h K/D`
- 若验证 `day`：
  - 至少足够算出 `13,3,3` 的 `day K/D`
- 若验证 `week`：
  - 必须提供足够周线历史
- 若关键历史不足：
  - 不宣称对应字段已完成真实接入
  - 统一写 `unknown`

## 第一份真实输入的保守样本要求

- 第一刀至少覆盖：
  - `1` 个 `s(up 或 down)` 样本
  - `1` 个 `conflict` 样本
  - `1` 个 `b` 或 `a` 样本
- 第一刀不强求：
  - 一次覆盖全部品种
  - 一次覆盖全部极值状态
  - 一次补齐 `month / 1h`

## 当前可执行口径（人工 / 脚本共用）

- 不管后续是人工整理还是写脚本，第一版都必须输出同一套中间列：
  - `week_k`
  - `week_d`
  - `day_k_prev`
  - `day_d_prev`
  - `day_k`
  - `day_d`
  - `h4_k`
  - `h4_d`
- `proof_output_v1.csv` 只能由这些中间列再派生：
  - `kd_week_bias`
  - `kd_day_signal`
  - `kd_4h_confirm`
  - `kd_alignment_tier`
  - `kd_direction_filter`
  - `kd_week_extreme_zone`

## 当前不做

- 不做 `month bias`
- 不做 `1h refine`
- 不做 `divergence / perfect / dispersion`
- 不把仓位倍率建议直接并入当前字段层

## 接入前必须联动

- `kd_mtf_p0_directory_index_card_v1.md`
- `kd_mtf_p0_quick_entry_card_v1.md`
- `kd_mtf_p0_object_responsibility_card_v1.md`
- `kd_mtf_p0_b_blocker_note_v1.md`
- `kd_mtf_p0_runtime_notes_v1.md`
- `kd_mtf_p0_runtime_gaps_v1.md`
- `kd_mtf_p0_runtime_append_protocol_v1.md`

## 当前已落 proof 样本

- 已新增：
  - `real_input_samples\kd_mtf_p0_proof_input_v1.csv`
  - `real_input_samples\kd_mtf_p0_proof_output_v1.csv`
- 当前作用：
  - 用真实 `EURUSD H1` canonical bars 重建出的高周期 KD 状态输入
  - 验证这 `6` 个字段的映射是否与当前 `v1` 口径一致
- 当前上游输入：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\real_input_samples\n01_first_real_input_bars_v1.csv`
- 当前首批目标 `bar_time`：
  - `2025-01-29T00:00:00Z`
  - `2025-02-13T04:00:00Z`
  - `2025-04-30T00:00:00Z`
  - `2025-05-09T00:00:00Z`
  - `2025-06-06T00:00:00Z`
  - `2025-06-12T00:00:00Z`
  - `2025-08-29T00:00:00Z`
- 当前覆盖：
  - `a(up + long_preferred + week_unknown)`
  - `a(down + short_preferred + week_unknown)`
  - `s(up)`
  - `s(down + short_preferred)`
  - `conflict`
- 当前真实样本尚未补出：
  - `b`
- 当前总 proof 行数：
  - `7`
- 当前边界：
  - 这两份 proof CSV 不是 broker 原始 bar 数据本体
  - 当前也还没有把这批最新真实 proof append 进 runtime csv

## 当前验证落点

- 当前这份长稿只继续承担：
  - 输入字段到输出字段的主线映射
  - `H1 -> 4h/day/week -> proof_input -> proof_output` 的完整转换链
  - 第一份真实 proof 已落地后的主线落点
- 当前已验证到：
  - `week_k / week_d` 可按 `UTC week` 稳定重建
  - `day_k_prev / day_d_prev / day_k / day_d` 可稳定派生 `golden_cross / death_cross / none / unknown`
  - `h4_k / h4_d` 可稳定派生 `confirm_up / confirm_down / unknown`
  - 当前真实 proof 已覆盖 `a / s / conflict`
- 当前未验证到：
  - 第一条真实 `b`
  - 最新真实 `proof_output_v1.csv` append 后的 runtime 刷新记录
- `b` 的长阻塞证据与扩扫边界：
  - 统一以 `kd_mtf_p0_b_blocker_note_v1.md` 为准
