# GLM_DELIVERY_09_A股跨市场适配审计与因子提取_v1.0.md

> 任务编号：GLM_TASK_09  
> 生产者：GLM  
> 来源：GLM_TASK_09 指令 + 现有仓库状态 [9][14][21]  
> 状态：已接收，待 Kimi 审核入库  
> 时间：2026-06-24

---

# 第一部分：A 股适配审计表 (9 个已冻结对象)

| 对象 ID | 对象名称 | A 股可用性 | 核心冲突点 (A 股特色) | 必须修改/新增字段 | 建议动作 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **KELLY_P0_R**<br>[10] | 凯利准则 | ⚠️ **需大幅修正** | **T+1 机制**：无法当日止损，导致实际风险远高于计算值。<br>**涨跌停限制**：价格被锁死，无法执行“再平衡”操作。 | 新增 `t1_penalty_factor` (建议 0.8)<br>新增 `limit_up/down_freeze_flag` | **降级使用**：强制使用半凯利 (Half-Kelly) 或四分之一凯利；单票仓位硬顶设为 20% [10]。 |
| **VOLTARGET_P0_R**<br>[11] | 波动率目标 | ✅ **高可用** (需微调) | **ATR 失真**：连续涨跌停会导致 ATR 极度压缩，误判为低波动而重仓。<br>**隔夜跳空**：集合竞价跳空导致开盘波动率剧增。 | 新增 `limit_atr_corrector` (剔除涨跌停日)<br>新增 `overnight_gap_adjustment` | **必须实现**：ATR 计算器需包含“非自然交易日”过滤逻辑 [11]。 |
| **VP_P0_E**<br>[12] | 成交量分布 | ✅ **高可用** | **T+1 导致的成交意愿扭曲**：散户因无法卖出而在尾盘挂单，导致尾盘 HVN 人为放大。<br>**庄家对倒**：某些小盘股 VP 形态可能是人为画出来的。 | 新增 `volume_integrity_score` (基于换手率/自由流通盘) | **谨慎使用**：仅用于大盘股或 ETF；小盘股 VP 需配合龙虎榜数据验证 [13]。 |
| **CHZL_BSD**<br>[2][8] | 缠论买卖点 | ⚠️ **中等可用** | **分型包含处理失效**：一字涨停板被视为一根 K 线，破坏了分型序列的连续性。<br>**笔的中断**：停牌导致笔的时间跨度失真。 | 新增 `suspend_merge_logic` (复牌后 K 线特殊处理)<br>新增 `limit_fractal_type` (涨停板分型) | **增加过滤器**：在出现买卖点信号时，检查是否处于“异常波动期”（如连板后）。 |
| **YTC_P0_E**<br>[15] | YTC 微观结构 | ⚠️ **受限** | **T+1 导致无法盘中止损**：TST (Test) 策略一旦触发，若当日无法平仓，风险敞口极大。<br>**整数关口效应**：A 股散户心理价位 (10, 20元) 产生强 S/R，比外盘更明显。 | 新增 `integer_level_s_r` (自动检测整数位阻力)<br>修改 `tst_stop_loss` 为 `next_day_open_limit` | **调整周期**：建议 YTC 信号仅用于 **日线/周线级别**，放弃日内 TST 操作 [15]。 |
| **BPB_P0_E**<br>[16] | Brooks 回调 | ⚠️ **受限** | **假突破频繁**：游资“一日游”行情导致突破后次日直接低开（跳空破位），BPB 失效。<br>**流动性陷阱**：小盘股突破后无量回调，无法成交。 | 新增 `gap_down_destroyer` (跳空破位检测)<br>新增 `liquidity_filter` (平均成交额 > 5000万) | **加强过滤**：要求突破日必须有 **放量** (Volume > 20日均量 * 1.5)，且非“一字板” [16]。 |
| **TKR7_P0_E**<br>[17] | AO 背离 | ✅ **完全兼容** | 无重大冲突。AO 指标基于价格均线，不受 T+1 影响。 | 无 | **直接使用**。 |
| **MFLOW_P0_A**<br>[9][14] | 资金流向 | 🆕 **待开发** | **北向资金 vs 内资**：A 股资金面割裂，需区分陆股通和内资机构行为。<br>**龙虎榜滞后**：数据 T+1 公布，无法用于实时决策。 | 待 GLM Task 07 交付 [9][21]。 | **作为选股层 (P0_A)** 使用，而非实时执行层。 |
| **VOLFAC_P0_A**<br>[9][14] | 波动率因子 | 🆕 **待开发** | **小盘股高波特性**：A 股小盘股波动率显著高于价值股，需分层处理。 | 待 GLM Task 07 交付 [9][21]。 | **作为选股层 (P0_A)** 使用，辅助 VolTarget 进行资产配置。 |

---

# 第二部分：S_BUCKET 可落地因子提取表

| 因子名称 | 来源 ID | 因子逻辑摘要 | 所需数据 | 可落地性 | 与现有对象关系 | 替代/互补对象 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **mfd_sellord**<br>(主力流出单数) | SBKT_F014<br>[21] | 统计大单卖出笔数占比。若该值异常升高，预示主力出逃。 | Wind 资金流向<br>(超大单/大单) | ✅ **高**<br>(常规数据) | **互补**：<br>KD MTF 给出买入信号时，若此因子显示主力流出，则**拒绝入场** (NOISE_IGNORE)。 | PV Corr (价量相关)<br>(若价升量缩且主力流出，则是危险信号) |
| **mfd_volinflowrate_open_m**<br>(开盘资金流入率) | SBKT_F014<br>[21] | 集合竞价阶段(9:25-9:30)的资金净流入占全天比例。反映早盘意图。 | Wind 分时资金流<br>(需分钟级) | ✅ **中**<br>(需分钟数据) | **互补**：<br>若 TK-CB (Closing Break) 信号触发，且此因子显示早盘抢筹明显，则增强信心。 | TK-IB (Inside Bar)<br>(结合开盘幅度判断) |
| **id2_std_3m**<br>(3个月收益率标准差) | SBKT_F006<br>[21] | 过去 60 个交易日的日收益率标准差。衡量个股波动率。 | 日收盘价 | ✅ **极高**<br>(基础计算) | **重叠/替代**：<br>这是 **VolTarget** 的核心输入参数。可直接作为 VOLFAC_P0_A 的主因子。 | Volty (已有)<br>VOLTARGET_P0_R |
| **hml_r_std_5m**<br>(5分钟高频波动率) | SBKT_F006<br>[21] | 基于 5 分钟高频数据的已实现波动率。捕捉日内突发波动。 | Level-2 或<br>5分钟 OHLC | ⚠️ **低**<br>(需高频数据) | **补充**：<br>用于日内 TK 策略的 **R8 (资格过滤)**。若日内波动率过高，暂停开仓。 | TK-R8 (B区域Qualify) |
| **inst_hold_ratio_chg**<br>(机构持仓变动) | SBKT_F007<br>[21] | 季报披露的基金/社保持仓比例变化。捕捉机构抱团/离散趋势。 | 季报/基金持仓<br>(季频更新) | ✅ **中**<br>(数据滞后) | **独立维度**：<br>作为 **P0_A 选股池** 的硬性门槛（如：只买机构季度加仓股）。 | 冯柳弱者体系<br>(逆向寻找机构抛售的错杀股) |
| **north_net_inflow**<br>(北向资金净流入) | 搜索补充<br>[13] | 陆股通每日净买入金额。聪明钱的短期风向标。 | 陆股通数据<br>(日频) | ✅ **高**<br>(公开数据) | **宏观过滤**：<br>若北向资金连续 3 日大幅流出，全局降低 **Kelly 仓位系数** (如 × 0.7)。 | KELLY_P0_R |

---

# 第三部分：A 股特殊规则字段化建议

## 1. 全局配置字段

```python
# 在 config.py 或 constants.py 中新增
class AStockConfig:
    # --- 交易机制约束 ---
    T_PLUS_ONE_ENABLED = True          # 启用 T+1 惩罚
    T1_PENALTY_FACTOR = 0.8            # Kelly 减少系数
    
    # --- 价格限制约束 ---
    LIMIT_UP_THRESHOLD = 1.099         # 涨停阈值 (10% or 20%)
    LIMIT_DOWN_THRESHOLD = 0.901       # 跌停阈值
    USE_LIMIT_CORRECTED_ATR = True     # 是否启用修正后的 ATR
    
    # --- 流动性与情绪约束 ---
    MIN_AVG_AMOUNT_CNY = 50_000_000    # 最小日均成交额 (5000万)
    INTEGER_LEVEL_SENSITIVITY = True   # 是否开启整数关口敏感度
```

## 2. 关键过滤器伪代码

### 过滤器 A: 涨跌停保护 (用于所有执行层对象)

```python
FUNCTION AStock_LimitFilter(current_bar, prev_bar):
    """
    目的: 防止在涨跌停板上发出错误信号 (如 IB/CB/BSD)
    输入: 当前K线, 前一K线
    输出: {valid: bool, reason: string}
    """
    
    # 1. 检测是否物理涨停/跌停
    is_limit_up = (current_bar.close >= current_bar.high * 0.999) AND \
                  (current_bar.close >= prev_bar.close * LIMIT_UP_THRESHOLD)
                  
    is_limit_down = (current_bar.close <= current_bar.low * 1.001) AND \
                    (current_bar.close <= prev_bar.close * LIMIT_DOWN_THRESHOLD)

    IF is_limit_up OR is_limit_down:
        RETURN {valid: False, reason: "PRICE_LIMIT_LOCKED"}
        
    # 2. 检测 "一字板" (无实体)
    if abs(current_bar.open - current_bar.close) < 0.001 * current_bar.open:
        if current_bar.limit_up: # 假设有此字段
             RETURN {valid: False, reason: "ZI_ZI_BOARD"}

    RETURN {valid: True, reason: "OK"}
```

### 过滤器 B: A 股情绪/资金综合门控 (用于 KD MTF Lock Signal)

```python
FUNCTION AStock_SentimentGate(lock_signal, mfd_sellord, north_net_flow):
    """
    目的: 在 KD MTF 发出 PERFECT_LONG 后，用 A 股特色因子进行二次确认
    输入: 原始 lock_signal, 主力流出因子, 北向资金
    输出: 最终 signal
    """
    
    IF lock_signal == 'PERFECT_LONG':
        # 规则 1: 主力资金背离检查
        IF mfd_sellord > MFD_SELLORD_THRESHOLD: # 阈值需回测确定
            RETURN 'DOWNGRADE_TO_WATCH' # 降级为观察，不开仓
            
        # 规则 2: 北向资金环境检查 (可选，用于风控)
        IF north_net_flow < NORTH_FLOW_DANGER_LINE:
            RETURN 'REDUCE_POSITION_SIZE' # 允许开仓，但减半
            
    RETURN lock_signal
```

### 3. 行业轮动字段化草案 (预留接口)

```sql
-- 在 stock_pool 表中新增字段
ALTER TABLE stock_pool ADD COLUMN sector_beta_exposure FLOAT DEFAULT 0; -- 行业Beta暴露
ALTER TABLE stock_pool ADD COLUMN style_factor VARCHAR(20) DEFAULT 'NEUTRAL'; -- 风格标签(LARGE/GROWTH/VALUE等)

-- 使用示例:
-- 当 KD MTF 信号出现时，检查当前持仓的行业集中度
-- IF SUM(sector_beta_exposure FOR Tech Stocks) > 0.6 -> 拒绝新的科技股买入信号 (分散化风控)
```

---

# 总结与下一步行动

1. **立即执行**：将 **第一部分的审计表** 下发给开发团队，要求他们对现有的 `KELLY`, `VOLTARGET`, `VP` 等模块添加 `AStockConfig` 适配开关。
2. **并行推进**：基于 **第二部分的因子表**，开始编写 `MFLOW_P0_A` 和 `VOLFAC_P0_A` 的数据清洗脚本（ETL），从 Wind/数据库中提取 `mfd_sellord` 和 `id2_std_3m` 数据。
3. **集成测试**：在回测框架 [5] 中加入 `AStock_LimitFilter`，观察其在 2024 年 A 股行情中对胜率的提升效果（预期可减少约 10%-15% 的无效交易）。

---

> 文件：GLM_DELIVERY_09_A股跨市场适配审计与因子提取_v1.0.md  
> 生产者：GLM 交付，Kimi 格式化审核  
> 状态：已接收，建议入库
