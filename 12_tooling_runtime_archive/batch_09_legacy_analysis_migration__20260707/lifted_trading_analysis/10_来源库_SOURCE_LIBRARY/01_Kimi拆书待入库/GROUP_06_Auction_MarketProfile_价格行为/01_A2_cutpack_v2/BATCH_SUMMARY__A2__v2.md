# A2_BATCH_SUMMARY__Auction_MarketProfile_IntradayStructure

## 批次信息

| 字段 | 内容 |
|------|------|
| **batch_id** | A2 |
| **batch_theme** | Auction / Market Profile / 盘中结构 |
| **cut_date** | 2025-06-16 |
| **model_mode** | kimi |
| **contract_used** | CUT_CONTRACT__Kimi_保留型切割_v2 |
| **total_books** | 4 |
| **extractable_books** | 4 |
| **scan_only_books** | 0 |

---

## 批次切割产出清单

| # | 文件名 | 书名 | 页数 | 状态 | 大小 |
|---|--------|------|------|------|------|
| 1 | `A2_Dalton_MindOverMarkets.md` | Mind Over Markets | 356 | 完成 | ~19.6 KB |
| 2 | `A2_Dalton_MarketsInProfile.md` | Markets in Profile | 225 | 完成 | ~23.5 KB |
| 3 | `A2_Harris_TradingAndExchanges.md` | Trading and Exchanges | 657 | 完成 | ~25.9 KB |
| 4 | `CUTPACK__A2__CN__市场轮廓理论__part1__v2.md` + `part2` | 市场轮廓理论 | 238 | 完成（split cutpack） | ~80.9 KB |

> 说明：`市场轮廓理论` 已由旧的单文件 `NEEDS_OCR` 占位版，替换为基于 `epub` 主文本与 `pdf` 交叉核对的正式 split cutpack。下文所有旧的“待OCR”判断均作废，以 `part1/part2` 为准。

---

## 核心对象覆盖矩阵

| 对象 | Dalton1 | Dalton2 | Harris | 市场轮廓理论 | 可量化标记 | A股对齐优先级 |
|------|---------|---------|--------|-------------|-----------|--------------|
| **initial balance** | ✅ 27 hits | ✅ 10 hits | ⚪ | ✅ 已完成 | `proxy_quantizable_now` | 🔴 高 |
| **value area** | ✅ 174 hits | ✅ 62 hits | ⚪ | ✅ 已完成 | `proxy_quantizable_now` | 🔴 高 |
| **point of control (POC)** | ✅ 34 hits | ✅ 3 hits | ⚪ 5 hits | ✅ 已完成 | `proxy_quantizable_now` | 🔴 高 |
| **single prints** | ✅ 12 hits | ✅ 6 hits | ⚪ | ✅ 已完成 | `proxy_quantizable_now` | 🟡 中 |
| **excess / tails** | ✅ 101 hits | ✅ 36 hits | ⚪ 78 hits | ✅ 已完成 | `needs_extra_data` | 🟡 中 |
| **balance / imbalance** | ✅ 251 hits | ✅ 223 hits | ⚪ 95 hits | ✅ 已完成 | `proxy_quantizable_now` | 🔴 高 |
| **trend day** | ✅ 75 hits | ✅ 33 hits | ⚪ | ✅ 已完成 | `proxy_quantizable_now` | 🔴 高 |
| **normal day** | ✅ 19 hits | ⚪ 1 hit | ⚪ | ✅ 已完成 | `proxy_quantizable_now` | 🟡 中 |
| **neutral day** | ✅ 17 hits | ⚪ 1 hit | ⚪ | ✅ 已完成 | `proxy_quantizable_now` | 🟡 中 |
| **double distribution** | ✅ 9 hits | ⚪ | ⚪ | ✅ 已完成 | `proxy_quantizable_now` | 🟡 中 |
| **responsive activity** | ✅ 88 hits | ✅ 10 hits | ⚪ 7 hits | ✅ 已完成 | `proxy_quantizable_now` | 🔴 高 |
| **initiative activity** | ✅ 78 hits | ✅ 7 hits | ⚪ 7 hits | ✅ 已完成 | `proxy_quantizable_now` | 🔴 高 |
| **open drive** | ⚪ 0 hits | ⚪ 0 hits | ⚪ | ✅ 已完成 | `proxy_quantizable_now` | 🔴 高 |
| **open test drive** | ⚪ 0 hits | ⚪ 0 hits | ⚪ | ✅ 已完成 | `proxy_quantizable_now` | 🔴 高 |
| **open rejection reverse** | ⚪ 0 hits | ⚪ 0 hits | ⚪ | ✅ 已完成 | `proxy_quantizable_now` | 🔴 高 |
| **opening auction** | ✅ 1 hit | ⚪ | ⚪ 14 hits (continuous) | ✅ 已完成 | `proxy_quantizable_now` | 🔴 高 |
| **auction process** | ✅ 18 hits | ✅ 42 hits | ⚪ | ✅ 已完成 | `proxy_quantizable_now` | 🔴 高 |
| **TPO** | ✅ 242 hits | ✅ 10 hits | ⚪ 1 hit | ✅ 已完成 | `proxy_quantizable_now` | 🟡 中 |
| **order book / DOM** | ✅ 33 hits | ✅ 15 hits | ✅ 90 hits | ✅ 已完成 | `needs_extra_data` | 🔴 高 |
| **level 2 / level II** | ⚪ | ⚪ | ✅ 5+2 hits | ✅ 已完成 | `needs_extra_data` | 🔴 高 |
| **call auction** | ⚪ | ⚪ | ✅ 0 hits (term not found) | ✅ 已完成 | `proxy_quantizable_now` | 🔴 高 |
| **continuous auction** | ⚪ | ⚪ | ✅ 14 hits | ✅ 已完成 | `proxy_quantizable_now` | 🔴 高 |
| **bid-ask spread** | ⚪ | ⚪ | ✅ (inferred) | ✅ 已完成 | `proxy_quantizable_now` | 🟡 中 |
| **trading halts / price limits** | ⚪ | ⚪ | ✅ (Ch.18) | ✅ 已完成 | `proxy_quantizable_now` | 🟡 中 |

---

## 数据源需求汇总

### `proxy_quantizable_now` (可用 OHLCV + session calendar 近似)
| 类别 | 具体对象 |
|------|----------|
| 日内结构 | initial balance, value area, POC, range extension, single prints proxy, TPO count proxy, rotation factor |
| 日类型 | Normal Day, Trend Day, Double-Distribution, Neutral Day, Nontrend Day |
| 活动分类 | Initiative Activity, Responsive Activity, Open-Drive, Open-Test-Drive, Open-Rejection-Reverse |
| 长期结构 | Bracketing vs. Trending, Value Area Shift, Balance Area Breakout, Gap |
| 开盘结构 | Opening Type (Within/Outside Value/Range), 集合竞价结果分析 |
| 交易成本 | Bid-Ask Spread, Price Impact (proxy), Volatility Regime |
| 特殊形态 | Spike, Poor High/Low, Auction Failure, 3-1 Day |

### `needs_extra_data` (需逐笔 / DOM / orderbook / Level2)
| 类别 | 具体对象 |
|------|----------|
| 订单簿结构 | Full LOB reconstruction, market depth, hidden orders, DOM imbalance |
| 参与者识别 | Other timeframe control, dealer inventory, participant type map |
| 微观质量 | True single print rejection vs. thin market, true excess confirmation, adverse selection per trade |
| 信息流 | VPIN (order flow toxicity), real-time bracket health, cross-market linkage |
| 交易成本 | Implementation shortfall (needs own trade data), true market impact decomposition |

### `future_bucket` (pending_ocr / pending_data)
| 类别 | 具体对象 |
|------|----------|
| 中文教材 | 更高精度图表OCR、术语校勘表、图表页补锚点 |
| 高精度数据 | Tick-level volume profile, millisecond-level LOB, cross-asset microstructure |
| 监管数据 | 席位资金流向、机构持仓分类、大宗交易内部细节 |

---

## A股集合竞价/开盘结构对齐方案

### 对齐映射表

| Market Profile / Auction 概念 | A股对应结构 | 数据来源 | 实现优先级 |
|------------------------------|------------|----------|-----------|
| **Opening Auction (Call Auction)** | 9:15-9:25 集合竞价 | 交易所集合竞价数据 | 🔴 P0 |
| **Initial Balance (A+B periods)** | 9:30-10:00 连续竞价首30-60分钟 | 分钟K线 / 逐笔 | 🔴 P0 |
| **POC (Point of Control)** | 早盘成交量峰值价 / 日内VWAP | 分钟K线成交量 | 🔴 P0 |
| **Value Area (70%)** | 日内成交量分布70%区间 | 分钟K线 | 🔴 P0 |
| **Open-Drive** | 重大利好/利空下高开高走/低开低走 | 开盘价+分钟K线 | 🔴 P0 |
| **Open-Test-Drive** | 开盘后短暂震荡再突破 | 分钟K线 | 🔴 P0 |
| **Open-Rejection-Reverse** | 开盘后冲高被拒回落 / 下探回升 | 分钟K线 | 🔴 P0 |
| **Single Prints / Tails** | 集合竞价/开盘后无成交价格区 | 逐笔/分钟K线 | 🟡 P1 |
| **Gap** | 隔夜/集合竞价跳空缺口 | 标准OHLC | 🔴 P0 |
| **Responsive Activity** | 开盘偏离前日价值后日内回归 | 前日VA+分钟K线 | 🟡 P1 |
| **Initiative Activity** | 突破箱体后趋势延续 | 多日线+分钟K线 | 🟡 P1 |
| **Auction Failure** | 假突破/诱多/诱空 | 分钟K线 | 🟡 P1 |
| **Bracketing (箱体震荡)** | 多日振幅重叠 | 多日线 | 🟡 P1 |
| **Trending (趋势)** | 多日价值区间方向移动 | 多日线 | 🟡 P1 |
| **Spike** | 尾盘/盘中极端冲刺 | 分钟K线 | 🟡 P1 |
| **Price Limits (涨跌停)** | A股10%/20%涨跌停 | 标准OHLC | 🔴 P0 |
| **LOB Depth** | Level2 十档订单簿 | 付费Level2 | 🟢 P2 |
| **Order Flow Toxicity** | 知情交易概率 | 逐笔 | 🟢 P2 |

### 特别说明：A股交易时间 → TPO 字母映射

| 时段 | 时间 | TPO字母 | 备注 |
|------|------|---------|------|
| 集合竞价 | 9:15-9:25 | Pre-A | 产生开盘价 |
| A | 9:30-10:00 | A | 初始平衡核心时段 |
| B | 10:00-10:30 | B | 初始平衡延续（S&P风格） |
| C | 10:30-11:00 | C | 区间扩展开始 |
| D | 11:00-11:30 | D | 上午收盘前 |
| 午休 | 11:30-13:00 | — | 无交易 |
| E | 13:00-13:30 | E | 下午开盘 |
| F | 13:30-14:00 | F | 下午中段 |
| G | 14:00-14:30 | G | 下午后段 |
| H | 14:30-15:00 | H | 收盘前（A股无I字母，顺延） |
| 收盘竞价 | 14:57-15:00 | Close | 深市/创业板收盘集合竞价 |

> **注意**: A股午休时段（11:30-13:00）与期货市场不同，分析长期轮廓时需考虑午休对日结构的影响。Dalton 原著基于 CME 期货（无午休），A股适配需调整。

---

## 下一步行动（批次级）

### 立即执行（P0 - 本周）
1. **A股初始平衡计算器**: 实现开盘后30/60分钟区间计算模块
2. **日内 Volume-Profile / POC 计算**: 基于分钟K线实现日内价值区间和控制点
3. **开盘类型分类器**: 实现 Open Within Value / Outside Value / Outside Range 三类分类
4. **日类型快速分类器**: 基于 OHLCV 实现 Normal/Trend/Neutral/Nontrend 初步分类
5. **提取中文术语表**: 从 `市场轮廓理论` part1/part2 汇总中英术语和 A 股映射

### 短期执行（P1 - 2周内）
1. **A股 TPO 字母标记系统**: 将A股交易时间映射为 A-H 时段，标记分钟K线
2. **Rotation Factor 实现**: 逐30/60分钟K线计算方向累加
3. **Initiative/Responsive 分类器**: 基于前日价值区间判断当日活动类型
4. **Spike / Gap / Auction Failure 检测器**: 日内特殊形态识别
5. **Bracketing/Trending 多日线分类器**: 基于N日价值区间重叠度判断

### 中期执行（P2 - 1月内）
1. **图表页补锚点**: 对 `市场轮廓理论` 中图表/价格网格页做人工补页码与图例说明
2. **Level2 数据接入评估**: 评估A股Level2数据源（交易所、第三方）及成本
3. **逐笔数据接入评估**: 评估逐笔成交/委托数据源
4. **Market Impact 模型校准**: 用A股历史大单数据校准 square-root 模型参数
5. **跨市场联动分析**: 现货-期货-ETF 的拍卖过程联动监测

### 长期储备（Future Bucket）
1. **True LOB Reconstruction**: 基于逐笔委托的完整订单簿重建
2. **VPIN / Order Flow Toxicity**: 知情交易概率实时监测
3. **Real-Time Manipulation Detection**: 幌骗、Layering等异常模式检测
4. **Dealer Inventory Tracking**: 科创板/北交所做市商库存动态
5. **Cross-Border Microstructure**: 港股通、沪伦通的跨市场微观结构分析

---

## 关键风险与限制

| 风险 | 描述 | 缓解措施 |
|------|------|----------|
| **文本层与图表混合** | `epub` 主文本可用，但少量图表页仍需 `pdf` 辅助核对 | 人工校对关键章节；术语表对照Dalton原著；图表页补锚点 |
| **A股T+1制度差异** | Dalton理论基于期货T+0，A股T+1影响日内策略 | 标记T+1影响；响应性活动分析调整 |
| **涨跌停板扭曲** | A股10%/20%涨跌停限制价格发现 | 涨跌停标记为特殊状态；分析时剔除或单独处理 |
| **午休时段断裂** | A股11:30-13:00无交易，与期货市场不同 | 日结构分析中标记午休；下午开盘视为新探索 |
| **Level2数据成本** | 完整Level2数据需要付费终端 | 先用Level1近似；评估Level2 ROI后接入 |
| **术语翻译偏差** | 中文教材翻译可能与英文原著有偏差 | 建立中英对照术语表；关键概念以英文原文为准 |
| **集合竞价信息有限** | A股集合竞价仅披露匹配量和未匹配量 | 充分利用现有数据；评估是否需要更细粒度数据 |

---

*End of A2 Batch Summary*
*Generated: 2025-06-16*
*Batch: A2 - Auction / Market Profile / 盘中结构*
