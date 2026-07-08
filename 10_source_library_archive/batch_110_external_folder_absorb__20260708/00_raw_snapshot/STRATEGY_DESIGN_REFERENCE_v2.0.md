# 策略设计参考 v2.0 — 微观结构、情绪指标与板块轮动的增强方案

> **文档编号**: REF-DESIGN-v2.0
> **创建日期**: 2026-07-07
> **依赖文档**: `EXTERNAL_STRATEGY_RAW_MATERIAL_v2.0.md` + `STRATEGY_DESIGN_REFERENCE_v1.0.md`
> **用途**: 将第三批外部搜索的启发（微观结构/情绪/板块轮动）转化为现有三层架构内的可落地方案。
> **原则**: 不新增独立模块，所有增强自然生长于现有架构内。

---

## 1. 第三批资料的启发摘要

本次搜索（4批次共40条结果）覆盖了：

| 方向 | 代表来源 | 核心启发 | 采纳状态 |
|------|----------|----------|----------|
| 集合竞价微观结构 | Quant67/视界量化/百度文库 | 缺口统计、竞价成交量占比、9:20后不可撤单规则 | **v1.0采纳** |
| 尾盘策略 | 新浪财经/沪深交易所统计 | 尾盘异动检测（上下影线）、尾盘新规影响回测 | **v1.0采纳** |
| 恐惧贪婪情绪指数 | CNN/华泰/海能投顾 | A股版情绪指数、逆向偏差参数、散户vs机构博弈 | **v1.1采纳** |
| 板块轮动 | BigQuant/光大证券/华宝证券 | 行业动量评分、风格切换、ADC三位一体模型 | **v1.1采纳** |
| 行为金融学偏差 | 微信公众号/凯金斯 | 控制台行为审查、心理清单、台谏系统增强 | **v1.2采纳** |

---

## 2. v1.0 增强（无需额外数据，立即实现）

### 2.1 增强一：缺口统计模型（CHZL_TREND）

**问题**: 现有 `CHZL_TREND` 未处理K线缺口，而缺口是集合竞价资金博弈的直接结果，包含趋势强度信息。

**外部启发**: 缺口理论——缺口是市场共识断裂的具象化，集合竞价是缺口形成的主要机制。

**设计方案**:

```python
# CHZL_TREND 对象卡增强（gap_analysis 字段）
interface_chzl_trend_enhanced = {
    # 原有字段
    "chzl_trend_type": str,            # 上升/下降/盘整
    "chzl_trend_strength": int,
    
    # 新增字段（v1.0）
    "chzl_gap_type": str,              # NONE / COMMON / BREAK / RUN / EXHAUSTION
    "chzl_gap_size": float,            # 缺口大小（%）
    "chzl_gap_direction": str,         # UP / DOWN
    "chzl_gap_filled": bool,           # 是否已回补
    "chzl_gap_days_since": int,        # 缺口出现后天数
}

# 缺口类型定义
gap_type_rules = {
    "COMMON": "缺口在3-5日内回补，无趋势意义",
    "BREAK": "突破缺口，出现在趋势启动时，不回补概率高",
    "RUN": "持续缺口，出现在趋势中段，不回补概率高",
    "EXHAUSTION": "衰竭缺口，出现在趋势末端，通常迅速回补",
}

# 缺口计算（日OHLCV）
def calculate_gap(df_ohlcv):
    """
    计算当日缺口类型
    """
    prev_close = df_ohlcv['close'].shift(1)
    current_low = df_ohlcv['low']
    current_high = df_ohlcv['high']
    
    # 向上缺口：当日最低 > 前日最高（但前日最高≈前日收盘，近似用close）
    up_gap = current_low > prev_close * 1.001  # 允许1‰误差
    down_gap = current_high < prev_close * 0.999
    
    gap_size = np.where(up_gap, (current_low - prev_close) / prev_close, 
                        np.where(down_gap, (current_high - prev_close) / prev_close, 0))
    
    return gap_type, gap_size, gap_direction

# 缺口对趋势的判断增强
def trend_strength_with_gap(trend_type, gap_type, gap_size):
    """
    结合缺口信息增强趋势强度判断
    """
    base_strength = trend_strength(trend_type)
    
    if gap_type == "BREAK" and gap_size > 0.02:  # 突破缺口>2%
        base_strength += 1  # 趋势启动信号增强
    elif gap_type == "EXHAUSTION":
        base_strength -= 1  # 趋势可能衰竭
    elif gap_type == "COMMON" and gap_size < 0.005:  # 普通缺口<0.5%
        base_strength -= 0  # 无影响
    
    return min(10, max(0, base_strength))
```

**对 STRATEGY_BUNDLES 的影响**:
- `TrendFollowing` 中，`BREAK` 缺口 + 上升趋势 → 增强 `3Buy` 信号（strength +1）
- `GradualExit` 中，`EXHAUSTION` 缺口 → 提前触发退出信号
- `TrialEntry` 中，`COMMON` 缺口回补后 → 可作为 `2Buy` 的辅助确认

**数据需求**: 日 OHLCV。已有。`proxy_quantizable_now`。

---

### 2.2 增强二：集合竞价成交量占比因子（MFLOW）

**问题**: 现有 `MFLOW` 的早盘意图判断（`mflow_open_intent`）缺乏量化强度指标。

**外部启发**: 光大证券因子——集合竞价成交量占比 = 集合竞价成交量 / 全天成交量，是有效选股因子。

**设计方案**:

```python
# MFLOW 对象卡增强（mflow_open_intensity 字段）
interface_mflow_enhanced = {
    # 原有字段
    "mflow_main_force_direction": str,   # IN / OUT / NEUTRAL
    "mflow_open_intent": str,            # STRONG_BUY / WEAK_BUY / NEUTRAL / etc.
    
    # 新增字段（v1.0）
    "mflow_open_intensity": float,         # 集合竞价成交量占比（0-1）
    "mflow_open_intensity_percentile": float,  # 历史分位数（过去60日）
    "mflow_open_vs_avg": float,          # 当日开盘量 / 5日平均开盘量
}

# 计算方法（基于日OHLCV的近似）
def calculate_open_intensity(df_ohlcv, use_approximation=True):
    """
    计算开盘强度
    
    如果 use_approximation=True（仅有日OHLCV）：
        - 近似：开盘30分钟成交量 = 当日开盘量 ≈ (open - low)相关推算
        - 更简单的近似：开盘第一小时成交量 / 全天成交量
        - 但日OHLCV没有小时数据，所以用：
          open_intensity = (open - prev_close).abs() / (high - low) * volume
          这个公式不直接给出开盘量...
    
    更好的近似（仅用日OHLCV）：
        - 无法直接计算开盘量
        - 但可以用"开盘缺口大小"作为"开盘强度"的代理变量
        - 大缺口通常伴随大开盘成交量
    
    如果有分钟级数据（60min）：
        - 开盘30分钟 = 前两根60min K线
        - 开盘30分钟成交量 / 全天成交量
    """
    if has_minute_data:
        # 精确计算
        open_30min_volume = volume_0930_to_1000
        open_intensity = open_30min_volume / total_volume
    else:
        # 日OHLCV近似：用缺口大小和全天成交量推算
        gap_size = abs(open - prev_close) / prev_close
        open_intensity = gap_size * volume / avg_volume_20  # 归一化
    
    return open_intensity

# 对信号的影响
open_intensity_signal_map = {
    "high": open_intensity > 0.15,       # 开盘量>15%全天 → 强意图
    "normal": 0.05 <= open_intensity <= 0.15,
    "low": open_intensity < 0.05,        # 开盘量<5% → 弱意图
}
```

**注意**: 日OHLCV**无法精确计算**开盘30分钟成交量。因此这个字段在v1.0使用**近似值**（缺口大小×成交量归一化），在v1.1有分钟级数据后替换为精确值。

**对 VoteEngine 的影响**: 当 `mflow_open_intensity` > 0.15（高）且 `mflow_open_intent` = STRONG_BUY 时，`MFLOW` 的 signal_strength 额外+1。

---

### 2.3 增强三：尾盘异动检测（YTC/BPB）

**问题**: 现有对象卡未处理"日内尾盘结构"（拉尾盘/打尾盘），而尾盘是主力行为的重要窗口。

**外部启发**: 拉尾盘/打尾盘是主力行为的典型信号，可通过上下影线检测。

**设计方案**:

```python
# YTC 对象卡增强（intraday_tail_analysis 字段）
interface_ytc_enhanced = {
    # 原有字段
    "ytc_srf_is_valid": bool,
    "ytc_nearest_sr": dict,
    
    # 新增字段（v1.0）
    "ytc_tail_abnormality_score": float,    # 0-1，尾盘异动程度
    "ytc_tail_type": str,                   # NONE / PULL_UP / PULL_DOWN / NORMAL
    "ytc_tail_confidence": float,          # 异动可信度
}

# 计算方法（仅用日OHLCV）
def calculate_tail_abnormality(open_price, high, low, close):
    """
    计算尾盘异动分数
    """
    total_range = high - low
    if total_range == 0:
        return 0, "NONE"
    
    # 上影线 = high - max(open, close)
    # 下影线 = min(open, close) - low
    upper_shadow = high - max(open_price, close)
    lower_shadow = min(open_price, close) - low
    
    body = abs(close - open_price)
    
    # 尾盘异动判断
    if upper_shadow / total_range > 0.6 and body / total_range < 0.2:
        # 长上影线 + 小实体 → 打尾盘（尾盘回落）
        tail_type = "PULL_DOWN"
        score = upper_shadow / total_range
    elif lower_shadow / total_range > 0.6 and body / total_range < 0.2:
        # 长下影线 + 小实体 → 拉尾盘（尾盘拉升）
        tail_type = "PULL_UP"
        score = lower_shadow / total_range
    else:
        tail_type = "NORMAL"
        score = 0
    
    return score, tail_type

# 对策略的影响
tail_strategy_map = {
    "PULL_UP": {
        "note": "尾盘被拉升，可能是主力做净值或诱多",
        "action": "若次日开盘高开，降低买入意愿（strength-1）；若低开，谨慎观察",
        "contrarian_bias": -0.5,  # 逆向偏差：拉尾盘通常不可持续
    },
    "PULL_DOWN": {
        "note": "尾盘被打压，可能是震仓或恐慌抛售",
        "action": "若次日开盘低开，可能是买入机会（但需确认非系统性风险）",
        "contrarian_bias": +0.3,  # 逆向偏差：恐慌抛售可能过度
    },
}
```

**对 PERIOD_QUEEN 的影响**: 当市场大量股票（>30%）同时出现 `PULL_UP` 时，可能是机构做净值（季末/年末），系统应降低 `ATTACK_SUSTAINED` 的置信度（因为次日可能回调）。

**数据需求**: 日 OHLCV。已有。`proxy_quantizable_now`。

---

### 2.4 增强四：市场结构版本（回测框架精度）

**问题**: 沪市基金尾盘规则在2026年6月15日变更，回测需要区分不同时间段的规则。

**外部启发**: 虎嗅报道——沪市基金尾盘14:57-15:00统一执行收盘集合竞价（此前为连续竞价）。

**设计方案**:

```python
# 回测框架配置（BACKTEST_FRAMEWORK_DESIGN 增强）
class MarketStructureVersion:
    """
    市场结构版本管理：不同时间段的交易规则不同
    """
    
    VERSIONS = {
        "pre_2026_06_15": {
            "sh_fund_close": "continuous_auction",  # 连续竞价
            "tail_abnormality_valid": True,         # 尾盘价格可能异动
            "close_price_source": "last_trade",     # 收盘价=最后一笔成交价
        },
        "post_2026_06_15": {
            "sh_fund_close": "call_auction",        # 集合竞价
            "tail_abnormality_valid": False,        # 尾盘价格更稳定
            "close_price_source": "auction_price",  # 收盘价=集合竞价结果
        },
    }
    
    def __init__(self, backtest_start_date, backtest_end_date):
        self.versions = self._determine_versions(backtest_start_date, backtest_end_date)
    
    def _determine_versions(self, start, end):
        """确定回测期间涉及哪些市场结构版本"""
        versions = []
        if start < "2026-06-15":
            versions.append("pre_2026_06_15")
        if end >= "2026-06-15":
            versions.append("post_2026_06_15")
        return versions
    
    def get_rules_for_date(self, date):
        """获取某日期适用的交易规则"""
        if date < "2026-06-15":
            return self.VERSIONS["pre_2026_06_15"]
        else:
            return self.VERSIONS["post_2026_06_15"]
```

**对回测的影响**:
- 当回测包含2026年6月15日前后的数据时，需要分段应用不同的规则
- 在 `pre_2026_06_15` 阶段，允许尾盘价格异动作为信号
- 在 `post_2026_06_15` 阶段，尾盘价格更稳定，异动检测的权重降低

**数据需求**: 无。纯规则参数。`proxy_quantizable_now`。

---

## 3. v1.1 增强（需补充数据，后续实现）

### 3.1 增强五：A股版恐惧贪婪指数（PERIOD_QUEEN输入）

**问题**: 现有 `PERIOD_QUEEN` 缺乏情绪量化输入，无法在市场极端情绪时调整策略。

**外部启发**: CNN Fear & Greed Index / 华泰港股情绪指数 / 海能投顾情绪模型。

**设计方案**:

```python
# 新增模块：A_SHARE_SENTIMENT_INDEX（A股情绪指数）
# 不新增对象卡，而是作为 PERIOD_QUEEN 的辅助输入模块

interface_a_share_sentiment = {
    "sentiment_score": float,          # 0-100
    "sentiment_zone": str,             # EXTREME_FEAR / FEAR / NEUTRAL / GREED / EXTREME_GREED
    "sub_scores": dict,                # 各子指标得分
}

# A股版子指标（7个，对应CNN原版）
sentiment_sub_indicators = {
    # 1. 市场动能（替代：股价动能）
    "market_momentum": {
        "source": "指数125日涨跌幅",
        "calculation": "沪深300当前价 / 125日前收盘价 - 1",
        "weight": 0.15,
    },
    
    # 2. 股价强度（替代：52周新高新低比率）
    "stock_strength": {
        "source": "全A股20日新高/新低比率",
        "calculation": "20日新高家数 / 20日新低家数",
        "weight": 0.15,
    },
    
    # 3. 股价广度（替代：上涨下跌股票比例）
    "stock_breadth": {
        "source": "全A股涨跌家数比",
        "calculation": "上涨家数 / (上涨家数 + 下跌家数)",
        "weight": 0.15,
    },
    
    # 4. 看跌/看涨比例（替代：Put/Call Ratio）
    "put_call_proxy": {
        "source": "融资融券余额变化",
        "calculation": "融资余额增速 / 融券余额增速（反向）",
        "note": "A股期权不成熟，用融资融券作为替代",
        "weight": 0.10,
    },
    
    # 5. 垃圾债券需求（替代：风险偏好）
    "risk_appetite": {
        "source": "信用债利差",
        "calculation": "AAA企业债收益率 - 国债收益率",
        "note": "利差扩大=风险厌恶，利差收窄=风险偏好",
        "weight": 0.10,
    },
    
    # 6. 市场波动率（替代：VIX）
    "market_volatility": {
        "source": "iVIX（中国波指）或 50ETF期权隐含波动率",
        "calculation": "iVIX指数值",
        "weight": 0.15,
    },
    
    # 7. 避险需求（替代：国债vs股票）
    "safe_haven_demand": {
        "source": "国债收益率与股票收益率对比",
        "calculation": "10年期国债收益率 / 沪深300股息率",
        "note": "比值越高=避险需求越强",
        "weight": 0.20,
    },
}

# 情绪区间映射
sentiment_zone_map = {
    (0, 25): "EXTREME_FEAR",
    (25, 40): "FEAR",
    (40, 60): "NEUTRAL",
    (60, 75): "GREED",
    (75, 100): "EXTREME_GREED",
}

# 对 PERIOD_QUEEN 的影响
def adjust_regime_by_sentiment(pq_state, sentiment_score, sentiment_zone):
    """
    根据情绪指数调整 regime_state 和交易参数
    """
    adjustments = {}
    
    if sentiment_zone == "EXTREME_GREED":
        # 极度贪婪：降低仓位上限，提高投票门槛
        adjustments["position_max_size"] = max(0, pq_state.max_position_size - 0.2)
        adjustments["entry_min_votes"] = pq_state.entry_min_votes + 1
        adjustments["contrarian_bias"] = -1.0  # 逆向偏差：不追涨
        
    elif sentiment_zone == "EXTREME_FEAR":
        # 极度恐惧：允许逆势建仓（但严格风控）
        adjustments["position_max_size"] = min(1.0, pq_state.max_position_size + 0.1)
        adjustments["entry_min_votes"] = max(2, pq_state.entry_min_votes - 1)
        adjustments["contrarian_bias"] = +1.0  # 逆向偏差：恐慌时找机会
        
    else:
        adjustments["contrarian_bias"] = 0
    
    return adjustments
```

**数据需求**:
- 全A股涨跌家数、新高新低家数 → 需要全市场数据（Wind可提供）
- 融资融券余额 → Wind已有
- iVIX指数 → Wind或东方财富
- 信用债利差 → Wind或中债登
- 国债收益率/沪深300股息率 → Wind已有

标记为 `needs_extra_data`（部分需补充），但核心数据（涨跌家数、融资融券）可用。

---

### 3.2 增强六：逆向偏差参数（Contrarian Bias）

**问题**: 现有 `PERIOD_QUEEN` 只根据技术状态输出交易权限，未考虑"市场由谁主导"（散户vs机构）。

**外部启发**: 海能投顾研究——78.6%散户高开时FOMO，开盘情绪>75时当日收跌概率82.3%，散户情绪与主力净流入负相关R²=0.82。

**设计方案**:

```python
# PERIOD_QUEEN 输出增强
interface_period_queen_enhanced = {
    # 原有字段
    "pq_state": str,
    "pq_trading_permission": str,
    "pq_position_max_size": float,
    "pq_entry_min_votes": int,
    
    # 新增字段（v1.1）
    "pq_contrarian_bias": float,        # -1.0 to +1.0
    "pq_market_dominator": str,          # RETAIL / INSTITUTION / MIXED
    "pq_retail_sentiment_score": float,  # 0-100（散户情绪）
}

# Contrarian Bias 对策略的影响
def apply_contrarian_bias(base_entry_min_votes, base_max_size, contrarian_bias, sentiment_zone):
    """
    应用逆向偏差调整
    """
    adjusted_votes = base_entry_min_votes
    adjusted_size = base_max_size
    
    if contrarian_bias <= -0.8:  # 强烈逆向（不追涨）
        # 提高门槛，降低仓位
        adjusted_votes += 1
        adjusted_size *= 0.7
        
    elif contrarian_bias >= 0.8:  # 强烈逆向（恐慌时找机会）
        # 降低门槛，但保持严格止损
        adjusted_votes = max(2, adjusted_votes - 1)
        adjusted_size = min(1.0, adjusted_size * 1.1)
        
    return adjusted_votes, adjusted_size

# 在 StrategyBundles 中的应用示例
# TrendFollowing (ATTACK_SUSTAINED):
#   base_votes = 3, base_size = 1.0
#   若 contrarian_bias = -1.0（EXTREME_GREED）:
#     adjusted_votes = 4, adjusted_size = 0.7
#   意味着：即使技术状态完美，但情绪极端乐观时，系统只给70%仓位，且需要4票确认

# TrialEntry (GESTATION):
#   base_votes = 4, base_size = 0.3
#   若 contrarian_bias = +1.0（EXTREME_FEAR）:
#     adjusted_votes = 3, adjusted_size = 0.33
#   意味着：恐慌时，试错门槛降低，允许略多仓位
```

**与 Fear & Greed 指数的协同**:
- `sentiment_score` → `sentiment_zone` → `contrarian_bias`
- 这形成了一个完整的"情绪→逆向偏差→策略调整"链条。

---

### 3.3 增强七：行业动量评分（A5选股层）

**问题**: 现有 `A5_FUNDAMENTAL_INTEGRATION` 只有个股层面的基本面筛选，缺少行业/板块层面的轮动判断。

**外部启发**: BigQuant/光大证券ADC模型——行业轮动是获取超额收益的重要途径。

**设计方案**:

```python
# A5 选股层增强（industry_momentum_filter）
class A5FundamentalSelectorEnhanced:
    """
    在原有A5排雷+评分+估值基础上，增加行业动量筛选
    """
    
    def __init__(self, industry_data):
        self.industry_data = industry_data  # 申万/中信行业指数数据
    
    def calculate_industry_momentum(self, industry_code, lookback=20):
        """
        计算行业动量评分
        """
        industry_index = self.industry_data[industry_code]
        
        # 动量因子
        mom_20 = industry_index['close'].pct_change(lookback).iloc[-1]  # 20日涨幅
        mom_10 = industry_index['close'].pct_change(10).iloc[-1]       # 10日涨幅
        
        # 相对强弱（vs 沪深300）
        benchmark_return = self.benchmark['close'].pct_change(lookback).iloc[-1]
        relative_strength = mom_20 - benchmark_return
        
        # 动量加速
        momentum_acceleration = mom_10 - industry_index['close'].pct_change(13).iloc[-1]
        
        # 综合评分（0-100）
        industry_score = (
            mom_20 * 40 +           # 20日动量权重40%
            relative_strength * 35 + # 相对强弱权重35%
            momentum_acceleration * 25  # 动量加速权重25%
        ) * 100  # 归一化
        
        return industry_score
    
    def filter_by_industry_momentum(self, stock_pool, top_percentile=0.3):
        """
        只保留行业动量排名前30%的行业中的个股
        """
        # 计算所有行业的动量评分
        industry_scores = {}
        for industry in self.industry_data:
            industry_scores[industry] = self.calculate_industry_momentum(industry)
        
        # 排序，取前30%
        sorted_industries = sorted(industry_scores.items(), key=lambda x: x[1], reverse=True)
        top_industries = [ind for ind, score in sorted_industries 
                          if score > np.percentile(list(industry_scores.values()), 70)]
        
        # 过滤个股
        filtered_pool = [stock for stock in stock_pool 
                        if stock['industry'] in top_industries]
        
        return filtered_pool

# 与现有A5流程的整合
# 原流程：A5候选池 = 排雷 → 评分 → 估值 → 输出
# 增强流程：A5候选池 = 排雷 → 行业动量筛选 → 评分 → 估值 → 输出
# 即：行业动量筛选作为第二层过滤器（在排雷之后，评分之前）
```

**数据需求**: 申万/中信行业指数数据（Wind已有）。`proxy_quantizable_now`。

**与组合风控的协同**:
- 行业动量筛选 + 组合风控的行业集中度上限（20%） → 形成"行业优选+风险控制"的双重机制
- 当行业动量筛选选出3个以上行业时，组合风控可以自然分散
- 当行业动量筛选只选出1-2个行业时，组合风控的20%上限防止过度集中

---

## 4. v1.2 增强（治理层/UI，远期实现）

### 4.1 增强八：控制台行为审查（台谏系统）

**问题**: 用户可能因行为金融学偏差（确认偏误、后悔厌恶、FOMO）做出非理性决策，现有控制台未提供心理审查。

**外部启发**: 行为金融学——散户亏损多源于心理偏差，需要"系统对抗本能"。

**设计方案**:

```python
# 台谏系统增强（TaiJianSystem）
class BehavioralAuditModule:
    """
    行为审查模块：检查用户决策是否存在心理偏差
    """
    
    def __init__(self, audit_logger):
        self.audit = audit_logger
    
    def check_decision_bias(self, user_decision, market_context, user_history):
        """
        检查用户决策是否存在偏差
        """
        warnings = []
        
        # 1. 确认偏误检查
        if user_decision.direction == "BUY":
            # 用户是否只看 bullish 信号，忽略 bearish 信号？
            bullish_signals = sum(1 for s in market_context.signals if s.type == "BULLISH")
            bearish_signals = sum(1 for s in market_context.signals if s.type == "BEARISH")
            if bullish_signals == 1 and bearish_signals >= 3:
                warnings.append("确认偏误警告：1个 bullish 信号 vs 3个 bearish 信号，建议重新评估")
        
        # 2. FOMO检查（追高）
        if user_decision.entry_price > market_context.20day_high * 0.95:
            warnings.append("FOMO警告：入场价接近20日高点，是否追高？建议等待回调")
        
        # 3. 后悔厌恶检查（不止损）
        if user_history.current_loss > 0.05 and user_decision.action == "HOLD":
            warnings.append("后悔厌恶警告：当前亏损>5%，建议按纪律止损，避免损失扩大")
        
        # 4. 羊群效应检查
        if market_context.sentiment_zone == "EXTREME_GREED" and user_decision.direction == "BUY":
            warnings.append("羊群效应警告：市场极度贪婪时买入，是否与散户同向？建议逆向思考")
        
        return warnings

# 在控制台中的应用
# 当用户尝试"批红"（确认交易）时，台谏系统弹出行为审查面板：
# ┌────────────────────────────────────────────┐
# │ 台谏御史 · 行为审查                          │
# ├────────────────────────────────────────────┤
# │ ⚠️ 确认偏误警告：1个 bullish 信号 vs 3个 bearish │
# │ ⚠️ FOMO警告：入场价接近20日高点              │
# │                                            │
# │ 是否仍要执行？ [是] [否] [暂缓]               │
# └────────────────────────────────────────────┘
```

**实现版本**: v1.2（治理层增强，不影响核心交易逻辑）。

---

## 5. 增强汇总表（v1.0 + v1.1 + v1.2）

| 版本 | 增强项 | 目标对象卡/模块 | 数据需求 | 状态 |
|------|--------|-----------------|----------|------|
| v1.0 | 缺口统计模型 | CHZL_TREND | 日OHLCV | 可编码 |
| v1.0 | 集合竞价成交量占比 | MFLOW | 日OHLCV（近似） | 可编码 |
| v1.0 | 尾盘异动检测 | YTC/BPB | 日OHLCV | 可编码 |
| v1.0 | 市场结构版本 | 回测框架 | 规则参数 | 可编码 |
| v1.0 | ADX趋势过滤器 | VOLFAC | 日OHLCV | 可编码（v1.0已有） |
| v1.0 | 动态阈值 | TKR7/KD_MTF | 日OHLCV+VOLFAC | 可编码（v1.0已有） |
| v1.0 | 交易量确认 | VoteEngine | 日OHLCV volume | 可编码（v1.0已有） |
| v1.1 | A股恐惧贪婪指数 | PERIOD_QUEEN输入 | 需补充（融资融券/涨跌家数） | 待数据 |
| v1.1 | 逆向偏差参数 | PERIOD_QUEEN输出 | 需情绪指标数据 | 依赖情绪指数 |
| v1.1 | 行业动量评分 | A5选股层 | 行业指数数据（Wind已有） | 可编码 |
| v1.1 | 组合风控层 | PORTFOLIO_RISK | 行业分类+风格因子 | 可编码（v1.1已有） |
| v1.1 | 均值回归策略包 | StrategyBundles | 全部现有数据 | 可编码（v1.1已有） |
| v1.2 | 控制台行为审查 | 台谏系统 | 无（纯UI） | 待实现 |

---

## 6. 对编程 AI 的指令（第三批）

### 6.1 v1.0 新增任务（第三批）

1. **实现缺口统计模块** (`src/backtest_engine/indicators/gap_analysis.py`):
   - 输入：日OHLCV
   - 输出：`gap_type`, `gap_size`, `gap_direction`, `gap_filled`
   - 测试：用已知的缺口案例验证分类正确性

2. **增强 MFLOW** (`src/backtest_engine/objects/mflow.py`):
   - 新增 `mflow_open_intensity` 字段（日OHLCV近似）
   - 注释：标记为近似值，v1.1有分钟级数据后替换

3. **增强 YTC/BPB** (`src/backtest_engine/objects/ytc.py`, `bpb.py`):
   - 新增 `tail_abnormality_score` 和 `tail_type` 字段
   - 测试：用长上下影线的K线验证检测正确性

4. **增强回测框架** (`src/backtest_engine/config/market_structure.py`):
   - 新增 `MarketStructureVersion` 类
   - 测试：验证不同日期段的规则切换正确

### 6.2 v1.1 新增任务（第三批）

5. **实现A股情绪指数模块** (`src/backtest_engine/sentiment/a_share_sentiment.py`):
   - 输入：全市场数据（涨跌家数、融资融券、iVIX等）
   - 输出：`sentiment_score`, `sentiment_zone`
   - 先实现可用子指标（涨跌家数、融资融券），标记缺失子指标为`future_bucket`

6. **增强 PERIOD_QUEEN** (`src/backtest_engine/objects/period_queen.py`):
   - 新增 `pq_contrarian_bias`, `pq_market_dominator`, `pq_retail_sentiment_score` 字段
   - 与情绪指数模块联动

7. **增强 A5 选股层** (`src/data_pipeline/fundamental/a5_selector.py`):
   - 新增 `industry_momentum_filter()` 方法
   - 与现有排雷→评分→估值流程整合

---

## 7. 与第一批/第二批的整合

第三批增强与第一批/第二批的增强形成了**完整的策略闭环**：

```
第一层（环境识别）━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PERIOD_QUEEN（状态机）
    ├─ 技术输入：ADX + VOLFAC + 缠论趋势 + KD多周期 + 缺口统计（v1.0）
    ├─ 情绪输入：A股恐惧贪婪指数 + 逆向偏差参数（v1.1）
    └─ 宏观输入：MACRO_ENVIRONMENT_SCORER（已有）

第二层（策略选择）━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  StrategyBundles
    ├─ TrendFollowing（趋势跟踪）← 动量确认 + 行业动量筛选（v1.1）
    ├─ BuildPosition（建仓确认）
    ├─ TrialEntry（试错建仓）← 集合竞价强度 + 缺口类型（v1.0）
    ├─ MeanReversion（均值回归）← 动态阈值 + 尾盘异动（v1.1）
    ├─ GradualExit（逐步退出）← 缺口衰竭检测（v1.0）
    └─ HoldCash（空仓等待）← 情绪极端 + 逆向偏差（v1.1）

第三层（执行管理）━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  VoteEngine + RiskGuard
    ├─ 投票：对象卡信号 + 交易量确认（v1.0）
    ├─ 风控：Van Tharp + Kelly + VolTarget（已有）
    ├─ 组合：行业集中度 + 风格暴露 + 相关性（v1.1）
    └─ 市场结构：版本规则适配（v1.0）

治理层（控制台）━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  台谏系统
    ├─ 技术审查（已有）
    ├─ 行为审查（v1.2）
    └─ 心理清单（v1.2）
```

---

> 文件：STRATEGY_DESIGN_REFERENCE_v2.0.md
> 生产者：Kimi（基于第三批搜索+现有架构融合）
> 用途：将第三批外部策略启发转化为可落地的增强方案
> 与v1.0关系：v1.0覆盖多因子/ADX/动态阈值/交易量确认/组合风控/均值回归；v2.0覆盖缺口/竞价/尾盘/情绪/行业轮动/行为审查
> 关联文件：
>   - `EXTERNAL_STRATEGY_RAW_MATERIAL_v2.0.md`（第三批原始资料）
>   - `STRATEGY_DESIGN_REFERENCE_v1.0.md`（第一批/第二批设计）
>   - `SYSTEM_ARCHITECTURE_DRAFT.md`（三层架构）
>   - `STRATEGY_BUNDLES_v1.0.md`（策略组合）
>   - `A5_FUNDAMENTAL_INTEGRATION_v1.0.md`（A5选股层）
>   - `MING_CABINET_HYBRID_ARCHITECTURE_v1.0.md`（治理架构）
>   - `EMPEROR_CONSOLE_UI_v1.0.md`（控制台UI）
