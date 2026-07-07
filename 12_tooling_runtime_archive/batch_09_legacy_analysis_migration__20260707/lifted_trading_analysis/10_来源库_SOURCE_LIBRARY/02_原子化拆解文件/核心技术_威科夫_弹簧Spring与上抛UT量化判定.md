# 核心技术_威科夫_弹簧Spring与上抛UT量化判定

## 核心定义
弹簧(Spring)是积累阶段价格短暂跌破区间下轨后迅速回到区间内的假突破形态；上抛(Upthrust, UT)是派发阶段价格短暂突破区间上轨后迅速回到区间内的假突破形态。两者是阶段转换的最强先行信号。

## 可量化执行标准

**弹簧(Spring)量化判定条件（全部满足）**：
1. 前期处于积累阶段横盘区间（≥10根K线）
2. 价格跌破区间下轨（跌破幅度<区间高度的20%）
3. 跌破后迅速回到区间内（5根K线内回到区间内）
4. 回到区间内后收盘于区间下轨之上
5. 跌破时成交量萎缩或正常（非恐慌放量）
6. 回到区间内后出现多头信号K线（评分≥6分）

**弹簧入场规则**：
- 入场点：价格回到区间内+多头信号K线收盘
- 止损：弹簧最低点下方+0.3xATR
- 目标位：区间上轨 + 区间高度等幅投射
- 仓位：标准仓位×1.2（高胜率形态）
- 最低R:R：1:2

**上抛(UT)量化判定条件（全部满足）**：
1. 前期处于派发阶段横盘区间（≥10根K线）
2. 价格突破区间上轨（突破幅度<区间高度的20%）
3. 突破后迅速回到区间内（5根K线内回到区间内）
4. 回到区间内后收盘于区间上轨之下
5. 突破时成交量未持续放大（诱多特征）
6. 回到区间内后出现空头信号K线（评分≥6分）

**上抛入场规则**：
- 入场点：价格回到区间内+空头信号K线收盘
- 止损：上抛最高点上方+0.3xATR
- 目标位：区间下轨 - 区间高度等幅投射
- 仓位：标准仓位×1.2
- 最低R:R：1:2

**弹簧/上抛失败判定**：
- 价格回到区间内后再次跌破/突破区间边界 = 假弹簧/假上抛
- 失败时立即止损，并等待新的确认信号
- 连续2次失败 = 阶段判定可能错误，重新分析

## 适用场景与禁忌
- **适用场景**：日线/周线级别积累/派发阶段的阶段确认交易，最佳胜率形态之一
- **禁忌场景**：无横盘区间基础的弹簧/上抛无效；跌破/突破幅度>区间高度30%为真突破
- **核心约束**：弹簧/上抛必须在收盘确认回到区间内后才可入场，禁止在跌破/突破过程中预判

## 对象入口（DIAG_ONLY）

- 当前角色：
  - `DIAG_ONLY_OBJECT_CANDIDATE`
- 当前边界：
  - v1 不推断“积累/派发阶段”，只接受输入 `wyckoff_phase`（`accumulation / distribution`）作为前置条件。
  - v1 不引入“信号K线评分≥6分”的完整评分体系，只保留为 `bull_bear_signal_score` 的外部输入。

## 最小合同（v1 草案）

| field | type | required | notes |
|---|---|---:|---|
| symbol | string | yes | 标的 |
| timeframe | string | yes | 例如 `D1/W1/H1` |
| t | string | yes | 当前K线时间戳（ISO8601） |
| wyckoff_phase | string | yes | `accumulation / distribution` |
| range_len | number | yes | 横盘区间长度（K线根数），必须 `>= 10` |
| range_high | number | yes | 区间上轨 |
| range_low | number | yes | 区间下轨 |
| range_height | number | yes | `range_high - range_low` |
| penetration_ratio_max | number | yes | 默认 `0.2`（跌破/突破幅度 < 区间高度 * 0.2） |
| return_within_bars | number | yes | 默认 `5`（5根K线内回到区间内） |
| bull_bear_signal_score | number | yes | “回到区间内后信号K线评分”，外部输入 |
| signal_score_min | number | yes | 默认 `6` |
| volume_state | string | yes | `low_or_normal / sustained_expand / panic`（外部输入） |
| atr | number | no | 若要输出 `stop_offset=0.3*atr` 则需要 |

输出字段（v1）：

| field | type | required | notes |
|---|---|---:|---|
| spring_ut_state | string | yes | `spring / ut / none / invalid` |
| validity_reason | string | yes | 未通过时写明卡在哪个硬条件 |
| stop_offset | number | no | `0.3 * atr` |
