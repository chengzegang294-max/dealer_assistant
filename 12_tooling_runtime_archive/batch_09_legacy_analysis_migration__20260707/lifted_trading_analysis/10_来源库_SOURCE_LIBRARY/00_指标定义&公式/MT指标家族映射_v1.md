# MT 指标家族映射 v1

更新时间：2026-06-10

目标：
- 把 `MT4/MT5` 指标文件从“单个文件名”收敛成“可复用的指标家族”
- 先定义本质、公式骨架、可字段化方向，再决定是否进入阶段二批次回测

---

## 1) 家族总表

| family_id | 来源文件 | 平台 | 家族本质 | 当前角色 | 工程化优先级 |
|---|---|---|---|---|---|
| MTF01_VOLTY_STOP | `VoltyChannel_Stop_v2_1M.mq4` | MT4 | MA+ATR 通道 + 趋势翻转止损 | RISK / EXIT / REGIME_DIAG | P0 |
| MTF02_HARMONIC_BASIC | `0_Harmony_06.mq4` | MT4 | ZigZag + XA/AB/BC/CD 比例 + 谐波形态识别 | DIAG_ONLY | P1 |
| MTF03_ZZ_RATIO | `a_ZZ.mq4` | MT4 | ZigZag 摆点 + fib/谐波比率标注 | DIAG_ONLY | P1 |
| MTF04_HARMONIC_FRAMEWORK | `ZUP_v15[1][1].1.mq4` | MT4 | 大型 ZigZag/Fractal/Fibo/谐波框架 | DIAG_ONLY / SOURCE_LIBRARY | P2 |
| MTF05_BREAKOUT_BINARY | `XBreaking.ex4/.ex5` | MT4/MT5 | 二进制突破类指标（源码未知） | NEED_PROBE | P1 |

---

## 2) 家族定义

### MTF01_VOLTY_STOP

- 来源：`VoltyChannel_Stop_v2_1M.mq4`
- 当前状态：已进入 `backtest_p0.py b82-volty-stop-fields` 字段实现 v1
- 本质：均线中心线 + ATR 波动通道 + 价格突破上一根通道触发趋势翻转 + 单边 trailing stop
- 公式骨架：
  - `center_ma = MA(price, ma_len, ma_mode)`
  - `upper = center_ma_high + Kv * ATR(atr_len)`
  - `lower = center_ma_low  - Kv * ATR(atr_len)`
  - `if High[t] > upper[t-1] => trend=up`
  - `if Low[t]  < lower[t-1] => trend=down`
  - `stop_up = lower - (MoneyRisk-1) * ATR`
  - `stop_dn = upper + (MoneyRisk-1) * ATR`
- 可字段化方向：
  - `volty_center_ma_1h`
  - `volty_band_upper_1h`
  - `volty_band_lower_1h`
  - `volty_trend_state_1h`
  - `volty_stop_dist_atr_1h`
  - `volty_flip_flag_1h`
- 进入阶段二建议：
  - 先做 `RISK/EXIT` 家族，不直接当 entry gate
  - 优先看“更稳/更不痛苦”，不是先看收益最大

### MTF02_HARMONIC_BASIC

- 来源：`0_Harmony_06.mq4`
- 当前状态：已完成源码复核与“非重绘确认时点”定义稿 v0；尚未进入字段实现
- 本质：先取 ZigZag/pivot 的 `X A B C D`，再用 `AB/XA`、`BC/AB`、`CD/BC`、`AD/XA` 等比例识别 `AB=CD / Gartley / Bat / Butterfly / Crab`
- 公式骨架：
  - `XA = abs(A-X)`
  - `AB = abs(B-A)`
  - `BC = abs(C-B)`
  - `CD = abs(D-C)`
  - `ratio_1 = BC / AB`
  - `ratio_2 = CD / BC`
  - `ratio_3 = AB / XA`
  - `ratio_4 = AD / XA`
- 可字段化方向：
  - `harmonic_pattern_code_1h`
  - `harmonic_prz_dist_atr_1h`
  - `harmonic_completion_flag_1h`
  - `harmonic_target1_atr_1h`
- 非重绘确认时点（定义稿 v0）：
  - 图上首现时点：当 `0_Harmony_06` 在 `ind[4]` 写入 pattern buffer 时，只说明“最新 ZigZag 候选 D 点”满足比例；这是预警，不是确认
  - 风险来源：源码把所有形态都画在 `ind[4]`，而 `ind[4]` 来自 `a_ZZ` 的最近一个 pivot；只要后续价格继续延伸，D 点本身就可能平移或消失
  - 工程确认时点：只有当后续出现新的反向 ZigZag pivot、使当前 D 不再是“最新 pivot”，且重新计算后 `pattern_code + D_bar` 保持不变，才视为“非重绘确认”
  - 最早可用时点：研究标签可记在“确认成立的收盘 bar”；若后续要接入交易级实验，最早只能用下一根 bar open
  - 红线：禁止把“图上第一次画出 pattern”的时刻直接当作 entry gate 或 hard signal
- 进入阶段二建议：
  - 只做 `DIAG_ONLY`
  - 后续如要字段化，必须先做 prefix/full 一致性审计，再讨论 `completion_flag / prz_dist`

### MTF03_ZZ_RATIO

- 来源：`a_ZZ.mq4`
- 当前状态：已进入 `backtest_p0.py b83-zz-ratio-fields` 字段实现 v1
- 本质：更轻量的 ZigZag 摆点比例标注器，本身不像完整交易信号，更像结构测量工具
- 公式骨架：
  - 取最近三段 swing
  - 计算 `un = abs(leg2) / abs(leg1)`
  - 与预置 fib/谐波比例表匹配
- 可字段化方向：
  - `zz_ratio_code_1h`
  - `zz_ratio_value_1h`
  - `zz_swing_span_atr_1h`
- 进入阶段二建议：
  - 作为 `结构诊断标签`
  - 可给 Volty / RSI / TK 类信号提供“是否处于扩展/回调比例区”的上下文

### MTF04_HARMONIC_FRAMEWORK

- 来源：`ZUP_v15[1][1].1.mq4`
- 本质：大而全的谐波识别框架，混合 ZigZag、Fractal、Fibo、Pesavento 等多套逻辑
- 特征：
  - 参数很多
  - 形态覆盖广
  - 重绘/确认时点定义复杂
- 可字段化方向：
  - 当前不直接字段化完整框架
  - 只拆可审计子结构：`swing_confirmed_flag`、`fib_ratio_bucket`、`pattern_completion_flag`
- 进入阶段二建议：
  - 暂列 `SOURCE_LIBRARY`
  - 不直接进通用候选清单

### MTF05_BREAKOUT_BINARY

- 来源：`XBreaking.ex4 / XBreaking.ex5`
- 本质：突破类指标，但当前仅确认“平台可加载/部分 buffer 可读”，未拿到源码级公式
- 当前已知：
  - `XBreaking.ex5` 可由 MT5 `iCustom` 加载
  - 至少 `buffer0` 可读
  - 其余 buffer/参数含义未知
- 可字段化方向：
  - 先不定义正式字段
  - 仅保留探针层：`buffer0_value`、`buffer_nonempty_n`
- 进入阶段二建议：
  - 继续走“效果验证”而非“公式还原”

---

## 3) 阶段二映射

| 家族 | 更适合映射到阶段二的角色 | 备注 |
|---|---|---|
| Volty Stop | RISK / EXIT / REGIME_DIAG | 最接近可工程化组件 |
| Harmonic Basic | DIAG_ONLY | 低频、小样本、确认时点难 |
| ZZ Ratio | DIAG_ONLY | 结构测量器，不宜直接做 gate |
| ZUP Framework | SOURCE_LIBRARY | 先拆子结构，不整包接入 |
| XBreaking Binary | NEED_PROBE | 先测效果，再决定是否纳入 |

---

## 4) 下一步最小动作

1. `MTF01_VOLTY_STOP` 已完成 strict latest-only + `MAE / max_drawdown_per_trade` 交互复核；下一步若继续，只值得看 `sizing / reduce / exit context`
2. 保持 `MTF03_ZZ_RATIO` 为 `DIAG_ONLY`，暂不接入 shortlist/gate
3. 谐波类 (`MTF02/04`) 已补“非重绘确认时点”定义稿；下一步只允许做确认审计，不直接升 gate
4. 二进制类 (`MTF05`) 继续以 probe/effect 验证为主
