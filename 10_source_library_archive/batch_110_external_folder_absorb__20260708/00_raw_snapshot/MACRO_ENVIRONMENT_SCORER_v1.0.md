# 宏观环境评分模块设计 v1.0

> **本文档全部内容源于用户（仓库所有者）的想法，由 Kimi 整理为结构化文档供编程 AI 参考。**
> 版本：v1.0 | 状态：设计阶段 | 来源：用户素材"私人投研管家"视频笔记
> 核心目标：将宏观环境5维度（利率/汇率/流动性/风险偏好/政策）量化为可编程评分系统

---

## 一、模块定位

```text
模块名称：MacroEnvironmentScorer（宏观环境评分器）
模块层级：第一层（环境识别）的扩展
与 PeriodQueen 的关系：
  - PeriodQueen 是"心脏"：决定情绪周期七态
  - MacroEnvironmentScorer 是"肺"：提供外部环境的氧气/毒素信号
  - 两者联合决定最终的"交易权限"

协作机制：
  ```
  PeriodQueen（七态）
       │
       │ 情绪周期判断
       ▼
  ┌─────────────────────────────────────┐
  │  联合决策矩阵                        │
  │                                     │
  │  PQ状态 + MacroScore → 最终权限     │
  │                                     │
  │  例：PQ=ATTACK + Macro=30 → 降级    │
  │      PQ=GESTATION + Macro=70 → 允许 │
  └─────────────────────────────────────┘
       │
       ▼
  最终交易权限（允许/限制/禁止）
  ```

独立性：
  - MacroEnvironmentScorer 独立于 PeriodQueen
  - 可以单独运行、单独回测
  - 不依赖 A 股行情数据（使用宏观数据）
```

---

## 二、五维度评分体系

### 2.1 维度总览

```text
┌─────────────────────────────────────────────────────────────────────┐
│                     宏观环境五维度评分体系                           │
│                                                                     │
│  维度        │ 权重  │ 数据来源            │ 更新频率   │ 评分方式 │
│  ────────────┼──────┼────────────────────┼───────────┼───────── │
│  1. 利率     │ 25%  │ 中国10年期国债收益率 │ 日频       │ 偏离度  │
│  2. 汇率     │ 20%  │ 在岸人民币兑美元    │ 日频       │ 趋势度  │
│  3. 流动性   │ 25%  │ M2增速 / SHIBOR    │ 月频/日频  │ 充裕度  │
│  4. 风险偏好 │ 15%  │ 沪深300波动率/VIX  │ 日频       │ 恐惧度  │
│  5. 政策     │ 15%  │ 政策事件/监管动态   │ 事件驱动   │ 友好度  │
│                                                                     │
│  总分：0-100                                                        │
│  interpretation：                                                   │
│    80-100：极度友好（宏观顺风）                                      │
│    60-79：  友好（宏观偏暖）                                         │
│    40-59：  中性（宏观混沌）                                         │
│    20-39：  不利（宏观偏冷）                                         │
│    0-19：   极度不利（宏观逆风）                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 维度 1：利率环境（25%）

```text
指标：中国 10 年期国债收益率（CGB10Y）
逻辑：
  - 利率下降 → 资金成本降低 → 利好股市 → 高分
  - 利率上升 → 资金成本升高 → 利空股市 → 低分
  - 但利率过低（<2%）可能暗示经济衰退 → 中等分

评分算法：
  ```python
  def score_interest_rate(cgb10y: float, historical_data: pd.Series) -> dict:
      """
      利率环境评分
      
      Args:
          cgb10y: 当前 10 年期国债收益率
          historical_data: 历史收益率序列（5年）
      
      Returns:
          {
              "score": float,           # 0-100
              "current": float,         # 当前收益率
              "percentile": float,      # 历史分位 0-100
              "trend": str,             # rising/falling/stable
              "interpretation": str,    # 文字解读
          }
      """
      median = historical_data.median()
      percentile = (historical_data < cgb10y).mean() * 100
      
      # 评分逻辑：
      # 收益率在历史 25% 分位以下（低利率）→ 70-100 分
      # 收益率在历史 25-75% 分位（正常）→ 40-70 分
      # 收益率在历史 75% 分位以上（高利率）→ 0-40 分
      
      if percentile < 25:
          score = 70 + (25 - percentile) / 25 * 30  # 70-100
      elif percentile < 75:
          score = 40 + (75 - percentile) / 50 * 30  # 40-70
      else:
          score = 40 - (percentile - 75) / 25 * 40  # 0-40
      
      # 趋势调整：利率下降中 → +10 分；利率上升中 → -10 分
      ma20 = historical_data.tail(20).mean()
      ma60 = historical_data.tail(60).mean()
      if ma20 < ma60:
          score = min(score + 10, 100)
          trend = "falling"
      elif ma20 > ma60:
          score = max(score - 10, 0)
          trend = "rising"
      else:
          trend = "stable"
      
      return {
          "score": round(score, 1),
          "current": round(cgb10y, 3),
          "percentile": round(percentile, 1),
          "trend": trend,
          "interpretation": _interpret_ir(score, trend),
      }
  
  def _interpret_ir(score: float, trend: str) -> str:
      if score >= 80:
          return f"利率环境极度友好（{trend}），资金成本低，利好股市"
      elif score >= 60:
          return f"利率环境友好（{trend}），资金成本适中"
      elif score >= 40:
          return f"利率环境中性（{trend}），无明显方向"
      elif score >= 20:
          return f"利率环境不利（{trend}），资金成本高，压制估值"
      else:
          return f"利率环境极度不利（{trend}），资金成本高企，警惕回调"
  ```

数据来源：
  - 首选：Wind（用户已有）
  - 备选：tushare（yield_curve 接口）/ akshare（bond_zh_us_rate）

更新频率：日频（收盘后更新）
```

### 2.3 维度 2：汇率环境（20%）

```text
指标：在岸人民币兑美元（USDCNY）
逻辑：
  - 人民币升值 → 外资流入 → 利好股市 → 高分
  - 人民币贬值 → 资本外流 → 利空股市 → 低分
  - 大幅波动（无论方向）→ 不确定性 → 中低分

评分算法：
  ```python
  def score_exchange_rate(usdcny: float, historical_data: pd.Series) -> dict:
      """
      汇率环境评分
      
      评分逻辑：
      1. 趋势：USDCNY 下降（人民币升值）→ 高分
      2. 波动：汇率波动率过高 → 扣分
      3. 偏离：偏离 5 年均线过多 → 扣分
      """
      # 1. 趋势评分（基于 20 日变化率）
      change_20d = (usdcny - historical_data.iloc[-20]) / historical_data.iloc[-20]
      
      if change_20d < -0.01:    # 人民币升值 >1%
          trend_score = 80 + min(abs(change_20d) * 1000, 20)
      elif change_20d < 0:      # 小幅升值
          trend_score = 60 + abs(change_20d) * 2000
      elif change_20d < 0.01:   # 小幅贬值
          trend_score = 40 - change_20d * 2000
      else:                     # 大幅贬值 >1%
          trend_score = 40 - min(change_20d * 1000, 40)
      
      # 2. 波动率扣分（基于 20 日标准差）
      volatility = historical_data.tail(20).std() / historical_data.tail(20).mean()
      if volatility > 0.005:    # 波动率 > 0.5%
          vol_penalty = min((volatility - 0.005) * 5000, 20)
      else:
          vol_penalty = 0
      
      # 3. 偏离度扣分（偏离 60 日均线）
      ma60 = historical_data.tail(60).mean()
      deviation = abs(usdcny - ma60) / ma60
      if deviation > 0.02:      # 偏离 >2%
          dev_penalty = min((deviation - 0.02) * 2000, 15)
      else:
          dev_penalty = 0
      
      score = max(trend_score - vol_penalty - dev_penalty, 0)
      
      return {
          "score": round(score, 1),
          "current": round(usdcny, 4),
          "change_20d": round(change_20d * 100, 2),
          "volatility": round(volatility * 100, 2),
          "deviation": round(deviation * 100, 2),
          "interpretation": _interpret_fx(score, change_20d),
      }
  ```

数据来源：
  - 首选：Wind（用户已有）
  - 备选：tushare（fx_daily）/ akshare（currency_boc_safe）

更新频率：日频（收盘后更新）
```

### 2.4 维度 3：流动性（25%）

```text
指标：
  - 长期：M2 同比增速（月频）
  - 短期：SHIBOR 隔夜利率（日频）
  - 市场：A 股两市成交额（日频）

逻辑：
  - 流动性充裕 → 资金多 → 利好股市 → 高分
  - 流动性紧缩 → 资金少 → 利空股市 → 低分

评分算法：
  ```python
  def score_liquidity(m2_yoy: float, shibor_overnight: float,
                      market_volume: float, historical_volume: pd.Series) -> dict:
      """
      流动性环境评分
      
      三个子指标加权：
      - M2 增速（40%）：反映央行货币政策取向
      - SHIBOR（30%）：反映银行间短期资金成本
      - 市场成交额（30%）：反映股市实际流动性
      """
      # 1. M2 增速评分
      if m2_yoy > 12:
          m2_score = 90
      elif m2_yoy > 10:
          m2_score = 75
      elif m2_yoy > 8:
          m2_score = 60
      elif m2_yoy > 6:
          m2_score = 45
      else:
          m2_score = 30
      
      # 2. SHIBOR 评分（越低越好）
      if shibor_overnight < 1.5:
          shibor_score = 90
      elif shibor_overnight < 2.0:
          shibor_score = 75
      elif shibor_overnight < 2.5:
          shibor_score = 60
      elif shibor_overnight < 3.0:
          shibor_score = 45
      else:
          shibor_score = 30
      
      # 3. 市场成交额评分（与 20 日均量比较）
      avg_volume = historical_volume.tail(20).mean()
      volume_ratio = market_volume / avg_volume
      
      if volume_ratio > 1.3:
          vol_score = 90
      elif volume_ratio > 1.1:
          vol_score = 75
      elif volume_ratio > 0.9:
          vol_score = 60
      elif volume_ratio > 0.7:
          vol_score = 45
      else:
          vol_score = 30
      
      # 加权
      score = m2_score * 0.4 + shibor_score * 0.3 + vol_score * 0.3
      
      return {
          "score": round(score, 1),
          "m2_yoy": m2_yoy,
          "shibor": shibor_overnight,
          "volume_ratio": round(volume_ratio, 2),
          "breakdown": {
              "m2": m2_score,
              "shibor": shibor_score,
              "volume": vol_score,
          },
          "interpretation": _interpret_liquidity(score, m2_yoy),
      }
  ```

数据来源：
  - M2：Wind / 央行官网（月频，滞后）
  - SHIBOR：Wind / shibor.org（日频）
  - 成交额：日 OHLCV（已有）

更新频率：日频（M2 用最新可用值，每月更新一次）
```

### 2.5 维度 4：风险偏好（15%）

```text
指标：
  - A 股：沪深 300 的 20 日历史波动率（HV20）
  - 港股：恒生指数 VIX（若不可得，用 HV20 替代）
  - 美股：VIX 指数（间接反映全球风险偏好）

逻辑：
  - 波动率低 → 市场情绪稳定 → 风险偏好高 → 高分
  - 波动率高 → 市场情绪恐慌 → 风险偏好低 → 低分
  - VIX 飙升 → 全球避险 → 低分

评分算法：
  ```python
  def score_risk_appetite(hv20_csi300: float, vix: float | None) -> dict:
      """
      风险偏好评分
      
      波动率越低，评分越高（逆序）
      """
      # 沪深 300 HV20 评分（占比 60%）
      if hv20_csi300 < 0.15:
          hv_score = 90
      elif hv20_csi300 < 0.20:
          hv_score = 75
      elif hv20_csi300 < 0.25:
          hv_score = 60
      elif hv20_csi300 < 0.35:
          hv_score = 45
      else:
          hv_score = 30
      
      # VIX 评分（占比 40%，若不可得则只用 HV20）
      if vix is not None:
          if vix < 15:
              vix_score = 90
          elif vix < 20:
              vix_score = 75
          elif vix < 25:
              vix_score = 60
          elif vix < 30:
              vix_score = 45
          else:
              vix_score = 30
          
          score = hv_score * 0.6 + vix_score * 0.4
      else:
          score = hv_score
      
      return {
          "score": round(score, 1),
          "hv20_csi300": round(hv20_csi300 * 100, 2),
          "vix": vix,
          "interpretation": _interpret_ra(score, hv20_csi300),
      }
  ```

数据来源：
  - HV20：从日 OHLCV 计算（已有数据）
  - VIX：Wind / Yahoo Finance（日频）

更新频率：日频（收盘后更新）
```

### 2.6 维度 5：政策环境（15%）

```text
指标：
  - 货币政策：降准/降息/MLF操作
  - 财政政策：专项债发行/减税降费
  - 监管政策：IPO节奏/减持规定/交易规则变化
  - 产业政策：重点支持/限制行业

逻辑：
  - 宽松/支持 → 利好股市 → 高分
  - 紧缩/限制 → 利空股市 → 低分

评分算法（半自动）：
  ```python
  def score_policy(events: list[dict], analyst_input: dict | None) -> dict:
      """
      政策环境评分
      
      这是一个半自动模块：
      - 系统自动识别已知政策事件（降准/降息等）
      - 重大/模糊事件需要人工输入 analyst_input
      
      Args:
          events: 近期政策事件列表
          analyst_input: 分析师手动输入的政策评估（可选）
      
      Returns:
          {
              "score": float,
              "events": list,       # 识别的政策事件
              "manual_override": bool,  # 是否有人工覆盖
          }
      """
      score = 50  # 默认中性
      
      # 自动评分规则
      for event in events:
          event_type = event.get("type")
          if event_type == "rrr_cut":           # 降准
              score += 10
          elif event_type == "rate_cut":        # 降息
              score += 15
          elif event_type == "mlf_injection":   # MLF 净投放
              score += 8
          elif event_type == "ipo_speedup":     # IPO 加速
              score -= 10
          elif event_type == "restrictions":    # 交易限制
              score -= 15
          elif event_type == "industry_support": # 产业支持
              score += 5
          elif event_type == "industry_restriction": # 产业限制
              score -= 5
      
      score = max(0, min(100, score))
      
      # 人工覆盖（如果提供）
      manual_override = False
      if analyst_input:
          score = analyst_input.get("score", score)
          manual_override = True
      
      return {
          "score": round(score, 1),
          "events": events,
          "event_count": len(events),
          "manual_override": manual_override,
          "interpretation": _interpret_policy(score, events),
      }
  ```

数据来源：
  - 自动：央行公告/证监会公告/国务院文件（需 NLP 或规则匹配）
  - 人工：用户或分析师定期输入

更新频率：事件驱动 + 每周检查一次

重要说明：
  - 政策评分是五个维度中"主观性最强"的
  - 默认采用"中性=50分"，避免过度解读
  - 重大政策（如降准 50bp、印花税调整）才有显著分数变化
  - 建议用户每周审查一次政策评分，必要时手动调整
```

---

## 三、综合评分计算

### 3.1 加权公式

```python
class MacroEnvironmentScorer:
    """
    宏观环境综合评分器
    """
    
    WEIGHTS = {
        "interest_rate": 0.25,
        "exchange_rate": 0.20,
        "liquidity": 0.25,
        "risk_appetite": 0.15,
        "policy": 0.15,
    }
    
    def calculate(self, data: dict) -> dict:
        """
        计算宏观环境综合评分
        
        Args:
            data: {
                "cgb10y": float,
                "cgb10y_history": pd.Series,
                "usdcny": float,
                "usdcny_history": pd.Series,
                "m2_yoy": float,
                "shibor_overnight": float,
                "market_volume": float,
                "volume_history": pd.Series,
                "hv20_csi300": float,
                "vix": float | None,
                "policy_events": list[dict],
                "policy_analyst_input": dict | None,
            }
        
        Returns:
            {
                "macro_score": float,           # 0-100 综合评分
                "interpretation": str,          # 文字解读
                "regime": str,                  # friendly/neutral/unfriendly
                "dimensions": dict,             # 五个维度的明细
                "recommendation": dict,         # 对 PeriodQueen 的建议
            }
        """
        # 计算各维度
        ir = score_interest_rate(data["cgb10y"], data["cgb10y_history"])
        fx = score_exchange_rate(data["usdcny"], data["usdcny_history"])
        liq = score_liquidity(
            data["m2_yoy"], data["shibor_overnight"],
            data["market_volume"], data["volume_history"]
        )
        ra = score_risk_appetite(data["hv20_csi300"], data.get("vix"))
        pol = score_policy(data.get("policy_events", []), data.get("policy_analyst_input"))
        
        # 加权计算
        macro_score = (
            ir["score"] * self.WEIGHTS["interest_rate"] +
            fx["score"] * self.WEIGHTS["exchange_rate"] +
            liq["score"] * self.WEIGHTS["liquidity"] +
            ra["score"] * self.WEIGHTS["risk_appetite"] +
            pol["score"] * self.WEIGHTS["policy"]
        )
        
        # 解读
        if macro_score >= 80:
            regime = "friendly"
            interpretation = "宏观环境极度友好，资金面充裕，风险偏好高，建议积极"
        elif macro_score >= 60:
            regime = "warm"
            interpretation = "宏观环境偏暖，整体有利，正常交易"
        elif macro_score >= 40:
            regime = "neutral"
            interpretation = "宏观环境混沌，方向不明，谨慎交易"
        elif macro_score >= 20:
            regime = "cold"
            interpretation = "宏观环境偏冷，资金收紧，降低仓位"
        else:
            regime = "hostile"
            interpretation = "宏观环境极度不利，建议防御或空仓"
        
        # 对 PeriodQueen 的建议
        recommendation = self._recommend_to_period_queen(macro_score, regime)
        
        return {
            "macro_score": round(macro_score, 1),
            "interpretation": interpretation,
            "regime": regime,
            "dimensions": {
                "interest_rate": ir,
                "exchange_rate": fx,
                "liquidity": liq,
                "risk_appetite": ra,
                "policy": pol,
            },
            "recommendation": recommendation,
        }
    
    def _recommend_to_period_queen(self, score: float, regime: str) -> dict:
        """
        生成对 PeriodQueen 的建议
        
        PeriodQueen 可以选择性地采纳这些建议：
        - 宏观评分是"输入"，不是"命令"
        - PeriodQueen 保留最终决策权
        """
        recommendations = {
            "friendly": {
                "position_ceiling_adjustment": +0.10,  # 仓位上限 +10%
                "entry_min_votes_adjustment": -1,      # 投票门槛 -1
                "risk_tolerance": "elevated",
                "note": "宏观顺风，可适当激进",
            },
            "warm": {
                "position_ceiling_adjustment": +0.05,
                "entry_min_votes_adjustment": 0,
                "risk_tolerance": "normal",
                "note": "宏观偏暖，正常交易",
            },
            "neutral": {
                "position_ceiling_adjustment": 0,
                "entry_min_votes_adjustment": 0,
                "risk_tolerance": "normal",
                "note": "宏观混沌，保持谨慎",
            },
            "cold": {
                "position_ceiling_adjustment": -0.10,
                "entry_min_votes_adjustment": +1,
                "risk_tolerance": "reduced",
                "note": "宏观偏冷，降低仓位",
            },
            "hostile": {
                "position_ceiling_adjustment": -0.20,
                "entry_min_votes_adjustment": +2,
                "risk_tolerance": "defensive",
                "note": "宏观逆风，防御为主",
            },
        }
        
        return recommendations.get(regime, recommendations["neutral"])
```

### 3.2 与 PeriodQueen 的联动

```text
联动规则（建议性，非强制性）：

PeriodQueen 原始参数：
  - ATTACK_SUSTAINED: max_size = 1.0, entry_min_votes = 3

MacroEnvironmentScorer 建议调整：
  - macro_score ≥ 80: max_size += 0.10 → 1.10（但不超过绝对上限 1.15）
  - macro_score ≤ 20: max_size -= 0.20 → 0.80

调整公式：
  ```python
  def adjust_pq_params(pq_params: dict, macro_score: float) -> dict:
      adjusted = pq_params.copy()
      
      if macro_score >= 80:
          adjusted["max_size"] = min(pq_params["max_size"] + 0.10, 1.15)
          adjusted["entry_min_votes"] = max(pq_params["entry_min_votes"] - 1, 2)
      elif macro_score <= 20:
          adjusted["max_size"] = max(pq_params["max_size"] - 0.20, 0.30)
          adjusted["entry_min_votes"] = min(pq_params["entry_min_votes"] + 2, 6)
      
      return adjusted
  ```

重要原则：
  - MacroEnvironmentScorer 的建议是"软性建议"
  - PeriodQueen 可以采纳，也可以不采纳
  - 采纳比例由用户配置（默认采纳 50%）
  - 极端情况下（macro_score < 10），PeriodQueen 必须采纳
```

---

## 四、输出格式

```python
MACRO_ENVIRONMENT_OUTPUT = {
    "object_id": "MACRO_ENV_P0_F",
    "object_name": "宏观环境评分",
    "function_bucket": "FILTER",
    "process_layer": "L1_ENV",
    
    "timestamp": "2024-06-24T15:00:00+08:00",
    "macro_score": 62.5,              # 综合评分
    "regime": "warm",                 # friendly/warm/neutral/cold/hostile
    "interpretation": "宏观环境偏暖，整体有利，正常交易",
    
    "dimensions": {
        "interest_rate": {
            "score": 75.0,
            "current": 2.35,
            "percentile": 20.5,
            "trend": "falling",
            "interpretation": "利率环境友好（falling），资金成本适中",
        },
        "exchange_rate": {
            "score": 55.0,
            "current": 7.2450,
            "change_20d": -0.15,
            "interpretation": "汇率环境中性，小幅贬值",
        },
        "liquidity": {
            "score": 65.0,
            "m2_yoy": 10.5,
            "shibor": 1.85,
            "volume_ratio": 1.12,
            "interpretation": "流动性偏充裕",
        },
        "risk_appetite": {
            "score": 60.0,
            "hv20_csi300": 18.5,
            "vix": 16.2,
            "interpretation": "风险偏好中性",
        },
        "policy": {
            "score": 55.0,
            "events": [{"type": "rrr_cut", "date": "2024-06-15"}],
            "manual_override": False,
            "interpretation": "政策中性偏松，近期有降准",
        },
    },
    
    "recommendation": {
        "position_ceiling_adjustment": 0.05,
        "entry_min_votes_adjustment": 0,
        "risk_tolerance": "normal",
        "note": "宏观偏暖，正常交易",
    },
    
    # 统一输出字段
    "signal_type": "NONE",            # 宏观环境不产生交易信号
    "signal_strength": 0,
    "signal_confidence": 0.625,       # macro_score / 100
    "maturity_status": "proxy_quantizable_now",
    "data_requirement": "宏观数据（利率/汇率/M2/SHIBOR/波动率/政策事件）",
}
```

---

## 五、实施路线图

```text
Phase 1：数据管道（Week 1）
  - 建立宏观数据 ETL 管道
  - 数据源：Wind（优先）/ tushare / akshare
  - 存储：每日一张 Parquet 表（macro_daily_YYYYMMDD.parquet）

Phase 2：各维度评分器（Week 1-2）
  - InterestRateScorer
  - ExchangeRateScorer
  - LiquidityScorer
  - RiskAppetiteScorer
  - PolicyScorer

Phase 3：综合评分器（Week 2）
  - MacroEnvironmentScorer（整合五个维度）
  - 与 PeriodQueen 的联动接口

Phase 4：回测验证（Week 3）
  - 验证宏观评分对系统绩效的贡献
  - 对比：有宏观评分 vs 无宏观评分
  - 目标：夏普提升 > 0.05，回撤降低 > 1%

Phase 5：日报集成（Week 3-4）
  - 将宏观评分纳入 AI 投研日报
  - 自动生成五维度解读文字
```

---

## 六、对编程 AI 的指令

```text
1. MacroEnvironmentScorer 不是对象卡，而是"环境过滤器"
2. 它的输出作为 PeriodQueen 的输入之一
3. 五个维度中，政策维度允许人工覆盖
4. 所有评分算法必须有明确的数学公式，不能黑盒
5. 历史数据缓存到本地，避免重复下载
6. 日频更新，收盘后自动计算
7. 输出必须包含"interpretation"文字解读（供日报使用）
```

---

> 文件：MACRO_ENVIRONMENT_SCORER_v1.0.md
> 生产者：Kimi（整理用户的"私人投研管家"素材）
> 核心设计：五维度评分体系（利率25%/汇率20%/流动性25%/风险偏好15%/政策15%）
> 与 PeriodQueen 的关系：软性建议，非强制命令
