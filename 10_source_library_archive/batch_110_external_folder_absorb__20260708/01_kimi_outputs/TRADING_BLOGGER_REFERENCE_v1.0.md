# 交易博主视频参考指南 — 对象卡体系对齐

> **版本**: v1.0  
> **日期**: 2026-07-07  
> **说明**: 按我们12张对象卡逐一匹配国内外可借鉴的交易博主视频资源，标注适合度与观看建议。

---

## 一、总体匹配原则

我们的系统特点是**对象化信号卡片 + 投票聚合**，不是单一方法打天下。因此参考博主时也按对象卡拆解学习，而非照搬某一个人的完整体系。

| 我们的对象卡 | 对应技术流派 | 国内博主 | 国外博主 |
|-------------|------------|---------|---------|
| PERIOD_QUEEN | 市场情绪/周期识别 | 淘股吧情绪周期帖 | Mark Minervini, Peter Brandt |
| VOLFAC/VOLTARGET | 波动率管理 | 较少 | Options Trading (TastyTrade) |
| CHZL_BSD | 缠论（分型/笔/中枢） | 谷粟、北斗解缠 | 无（中国特色） |
| BPB | 价格行为（突破回调） | 较少 | **Al Brooks**（核心参考） |
| TKR7 | AO/动量背离 | 较少 | **Linda Raschke** |
| MFLOW | 资金流向 | 东财/同花顺数据 | 较少 |
| INSTB | 机构行为/筹码 | 筹码分布教程 | 较少 |
| KELLY | 仓位管理 | 较少 | **Edward Thorp**（理论）、Kelly Criterion |
| VP | 成交量分布 | 德湃订单流 | **Trader Dale**、**Jigsaw Trading** |
| YTC | 微观结构/订单流 | 德湃订单流 | **Jigsaw Trading**、**Axia Futures** |
| ATRATIO | 活跃度/换手率 | A股打板族 | 较少 |

---

## 二、国内B站资源

### 2.1 缠论（CHZL_BSD_P0_E）— 高优先级

**推荐频道**（按体系完整度排序）：

| 博主 | 频道/内容 | 适合度 | 必看内容 | 注意点 |
|------|----------|--------|---------|--------|
| **谷粟** | 谷粟解禅 / 腾讯课堂 | ⭐⭐⭐⭐⭐ | 分型→笔→线段→中枢→三类买卖点 | 体系最完整，适合作为对象卡的标准化输入 |
| **北斗解缠** | B站合集"缠论笔、线段、中枢、背驰、买卖点详解" | ⭐⭐⭐⭐ | 8.5小时系统课程 | 讲解细致，适合零基础到精通 |
| **牛解缠论** | B站108课逐句讲解 | ⭐⭐⭐⭐ | 第47课、第67课、第98课 | 逐句解读原文，避免理解偏差 |
| **妙手缠君** | B站缠论系列 | ⭐⭐⭐ | 分型精讲、中枢划分 | 短视频形式，适合碎片学习 |
| **李晓军** | 简约缠论（45集） | ⭐⭐⭐⭐ | 中枢与级别 | 偏实战，减少哲学讨论 |
| **都业华** | 缠中说禅培训班 | ⭐⭐⭐ | 中枢、背驰 | 偏讲座风格，需筛选 |

**为什么适合我们的系统**：
- 缠论的分型/笔/中枢/买卖点结构天然是**对象化**的，可直接映射为 `CHZL_BSD_P0_E` 的输入/输出
- 三类买卖点（1Buy/2Buy/3Buy）可以直接输出为 `signal_type=BUY` 的不同强度等级
- 建议只看技术结构部分，忽略过多哲学/禅宗论述（我们的原则：哲学类归为 `NOT_QUANT_YET`）

**建议提取到我们对象卡的规则**：
```
底分型 = 中间K线低点最低 + 高点也低于两侧 → 1Buy候选
顶分型 = 中间K线高点最高 + 低点也高于两侧 → Sell候选（A股纯多头下降级）
中枢区间 = 三段重叠区域 → 支撑/阻力参考
背驰 = 价格新高 + MACD/面积未新高 → 2Buy/3Buy信号
```

---

### 2.2 成交量分布 + 订单流（VP_P0_E + YTC_P0_E）— 高优先级

**推荐频道**：

| 博主 | 频道 | 适合度 | 必看内容 | 注意点 |
|------|------|--------|---------|--------|
| **德湃订单流交易分享** | B站 | ⭐⭐⭐⭐ | Volume Profile指标用法、POC/VAH/VAL、异常成交 | 香港中文大学计量金融背景，偏学术化 |
| **量化姜太公** | B站 | ⭐⭐⭐ | 订单流逻辑、高频交易入门 | 内容较杂，需筛选 |
| **独醉or独醒** | B站 | ⭐⭐⭐ | 量价分析、供求法则、努力结果法则 | Wyckoff体系，可借鉴到YTC对象卡 |

**为什么适合**：
- VP对象卡的核心是 POC/VAH/VAL/HVN/LVN，这些在订单流视频中有标准教学
- YTC对象卡的微观结构（TST/BOF/BP/P）需要理解订单流背景
- **注意**：A股没有真实的DOM/Level-2逐笔数据，订单流教学中的很多工具（Footprint Chart、Delta）无法直接复现，需要降级为基于OHLCV的模拟实现

---

### 2.3 多因子/系统化（整体投票聚合思路）— 中优先级

**问题**：国内B站很少有**模块化多信号投票**的体系教学。大多数是：
- 单一指标教学（MACD、KDJ、布林等）
- 通达信公式推销
- 大而全的评分系统（与我们原则冲突）

**建议方向**：
- 不要试图在B站找"模块化对象卡"的现成教学，这个概念是我们自己构建的
- 可以借鉴的是**多周期共振**的思路（如"日线+60分钟+15分钟共振"），映射到我们的 `MTF_SEB`（多时间框架）对象卡

---

### 2.4 资金流向/机构行为（MFLOW_P0_A + INSTB_P0_A）— 低优先级

**推荐**：
- 东财、同花顺的**资金流向**页面直接看数据含义
- B站搜索"龙虎榜分析"、"北向资金"，但注意：
  - 大部分视频是**事后解释**而非**可量化规则**
  - 我们的原则：依赖龙虎榜/北向数据的条目标记为 `needs_extra_data`，不作为核心对象卡

---

## 三、国外YouTube资源

### 3.1 价格行为 — Al Brooks（BPB_P0_E 核心参考）— 最高优先级

| 资源 | 链接/搜索 | 适合度 | 必看内容 |
|------|----------|--------|---------|
| **Brooks Trading Course** | YouTube频道 + brookstradingcourse.com | ⭐⭐⭐⭐⭐ | 全部免费视频 |
| **Al Brooks: The Godfather of Price Action** | Podcast访谈（Tradacc） | ⭐⭐⭐⭐⭐ | 1小时系统讲解 |
| **Desire To Trade Podcast** | 第523期 Al Brooks专访 | ⭐⭐⭐⭐ | 40-60%概率世界、风险管理 |
| **UKSpreadBetting** | Al Brooks Trader Training Call | ⭐⭐⭐⭐ | 1小时实战问答 |

**为什么是最重要的外部参考**：
- Al Brooks是**突破回调（BPB）**方法的定义者，我们的 `BPB_P0_E` 对象卡直接基于他的体系
- 核心概念：`Low 1` / `Low 2` / `High 1` / `High 2` 信号条、通道、交易区间
- 回调到38.2%/50%/61.8%的二次入场，与我们的Fib区域检测直接对应

**建议提取规则**：
```
突破后第一腿回调（1-legged pullback）= 测试突破点 → Low 2 Buy
突破后第二腿回调（2-legged pullback）= 更深回调 → 更高胜率 Buy
信号条（signal bar）= 反转K线（反转形态）→ BPB触发条件
```

**Al Brooks的重要原则（直接对齐我们的设计）**：
- 任何设置的胜率只有40-60%，因此必须**结合多因素**（=我们的投票聚合）
- 反对过度依赖指标，主张纯价格行为（=我们的执行层 P0_E 是技术层，不含基本面）
- 强调数学期望和盈亏比（=我们的KELLY对象卡）

---

### 3.2 成交量分布（VP_P0_E）— Trader Dale — 高优先级

| 资源 | 搜索 | 适合度 | 必看内容 |
|------|------|--------|---------|
| **Trader Dale** | YouTube: Trader Dale | ⭐⭐⭐⭐⭐ | Volume Profile课程（15小时+） |
| **Jigsaw Trading** | YouTube: Jigsaw Trading | ⭐⭐⭐⭐ | 订单流基础、DOM交易 |
| **Axia Futures** | YouTube: Axia Futures | ⭐⭐⭐⭐ | 机构级订单流、Footprint Chart |

**核心内容映射**：
```
POC (Point of Control) = 成交量最大价格 → VP对象卡核心输出
VAH/VAL (Value Area High/Low) = 70%成交量区间 → 支撑/阻力边界
HVN (High Volume Node) = 高成交量节点 → 价格吸附/阻力
LVN (Low Volume Node) = 低成交量节点 → 价格快速穿越（真空地带）
```

**注意**：
- Trader Dale的课程是**付费**的（$699），但YouTube上有大量免费片段和每日分析视频
- Jigsaw Trading的免费教育内容非常丰富，适合自学订单流基础
- A股没有逐笔Tick数据，所以Footprint Chart/Delta无法直接复现，需降级为基于OHLCV的Volume Profile近似

---

### 3.3 系统化交易/多策略管理 — 中优先级

| 资源 | 搜索 | 适合度 | 必看内容 | 注意点 |
|------|------|--------|---------|--------|
| **Adam Grimes** | YouTube: Adam Grimes | ⭐⭐⭐⭐ | The Art and Science of Trading | 强调系统化、统计思维，与我们的回测诚实性原则一致 |
| **Mark Minervini** | YouTube: Mark Minervini | ⭐⭐⭐ | Trend Template、SEPA方法 | 偏美股趋势交易，但市场状态分类思路可借鉴到PeriodQueen |
| **Peter Brandt** | YouTube: Peter Brandt | ⭐⭐⭐ | 经典图表形态、市场情绪 | 老牌交易员，强调纪律 |

**为什么适合**：
- Adam Grimes 的 "The Art and Science of Trading" 免费课程是**系统化交易**的入门标杆，强调：
  - 任何方法的概率都只有50%左右（=我们的投票聚合必要性）
  - 严格的回测和统计验证（=我们的CSCV-PBO要求）
  - 交易者的概率思维（=我们的confidence字段设计）
- Mark Minervini 的 "Trend Template" 可作为 PERIOD_QUEEN 的 ATTACK_SUSTAINED 状态检测参考

---

### 3.4 动量/背离（TKR7_P0_E）— Linda Raschke — 中优先级

| 资源 | 搜索 | 适合度 | 必看内容 |
|------|------|--------|---------|
| **Linda Raschke** | YouTube: Linda Raschke | ⭐⭐⭐⭐ | Holy Grail setup、动量背离 |
| **SMB Capital** | YouTube: SMB Capital | ⭐⭐⭐ | 动量交易、开盘区间 |

Linda Raschke 的 "Holy Grail" 设置是经典的动量+均线回踩策略，与我们的 `TKR7_P0_E`（AO背离）有类似思想：在动量趋势中的回调入场。

---

### 3.5 仓位管理（KELLY_P0_R）— 理论级

| 资源 | 搜索 | 适合度 | 必看内容 |
|------|------|--------|---------|
| **Edward Thorp** | YouTube: Edward Thorp interviews | ⭐⭐⭐ | 凯利公式、概率优势 |
| **TastyTrade** | YouTube: TastyTrade | ⭐⭐⭐ | 概率交易、波动率管理 |

TastyTrade（Tom Sosnoff）的核心是**概率思维和波动率管理**，与我们的 `VOLFAC` + `VOLTARGET` + `KELLY` 三层风控体系高度一致：
- 波动率（IV Rank）决定仓位大小
- 凯利式仓位管理（固定风险比例）
- 强调统计期望而非单次盈亏

---

### 3.6 ⚠️ 谨慎参考的YouTube博主

| 博主 | 为什么谨慎 | 我们的态度 |
|------|----------|----------|
| **ICT (Inner Circle Trader)** | 概念极其复杂，大量术语和"秘传"色彩，难以量化 | 部分市场结构概念可借鉴（如PD Array、Breaker），但大部分内容归为 `NOT_QUANT_YET` 或 `shell_only` |
| **各种"保证盈利"的Guru** | 违背统计常识 | 直接排除 |
| **纯指标推销频道** | 指标参数不公开，无法复现 | 违背回测诚实性原则，排除 |

---

## 四、推荐学习路径（按我们的开发优先级）

### 阶段一：夯实单卡理论（当前阶段）

| 对象卡 | 优先学习资源 | 预计时间 |
|--------|------------|---------|
| CHZL_BSD | 谷粟解禅（B站）+ 北斗解缠合集 | 20小时 |
| BPB | Al Brooks YouTube全部免费视频 | 30小时 |
| VP | Trader Dale免费视频 + Jigsaw Trading入门 | 10小时 |
| YTC | 德湃订单流（B站）+ Jigsaw Trading | 10小时 |
| TKR7 | Linda Raschke Holy Grail + Adam Grimes | 5小时 |

### 阶段二：理解系统化整合（后续）

| 主题 | 资源 | 目的 |
|------|------|------|
| 多信号投票 | Adam Grimes系统课程 | 理解为什么单一方法不够 |
| 市场状态分类 | Mark Minervini Trend Template | 优化PeriodQueen状态机 |
| 波动率管理 | TastyTrade教育视频 | 优化VOLFAC/VOLTARGET |
| 回测诚实性 | Marcos Lopez de Prado演讲（YouTube） | 实现CSCV-PBO框架 |

---

## 五、可直接用于我们系统的规则提取

### 5.1 从Al Brooks提取（BPB对象卡）

```python
# 伪代码 — 可纳入 object_card_bpb.py
# Al Brooks 核心概念映射

def classify_setup(klines):
    # 突破后的腿数（leg count）
    legs = count_pullback_legs(klines, breakout_level)
    
    if legs == 1:
        # 1-legged pullback = 浅回调，通常突破点附近
        return {"setup": "Low2_Buy", "strength": 1.5, "confidence": 0.55}
    elif legs == 2:
        # 2-legged pullback = 更深回调，胜率更高
        return {"setup": "Low2_Buy_v2", "strength": 2.0, "confidence": 0.60}
    
    # 信号条质量
    signal_bar = klines[-1]
    if is_reversal_bar(signal_bar) and signal_bar.close > signal_bar.open:
        return {"signal_bar": "Bull_Reversal", "valid": True}
    
    # 通道检测
    if is_channel(klines[-20:]):
        return {"context": "Channel", "trade_direction": "with_trend"}
```

### 5.2 从Volume Profile提取（VP对象卡）

```python
# 伪代码 — 可纳入 object_card_vp.py

def calculate_vp_levels(klines):
    price_vol = {}  # 价格→成交量映射
    for k in klines:
        for price in range(int(k.low), int(k.high)+1):
            price_vol[price] = price_vol.get(price, 0) + k.vol / (k.high - k.low)
    
    # POC: 成交量最大价格
    poc = max(price_vol, key=price_vol.get)
    
    # Value Area: 累计70%成交量的价格区间
    total_vol = sum(price_vol.values())
    sorted_prices = sorted(price_vol.items(), key=lambda x: x[1], reverse=True)
    cumsum = 0
    va_prices = []
    for price, vol in sorted_prices:
        cumsum += vol
        va_prices.append(price)
        if cumsum >= total_vol * 0.7:
            break
    
    vah, val = max(va_prices), min(va_prices)
    
    return {"poc": poc, "vah": vah, "val": val}
```

---

## 六、关键提醒

1. **不要照搬任何单一博主的体系**。我们的价值在于**对象化拆解 + 投票聚合**，不是成为Al Brooks的复制或缠论的复制。

2. **A股数据限制**：国外订单流教学（Jigsaw/Axia）中的DOM/Footprint/Delta等工具需要逐笔Tick数据，A股没有公开Level-2逐笔，所以YTC/VP对象卡必须降级为基于OHLCV的近似实现。

3. **回测诚实性**：所有外部学习的规则，必须通过我们的CSCV-PBO框架验证后才能纳入对象卡。不要因为某个博主"说"这个方法有效就直接编码。

4. **哲学/心法内容降级**：Al Brooks强调的交易心理、缠论中的禅宗思想，都归为 `NOT_QUANT_YET`，不进入对象卡逻辑，只作为人类交易者的参考。

---

## 七、资源索引速查表

| 想学什么 | 去哪里 | 搜索关键词 |
|----------|--------|----------|
| 缠论分型/笔/中枢 | B站 | "谷粟解禅" / "北斗解缠" / "缠论108课" |
| 价格行为/突破回调 | YouTube | "Al Brooks" / "Brooks Trading Course" |
| 成交量分布 | YouTube + B站 | "Trader Dale" / "Jigsaw Trading" / "德湃订单流" |
| 订单流/微观结构 | YouTube | "Jigsaw Trading" / "Axia Futures" / "Order Flow Trading" |
| 系统化交易思维 | YouTube | "Adam Grimes" / "The Art and Science of Trading" |
| 趋势状态识别 | YouTube | "Mark Minervini" / "Trend Template" |
| 波动率/仓位管理 | YouTube | "TastyTrade" / "Tom Sosnoff" / "Kelly Criterion" |
| 动量/背离 | YouTube | "Linda Raschke" / "Holy Grail Trading" |
| A股资金流向 | B站 | "龙虎榜分析" / "北向资金"（注意降级处理） |

---

*本指南随对象卡系统演进更新。如发现新的高质量资源，建议按上述格式补充到对应对象卡章节。*
