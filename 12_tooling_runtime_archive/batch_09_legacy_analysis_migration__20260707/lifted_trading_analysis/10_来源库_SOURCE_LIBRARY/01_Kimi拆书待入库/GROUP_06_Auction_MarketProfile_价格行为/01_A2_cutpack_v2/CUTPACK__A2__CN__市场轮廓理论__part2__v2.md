CUTPACK__A2__CN__市场轮廓理论__part2__v2.md

---

# QUANTIZATION_TABLE

| # | concept | raw_rule_from_text | observable_proxy | data_needed | timeframe_hint | quant_status | implementation_hint | notes |
|---|---------|-------------------|------------------|-------------|----------------|--------------|---------------------|-------|
| 1 | **初期平衡 (Initial Balance)** | 由A、B分区（第一小时）组成，主要由风险套利商建立。风险套利商试图寻找满足买卖双方的价位。IB阶段成交量可达全日50%。 | `first_30min_ohlc` 或 `first_60min_ohlc` 区间。`ib_high`, `ib_low`, `ib_range` | OHLCV + 分钟K线（30/60分钟） | 日级别，开盘首小时 | `proxy_quantizable_now` | 取开盘后N根分钟K线（30/60分钟）的最高/最低。A股30分钟=2根K线（9:30-10:00），60分钟=4根K线（9:30-10:30） | 原文基于CBOT期货每半小时一个字母。A股直接映射为分钟/30分钟K线。 |
| 2 | **价值区间 (Value Area)** | 每个交易日总成交70%发生的区间。从成交量最大价位开始，向上下两侧累加相邻价位，直到覆盖70%。 | `volume_profile_70pct_range`：日内成交量分布从峰值价上下累加至70% | OHLCV + 分钟K线（或tick） | 日级别 | `proxy_quantizable_now` | 1. 找日内成交量最大价位（POC）。2. 向上加2个价位、向下加2个价位，比大小。3. 大的一边加入价值区间，累加成交量。4. 重复至≥70% | 附录给出精确算法。TPO法可作为近似。 |
| 3 | **控制点 (POC)** | 最长且最接近价格幅度中部的TPO线。当日成交最活跃、最合理的价格。 | `intraday_volume_peak_price` 或 `volume_weighted_average_price` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 直接用日内成交量最大的价格（close/volume聚合），或用VWAP。分钟级精度足够。 | 多日线POC移动方向=趋势判断。 |
| 4 | **价格幅度扩展 (Range Extension)** | 价格运动超出IB阶段价格幅度。表示长线买方/卖方参与，市场发生变化。风险套利商不是运动主因。 | `price_break_ib_high` / `price_break_ib_low` 后的运行距离。`range_extension_up`, `range_extension_down` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 实时监测价格是否突破`ib_high`/`ib_low`。突破后记录延伸幅度和方向。 | 单边扩展=趋势信号；双向扩展=中立日信号。 |
| 5 | **单字母尾部 / 买入尾部 (Single-Print Buyer Tail)** | 极端低位出现的单字母分区。长线买方热烈响应低于价值的价位。买方竞争使价格快速上升。尾部至少需两个TPO，且在非收盘时段出现。 | `extreme_low_single_print`：分钟K线中最低价仅出现1-2个时段，且快速反弹。`tail_volume_ratio < 5%` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 遍历日内各价位：若在最低20%价格区，且该价位成交时段数≤2，且之后价格迅速回升→标记为买入尾部。 | 严格判断需逐笔/Level2确认"仅1个时段成交"。分钟K线可近似。 |
| 6 | **单字母尾部 / 卖出尾部 (Single-Print Seller Tail)** | 极端高位出现的单字母分区。长线卖方在高价抛售，价格很快降低。 | `extreme_high_single_print`：同理，在最高20%价格区。 | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 与买入尾部对称逻辑。 | 尾部越长（更多价位单字母），拒绝信号越强。 |
| 7 | **收市分区 (Closing Range)** | M分区（最后一个时段）反映当日整体市场情绪。与次日开市价位比较，观察情绪变化。 | `last_30min_range` 或 `last_15min_range`：尾盘区间。`close_vs_prev_close` | OHLCV | 日级别 | `proxy_quantizable_now` | 取最后30/15分钟最高-最低。记录收盘价在其中的位置（高/中/低）。 | 次日开盘价 vs 收市分区 = 情绪连续/变化判断。 |
| 8 | **平衡交易日 (Normal Day)** | 初期平衡阶段价格幅度很宽，全天在IB内震荡。通常由开盘消息引起，长线参与者过早介入。 | `ib_range > 0.6 * avg_daily_range` AND `no_range_extension` AND `close_inside_ib` | OHLCV + 多日线 | 日级别 | `proxy_quantizable_now` | 判断IB区间是否占全日大部分。无扩展且收盘在IB内→平衡日。 | 成交量通常较大（消息刺激）。 |
| 9 | **变形平衡交易日 (Normal Variation)** | IB幅度比平衡日小，之后被长线突破。突破常发生在市场前半段。 | `ib_range < 0.6 * avg_range` AND `range_extension_occurs` AND `close_inside_extended_range` | OHLCV + 多日线 | 日级别 | `proxy_quantizable_now` | IB较小+有扩展+收盘在扩展后的区间内→变形平衡日。 | 变形平衡日=长线有信心但非绝对控制。 |
| 10 | **强趋势交易日 (Trend Day)** | 长线从开盘到收盘单向控制。每个时段都推向更高/更低（单方市）。TPO轮廓狭长，成交量高。 | `open_near_extreme` + `close_near_opposite_extreme` + `consecutive_same_direction_periods >= 4` + `volume > avg_volume` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 开盘后连续N个时段（30/60分钟）同方向运动。开盘在全日极端附近，收盘在另一端极端附近。 | 强趋势日是A股"板块/题材爆发日"的典型结构。 |
| 11 | **弱趋势交易日 / 双重分布 (Double Distribution)** | IB窄，后期长线介入推动价格到新水平，形成第二价值区。两区被单字母TPO分开。 | `bimodal_volume_profile` + `inter_peak_low_volume_zone` + `second_peak_accepted` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 日内成交量分布出现两个峰值，中间有低成交量区（单字母/低成交带）。 | 双重分布="午后再起一波"的A股常见结构。 |
| 12 | **无趋势交易日 (Nontrend Day)** | IB窄，像趋势日但无扩展。市场等待消息。参与者信心不足，成交低。 | `ib_range < 0.4 * avg_range` AND `no_range_extension` AND `volume < 0.7 * avg_volume` | OHLCV + 多日线 | 日级别 | `proxy_quantizable_now` | 窄IB+无扩展+低成交量。A股常见"地量震荡日"。 | 无趋势日→观望。 |
| 13 | **标准中立交易日 (Neutral Day)** | 买卖双方都在两端扩展，收盘在中间。双方力量均衡。 | `range_extension_both_directions` AND `close_in_middle_50pct` | OHLCV | 日级别 | `proxy_quantizable_now` | 同时有向上和向下扩展，且收盘价在全日的中间50%区域。 | 中立日→次日方向选择。 |
| 14 | **高/低收中立交易日 (Neutral-Extreme Day)** | 买卖双方都在两端扩展，但收盘在极端。收市方获胜。 | `range_extension_both_directions` AND `close_in_top_20pct` (高收) OR `close_in_bottom_20pct` (低收) | OHLCV | 日级别 | `proxy_quantizable_now` | 双向扩展+收盘在极端。高收→次日可能高开；低收→次日可能低开。 | 统计上92%次日90分钟内好于前日价值区。 |
| 15 | **驱动开市 (Open-Drive)** | 开盘后价格立即向一个方向有力运动，不反向试探。长线预先决策。 | `first_30min_unidirectional` + `no_retrace > 50%` + `open_outside_prev_range` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 开盘后N分钟（如30分钟）单向运行，最大回撤<初始运动的50%。 | 最强开盘信号。A股利好/利空驱动日。 |
| 16 | **试探驱动开市 (Open-Test-Drive)** | 开市后在已知参考点外探测，确认无新动向后，迅速返回并穿过开市价位，向反方向运动。 | `initial_move_beyond_ref` + `failure_to_extend` + `reversal_through_open` + `new_extreme_in_opposite` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 开盘后先突破某参考位（前高/前低/均线），失败后反向突破开盘价，创出新极端。 | "先回落以便反弹，先反弹以便回落"。 |
| 17 | **失败反转开市 (Open-Rejection-Reverse)** | 开市后沿一个方向运动，遇反向强力量，反转回开盘区间。 | `initial_move_beyond_ib` + `reversal_back_to_open_range` + `close_near_open_or_middle` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 开盘后先突破某一方向，之后回到开盘区间内收盘。确信度低。 | A股常见"诱多/诱空"开盘。 |
| 18 | **无方向感开市—区间内 (Open-Auction in Range)** | 开市价在前一交易日价格幅度内，随机叫价，无方向感。通常发展为无趋势/平衡/中立日。 | `open_inside_prev_range` + `first_30min_oscillation_small` + `no_clear_direction` | OHLCV + 前日数据 | 日级别 | `proxy_quantizable_now` | 开盘价在前日最高-最低之间，开盘后30分钟振幅小，无单边趋势。 | 区间内无方向感→观望。 |
| 19 | **无方向感开市—区间外 (Open-Auction Out of Range)** | 开市价在前一交易日价格幅度外，但围绕开市价震荡。表明新长线交投在寻找新价位。 | `open_outside_prev_range` + `first_30min_oscillation_around_open` + `potential_trend_forming` | OHLCV + 前日数据 | 日级别 | `proxy_quantizable_now` | 开盘价在前日范围外，但开盘后震荡而非单向驱动。观察是否后续形成趋势。 | 区间外无方向感→潜在突破日。 |
| 20 | **响应买方 (Responsive Buying)** | 价格低于价值区间时，长线买方介入，使价格回升。 | `price_below_prev_va` + `buying_pressure_detected` + `price_returns_toward_va` | OHLCV + 前日数据 | 日级别 | `proxy_quantizable_now` | 价格低于前日价值区底部后，出现成交量放大或价格反弹→响应买方信号。 | 响应=价值回归力量。 |
| 21 | **响应卖方 (Responsive Selling)** | 价格高于价值区间时，长线卖方介入，使价格回落。 | `price_above_prev_va` + `selling_pressure_detected` + `price_returns_toward_va` | OHLCV + 前日数据 | 日级别 | `proxy_quantizable_now` | 价格高于前日价值区顶部后，出现抛压或回调→响应卖方信号。 | 响应=价值回归力量。 |
| 22 | **主动买方 (Initiative Buying)** | 在价值区内或价值区外推动价格上升，试图建立新价值。 | `price_breaks_above_prev_va` + `new_volume_cluster_above` + `acceptance_time > threshold` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 突破前日价值区顶部后，在新区间停留并形成新成交量聚集→主动买方确认。 | 主动=趋势延续力量。 |
| 23 | **主动卖方 (Initiative Selling)** | 在价值区内或价值区外推动价格下降，试图建立新价值。 | `price_breaks_below_prev_va` + `new_volume_cluster_below` + `acceptance_time > threshold` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 与主动买方对称。 | 主动=趋势延续力量。 |
| 24 | **31买入交易日 (3I Buying Day)** | 自发买入尾部 + 自发买入TPO + 自发买入价格幅度扩展。三个方向信号一致。 | `initiative_tail_buy` + `initiative_tpo_buy` + `initiative_range_extension_buy` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 检测三个自发信号同向：买入尾部（极端低单字母+反弹）+ 买入TPO（在价值区上方）+ 买入扩展（突破IB上沿）。 | 统计：次日94% 90分钟内好于前日VA；97%全日≥前日VA。 |
| 25 | **31卖出交易日 (3I Selling Day)** | 自发卖出尾部 + 自发卖出TPO + 自发卖出价格幅度扩展。 | `initiative_tail_sell` + `initiative_tpo_sell` + `initiative_range_extension_sell` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 三个自发卖出信号同向。 | 与31买入对称。 |
| 26 | **价值区间规则 (Value Area Rule)** | 前日价值区顶部提供支持，底部提供阻力。重新进入价值区且被接受（双TPO）→可能突破。开市价越接近价值区，突破可能性越大。区间狭窄更易突破。 | `prev_va_top`/`prev_va_bottom` as key_levels + `breakthrough_after_re_entry` | OHLCV + 多日线 | 日级别 | `proxy_quantizable_now` | 次日价格相对于前日VA的位置判断。进入VA后是否被接受（停留时间+成交量）决定突破概率。 | 跨日关键位系统。 |
| 27 | **剧变 (Spikes)** | 最后几个时段价格迅速偏离已形成的价值区。次日剧变区间内开市=确认；区间外同向=方向延续；反向=拒绝。 | `last_30min_spike_range` + `spike_deviation_from_va` + `next_day_open_vs_spike` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 尾盘30分钟价格偏离日内VA的程度。记录剧变区间[spike_low, spike_high]。次日开盘位置判断。 | 剧变价位首次试探时有效；反复试探后失效。 |
| 28 | **平衡区突破 (Balance Area Breakout)** | 多个交易日价值区间重叠形成平衡区。突破后价格运动突然且剧烈。 | `multi_day_va_overlap` + `breakout_from_consolidation` + `volume_confirmation` | OHLCV + 多日线（5日+） | 多日线 | `proxy_quantizable_now` | 连续N日（如5日）VA重叠度>60%定义为平衡区。突破后成交量放大确认。 | 突破方向+止损设在突破点上下。 |
| 29 | **空跳缺口—突破型 (Break-Away Gap)** | 趋势早期，新长线参与者引起。缺口成为支持/阻力。 | `gap_size` + `trend_stage_early` + `gap_not_filled` | OHLCV | 日级别 | `proxy_quantizable_now` | 跳空发生在趋势初期（前日已有方向），缺口未被快速填补。 | 突破空跳=趋势启动确认。 |
| 30 | **空跳缺口—加速型 (Acceleration Gap)** | 趋势中途，再次确认方向。 | `gap_size` + `trend_stage_mid` + `gap_not_filled` | OHLCV | 日级别 | `proxy_quantizable_now` | 跳空发生在趋势中段，加速原有方向。 | 加速空跳=趋势延续确认。 |
| 31 | **空跳缺口—衰竭型 (Exhaustion Gap)** | 趋势最后阶段，几乎人人成为一方，趋势结束。 | `gap_size` + `trend_stage_late` + `gap_filled_quickly` | OHLCV | 日级别 | `proxy_quantizable_now` | 跳空发生在趋势末期，随后被快速填补→衰竭信号。 | 衰竭空跳=趋势结束预警。 |
| 32 | **TPO计数 (TPO Count)** | 控制点上方TPO总数 vs 下方TPO总数。比例估计价值区内买卖失衡。 | `volume_above_poc` / `volume_below_poc` 或 `periods_above_poc` / `periods_below_poc` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 日内POC上方成交量 vs 下方成交量。比例>1.2=卖方失衡；<0.8=买方失衡。 | 分钟K线可替代TPO字母计数。 |
| 33 | **TPO图字母映射** | 每半小时一个字母：A=第一半小时，B=第二半小时... | A=9:30-10:00, B=10:00-10:30, C=10:30-11:00, D=11:00-11:30, E=13:00-13:30, F=13:30-14:00, G=14:00-14:30, H=14:30-15:00（A股无I，顺延） | OHLCV + 30分钟K线 | 日级别 | `proxy_quantizable_now` | 直接用30分钟K线生成8根K线，对应A-H。 | 注意A股午休11:30-13:00与期货市场不同。 |
| 34 | **无趋势/不确定交易日 (Nontrend/Nonconviction)** | 无趋势：IB窄，无扩展，成交低。不确定：似乎有机会但无真正参考点。 | `nontrend`: `narrow_ib` + `no_extension` + `low_volume`。<br>`nonconviction`: `open_in_prev_va` + `random_oscillation` + `no_reference_point` | OHLCV | 日级别 | `proxy_quantizable_now` | 两者都是"观望"信号。不确定日更容易诱多，因为似乎有驱动型态但实际无方向。 | 不确定日=假的驱动型态。 |
| 35 | **空头补仓止跌回稳 ("P"形)** | 价格狂跌后，空头回补（买回）引起反弹，无新买方。图形呈"P"字。补仓结束后价格返回原轨道。 | `rapid_rally_after_drop` + `rally_volume_anomaly` + `subsequent_selling_resumes` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 急跌后快速反弹，但反弹中买方力量逐波减弱（每半小时高点降低），之后卖方重新出现。 | 图形识别需分钟级数据。可作为模式库。 |
| 36 | **多头斩仓狂跌 ("b"形)** | 上升趋势后，多头平仓（卖出）引起下跌，无新卖方。图形呈"b"字。 | `rapid_drop_after_rally` + `drop_lacks_selling_follow_through` + `buying_resumes` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 急涨后快速下跌，但下跌中卖方无持续力量，之后买方重新"完成"市场轮廓。 | 图形识别需分钟级数据。 |
| 37 | **平衡板 (Ledge)** | 某价位区反复形成单字母/双字母停留，成为日内支撑/阻力。 | `repeated_price_halts` + `low_volume_zone` + `acceptance_vs_rejection` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 日内某价位多次出现停留（TPO聚集），之后被接受或拒绝。 | 平衡板=日内关键位。 |
| 38 | **长线极端价位 / 价格偏离** | 长期趋势中的极端价位，远离已建立的价值。响应参与者在此介入。 | `price_vs_long_term_va` + `deviation_multiple` + `responsive_volume_surge` | OHLCV + 多日线 | 多日线/周线 | `proxy_quantizable_now` | 多日VA的移动平均。价格偏离多日VA超过1.5-2个标准差→价格偏离信号。 | 长线极端=中长线建仓/减仓点。 |

---

# FORMULAS_AND_ALGOS

## Formula 1: 价值区间计算（成交量法）—— 原文附录算法
**source_basis**: 附录"价值区间的计算方法"  
**proxy_formula_or_logic**:  
```
步骤1: 确定成交量最大的价位，取其成交量为基数；
步骤2: 分别计算该价位之上(之下)的两个价位发生的成交量之和，
       并将两和数相比较，较大的一方和数与基数相加，成为新的基数，
       对应两个价位成为价值区间的一部分；
步骤3: 将基数与总成交相比较，若未达到70%，则重复步骤2，
       直至达到70%为止。
```
**required_fields**: `price`, `volume` (intraday aggregation, e.g., by close price or typical price)  
**caveats**: 原文使用债券32分之1价位的离散价格。A股价格连续，需先分桶（如1分钱、1毛钱或固定tick）再聚合。分桶粒度影响VA宽度。  
**quant_status**: `proxy_quantizable_now` — 可用分钟K线成交量聚合实现。

---

## Formula 2: 价值区间计算（TPO法）—— 原文隐含算法
**source_basis**: 第一章第三节 + 第三章TPO计数法  
**proxy_formula_or_logic**:  
```
1. 将交易日划分为N个时段（如30分钟一个，A-H共8个时段）
2. 对每个时段，记录该时段出现过的价格（OHLC范围内的所有价位，或仅close）
3. 每个价格每出现一次，记为一个TPO
4. 找到TPO最多的价格 = POC
5. 从POC开始，向上下两侧各取2个价格，比较两侧TPO总数
6. 将TPO较多的一侧加入价值区间，累加TPO数
7. 重复直至TPO总数 ≥ 70% of 全日TPO总数
```
**required_fields**: 分钟K线或30分钟K线的 `open`, `high`, `low`, `close`  
**caveats**: 原文以债券的1/32离散价位计算。A股连续价格若直接取所有OHLC内价位，TPO数会过多。建议：用分桶聚合（如0.1%或固定档位），或仅用close/typical price作为每个时段的代表价。  
**quant_status**: `proxy_quantizable_now` — 分钟K线可近似。

---

## Formula 3: 控制点 (POC) 近似重建
**source_basis**: 第一章第三节"最长的且最接近价格幅度中部的TPOs称为控制点"  
**proxy_formula_or_logic**:  
```
POC = argmax(volume_by_price)
# 如果多个价格成交量相同，取最接近日中位价的那个
if tie:
    POC = price_with_max_volume_and_min_abs(price - mid_price)
```
**required_fields**: `volume_by_price` (intraday)  
**caveats**: 原文要求"最长且最接近价格幅度中部"，同时考虑TPO长度和位置。纯成交量法只保证"最长"，不保证"最接近中部"。A股近似中，如果成交量峰值在极端价位，需人工判断是否为异常。  
**quant_status**: `proxy_quantizable_now` — 分钟K线聚合即可。

---

## Formula 4: 日类型分类打分逻辑
**source_basis**: 第二章七种日类型定义  
**proxy_formula_or_logic**:  
```python
def classify_day_type(open_price, high, low, close, ib_high, ib_low, 
                       volume, avg_volume, avg_range, prev_high, prev_low, prev_close):
    ib_range = ib_high - ib_low
    day_range = high - low
    ib_ratio = ib_range / max(day_range, 1e-6)
    
    # 1. 强趋势日
    if (open_price > low + 0.2 * day_range and close < high - 0.2 * day_range 
        and open_price > high - 0.3 * day_range and close < low + 0.3 * day_range
        and volume > 1.2 * avg_volume):
        return "TREND_DAY"
    
    # 2. 无趋势日
    if ib_range < 0.4 * avg_range and day_range < 0.6 * avg_range and volume < 0.7 * avg_volume:
        return "NONTREND_DAY"
    
    # 3. 平衡日
    if ib_range > 0.6 * day_range and high <= ib_high * 1.001 and low >= ib_low * 0.999:
        return "NORMAL_DAY"
    
    # 4. 变形平衡日
    if ib_range < 0.6 * day_range and (high > ib_high or low < ib_low) and volume > avg_volume:
        return "NORMAL_VARIATION"
    
    # 5. 中立日（高/低收）
    if (high > ib_high and low < ib_low) or (high > prev_high and low < prev_low):
        if close > low + 0.4 * day_range and close < high - 0.4 * day_range:
            return "NEUTRAL_DAY"
        elif close > high - 0.2 * day_range:
            return "NEUTRAL_HIGH"
        elif close < low + 0.2 * day_range:
            return "NEUTRAL_LOW"
    
    # 6. 弱趋势日 / 双重分布
    if bimodal_volume_profile_detected():
        return "DOUBLE_DISTRIBUTION"
    
    return "UNCLASSIFIED"
```
**required_fields**: OHLCV + 前日数据 + 多日线统计  
**caveats**: proxy/approximation。原文的日类型判断依赖于TPO图的完整形态（如"每个时段推向更高"），而非仅OHLCV。上述逻辑用简化阈值近似，准确率有限。建议用机器学习辅助分类。  
**quant_status**: `proxy_quantizable_now` — 可用，但需持续校准。

---

## Formula 5: 开市型态分类逻辑
**source_basis**: 第三章四种开市型态定义  
**proxy_formula_or_logic**:  
```python
def classify_opening_type(open_price, first_30min_high, first_30min_low, first_30min_close,
                          prev_va_high, prev_va_low, prev_range_high, prev_range_low,
                          ib_high, ib_low):
    in_prev_va = prev_va_low <= open_price <= prev_va_high
    in_prev_range = prev_range_low <= open_price <= prev_range_high
    
    # 驱动开市：开盘后单向有力运动，不反向试探
    if (first_30min_high > max(open_price, prev_range_high) and 
        first_30min_low > min(open_price, prev_range_low) and
        first_30min_close > first_30min_high - 0.1 * (first_30min_high - first_30min_low)):
        return "OPEN_DRIVE"
    
    # 试探驱动：先试探参考点外，失败后反向穿过开盘价
    if (first_30min_high > max(prev_range_high, open_price) and 
        first_30min_low < min(prev_range_low, open_price) and
        first_30min_close > open_price):
        return "OPEN_TEST_DRIVE"
    
    # 失败反转：沿一个方向运动后反转回开盘区间
    if (first_30min_high > open_price and first_30min_low < open_price and
        abs(first_30min_close - open_price) < 0.3 * (first_30min_high - first_30min_low)):
        return "OPEN_REJECTION_REVERSE"
    
    # 无方向感：在开盘价附近震荡
    if abs(first_30min_close - open_price) < 0.2 * (first_30min_high - first_30min_low):
        if in_prev_range:
            return "OPEN_AUCTION_IN_RANGE"
        else:
            return "OPEN_AUCTION_OUT_OF_RANGE"
    
    return "UNKNOWN"
```
**required_fields**: 开盘后30分钟OHLC + 前日价值区/价格幅度  
**caveats**: proxy/approximation。原文判断依赖于TPO图的逐字母观察（如"A分区构成明显买入尾部"），上述逻辑用30分钟区间的简化规则替代。驱动开市和试探驱动的区分在A股中需要更细粒度（5/15分钟）才能准确。  
**quant_status**: `proxy_quantizable_now` — 30分钟级可用；5分钟级更准。

---

## Formula 6: 31交易日检测器
**source_basis**: 第八章第一节  
**proxy_formula_or_logic**:  
```python
def detect_3i_day(tail_type, tpo_bias, range_extension_direction, close_position):
    """
    tail_type: "buy" / "sell" / "none"
    tpo_bias: "buy" (TPOs above POC > below) / "sell" / "neutral"
    range_extension_direction: "up" / "down" / "none"
    close_position: "high" / "low" / "middle"
    """
    if tail_type == "buy" and tpo_bias == "buy" and range_extension_direction == "up":
        if close_position in ["high", "middle-high"]:
            return "3I_BUYING_DAY"
    elif tail_type == "sell" and tpo_bias == "sell" and range_extension_direction == "down":
        if close_position in ["low", "middle-low"]:
            return "3I_SELLING_DAY"
    return "NOT_3I"
```
**required_fields**: 日内TPO/成交量分布 + 尾部检测 + 扩展方向 + 收盘位置  
**caveats**: proxy/approximation。原文要求"自发尾部/自发TPO/自发扩展"，需区分"自发"vs"响应"。简化版本仅检测三个信号同向，不区分自发/响应。需结合第三章主动/响应定义改进。  
**quant_status**: `proxy_quantizable_now` — 可用分钟级数据实现基础版。

---

## Formula 7: 价值区间规则（次日关键位判断）
**source_basis**: 第八章第三节  
**proxy_formula_or_logic**:  
```python
def value_area_rule(prev_va_high, prev_va_low, current_open, current_price, volume_profile):
    if current_open > prev_va_high:
        support = prev_va_high
        if current_price < prev_va_high:
            return {"signal": "RETURN_TO_VA", "bias": "watch_for_rejection"}
    elif current_open < prev_va_low:
        resistance = prev_va_low
        if current_price > prev_va_low:
            return {"signal": "RETURN_TO_VA", "bias": "watch_for_rejection"}
    else:
        if current_price > prev_va_high and time_in_zone > threshold:
            return {"signal": "BREAKOUT_UP", "support": prev_va_high}
        elif current_price < prev_va_low and time_in_zone > threshold:
            return {"signal": "BREAKOUT_DOWN", "resistance": prev_va_low}
        else:
            return {"signal": "BALANCED", "range": [prev_va_low, prev_va_high]}
    
    va_width = prev_va_high - prev_va_low
    if va_width < avg_va_width * 0.5:
        return {"signal": "NARROW_VA", "breakout_probability": "high"}
```
**required_fields**: 前日价值区 + 次日开盘/分钟价格 + 成交量分布  
**caveats**: proxy/approximation。原文要求"双TPO字母"（进入VA后接受）来判断突破，简化版本用"时间和成交量"替代。  
**quant_status**: `proxy_quantizable_now` — 标准跨日分析。

---

## Formula 8: 剧变 (Spike) 检测与次日判断
**source_basis**: 第八章第四节  
**proxy_formula_or_logic**:  
```python
def detect_spike(day_va_high, day_va_low, last_30min_high, last_30min_low, 
                 last_30min_volume, avg_30min_volume):
    spike_range = last_30min_high - last_30min_low
    if last_30min_low < day_va_low and last_30min_high < day_va_low + spike_range * 0.5:
        return {"type": "SELLING_SPIKE", "range": [last_30min_low, last_30min_high]}
    elif last_30min_high > day_va_high and last_30min_low > day_va_high - spike_range * 0.5:
        return {"type": "BUYING_SPIKE", "range": [last_30min_low, last_30min_high]}
    return None

def next_day_spike_signal(spike, next_day_open):
    if spike["type"] == "SELLING_SPIKE":
        if next_day_open < spike["range"][0]:
            return "CONTINUATION"
        elif next_day_open > spike["range"][1]:
            return "REJECTION"
        else:
            return "BALANCED"
```
**required_fields**: 日内VA + 尾盘30分钟OHLC + 次日开盘  
**caveats**: proxy/approximation。原文中剧变可以是任意时段（不一定是尾盘），但尾盘剧变最常见且影响最大。  
**quant_status**: `proxy_quantizable_now` — 尾盘检测直接可用。

---

# NOT_QUANT_YET

| # | concept | why_not_now | what_extra_data_is_needed | whether_it_is_still_valuable |
|---|---------|-------------|---------------------------|------------------------------|
| 1 | **真正的TPO字母生成** | 原文要求每半小时记录所有成交价位，A股标准行情只提供OHLC。无法生成每个价位的TPO字母矩阵。 | 逐笔成交明细（含每笔成交价格+时间），或Level2快照 | 是。TPO图是MP的原生形态，有精确数据后可重建完整轮廓。 |
| 2 | **风险套利商库存动态** | 原文中Locals的库存平衡（"空仓太多/买得太多"）直接影响短期价格。A股无公开Locals库存数据。 | 券商自营盘数据、主力资金流、大单流向 | 是。可间接用主力资金流/大单比例近似。 |
| 3 | **场内叫价/Opening Call序列** | 原文第三章强调"开市叫价"（Opening Call）序列的重要性。A股集合竞价有虚拟成交价序列，但非标准数据。 | 集合竞价逐笔撮合明细（虚拟匹配价序列） | 是。A股集合竞价9:15-9:25的虚拟匹配价序列可近似Opening Call。 |
| 4 | **"自发"vs"响应"的精确区分** | 原文第三章和第八章中，自发(Initiative)和响应(Responsive)的区分依赖于价格相对于前日VA的位置+参与者意图。意图无法直接从OHLCV推断。 | 订单簿深度、大单主动/被动方向、资金流向 | 是。这是MP的核心行为分类。可用大单方向/委托簿倾斜度近似。 |
| 5 | **图表的"P"形/"b"形精确识别** | 第五章的图形识别需要逐字母观察TPO形状（如"P"形的右侧回落）。仅用OHLCV无法精确识别。 | 完整TPO矩阵或分钟级逐笔重建 | 是。可作为模式库，在数据充足后启用。 |
| 6 | **平衡板(Ledge)的精确确认** | 需要观察某价位反复出现停留（双TPO/单TPO），且接受/拒绝的细微差别。 | 分钟级或TPO级数据 | 是。日内关键位识别的重要组成部分。 |
| 7 | **TPO计数法中"单字母尾部排除"** | 原文要求尾部不计入TPO计数。但分钟级数据无法精确判断哪些是"单字母"。 | 30分钟时段的精确成交价位集合 | 是。影响价值区内买卖失衡的估计。 |
| 8 | **31交易日的"自发/响应"尾部区分** | 31日要求"自发尾部"（Initiative Tail），而非"响应尾部"。响应尾部出现在前日价值区外，自发尾部出现在价值区内。精确区分需要跨日VA位置。 | 前日VA + 日内逐笔/Level2 | 是。区分错误会导致31日检测假阳性。 |
| 9 | **"价格×时间=价值"的精确时间加权** | 原文中时间不是简单的分钟数，而是"拍卖停留时间"。A股中某价格停留1分钟但实际成交极少，不等于"被接受"。 | 逐笔成交时间戳 + 价格停留时间 | 是。可用成交量×时间作为近似。 |
| 10 | **长线极端价位的精确偏离度量** | 第七章涉及长期VA的移动和偏离。需要多日线（周/月）的VA序列，且长期VA本身需要更高精度。 | 多日/多周线 + 分钟级数据重建 | 是。长线交易的核心参考。 |
| 11 | **空跳缺口的三种类型精确区分** | 突破/加速/衰竭缺口的区分依赖于趋势阶段判断。趋势阶段本身是主观判断。 | 完整的多日线结构+成交量趋势分析 | 是。缺口类型直接影响交易策略（跟随/观望/反向）。 |
| 12 | **市场情绪/消息影响量化** | 第八章第七节讨论消息影响市场。原文表格给出"主要方向+消息+市场动向→情绪"的定性映射。 | 新闻/事件数据 + 市场情绪指标（如散户情绪指数） | 是。可构建事件驱动触发器。 |

---

# NEXT_ACTION

## 可直接进入A2字段池的对象（proxy_quantizable_now，本周实施）

1. **`initial_balance` (初期平衡)** → 开盘后30/60分钟OHLC区间
2. **`value_area_70pct` (价值区间)** → 日内成交量分布70%区间（从POC向上下累加）
3. **`point_of_control` (控制点)** → 日内成交量峰值价或VWAP
4. **`range_extension` (价格幅度扩展)** → 突破IB后的延伸幅度和方向
5. **`day_type_classifier` (日类型分类器)** → 基于OHLCV + 前日数据的七种日类型初步分类
6. **`opening_type_classifier` (开市型态分类器)** → 驱动/试探/失败反转/无方向感四类
7. **`single_print_tail_proxy` (单字母尾部代理)** → 分钟K线极端价位快速反转+低成交量
8. **`tpo_count_proxy` (TPO计数代理)** → 分钟/30分钟成交量在POC上方/下方的比例
9. **`closing_range` (收市分区)** → 尾盘30/15分钟区间
10. **`prev_va_key_levels` (前日价值区关键位)** → 前日VA_top/VA_bottom作为次日支持/阻力
11. **`gap_detector` (缺口检测)** → 隔夜跳空幅度+类型判断+回补检测
12. **`spike_detector` (剧变检测)** → 尾盘/盘中快速偏离VA的区间检测
13. **`3i_day_detector` (31日检测器)** → 三个同向自发信号的简化版
14. **`responsive_vs_initiative_proxy` (响应/主动代理)** → 价格相对于前日VA的位置+突破后的接受度
15. **`balance_area_detector` (平衡区检测)** → 连续N日VA重叠度判断
16. **`long_term_trend_proxy` (长线趋势代理)** → 多日POC移动方向+VA重叠度

## 适合先做代理版本（proxy_quantizable_now，2周内实施）

1. **A股30分钟K线→TPO字母映射** → A=9:30-10:00, B=10:00-10:30...H=14:30-15:00
2. **"P"形/"b"形粗略检测** → 急跌后反弹但高点降低/急涨后下跌但低点抬高
3. **价值区间规则自动化** → 次日开盘位置 vs 前日VA → 自动输出支持/阻力/突破信号
4. **剧变次日策略** → 剧变区间+次日开盘 → 自动标记"延续/平衡/拒绝"
5. **中立日次日策略** → 高/低收中立日 → 次日开盘方向概率提示
6. **空头补仓/多头斩仓检测** → 基于分钟级成交量异常+价格形态的粗略识别

## 先放future bucket（needs_extra_data，1月+）

1. **精确TPO矩阵重建** → 需逐笔成交明细
2. **集合竞价虚拟匹配价序列分析** → 需交易所集合竞价详细数据
3. **Locals库存动态跟踪** → 需主力资金流/大单拆分数据
4. **自发vs响应的精确意图识别** → 需Level2订单簿+主动被动大单分类
5. **完整图形模式库（P/b/Ledge）** → 需高精度TPO数据+机器学习训练
6. **长线极端价位的精确偏离度量** → 需多周线VA重建
7. **缺口类型精确分类模型** → 需趋势阶段模型+事件数据
8. **消息影响量化模型** → 需新闻事件库+市场情绪数据

## 适合与A股集合竞价/开盘结构对齐的对象

| MP/Auction概念 | A股对应结构 | 对齐方式 | 实施优先级 |
|-----------------|------------|---------|-----------|
| **Opening Call (开市叫价)** | 9:15-9:25集合竞价虚拟匹配价序列 | 分析集合竞价期间的虚拟匹配价变化趋势，识别"隐藏的尾部" | P1 |
| **Initial Balance (初期平衡)** | 9:30-10:00 / 9:30-10:30连续竞价首段 | 直接用30/60分钟K线计算IB区间 | P0 |
| **Open-Drive (驱动开市)** | 集合竞价大幅跳空+开盘后持续单向 | 集合竞价方向+开盘后30分钟不回调 | P0 |
| **Open-Test-Drive (试探驱动)** | 开盘后测试前高/前低/均线后突破 | 开盘后先触及参考位再反向突破 | P0 |
| **Open-Rejection-Reverse (失败反转)** | 开盘后冲高被拒回落 / 下探回升 | 开盘后30分钟方向+随后1-2小时反转回开盘区间 | P0 |
| **Open-Auction (无方向感)** | 开盘后围绕开盘价震荡 | 开盘价在前日范围内→观望；在前日范围外→观察突破 | P0 |
| **Value Area (价值区间)** | 日内成交量密集区 | 用分钟K线成交量分布重建 | P0 |
| **POC (控制点)** | 日内成交量峰值价 / 早盘主力成本 | VWAP或成交量峰值价 | P0 |
| **Tails (尾部)** | 开盘后/盘中极端价位快速反转 | 分钟K线长影线+低成交量 | P1 |
| **Gaps (空跳缺口)** | 隔夜跳空 / 集合竞价跳空 | 标准缺口识别+类型判断 | P0 |
| **Spikes (剧变)** | 尾盘急拉/急跌 / 开盘大幅跳空 | 尾盘30分钟偏离VA程度 | P1 |
| **31 Day (31交易日)** | 强趋势日的精确结构 | 三个自发信号同向检测 | P1 |
| **Balance Area (平衡区)** | A股箱体震荡 / 平台整理 | 连续N日VA重叠 | P1 |
| **Neutral Day (中立日)** | 放量十字星 / 双向波动 | 双向扩展+收盘在中间 | P1 |
| **Long-term Control (长线控制)** | 主力资金成本区移动 | 多日POC方向+大单验证 | P2 |

## 建议二次精修的章节

1. **第三章 市场控制力量分析I** — 开市型态与位置效应是A2最核心内容，建议提取更多原文细节（尤其是"位置效应"中关于前日VA/Range/价格幅度内外的细分讨论）。
2. **第四章 市场控制力量分析II** — TPO计数法、主动/响应行为定义、长线控制判断逻辑。该章有大量可工程化的规则，当前Part 1摘录不足，需二次补充。
3. **第六章 市场成交分析** — 成交量与价格方向的关系、高成交量减速特性。该章可直接转化为成交量因子。
4. **第八章 特殊交易机会** — 31日、中立日、价值区间规则、剧变、平衡区突破、缺口均有具体统计数字和案例，建议将统计表格全部提取为结构化数据。

## 可作为后续策略设计依据的Excerpt

- **Excerpt 5**（风险套利商/长线交易者二分法）→ 所有策略的参与者前提
- **Excerpt 7**（价值区间/控制点/尾部/收市分区）→ 日内策略的四大参照点
- **Excerpt 11-14**（四种开市型态）→ 开盘策略的触发条件
- **Excerpt 15**（31日统计）→ 高胜率次日持仓策略
- **Excerpt 16**（价值区间规则）→ 跨日支撑阻力突破策略
- **Excerpt 17**（剧变）→ 尾盘/跳空次日方向判断策略
- **Excerpt 18**（平衡区突破+缺口）→ 中线趋势跟踪策略

---

*End of Part 2*
*File: CUTPACK__A2__CN__市场轮廓理论__part2__v2.md*
