# INSTB_P0_A — 机构行为因子（Institutional Behavior）对象卡

> 功能层：P0_A（选股层 / 方法层）  
> 成熟度：needs_extra_data（季频滞后，数据获取成本高）  
> 生产者：Kimi（基于 SBKT_F007 + GLM_DELIVERY_09 提取）  
> 来源：华泰证券《多因子系列 8：单因子测试之机构行为因子》  
> 状态：已冻结核心字段，标记为 needs_extra_data，仅作为方法层参考

---

## 1. 基本定义

机构行为因子（Institutional Behavior）通过分析 **机构投资者持仓变动**，识别机构资金动向。A 股机构投资者包括：公募基金、私募基金、社保基金、QFII、保险资金、券商自营等。

**核心洞察**：机构持仓变动反映专业投资者的判断，但数据**严重滞后**（季报披露），且只能看到季度末快照，无法捕捉实时调仓行为。

**SBKT_F007 固化结论**：
- 核心因子：`instb_holder_change_pct`（机构持仓变动百分比）
- 持仓调整期：约 30 个交易日（一个半月）
- 数据频率：季频（每季度末披露）
- 滞后性：数据公布时，机构可能已调仓完毕
- **功能定位**：方法层参考（判断机构整体偏好），不适合实时执行层

---

## 2. 核心概念与字段冻结

### 2.1 基础字段（原始数据输入，需季报数据）

```text
instb_fund_holding_pct        FLOAT   -- 公募基金持仓占比（季度末）
instb_social_security_pct     FLOAT   -- 社保基金持仓占比（季度末）
instb_qfii_pct                FLOAT   -- QFII 持仓占比（季度末）
instb_insurance_pct           FLOAT   -- 保险资金持仓占比（季度末）
instb_broker_self_pct         FLOAT   -- 券商自营持仓占比（季度末）
instb_total_inst_pct          FLOAT   -- 机构总持仓占比（季度末）
instb_prev_quarter_total      FLOAT   -- 上季度机构总持仓占比
instb_shareholder_count       INT     -- 股东户数（季度末）
instb_prev_shareholder_count  INT     -- 上季度股东户数
```

### 2.2 核心因子字段（已冻结）

```text
instb_holder_change_pct     FLOAT   -- 机构持仓变动百分比（核心因子）：
                                        -- = (本季度机构总持仓 - 上季度机构总持仓) / 上季度机构总持仓
                                        -- 正值 = 机构增持，负值 = 机构减持
                                        -- SBKT_F007 核心因子：持仓调整期约 30 个交易日
                                        -- 但数据严重滞后，实时性差

instb_concentration_change  FLOAT   -- 筹码集中度变化：
                                        -- = 上季度股东户数 / 本季度股东户数
                                        -- > 1.0 = 筹码集中（散户减少，机构吸筹）
                                        -- < 1.0 = 筹码分散（散户增加，机构派发）
                                        -- 与 MFLOW 的主力流入因子互补（信息源不同）

instb_fund_flow_trend       ENUM    -- 基金流向趋势：
                                        -- 'STRONG_INFLOW' = 公募基金大幅增持（>5%）
                                        -- 'MODERATE_INFLOW' = 公募基金小幅增持（2%-5%）
                                        -- 'STABLE' = 持仓变化不大（-2% 到 +2%）
                                        -- 'MODERATE_OUTFLOW' = 公募基金小幅减持（-2% 到 -5%）
                                        -- 'STRONG_OUTFLOW' = 公募基金大幅减持（<-5%）
```

### 2.3 派生字段（计算后）

```text
instb_data_lag_days         INT     -- 数据滞后天数：
                                        -- 季报披露截止日 - 当前日期
                                        -- 通常 45-90 天（季报披露有 1 个月窗口期）
                                        -- 滞后 > 60 天 → 数据可信度低

instb_signal_freshness      ENUM    -- 信号新鲜度：
                                        -- 'FRESH' = 季报刚披露（< 15 天），数据最新
                                        -- 'STALE' = 季报披露已有一段时间（15-45 天）
                                        -- 'OUTDATED' = 季报披露已久（> 45 天），数据可能已失效

instb_composite_score       FLOAT   -- 机构行为综合评分（0.0-1.0）：
                                        -- 综合持仓变动、筹码集中度、基金流向趋势
                                        -- 高值 = 机构整体看好，但信号滞后
                                        -- 低值 = 机构整体看空，但信号滞后
```

### 2.4 信号字段（已冻结，标记为方法层）

```text
instb_signal_type           ENUM    -- 机构行为信号：
                                        -- 'NONE' = 无信号（数据滞后过久）
                                        -- 'INST_ACCUMULATION' = 机构吸筹（持仓增加 + 筹码集中）
                                        -- 'INST_DISTRIBUTION' = 机构派发（持仓减少 + 筹码分散）
                                        -- 'FUND_INFLOW' = 基金流入（公募基金大幅增持）
                                        -- 'FUND_OUTFLOW' = 基金流出（公募基金大幅减持）

instb_kd_filter_action      ENUM    -- 对 KD MTF 信号的操作：
                                        -- 'PASS' = 通过（默认，因数据滞后，不干预实时信号）
                                        -- 'CONTEXT_ONLY' = 仅作为背景信息（不直接干预交易）
                                        -- 注：INSTB 不直接阻断或增强 KD 信号，只提供背景判断

instb_method_layer_use      ENUM    -- 方法层使用方式：
                                        -- 'SECTOR_PREFERENCE' = 判断机构对某行业的整体偏好
                                        -- 'STOCK_SCREENING' = 作为选股池的初步过滤（季频）
                                        -- 'TREND_CONFIRMATION' = 作为趋势的辅助确认（滞后确认）
                                        -- 'RISK_WARNING' = 作为风险预警（机构大幅减持时）
```

---

## 3. 计算逻辑（伪代码）

### 3.1 核心因子计算（季频数据）

```python
def calculate_institutional_behavior(quarterly_data, current_date):
    """
    计算机构行为因子
    
    参数:
        quarterly_data: dict with [instb_total_inst_pct, instb_prev_quarter_total,
                                     instb_shareholder_count, instb_prev_shareholder_count,
                                     instb_fund_holding_pct, prev_quarter_fund_pct,
                                     report_date]  # 季报披露日期
        current_date: datetime  # 当前日期
    
    返回:
        dict with instb_* fields
    """
    from datetime import datetime
    
    # 1. 机构持仓变动百分比
    instb_holder_change_pct = (
        (quarterly_data['instb_total_inst_pct'] - quarterly_data['instb_prev_quarter_total']) /
        quarterly_data['instb_prev_quarter_total']
    )
    
    # 2. 筹码集中度变化
    instb_concentration_change = (
        quarterly_data['instb_prev_shareholder_count'] / quarterly_data['instb_shareholder_count']
    )
    
    # 3. 基金流向趋势
    fund_change = quarterly_data['instb_fund_holding_pct'] - quarterly_data['prev_quarter_fund_pct']
    if fund_change > 0.05:
        instb_fund_flow_trend = 'STRONG_INFLOW'
    elif fund_change > 0.02:
        instb_fund_flow_trend = 'MODERATE_INFLOW'
    elif fund_change > -0.02:
        instb_fund_flow_trend = 'STABLE'
    elif fund_change > -0.05:
        instb_fund_flow_trend = 'MODERATE_OUTFLOW'
    else:
        instb_fund_flow_trend = 'STRONG_OUTFLOW'
    
    # 4. 数据滞后天数
    report_date = datetime.strptime(quarterly_data['report_date'], '%Y-%m-%d')
    instb_data_lag_days = (current_date - report_date).days
    
    # 5. 信号新鲜度
    if instb_data_lag_days < 15:
        instb_signal_freshness = 'FRESH'
    elif instb_data_lag_days < 45:
        instb_signal_freshness = 'STALE'
    else:
        instb_signal_freshness = 'OUTDATED'
    
    # 6. 综合评分（仅 FRESH 和 STALE 时有效）
    instb_composite_score = 0.0
    if instb_signal_freshness in ['FRESH', 'STALE']:
        instb_composite_score = (
            max(0, instb_holder_change_pct) * 0.4 +  # 持仓增加 = 看好
            max(0, instb_concentration_change - 1) * 0.3 +  # 筹码集中 = 吸筹
            (1 if instb_fund_flow_trend in ['STRONG_INFLOW', 'MODERATE_INFLOW'] else 0) * 0.3
        )
        instb_composite_score = min(1.0, instb_composite_score)
    
    # 7. 信号类型
    instb_signal_type = 'NONE'
    if instb_signal_freshness in ['FRESH', 'STALE']:
        if instb_holder_change_pct > 0.05 and instb_concentration_change > 1.1:
            instb_signal_type = 'INST_ACCUMULATION'
        elif instb_holder_change_pct < -0.05 and instb_concentration_change < 0.9:
            instb_signal_type = 'INST_DISTRIBUTION'
        elif instb_fund_flow_trend in ['STRONG_INFLOW', 'MODERATE_INFLOW']:
            instb_signal_type = 'FUND_INFLOW'
        elif instb_fund_flow_trend in ['STRONG_OUTFLOW', 'MODERATE_OUTFLOW']:
            instb_signal_type = 'FUND_OUTFLOW'
    
    return {
        'instb_holder_change_pct': round(instb_holder_change_pct, 4),
        'instb_concentration_change': round(instb_concentration_change, 4),
        'instb_fund_flow_trend': instb_fund_flow_trend,
        'instb_data_lag_days': instb_data_lag_days,
        'instb_signal_freshness': instb_signal_freshness,
        'instb_composite_score': round(instb_composite_score, 4),
        'instb_signal_type': instb_signal_type,
    }
```

### 3.2 方法层使用（不直接干预交易）

```python
def apply_institutional_method_layer(factors, sector_data):
    """
    机构行为因子的方法层使用
    
    核心原则：
    - INSTB 不直接干预 KD/缠论/TK 等执行层信号
    - 仅作为背景信息，辅助判断行业偏好和选股池构建
    """
    
    method_use = 'CONTEXT_ONLY'
    
    # 1. 行业偏好判断
    if factors['instb_signal_freshness'] == 'FRESH':
        # 季报刚披露，数据可靠，可用于行业偏好判断
        if factors['instb_signal_type'] == 'FUND_INFLOW':
            method_use = 'SECTOR_PREFERENCE'
            # 记录：该行业受到机构青睐，可作为选股池优先方向
        elif factors['instb_signal_type'] == 'FUND_OUTFLOW':
            method_use = 'RISK_WARNING'
            # 记录：该行业被机构减持，需警惕
    
    # 2. 选股池初步过滤（季频）
    if factors['instb_composite_score'] > 0.7 and factors['instb_signal_freshness'] == 'FRESH':
        # 机构高度看好 + 数据新鲜 → 纳入优先选股池
        method_use = 'STOCK_SCREENING'
    elif factors['instb_composite_score'] < 0.3 and factors['instb_signal_freshness'] == 'FRESH':
        # 机构大幅看空 + 数据新鲜 → 从选股池剔除
        method_use = 'STOCK_SCREENING'
    
    # 3. 趋势滞后确认
    # 当 KD/缠论发出买入信号时，如果 INSTB 显示机构在吸筹 → 增强信心（但不直接干预）
    # 当 KD/缠论发出卖出信号时，如果 INSTB 显示机构在派发 → 增强信心（但不直接干预）
    if factors['instb_signal_type'] == 'INST_ACCUMULATION':
        method_use = 'TREND_CONFIRMATION'
    
    return {
        'instb_kd_filter_action': 'PASS',  # 不直接干预 KD 信号
        'instb_method_layer_use': method_use,
    }
```

---

## 4. 与现有指标的互锁逻辑（已冻结）

### 4.1 与 KD MTF 的互锁（方法层）

```text
互锁规则 INSTB × KD MTF（方法层，不直接干预）：

1. 背景信息协同：
   - KD 发出 PERFECT_LONG 且 instb_signal_type = 'INST_ACCUMULATION' → 背景有利，但不增强信号
   - KD 发出 PERFECT_LONG 且 instb_signal_type = 'INST_DISTRIBUTION' → 背景不利，但不阻断信号
   - 原因：INSTB 数据滞后，不能干预实时执行层

2. 季度调仓窗口：
   - 季报披露期（1-4月、4-7月、7-10月、10-1月）→ 机构调仓行为可能变化
   - 此时 INSTB 数据可能快速失效，标记为 'REBALANCING_PERIOD'
```

### 4.2 与 MFLOW 的互锁

```text
互锁规则 INSTB × MFLOW：

1. 信息互补：
   - MFLOW：实时资金流向（日频/分钟频）
   - INSTB：季度机构持仓（季频滞后）
   - 两者信息源不同，理论上可互补

2. 矛盾时的处理：
   - MFLOW 显示主力流入 + INSTB 显示机构减持 → 可能是短期资金炒作（非机构行为）
   - MFLOW 显示主力流出 + INSTB 显示机构增持 → 可能是机构在低位吸筹（但数据滞后）
   - 矛盾时，以 MFLOW（实时）为准，INSTB 仅作为背景参考
```

### 4.3 与 VOLFAC 的互锁

```text
互锁规则 INSTB × VOLFAC：

1. 机构调仓与波动率：
   - 机构大幅增持期（instb_holder_change_pct > 10%）→ 通常伴随波动率上升
   - 机构稳定持仓期 → 波动率通常较低
   - 可用于验证：机构行为是否导致波动率变化

2. 小盘股特殊性：
   - 小盘股机构持仓变动对波动率影响更大（流动性差）
   - 大盘股机构持仓变动对波动率影响较小（流动性好）
```

### 4.4 与缠论 BSD 的互锁（方法层）

```text
互锁规则 INSTB × CHZL_BSD（方法层）：

1. 1Buy 与机构吸筹：
   - BSD 1Buy（背驰） + INSTB 显示机构吸筹 → 背景有利，可能是机构在低位建仓
   - 但不改变 1Buy 的止损位置（执行层独立）

2. 3Buy 与机构增仓：
   - BSD 3Buy（离开中枢） + INSTB 显示机构增仓 → 背景有利，趋势可能加速
   - 但 3Buy 的止损仍为 prev_low - 0.2ATR（执行层独立）
```

---

## 5. 失效模式（已冻结）

```text
INSTB 失效条件：

1. 数据严重滞后（核心失效）：
   - 季报数据滞后 45-90 天 → 实时性差
   - 机构可能在数据披露前已调仓完毕
   - 应对：标记为 needs_extra_data，仅作为方法层参考

2. 季报披露窗口期：
   - 1-4月（年报）、4-7月（一季报）、7-10月（半年报）、10-1月（三季报）
   - 披露窗口期内数据快速变化，INSTB 信号可能失效
   - 应对：披露窗口期内，INSTB 信号降级为 'REBALANCING_PERIOD'

3. 机构类型差异：
   - 公募基金（追求相对收益） vs 社保基金（追求绝对收益）行为不同
   - 简单汇总可能掩盖机构间的分歧
   - 应对：按机构类型分别计算（未来扩展）

4. 北向资金 vs 内资机构：
   - 北向资金（外资）与内资机构行为可能相反
   - 当前 INSTB 主要统计内资机构，北向资金需单独处理
   - 应对：未来扩展北向资金因子
```

---

## 6. 成熟度与数据需求

| 维度 | 评估 |
|------|------|
| **所需数据** | 季报机构持仓数据（Wind/同花顺 F10） |
| **计算复杂度** | 极低（简单比率计算） |
| **实时性能** | 极差（季频滞后 45-90 天） |
| **回测可行性** | 高（季报历史数据完整） |
| **A 股落地** | 方法层可用，执行层不可用（数据滞后） |
| **外汇/期货/币圈落地** | 不适用（无"机构持仓"概念） |
| **跨周期** | 季频为主，不适合日频/分钟频 |

---

## 7. 使用建议

| 场景 | 建议 |
|------|------|
| 实时交易执行 | ❌ 不使用（数据滞后） |
| 选股池构建 | ⚠️ 季频参考，结合 MFLOW 实时数据 |
| 行业偏好判断 | ✅ 季报披露后 15 天内有效 |
| 趋势背景确认 | ✅ 作为辅助信息，不干预执行层 |
| 风险预警 | ✅ 机构大幅减持时作为风险提示 |

---

> 文件：OBJECT_CARD_INSTB_P0_A__InstitutionalBehavior_v1.0.md  
> 生产者：Kimi  
> 状态：已冻结核心字段，标记为 needs_extra_data，仅作为方法层参考
