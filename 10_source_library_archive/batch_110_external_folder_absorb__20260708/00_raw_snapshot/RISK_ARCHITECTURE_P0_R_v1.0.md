# RISK_ARCHITECTURE_P0_R — 三层风控联动总览 v1.0

> 版本：v1.0 | 状态：风控层核心文档 | 与 KELLY_P0_R / VOLTARGET_P0_R / VOTE_DECISION_TABLE 配合使用
> 目标：将 Van Tharp 2% 硬性上限、Kelly Criterion、Volatility Targeting 三个风控对象卡的联动规则整合为一份可执行文档
> 核心原则：三层风控取 min，Van Tharp 是绝对红线，不可突破

---

## 1. 三层风控架构总览

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 第一层：Van Tharp 硬性上限（Hard Stop）                                      │
│ 功能：绝对否决，任何交易若导致单票风险 > 2% → 强制 ABORT                    │
│ 触发时机：投票通过后，执行前检查                                            │
│ 性质：不可协商，不可覆盖，不可降级                                          │
│                                                                             │
│ 输出：van_tharp_pass  BOOL    -- True = 通过，False = 强制 ABORT            │
│       van_tharp_risk_pct  FLOAT  -- 当前单票风险百分比                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼（若通过）
┌─────────────────────────────────────────────────────────────────────────────┐
│ 第二层：Kelly Criterion 动态优化（Position Sizing）                        │
│ 功能：根据历史交易胜率，动态计算最优仓位                                    │
│ 触发时机：投票通过后，Van Tharp 检查前（先计算，再检查）                    │
│ 性质：可调制（半凯利/四分之一凯利/自适应），但不可超过 Van Tharp 上限        │
│                                                                             │
│ 输出：kelly_f_star  FLOAT       -- 凯利最优比例（0.0-1.0）                  │
│       kelly_size_scalar  FLOAT  -- 实际仓位缩放（半凯利 = f_star / 2）      │
│       kelly_mode  ENUM          -- "half_kelly" / "quarter_kelly" / "adaptive"│
│       kelly_crisis  BOOL        -- 是否处于危机模式（连续亏损 3 笔）        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 第三层：Volatility Targeting 环境系数（Environment Scalar）                  │
│ 功能：根据当前波动率环境，调整仓位大小                                       │
│ 触发时机：投票通过后，与 Kelly 并行计算                                     │
│ 性质：环境系数，高波动时降仓，低波动时允许加仓                               │
│                                                                             │
│ 输出：vt_scalar  FLOAT          -- 波动率缩放系数（0.2-2.0）                │
│       vt_size_scalar  FLOAT     -- 实际仓位缩放（目标波动率 / 当前波动率）  │
│       vt_vol_regime  ENUM       -- "LOW_VOL" / "NORMAL_VOL" / "HIGH_VOL" / "EXTREME_VOL"│
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 最终仓位调制（三层取 min）                                                   │
│                                                                             │
│ final_size_scalar = min(                                                    │
│     kelly_size_scalar,      -- Kelly 动态优化层                            │
│     vt_size_scalar,         -- VolTarget 环境系数层                        │
│     pq_position_max_size,   -- PeriodQueen 状态上限（若适用）              │
│     1.0                     -- 理论最大仓位                                │
│ )                                                                           │
│                                                                             │
│ 若 final_size_scalar <= 0.05 → 视为禁止交易 → ABORT                        │
│ 若 van_tharp_pass = False → 强制 ABORT                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. 第一层：Van Tharp 硬性上限（已冻结）

### 2.1 核心规则

```text
规则 1：单票风险上限
  - 任何单一标的的最大风险 ≤ 账户总资金的 2%
  - 风险定义：|entry_price - stop_loss| × position_size / account_total
  - 公式：risk_pct = (entry_price - stop_loss) × shares / account_total
  - 若 risk_pct > 0.02 → 强制 ABORT，无论其他信号多强

规则 2：总风险上限（可选扩展）
  - 所有持仓的总风险 ≤ 账户总资金的 6%
  - 总风险 = Σ(|entry_price_i - stop_loss_i| × shares_i) / account_total
  - 若总风险 > 0.06 → 禁止新入场，仅允许退出

规则 3：连续亏损保护
  - 连续亏损 3 笔后，Kelly 进入危机模式，但 Van Tharp 规则不变
  - Van Tharp 不因连续亏损而放宽（硬性上限始终有效）
```

### 2.2 检查时机

```text
时机 1：投票通过后（NODE_007 之前）
  - 在生成最终交易信号前，先计算该交易的风险
  - 若风险 > 2% → 直接 ABORT，不进入 Kelly/VolTarget 计算
  - 这是第一道防线

时机 2：持仓后每日检查
  - 每日收盘后，检查所有持仓的当前风险（用当前价格重新计算）
  - 若任何持仓风险 > 2%（因价格跳空或波动扩大）→ 强制减仓或平仓
  - 这是第二道防线

时机 3：新信号与现有持仓的叠加风险
  - 若新交易 + 现有持仓的总风险 > 6% → 禁止新入场
  - 或要求先减仓现有持仓，再开新仓
```

### 2.3 伪代码实现

```python
def van_tharp_check(entry_price, stop_loss, account_total, existing_positions=None):
    """
    Van Tharp 硬性上限检查
    
    参数:
        entry_price: 入场价格
        stop_loss: 止损价格
        account_total: 账户总资金
        existing_positions: 现有持仓列表（可选）
    
    返回:
        dict with van_tharp_pass, van_tharp_risk_pct, van_tharp_action
    """
    # 单票风险计算
    risk_per_share = abs(entry_price - stop_loss)
    
    # 假设标准仓位（稍后由 Kelly/VolTarget 调制）
    # 先计算最大可持仓股数（基于 2% 风险）
    max_risk_amount = account_total * 0.02
    max_shares = max_risk_amount / risk_per_share
    
    # 单票风险百分比
    risk_pct = risk_per_share * max_shares / account_total
    
    # 检查是否通过
    van_tharp_pass = risk_pct <= 0.02
    
    # 总风险检查（如有现有持仓）
    if existing_positions:
        total_risk = sum(pos['risk_amount'] for pos in existing_positions)
        total_risk_pct = total_risk / account_total
        
        if total_risk_pct > 0.06:
            van_tharp_pass = False
            van_tharp_action = "HALT_NEW_POSITIONS"
        else:
            van_tharp_action = "PASS"
    else:
        van_tharp_action = "PASS" if van_tharp_pass else "ABORT"
    
    return {
        "van_tharp_pass": van_tharp_pass,
        "van_tharp_risk_pct": risk_pct,
        "van_tharp_action": van_tharp_action,
        "max_shares": max_shares,
    }
```

---

## 3. 第二层：Kelly Criterion 动态优化（已冻结）

### 3.1 核心规则

```text
规则 1：Kelly 公式
  - f* = (W × R - L) / R
  - W = 胜率（Win Rate），历史交易中盈利的比例
  - L = 败率（Loss Rate），= 1 - W
  - R = 盈亏比（Reward/Risk Ratio），平均盈利 / 平均亏损
  - f* = 最优仓位比例（0.0-1.0）

规则 2：半凯利（保守策略）
  - kelly_size_scalar = f* / 2
  - 默认使用半凯利（降低风险，减少回撤）
  - 当历史交易 < 30 笔时，使用默认半凯利（f* = 0.25，scalar = 0.25）

规则 3：四分之一凯利（更保守）
  - kelly_size_scalar = f* / 4
  - 在以下情况使用：
    - 试错状态（GESTATION / POWER_TRANSITION）
    - 高波动环境（volfac_vol_regime = 'HIGH_VOL'）
    - 连续亏损 2 笔（接近危机模式）

规则 4：自适应模式
  - 根据近期表现动态调整：
    - 最近 10 笔胜率 > 60% → 使用半凯利（f* / 2）
    - 最近 10 笔胜率 40-60% → 使用四分之一凯利（f* / 4）
    - 最近 10 笔胜率 < 40% → 使用八分之一凯利（f* / 8）
    - 连续亏损 3 笔 → 危机模式（kelly_crisis = True，scalar = 0.1）

规则 5：T+1 惩罚系数
  - A 股 T+1 限制，隔夜风险无法当日平仓
  - 在 f* 计算结果上 × 0.8（惩罚系数）
  - 即：kelly_size_scalar = (f* / 2) × 0.8（默认）
```

### 3.2 检查时机

```text
时机：投票通过后，Van Tharp 检查之前（或并行）
  - 先计算 Kelly 的建议仓位
  - 然后检查 Van Tharp 是否允许该仓位
  - 若 Kelly 建议的仓位导致 Van Tharp 风险 > 2% → 降低 Kelly 仓位至 Van Tharp 允许上限

数据需求：
  - 历史交易日志（至少最近 30 笔）
  - 每笔交易的盈亏、R 倍数
  - 若历史交易不足 → 使用默认半凯利（f* = 0.25）
```

### 3.3 伪代码实现

```python
def kelly_criterion(trade_log, current_mode="half_kelly", t1_penalty=0.8):
    """
    Kelly Criterion 动态仓位计算
    
    参数:
        trade_log: DataFrame with [profit_loss, r_multiple, direction, entry_date]
        current_mode: "half_kelly" / "quarter_kelly" / "adaptive" / "crisis"
        t1_penalty: A股 T+1 惩罚系数（默认 0.8）
    
    返回:
        dict with kelly_f_star, kelly_size_scalar, kelly_mode, kelly_crisis
    """
    n_trades = len(trade_log)
    
    # 历史交易不足 → 默认半凯利
    if n_trades < 30:
        return {
            "kelly_f_star": 0.25,
            "kelly_size_scalar": 0.25 * t1_penalty,
            "kelly_mode": "default_half_kelly",
            "kelly_crisis": False,
        }
    
    # 计算胜率 W 和盈亏比 R
    wins = trade_log[trade_log['profit_loss'] > 0]
    losses = trade_log[trade_log['profit_loss'] < 0]
    
    W = len(wins) / n_trades
    L = 1 - W
    R = abs(wins['profit_loss'].mean() / losses['profit_loss'].mean()) if len(losses) > 0 else 1.0
    
    # Kelly 公式
    f_star = (W * R - L) / R
    f_star = max(0.0, min(1.0, f_star))  # 限制在 0-1
    
    # 根据模式调整
    if current_mode == "half_kelly":
        scalar = f_star / 2
    elif current_mode == "quarter_kelly":
        scalar = f_star / 4
    elif current_mode == "adaptive":
        # 自适应模式：根据最近 10 笔胜率调整
        recent_10 = trade_log.tail(10)
        recent_win_rate = len(recent_10[recent_10['profit_loss'] > 0]) / 10
        
        if recent_win_rate > 0.6:
            scalar = f_star / 2
        elif recent_win_rate > 0.4:
            scalar = f_star / 4
        else:
            scalar = f_star / 8
    elif current_mode == "crisis":
        scalar = 0.1
    else:
        scalar = f_star / 2
    
    # 检查危机模式（连续亏损 3 笔）
    recent_3 = trade_log.tail(3)
    kelly_crisis = all(recent_3['profit_loss'] < 0)
    
    if kelly_crisis:
        scalar = 0.1
        current_mode = "crisis"
    
    # T+1 惩罚
    final_scalar = scalar * t1_penalty
    
    return {
        "kelly_f_star": f_star,
        "kelly_size_scalar": final_scalar,
        "kelly_mode": current_mode,
        "kelly_crisis": kelly_crisis,
    }
```

---

## 4. 第三层：Volatility Targeting 环境系数（已冻结）

### 4.1 核心规则

```text
规则 1：目标波动率
  - 大盘股（>500亿）：target_vol = 10%（年化）
  - 小盘股（<50亿）：target_vol = 20%（年化）
  - 中盘股（50-500亿）：target_vol = 15%（年化）

规则 2：Scalar 计算
  - vt_scalar = target_vol / current_vol
  - current_vol = 当前年化波动率（来自 VOLFAC 的 volfac_annualized_vol）
  - 若 current_vol = 0（数据缺失）→ 使用默认 scalar = 1.0

规则 3：VolRegime 映射
  - volfac_vol_regime = 'LOW_VOL'（<20% 分位）→ scalar > 1.0（允许加仓）
  - volfac_vol_regime = 'NORMAL_VOL'（20%-80% 分位）→ scalar ≈ 1.0（正常）
  - volfac_vol_regime = 'HIGH_VOL'（>80% 分位）→ scalar < 1.0（降仓）
  - volfac_vol_regime = 'EXTREME_VOL'（>95% 分位）→ scalar = 0.2（极度保守）

规则 4：涨跌停 ATR 修正
  - 连续涨跌停日 ATR 失真（价格被压缩）
  - 使用 limit_atr_corrector：剔除涨跌停日后重新计算 ATR
  - 修正后的 ATR 用于 VolTarget 计算

规则 5：T+1 隔夜风险
  - A 股 T+1 无法当日平仓，隔夜风险增加
  - target_vol 增加 2-3% 缓冲（大盘股 10% → 12-13%，小盘股 20% → 22-23%）
```

### 4.2 检查时机

```text
时机：投票通过后，与 Kelly 并行计算
  - 根据 VOLFAC 的输出（volfac_annualized_vol）计算 scalar
  - 同时考虑当前 regime_state（PeriodQueen）的波动率环境
  - 若 PeriodQueen 处于 HIGH_VOL 环境（如 REMAINING_WARMTH）→ scalar 额外降低

数据需求：
  - VOLFAC 的 volfac_annualized_vol（当前年化波动率）
  - 个股市值（用于分层 target_vol）
  - 涨跌停标记（用于 ATR 修正）
```

### 4.3 伪代码实现

```python
def volatility_targeting(volfac_data, market_cap, regime_state, limit_up_days=None):
    """
    Volatility Targeting 环境系数计算
    
    参数:
        volfac_data: VOLFAC 输出（含 volfac_annualized_vol）
        market_cap: 个股市值（亿元）
        regime_state: 当前周期状态（PeriodQueen）
        limit_up_days: 连续涨跌停日列表（用于 ATR 修正）
    
    返回:
        dict with vt_scalar, vt_size_scalar, vt_vol_regime
    """
    current_vol = volfac_data['volfac_annualized_vol']
    vol_regime = volfac_data['volfac_vol_regime']
    
    # 1. 根据市值分层确定目标波动率
    if market_cap > 500:
        target_vol = 0.10
    elif market_cap < 50:
        target_vol = 0.20
    else:
        target_vol = 0.15
    
    # 2. T+1 隔夜风险缓冲
    target_vol += 0.02
    
    # 3. ATR 修正（剔除涨跌停日）
    if limit_up_days and len(limit_up_days) > 0:
        # 使用修正后的 ATR 重新计算 current_vol
        current_vol = correct_atr_for_limit_days(current_vol, limit_up_days)
    
    # 4. Scalar 计算
    if current_vol > 0:
        vt_scalar = target_vol / current_vol
    else:
        vt_scalar = 1.0  # 默认
    
    # 5. 根据 vol_regime 限制 scalar
    if vol_regime == 'EXTREME_VOL':
        vt_scalar = min(vt_scalar, 0.2)
    elif vol_regime == 'HIGH_VOL':
        vt_scalar = min(vt_scalar, 0.5)
    elif vol_regime == 'LOW_VOL':
        vt_scalar = min(vt_scalar, 1.5)  # 低波动时最多加仓到 1.5 倍
    
    # 6. PeriodQueen 状态额外调制
    if regime_state == 'REMAINING_WARMTH':
        vt_scalar *= 0.5  # 余温期额外降仓
    elif regime_state == 'GESTATION':
        vt_scalar *= 0.8  # 孕化期略微保守
    elif regime_state == 'POWER_TRANSITION':
        vt_scalar *= 0.7  # 交权期保守
    
    # 确保 scalar 在合理范围
    vt_scalar = max(0.1, min(2.0, vt_scalar))
    
    return {
        "vt_scalar": vt_scalar,
        "vt_size_scalar": vt_scalar,  # 直接作为仓位缩放
        "vt_vol_regime": vol_regime,
        "vt_target_vol": target_vol,
        "vt_current_vol": current_vol,
    }
```

---

## 5. 三层联动：最终仓位计算

### 5.1 联动公式（已冻结）

```text
最终仓位计算步骤：

步骤 1：Van Tharp 检查（第一道防线）
  - 计算该交易的最大允许股数（基于 2% 风险）
  - 若风险 > 2% → ABORT
  - 输出：van_tharp_max_shares

步骤 2：Kelly 计算（第二道防线）
  - 根据历史交易日志计算 f*
  - 根据模式（半凯利/四分之一凯利/自适应）计算 scalar
  - 应用 T+1 惩罚
  - 输出：kelly_size_scalar

步骤 3：VolTarget 计算（第三道防线）
  - 根据当前波动率环境计算 scalar
  - 应用市值分层和涨跌停修正
  - 输出：vt_size_scalar

步骤 4：PeriodQueen 上限（环境限制）
  - 根据 regime_state 获取 pq_position_max_size
  - 输出：pq_position_max_size

步骤 5：取最小值（最终仓位）
  - final_size_scalar = min(kelly_size_scalar, vt_size_scalar, pq_position_max_size, 1.0)
  - 若 final_size_scalar <= 0.05 → ABORT（仓位过小，不经济）
  - 若 final_size_scalar > van_tharp_max_shares / 标准股数 → 降低至 Van Tharp 允许上限

步骤 6：生成最终交易信号
  - position_size = 标准仓位 × final_size_scalar
  - 确保 position_size × |entry - stop| / account_total <= 0.02
```

### 5.2 联动示例

```text
示例 1：攻击有持续，趋势跟踪

  环境：
    - regime_state = ATTACK_SUSTAINED
    - pq_position_max_size = 1.0
    - market_cap = 300亿（中盘股，target_vol = 15%）
    - current_vol = 12%（NORMAL_VOL）
    - trade_log: 30 笔，胜率 50%，盈亏比 1.5
    - entry_price = 100，stop_loss = 95，account_total = 1,000,000
  
  计算：
    1. Van Tharp: risk = 5 × shares / 1,000,000 ≤ 0.02 → max_shares = 4000
    2. Kelly: f* = (0.5×1.5 - 0.5)/1.5 = 0.167 → 半凯利 = 0.083 → T+1 惩罚 = 0.083×0.8 = 0.066
    3. VolTarget: scalar = 0.15/0.12 = 1.25 → NORMAL_VOL 无限制 → 1.25
    4. PeriodQueen: max = 1.0
    5. final = min(0.066, 1.25, 1.0) = 0.066
    6. position_size = 0.066 × 标准仓位（如 10% 账户）= 0.66% 账户
    7. shares = 0.0066 × 1,000,000 / 100 = 66 股
    8. 检查 Van Tharp: 5 × 66 / 1,000,000 = 0.033% < 2% → PASS

  结论：实际仓位只有 0.66%，非常保守。这是因为 Kelly 的胜率 50% 较低，导致 f* 很小。
  若胜率提升到 60%，盈亏比 2.0：
    Kelly: f* = (0.6×2 - 0.4)/2 = 0.4 → 半凯利 = 0.2 → T+1 = 0.16
    final = min(0.16, 1.25, 1.0) = 0.16
    position_size = 1.6% 账户 → 更合理

示例 2：孕化期，试错建仓

  环境：
    - regime_state = GESTATION
    - pq_position_max_size = 0.3
    - market_cap = 20亿（小盘股，target_vol = 20%）
    - current_vol = 25%（HIGH_VOL）
    - trade_log: 15 笔（<30），使用默认半凯利 f* = 0.25
    - 模式：quarter_kelly（孕化期保守）
  
  计算：
    1. Van Tharp: max_shares = 4000（同上）
    2. Kelly: f* = 0.25（默认）→ 四分之一凯利 = 0.0625 → T+1 = 0.05
    3. VolTarget: scalar = 0.20/0.25 = 0.8 → HIGH_VOL 限制 → 0.5
    4. PeriodQueen: max = 0.3
    5. final = min(0.05, 0.5, 0.3) = 0.05
    6. position_size = 0.5% 账户
  
  结论：孕化期 + 高波动 + 历史不足 → 仓位极低（0.5%），符合保守原则。

示例 3：余温期，逐步退出

  环境：
    - regime_state = REMAINING_WARMTH
    - pq_position_max_size = 0.0
    - 已有持仓：盈利 2R
  
  计算：
    1. PeriodQueen: EXIT_ONLY → 禁止新入场
    2. VolTarget: 强制 scalar = 0.5（降仓 50%）
    3. Kelly: 危机模式 → 不新增
    4. 操作：卖出 50% 持仓，剩余 50% 移动止盈
```

---

## 6. 三层风控的互锁规则

### 6.1 与 PERIOD_QUEEN 的互锁

```text
互锁规则 RISK × PERIOD_QUEEN：

1. 状态限制：
   - ATTACK_SUSTAINED: Kelly 半凯利，VolTarget 正常
   - ATTACK_CONFIRMED: Kelly 半凯利，VolTarget 正常
   - POWER_TRANSITION: Kelly 四分之一凯利，VolTarget × 0.7
   - GESTATION: Kelly 四分之一凯利，VolTarget × 0.8
   - REMAINING_WARMTH: Kelly 危机模式，VolTarget 强制 × 0.5
   - ATTACK_UNSUSTAINED / CUTTING_COMPLETE: Kelly 危机模式，VolTarget HALT_NEW

2. 紧急状态：
   - PeriodQueen 检测到 "极端市场"（千股涨停/跌停）→ Van Tharp 风险上限临时降至 1%
   - PeriodQueen 状态频繁切换（2 日内切换 2 次以上）→ Kelly 强制使用四分之一凯利
```

### 6.2 与 VOLFAC 的互锁

```text
互锁规则 RISK × VOLFAC：

1. 波动率状态联动：
   - VOLFAC EXTREME_VOL → VolTarget scalar = 0.2，Kelly 强制四分之一凯利
   - VOLFAC HIGH_VOL → VolTarget scalar < 0.5，Kelly 半凯利
   - VOLFAC LOW_VOL → VolTarget scalar > 1.0，Kelly 半凯利（允许加仓）

2. 小盘股特殊处理：
   - 小盘股（<50亿）volfac_annualized_vol 通常 > 50%
   - target_vol 提高到 20%（而非默认 10%）
   - 但 VolTarget scalar 仍可能 < 1.0（因为 20%/50% = 0.4）
```

### 6.3 与 CHZL_BSD 的互锁

```text
互锁规则 RISK × CHZL_BSD：

1. 止损位置与 Van Tharp：
   - CHZL_BSD 的止损位置（bi.low - 0.5ATR / prev_low - 0.2ATR / zs.zd - 0.1ATR）
   - 必须满足：|entry - stop| × position_size / account_total ≤ 0.02
   - 若止损太宽（如小盘股 bi.low 很远）→ 降低 position_size 以满足 Van Tharp

2. 移动止盈与 Kelly：
   - 盈利达到 1R 后，Kelly 允许重新评估仓位（可能加仓或减仓）
   - 盈利达到 2R 后，Kelly 建议止盈一半（与 GAS "进退有度" 一致）
```

---

## 7. 风控触发日志与审计

### 7.1 风控日志字段

```text
risk_audit_log 字段：
  - timestamp: 风控检查时间戳
  - trade_id: 交易标识
  - van_tharp_pass: BOOL
  - van_tharp_risk_pct: FLOAT
  - kelly_f_star: FLOAT
  - kelly_size_scalar: FLOAT
  - kelly_mode: ENUM
  - kelly_crisis: BOOL
  - vt_scalar: FLOAT
  - vt_size_scalar: FLOAT
  - vt_vol_regime: ENUM
  - pq_position_max_size: FLOAT
  - final_size_scalar: FLOAT
  - abort_reason: STRING（若 ABORT）
  - triggered_risk_layer: STRING（触发风控的层级："van_tharp" / "kelly" / "voltarget" / "period_queen"）
```

### 7.2 风控复盘规则

```text
每日复盘：
  1. 统计当日风控触发次数（按层级分类）
  2. 统计 Van Tharp 触发原因（风险过高 / 总风险超限）
  3. 统计 Kelly 模式分布（半凯利 / 四分之一凯利 / 危机模式）
  4. 统计 VolTarget 调制分布（加仓 / 正常 / 降仓 / 极端降仓）
  5. 检查是否有频繁 ABORT 的情况（可能意味着参数过紧）

每周复盘：
  1. 检查 Kelly 的 f* 趋势（是否持续下降？若是，可能需要调整策略）
  2. 检查 VolTarget 的 scalar 分布（是否大部分时间 < 0.5？若是，可能 target_vol 设置过高）
  3. 检查 Van Tharp 的实际风险分布（是否接近 2% 上限？若是，说明仓位利用率高）
```

---

## 8. 对编程 AI 的实现要求

### 8.1 风控联动引擎

```python
class RiskArchitectureEngine:
    """
    三层风控联动引擎
    """
    
    def __init__(self, account_total):
        self.account_total = account_total
        self.risk_log = []
    
    def calculate_final_position(self, entry_price, stop_loss, trade_log, 
                                  volfac_data, market_cap, regime_state,
                                  existing_positions=None):
        """
        计算最终仓位（三层风控联动）
        
        返回:
            final_size_scalar, position_size, abort_reason
        """
        # 第一层：Van Tharp 检查
        van_tharp = self.van_tharp_check(entry_price, stop_loss, existing_positions)
        if not van_tharp['van_tharp_pass']:
            return 0.0, 0, van_tharp['van_tharp_action']
        
        # 第二层：Kelly 计算
        kelly = self.kelly_calculate(trade_log, regime_state)
        
        # 第三层：VolTarget 计算
        voltarget = self.voltarget_calculate(volfac_data, market_cap, regime_state)
        
        # PeriodQueen 上限
        pq_max = self.get_pq_max_size(regime_state)
        
        # 最终仓位
        final_scalar = min(
            kelly['kelly_size_scalar'],
            voltarget['vt_size_scalar'],
            pq_max,
            1.0
        )
        
        # 检查仓位过小
        if final_scalar <= 0.05:
            return 0.0, 0, "position_too_small"
        
        # 计算实际股数
        max_shares = van_tharp['max_shares']
        standard_position = self.account_total * 0.10  # 假设标准仓位 10%
        position_value = standard_position * final_scalar
        shares = int(position_value / entry_price)
        
        # 确保不超过 Van Tharp 允许上限
        shares = min(shares, max_shares)
        
        # 记录日志
        self.risk_log.append({
            "van_tharp": van_tharp,
            "kelly": kelly,
            "voltarget": voltarget,
            "final_scalar": final_scalar,
            "shares": shares,
        })
        
        return final_scalar, shares, None
```

---

> 文件：RISK_ARCHITECTURE_P0_R_v1.0.md
> 生产者：Kimi
> 状态：风控层核心文档，可直接转化为代码
> 核心交付：
> - 三层风控的详细定义（Van Tharp / Kelly / VolTarget）
> - 联动公式：final_size_scalar = min(kelly, voltarget, pq_max, 1.0)
> - 每个层级的伪代码实现
> - 联动示例（攻击有持续 / 孕化期 / 余温期）
> - 与 PeriodQueen / VOLFAC / CHZL_BSD 的互锁规则
> - 风控日志与审计规范
> - RiskArchitectureEngine 类伪代码
