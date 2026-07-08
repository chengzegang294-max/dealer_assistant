# GAS_12_INDICATOR_MAP_P0_A — GAS 12 指标参数映射到现有对象卡 v1.0

> 版本：v1.0 | 状态：参数映射参考文档 | 与现有对象卡配合使用
> 目标：将 GAS 12 指标的参数和阈值提取出来，补充到现有对象卡，避免创建冗余对象卡
> 核心原则：GAS 指标是现有对象卡的"参数参考"，不单独创建对象卡

---

## 1. 映射总览

| GAS 指标 | 诗意名称 | 核心功能 | 对应现有对象卡 | 可补充参数 | 是否需要新对象卡 |
|----------|----------|----------|----------------|------------|----------------|
| 五里神马 | 量增价涨 | 量价确认 | MFLOW（资金流向）/ PV_CORR（价量相关性） | 量价同步阈值 | 否 |
| 五里金山 | 量缩价稳 | 蓄势整理 | VOLFAC（波动率）/ VP（成交量分布） | 缩量整理识别 | 否 |
| 五里趋势 | DIFF 金叉+拐点 | 趋势启动 | KD_MTF / GMMA / CHZL_TREND | EMA 组合参数 | 否 |
| 随波逐流 | EMA 趋势跟随 | 趋势跟踪 | GMMA / CHZL_TREND | EMA 斜率阈值 | 否 |
| 觅庄建仓 | 主力吸筹信号 | 资金流入 | MFLOW（资金流向） | 吸筹确认条件 | 否 |
| 高山低谷 | 波峰波谷判断 | 支撑阻力 | VP（HVN/LVN）/ CHZL_FX（分型） | 波峰波谷量化 | 否 |
| 进退有度 | 止损/止盈规则 | 风险管理 | Van Tharp / CHZL_BSD / KELLY | 移动止盈规则 | 否 |
| 否极泰来 | RSI 超卖反弹 | 极端反转 | KD_MTF（KD 极端区）/ TKR7（AO 背离） | RSI 阈值修正 | 否 |
| 归真返璞 | MACD 归零轴 | 趋势回归 | CHZL_BEICHI（背驰） | MACD 零轴参考 | 否 |
| 物极必反 | RSI 超买超卖 | 极端预警 | KD_MTF（KD 极端区） | RSI 75/25 阈值 | 否 |
| 八字箴言 | 动量确认 | 动量过滤 | TKR7（AO 动量）/ VOLTY | 动量确认规则 | 否 |
| 明镜非台 | 多指标共振 | 信号过滤 | 投票机制（VOTE_POOL） | 共振评分标准 | 否 |

---

## 2. 详细映射与参数补充

### 2.1 五里神马 → MFLOW / PV_CORR

```text
GAS 定义：量增价涨 = 成交量放大 + 价格上涨 → 确认趋势有效

对应现有对象卡：
  - MFLOW_P0_A：mflow_inflow_ratio（主力净流入）+ mflow_sellord_ratio（主力流出单数）
  - PV_CORR：pv_corr_value（价量相关性）

可补充参数：
  ```text
  mflow_volume_price_sync_threshold  FLOAT  -- 量价同步阈值：
                                              -- 当 volume > 前20日均量 × 1.5 AND close > open × 1.02
                                              -- → 标记为 "量增价涨"
                                              -- 这与 GAS "五里神马" 的定义一致
                                              -- 用途：增强 MFLOW 的 "MAIN_FORCE_IN" 信号
                                              -- 当 mflow_signal_type = 'MAIN_FORCE_IN' 且量价同步 → strength +1
  
  pv_corr_gas_sync_window  INT  -- GAS 量价同步观察窗口（默认 5 日）：
                                    -- 连续 5 日 volume > 前20日均量 AND close > 前日 close
                                    -- → 标记为 "持续量增价涨"
                                    -- 用途：在 PV_CORR 中增加 "持续同步" 字段
  ```

补充位置：
  - MFLOW_P0_A 对象卡：2.2 派生字段中增加 mflow_volume_price_sync
  - PV_CORR 对象卡：增加 pv_corr_gas_sync 字段
```

### 2.2 五里金山 → VOLFAC / VP

```text
GAS 定义：量缩价稳 = 成交量萎缩 + 价格稳定 → 蓄势整理，可能突破

对应现有对象卡：
  - VOLFAC_P0_A：volfac_vol_regime（波动率状态）
  - VP_P0_E：volume_integrity_score（成交量完整性）

可补充参数：
  ```text
  volfac_consolidation_signal  ENUM  -- 缩量整理信号：
                                        -- 'NONE' = 无整理信号
                                        -- 'CONSOLIDATION' = 量缩价稳（volume < 前20日均量 × 0.7 AND |price_change| < 2%）
                                        -- 'BREAKOUT_READY' = 整理后放量突破（CONSOLIDATION + 次日放量突破）
                                        -- 这与 GAS "五里金山" 的定义一致
                                        -- 用途：VOLFAC 在 LOW_VOL 状态下，若出现 CONSOLIDATION → 可能即将突破
  
  vp_hvn_consolidation  BOOL  -- HVN 区域的缩量整理：
                                  -- True = 价格在 HVN 区域附近整理，volume < HVN 区域平均量
                                  -- 用途：VP 中识别 HVN 支撑/阻力位的蓄势阶段
  ```

补充位置：
  - VOLFAC_P0_A 对象卡：2.3 派生字段中增加 volfac_consolidation_signal
  - VP_P0_E 对象卡：2.4 信号字段中增加 vp_hvn_consolidation
```

### 2.3 五里趋势 → KD_MTF / GMMA / CHZL_TREND

```text
GAS 定义：五里趋势 = DIFF 金叉 + 拐点确认 → 趋势启动

对应现有对象卡：
  - KD_MTF_P0：kd_week_extreme_zone（周线极端区）
  - GMMA（用户仓库中提到的概念，可能已有对象卡）
  - CHZL_TREND：chzl_trend_type（走势类型）

可补充参数：
  ```text
  kd_mtf_ema_combo  ENUM  -- EMA 组合判断（GAS 五里趋势的核心）：
                              -- 'GOLDEN_CROSS' = 短期 EMA（5/13）上穿长期 EMA（21/55）
                              -- 'DEAD_CROSS' = 短期 EMA 下穿长期 EMA
                              -- 'BULLISH_ALIGN' = 所有 EMA 多头排列（5>13>21>55）
                              -- 'BEARISH_ALIGN' = 所有 EMA 空头排列（5<13<21<55）
                              -- 'MIXED' = 排列混乱，无明确趋势
                              -- 用途：补充 KD_MTF 的趋势判断，与 KD 极端区形成互补
  
  gmma_gas_slope_threshold  FLOAT  -- EMA 斜率阈值（GAS 随波逐流）：
                                      -- 短期 EMA 斜率 > 0.5% / 日 → "顺势"
                                      -- 短期 EMA 斜率 < -0.5% / 日 → "逆势"
                                      -- 斜率绝对值 < 0.5% / 日 → "横盘"
                                      -- 用途：GMMA 对象卡中增加斜率判断，过滤无效趋势
  ```

补充位置：
  - KD_MTF_P0 对象卡：在现有字段中增加 kd_mtf_ema_combo
  - GMMA 对象卡（如有）：增加 gmma_gas_slope_threshold
  - CHZL_TREND：与 EMA 趋势判断互锁（EMA 多头 + 缠论上升趋势 = 高确认）
```

### 2.4 随波逐流 → GMMA / CHZL_TREND

```text
GAS 定义：随波逐流 = EMA 趋势跟随，不逆势操作

对应现有对象卡：
  - GMMA：EMA 组合趋势判断
  - CHZL_TREND：chzl_trend_direction（走势方向）

可补充参数：
  ```text
  chzl_trend_ema_confirm  BOOL  -- 缠论趋势与 EMA 趋势共振确认：
                                    -- True = 缠论上升趋势 + EMA 多头排列（GAS 随波逐流）
                                    -- 用途：CHZL_TREND 中增加 EMA 共振确认，提高趋势判断可靠性
                                    -- 当 chzl_trend_direction = 'up' 且 EMA 多头排列 → 趋势确认度 +1
  ```

补充位置：
  - CHZL_TREND 对象卡：与 GMMA 的互锁规则中增加 EMA 共振确认
```

### 2.5 觅庄建仓 → MFLOW

```text
GAS 定义：觅庄建仓 = 识别主力资金吸筹阶段

对应现有对象卡：
  - MFLOW_P0_A：mflow_main_force_in（主力流入）+ mflow_sellord_ratio（主力流出单数占比）

可补充参数：
  ```text
  mflow_accumulation_pattern  ENUM  -- 主力吸筹模式（GAS 觅庄建仓）：
                                        -- 'NONE' = 无吸筹模式
                                        -- 'STEALTH' = 隐蔽吸筹（小单持续买入，大单偶尔托底）
                                        -- 'AGGRESSIVE' = 激进吸筹（大单持续买入，成交量温和放大）
                                        -- 'PANIC' = 恐慌吸筹（大跌后放量承接，V 型反转）
                                        -- 用途：MFLOW 中增加吸筹模式识别，辅助判断 1Buy（缠论背驰）的可靠性
                                        -- 当 mflow_accumulation_pattern = 'AGGRESSIVE' 且 CHZL_BSD 1Buy → 信号增强
  ```

补充位置：
  - MFLOW_P0_A 对象卡：2.3 派生字段中增加 mflow_accumulation_pattern
```

### 2.6 高山低谷 → VP / CHZL_FX

```text
GAS 定义：高山低谷 = 波峰波谷判断，识别支撑/阻力位

对应现有对象卡：
  - VP_P0_E：poc / vah / val（成交量分布的核心水平）
  - CHZL_FX：fx_price（分型价格）

可补充参数：
  ```text
  vp_gas_peak_trough  ENUM  -- GAS 波峰波谷类型：
                                -- 'PEAK' = 波峰（局部最高点，对应 VP 的 HVN 或 VAH）
                                -- 'TROUGH' = 波谷（局部最低点，对应 VP 的 HVN 或 VAL）
                                -- 'NEUTRAL' = 非波峰非波谷
                                -- 用途：VP 中增加波峰波谷标记，与 HVN/LVN 形成互补
                                -- 波峰 + HVN = 强阻力；波谷 + HVN = 强支撑（罕见，说明筹码集中）
  
  chzl_fx_gas_confirm  BOOL  -- 分型与 GAS 波峰波谷共振：
                                  -- True = 缠论顶分型 + GAS 波峰（高点确认）
                                  -- True = 缠论底分型 + GAS 波谷（低点确认）
                                  -- 用途：CHZL_FX 中增加 GAS 波峰波谷确认，提高分型可靠性
  ```

补充位置：
  - VP_P0_E 对象卡：2.4 信号字段中增加 vp_gas_peak_trough
  - CHZL_FX 对象卡：互锁规则中增加与 GAS 波峰波谷的共振
```

### 2.7 进退有度 → Van Tharp / CHZL_BSD / KELLY

```text
GAS 定义：进退有度 = 止损/止盈规则，有纪律地进出

对应现有对象卡：
  - Van Tharp（硬性上限）：2% 最大风险
  - CHZL_BSD：bsd_stop_price（三类买卖点止损）
  - KELLY：kelly_size_scalar（动态仓位）

可补充参数：
  ```text
  chzl_bsd_trailing_stop  ENUM  -- GAS 移动止盈规则（进退有度的止盈部分）：
                                    -- 'NONE' = 不使用移动止盈
                                    -- 'BREAK_EVEN' = 盈利达到 1R 后，止损移至成本价
                                    -- 'HALF_PROFIT' = 盈利达到 2R 后，止盈一半，剩下一半移动止盈
                                    -- 'TRAILING_ATR' = 使用 ATR 跟踪止盈（如 2×ATR 跟踪）
                                    -- 用途：CHZL_BSD 中增加移动止盈选项，补充固定止损的不足
                                    -- 这与 GAS "进退有度" 的灵活止盈理念一致
  
  kelly_gas_position_map  ENUM  -- GAS 仓位映射（八字箴言中的仓位建议）：
                                    -- 'FULL' = 信号强度 8-10 → Kelly 标准仓位
                                    -- 'HALF' = 信号强度 5-7 → Kelly 半仓
                                    -- 'QUARTER' = 信号强度 3-4 → Kelly 四分之一仓
                                    -- 'SKIP' = 信号强度 < 3 → 不交易
                                    -- 用途：Kelly 对象卡中增加 GAS 仓位映射，作为 size_scalar 的辅助参考
  ```

补充位置：
  - CHZL_BSD 对象卡：2.4 信号字段中增加 chzl_bsd_trailing_stop
  - KELLY 对象卡：2.3 派生字段中增加 kelly_gas_position_map
```

### 2.8 否极泰来 → KD_MTF / TKR7

```text
GAS 定义：否极泰来 = RSI 超卖（< 25）+ 价格企稳 → 反弹信号

对应现有对象卡：
  - KD_MTF：kd_week_extreme_zone = 'OVERSOLD'（超卖区）
  - TKR7：ao_divergence_type = 'REGULAR_BULLISH'（常规底背离）

可补充参数：
  ```text
  kd_mtf_rsi_threshold  FLOAT  -- GAS RSI 阈值（修正传统阈值）：
                                    -- 传统 RSI：超买 70 / 超卖 30
                                    -- GAS 阈值：超买 75 / 超卖 25（更严格，减少假信号）
                                    -- 用途：KD_MTF 中增加 RSI 阈值字段，与 KD 值形成互补
                                    -- 当 RSI < 25 且 KD < 20 → 双重超卖，反弹概率更高
  
  tkr7_gas_rsi_confirm  BOOL  -- GAS RSI 与 AO 背离共振：
                                    -- True = RSI < 25（超卖）+ TKR7 常规底背离 → 反弹信号增强
                                    -- 用途：TKR7 中增加 RSI 确认，与 AO 背离形成双重验证
  ```

补充位置：
  - KD_MTF 对象卡：增加 kd_mtf_rsi_threshold 字段
  - TKR7 对象卡：互锁规则中增加与 RSI 的共振
```

### 2.9 归真返璞 → CHZL_BEICHI

```text
GAS 定义：归真返璞 = MACD 回归零轴 → 趋势力量减弱，可能反转或整理

对应现有对象卡：
  - CHZL_BEICHI：macd_area_a / macd_area_c（MACD 面积对比）

可补充参数：
  ```text
  chzl_beichi_macd_zero_cross  ENUM  -- MACD 零轴穿越（GAS 归真返璞）：
                                          -- 'NONE' = 无零轴穿越
                                          -- 'ABOVE_TO_BELOW' = 从零轴上方穿越到下方（多头力量减弱）
                                          -- 'BELOW_TO_ABOVE' = 从零轴下方穿越到上方（空头力量减弱）
                                          -- 用途：CHZL_BEICHI 中增加零轴穿越判断，辅助背驰识别
                                          -- 当 macd_zero_cross = 'ABOVE_TO_BELOW' 且出现背驰 → 顶背驰确认度 +1
  ```

补充位置：
  - CHZL_BEICHI 对象卡：增加 chzl_beichi_macd_zero_cross 字段
```

### 2.10 物极必反 → KD_MTF

```text
GAS 定义：物极必反 = RSI 超买（> 75）或超卖（< 25）→ 极端状态，可能反转

对应现有对象卡：
  - KD_MTF：kd_week_extreme_zone = 'OVERBOUGHT' / 'OVERSOLD'

可补充参数：
  ```text
  kd_mtf_extreme_gas_confirm  BOOL  -- GAS 极端状态确认：
                                          -- True = KD 极端区（>80/<20）+ RSI 极端（>75/<25）
                                          -- 用途：KD_MTF 中增加 GAS 极端确认，过滤单一指标的假极端
                                          -- 当 KD > 80 且 RSI > 75 → 双重超买，反转概率更高
                                          -- 当 KD < 20 且 RSI < 25 → 双重超卖，反弹概率更高
  ```

补充位置：
  - KD_MTF 对象卡：增加 kd_mtf_extreme_gas_confirm 字段
```

### 2.11 八字箴言 → TKR7 / VOLTY

```text
GAS 定义：八字箴言 = 动量确认，八个字的动量口诀（具体内容需用户确认，推测为动量相关）

对应现有对象卡：
  - TKR7：AO（Awesome Oscillator）动量指标
  - VOLTY：volty_trend_state（趋势状态）

可补充参数：
  ```text
  tkr7_gas_momentum_confirm  ENUM  -- GAS 动量确认（八字箴言）：
                                        -- 'NONE' = 无动量确认
                                        -- 'ACCELERATING' = 动量加速（AO 连续 3 日增大）
                                        -- 'DECELERATING' = 动量减速（AO 连续 3 日减小）
                                        -- 'STABLE' = 动量稳定（AO 波动 < 10%）
                                        -- 用途：TKR7 中增加动量状态判断，辅助背离识别
                                        -- 当 ao_divergence_type = 'REGULAR_BULLISH' 且 momentum = 'ACCELERATING' → 背离信号增强
  ```

补充位置：
  - TKR7 对象卡：增加 tkr7_gas_momentum_confirm 字段
```

### 2.12 明镜非台 → 投票机制（VOTE_POOL）

```text
GAS 定义：明镜非台 = 多指标共振，心如明镜，不被单一指标迷惑

对应现有对象卡：
  - 投票机制（VOTE_POOL）：entry_min_votes = 3

可补充参数：
  ```text
  vote_gas_resonance_score  FLOAT(0-1)  -- GAS 多指标共振评分（明镜非台）：
                                                -- 计算多个指标的同向信号比例
                                                -- 例如：KD 超卖 + RSI 超卖 + MACD 底背离 + AO 底背离 = 4/4 = 1.0（完全共振）
                                                -- 评分 > 0.75 → 高共振，信号可靠性极高
                                                -- 评分 0.5-0.75 → 中等共振，信号可靠
                                                -- 评分 < 0.5 → 低共振，信号可疑
                                                -- 用途：投票机制中增加共振评分，作为 signal_confidence 的辅助
                                                -- 当 resonance_score > 0.75 → signal_confidence 最低为 0.7
  
  vote_gas_indicators[]  ARRAY<STRING>  -- GAS 参与共振的指标列表：
                                                -- 默认 = ["KD", "RSI", "MACD", "AO", "EMA", "VOL", "MFLOW"]
                                                -- 用户可自定义参与共振的指标组合
  ```

补充位置：
  - 投票机制（VOTE_DECISION_TABLE）：在 NODE_005 计算赞成票时，增加共振评分计算
  - 或在 VOTE_DECISION_TABLE 中新增 NODE_005b：共振评分检查
```

---

## 3. 参数补充优先级

| 优先级 | 参数 | 补充对象卡 | 影响程度 | 实施难度 |
|--------|------|------------|----------|----------|
| **高** | kd_mtf_rsi_threshold（RSI 75/25） | KD_MTF | 高（影响极端区判断） | 低（标准指标） |
| **高** | mflow_volume_price_sync_threshold | MFLOW | 高（增强资金流向信号） | 低（简单计算） |
| **中** | chzl_bsd_trailing_stop（移动止盈） | CHZL_BSD | 中（补充固定止损） | 中（需跟踪逻辑） |
| **中** | chzl_beichi_macd_zero_cross | CHZL_BEICHI | 中（辅助背驰识别） | 低（标准 MACD） |
| **中** | tkr7_gas_momentum_confirm | TKR7 | 中（辅助动量判断） | 低（AO 已有） |
| **低** | vote_gas_resonance_score | VOTE_POOL | 中（辅助投票质量） | 中（需多指标计算） |
| **低** | volfac_consolidation_signal | VOLFAC | 低（整理识别） | 中（需模式识别） |
| **低** | mflow_accumulation_pattern | MFLOW | 低（吸筹模式） | 高（需资金流特征工程） |

---

## 4. 对编程 AI 的实现建议

### 4.1 高优先级参数（立即实现）

```python
# 1. KD_MTF 增加 RSI 阈值
def calculate_kd_mtf_with_rsi(kd_data, rsi_data):
    """
    在 KD_MTF 中增加 GAS RSI 阈值（75/25）
    """
    kd_zone = kd_data['kd_week_extreme_zone']
    rsi_value = rsi_data['rsi_14']
    
    # GAS 修正：RSI 75/25 而非传统 70/30
    if rsi_value > 75 and kd_zone == 'OVERBOUGHT':
        kd_data['kd_mtf_extreme_gas_confirm'] = True
        kd_data['signal_confidence'] = min(1.0, kd_data['signal_confidence'] + 0.1)
    elif rsi_value < 25 and kd_zone == 'OVERSOLD':
        kd_data['kd_mtf_extreme_gas_confirm'] = True
        kd_data['signal_confidence'] = min(1.0, kd_data['signal_confidence'] + 0.1)
    else:
        kd_data['kd_mtf_extreme_gas_confirm'] = False
    
    return kd_data

# 2. MFLOW 增加量价同步
def calculate_mflow_with_volume_sync(mflow_data, price_data):
    """
    在 MFLOW 中增加 GAS 量价同步（五里神马）
    """
    volume = price_data['volume']
    avg_volume = price_data['volume_20ma']
    close = price_data['close']
    open_price = price_data['open']
    
    is_sync = volume > avg_volume * 1.5 and close > open_price * 1.02
    
    mflow_data['mflow_volume_price_sync'] = is_sync
    if is_sync and mflow_data['mflow_signal_type'] == 'MAIN_FORCE_IN':
        mflow_data['signal_strength'] = min(10, mflow_data['signal_strength'] + 1)
    
    return mflow_data
```

### 4.2 中优先级参数（第二批实现）

```python
# 3. CHZL_BSD 增加移动止盈
def calculate_chzl_bsd_with_trailing_stop(bsd_data, atr_data, profit_ratio):
    """
    在 CHZL_BSD 中增加 GAS 移动止盈（进退有度）
    """
    if profit_ratio >= 1.0:  # 盈利达到 1R
        bsd_data['chzl_bsd_trailing_stop'] = 'BREAK_EVEN'
        bsd_data['bsd_stop_price'] = bsd_data['entry_price']  # 移至成本价
    elif profit_ratio >= 2.0:  # 盈利达到 2R
        bsd_data['chzl_bsd_trailing_stop'] = 'HALF_PROFIT'
        bsd_data['bsd_target_action'] = 'HALF_EXIT'
    
    return bsd_data

# 4. CHZL_BEICHI 增加 MACD 零轴穿越
def calculate_chzl_beichi_with_zero_cross(beichi_data, macd_data):
    """
    在 CHZL_BEICHI 中增加 GAS 归真返璞（MACD 零轴穿越）
    """
    macd_prev = macd_data['macd_line'][-2]
    macd_curr = macd_data['macd_line'][-1]
    
    if macd_prev > 0 and macd_curr < 0:
        beichi_data['chzl_beichi_macd_zero_cross'] = 'ABOVE_TO_BELOW'
    elif macd_prev < 0 and macd_curr > 0:
        beichi_data['chzl_beichi_macd_zero_cross'] = 'BELOW_TO_ABOVE'
    else:
        beichi_data['chzl_beichi_macd_zero_cross'] = 'NONE'
    
    return beichi_data
```

---

## 5. 结论

```text
GAS 12 指标的处理原则：

1. 不创建新对象卡：所有 GAS 指标都是现有对象卡的参数补充，不是独立信号源
2. 参数提取：从 GAS 中提取有价值的阈值（如 RSI 75/25、量价同步条件），补充到现有对象卡
3. 互锁增强：GAS 指标作为互锁条件的一部分，增强现有信号的可靠性（如 KD + RSI 双重极端确认）
4. 策略映射：GAS 指标参与投票池的共振评分（明镜非台），作为信号质量的辅助判断
5. 优先级：高优先级参数（RSI 阈值、量价同步）在第一批实现，中低优先级在后续批次实现

最终效果：
- 现有对象卡的字段更丰富，参数更贴合 A 股实际
- 不增加系统复杂度，不引入新的决策节点
- GAS 的经验被"吸收"到现有体系中，而非作为独立模块运行
```

---

> 文件：GAS_12_INDICATOR_MAP_P0_A_v1.0.md
> 生产者：Kimi（基于原子规则表中的 GAS 12 指标提取）
> 状态：参数映射参考文档，与现有对象卡配合使用
> 核心交付：
> - 12 个 GAS 指标与现有对象卡的一一映射
> - 每个映射有可补充的具体字段和阈值
> - 参数补充优先级（高/中/低）
> - 对编程 AI 的实现建议（伪代码）
> - 结论：GAS 是参数补充，不是新对象卡
