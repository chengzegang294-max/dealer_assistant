CUTPACK__A2__CN__市场轮廓理论__part2__v2_r1.md

---

# QUANTIZATION_TABLE

| # | concept | raw_rule_from_text | observable_proxy | data_needed | timeframe_hint | quant_status | implementation_hint | notes |
|---|---------|-------------------|------------------|-------------|----------------|--------------|---------------------|-------|
| 1 | **初期平衡 (Initial Balance)** | 由A、B分区（第一小时）组成，主要由风险套利商建立。风险套利商试图寻找满足买卖双方的价位。IB阶段成交量可达全日50%。 | `first_30min_ohlc` 或 `first_60min_ohlc` 区间。`ib_high`, `ib_low`, `ib_range` | OHLCV + 分钟K线（30/60分钟） | 日级别，开盘首小时 | `proxy_quantizable_now` | 取开盘后N根分钟K线（30/60分钟）的最高/最低。A股30分钟=2根K线（9:30-10:00），60分钟=4根K线（9:30-10:30） | 原文基于CBOT期货每半小时一个字母。A股直接映射为分钟/30分钟K线。 |
| 2 | **价值区间 (Value Area)** | 每个交易日总成交70%发生的区间。从成交量最大价位开始，向上下两侧累加相邻价位，直到覆盖70%。 | `volume_profile_70pct_range`：日内成交量分布从峰值价上下累加至70% | OHLCV + 分钟K线（或tick） | 日级别 | `proxy_quantizable_now` | 1. 找日内成交量最大价位（POC）。2. 向上加2个价位、向下加2个价位，比大小。3. 大的一边加入价值区间，累加成交量。4. 重复至≥70% | 近似代理：附录给出精确算法。TPO法可作为近似。 |
| 3 | **控制点 (POC)** | 最长且最接近价格幅度中部的TPO线。当日成交最活跃、最合理的价格。 | `intraday_volume_peak_price` 或 `volume_weighted_average_price` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 直接用日内成交量最大的价格（close/volume聚合），或用VWAP。分钟级精度足够。 | 近似代理：多日线POC移动方向=趋势判断。 |
| 4 | **价格幅度扩展 (Range Extension)** | 价格运动超出IB阶段价格幅度。表示长线买方/卖方参与，市场发生变化。风险套利商不是运动主因。 | `price_break_ib_high` / `price_break_ib_low` 后的运行距离。`range_extension_up`, `range_extension_down` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 实时监测价格是否突破`ib_high`/`ib_low`。突破后记录延伸幅度和方向。 | 单边扩展=趋势信号；双向扩展=中立日信号。 |
| 5 | **单字母尾部 / 买入尾部 (Single-Print Buyer Tail)** | 极端低位出现的单字母分区。长线买方热烈响应低于价值的价位。买方竞争使价格快速上升。尾部至少需两个TPO，且在非收盘时段出现。 | `extreme_low_single_print`：分钟K线中最低价仅出现1-2个时段，且快速反弹。`tail_volume_ratio < 5%` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 遍历日内各价位：若在最低20%价格区，且该价位成交时段数≤2，且之后价格迅速回升→标记为买入尾部。 | 近似代理：严格判断需逐笔/Level2确认“仅1个时段成交”。分钟K线可近似。 |
| 6 | **单字母尾部 / 卖出尾部 (Single-Print Seller Tail)** | 极端高位出现的单字母分区。长线卖方在高价抛售，价格很快降低。 | `extreme_high_single_print`：同理，在最高20%价格区。 | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 与买入尾部对称逻辑。 | 近似代理：尾部越长（更多价位单字母），拒绝信号越强。 |
| 7 | **收市分区 (Closing Range)** | M分区（最后一个时段）反映当日整体市场情绪。与次日开市价位比较，观察情绪变化。 | `last_30min_range` 或 `last_15min_range`：尾盘区间。`close_vs_prev_close` | OHLCV | 日级别 | `proxy_quantizable_now` | 取最后30/15分钟最高-最低。记录收盘价在其中的位置（高/中/低）。 | 次日开盘价 vs 收市分区 = 情绪连续/变化判断。 |
| 8 | **平衡交易日 (Normal Day)** | 初期平衡阶段价格幅度很宽，全天在IB内震荡。通常由开盘消息引起，长线参与者过早介入。 | `ib_range > 0.6 * avg_daily_range` AND `no_range_extension` AND `close_inside_ib` | OHLCV + 多日线 | 日级别 | `needs_extra_data` | 判断IB区间是否占全日大部分。无扩展且收盘在IB内→平衡日。 | 近似代理：成交量通常较大（消息刺激）。日类型强依赖TPO形态，OHLCV只能近似。 |
| 9 | **变形平衡交易日 (Normal Variation)** | IB幅度比平衡日小，之后被长线突破。突破常发生在市场前半段。 | `ib_range < 0.6 * avg_range` AND `range_extension_occurs` AND `close_inside_extended_range` | OHLCV + 多日线 | 日级别 | `needs_extra_data` | IB较小+有扩展+收盘在扩展后的区间内→变形平衡日。 | 近似代理：变形平衡日=长线有信心但非绝对控制。日类型强依赖TPO形态，OHLCV只能近似。 |
| 10 | **强趋势交易日 (Trend Day)** | 长线从开盘到收盘单向控制。每个时段都推向更高/更低（单方市）。TPO轮廓狭长，成交量高。 | `open_near_extreme` + `close_near_opposite_extreme` + `consecutive_same_direction_periods >= 4` + `volume > avg_volume` | OHLCV + 分钟K线 | 日级别 | `needs_extra_data` | 开盘后连续N个时段（30/60分钟）同方向运动。开盘在全日极端附近，收盘在另一端极端附近。 | 近似代理：强趋势日是A股“板块/题材爆发日”的典型结构。日类型强依赖TPO形态，OHLCV只能近似。 |
| 11 | **弱趋势交易日 / 双重分布 (Double Distribution)** | IB窄，后期长线介入推动价格到新水平，形成第二价值区。两区被单字母TPO分开。 | `bimodal_volume_profile` + `inter_peak_low_volume_zone` + `second_peak_accepted` | OHLCV + 分钟K线 | 日级别 | `needs_extra_data` | 日内成交量分布出现两个峰值，中间有低成交量区（单字母/低成交带）。 | 近似代理：双重分布=“午后再起一波”的A股常见结构。日类型强依赖TPO形态，OHLCV只能近似。 |
| 12 | **无趋势交易日 (Nontrend Day)** | IB窄，像趋势日但无扩展。市场等待消息。参与者信心不足，成交低。 | `ib_range < 0.4 * avg_range` AND `no_range_extension` AND `volume < 0.7 * avg_volume` | OHLCV + 多日线 | 日级别 | `needs_extra_data` | 窄IB+无扩展+低成交量。A股常见“地量震荡日”。 | 近似代理：无趋势日→观望。日类型强依赖TPO形态，OHLCV只能近似。 |
| 13 | **标准中立交易日 (Neutral Day)** | 买卖双方都在两端扩展，收盘在中间。双方力量均衡。 | `range_extension_both_directions` AND `close_in_middle_50pct` | OHLCV | 日级别 | `needs_extra_data` | 同时有向上和向下扩展，且收盘价在全日的中间50%区域。 | 近似代理：中立日→次日方向选择。日类型强依赖TPO形态，OHLCV只能近似。 |
| 14 | **高/低收中立交易日 (Neutral-Extreme Day)** | 买卖双方都在两端扩展，但收盘在极端。收市方获胜。 | `range_extension_both_directions` AND `close_in_top_20pct` (高收) OR `close_in_bottom_20pct` (低收) | OHLCV | 日级别 | `needs_extra_data` | 双向扩展+收盘在极端。高收→次日可能高开；低收→次日可能低开。 | 近似代理：统计上92%次日90分钟内好于前日价值区。日类型强依赖TPO形态，OHLCV只能近似。 |
| 15 | **驱动开市 (Open-Drive)** | 开盘后价格立即向一个方向有力运动，不反向试探。长线预先决策。 | `first_30min_unidirectional` + `no_retrace > 50%` + `open_outside_prev_range` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 开盘后N分钟（如30分钟）单向运行，最大回撤<初始运动的50%。 | 近似代理：最强开盘信号。A股利好/利空驱动日。 |
| 16 | **试探驱动开市 (Open-Test-Drive)** | 开市后在已知参考点外探测，确认无新动向后，迅速返回并穿过开市价位，向反方向运动。 | `initial_move_beyond_ref` + `failure_to_extend` + `reversal_through_open` + `new_extreme_in_opposite` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 开盘后先突破某参考位（前高/前低/均线），失败后反向突破开盘价，创出新极端。 | 近似代理：“先回落以便反弹，先反弹以便回落”。 |
| 17 | **失败反转开市 (Open-Rejection-Reverse)** | 开市后沿一个方向运动，遇反向强力量，反转回开盘区间。 | `initial_move_beyond_ib` + `reversal_back_to_open_range` + `close_near_open_or_middle` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 开盘后先突破某一方向，之后回到开盘区间内收盘。确信度低。 | 近似代理：A股常见“诱多/诱空”开盘。 |
| 18 | **无方向感开市—区间内 (Open-Auction in Range)** | 开市价在前一交易日价格幅度内，随机叫价，无方向感。通常发展为无趋势/平衡/中立日。 | `open_inside_prev_range` + `first_30min_oscillation_small` + `no_clear_direction` | OHLCV + 前日数据 | 日级别 | `proxy_quantizable_now` | 开盘价在前日最高-最低之间，开盘后30分钟振幅小，无单边趋势。 | 区间内无方向感→观望。 |
| 19 | **无方向感开市—区间外 (Open-Auction Out of Range)** | 开市价在前一交易日价格幅度外，但围绕开市价震荡。表明新长线交投在寻找新价位。 | `open_outside_prev_range` + `first_30min_oscillation_around_open` + `potential_trend_forming` | OHLCV + 前日数据 | 日级别 | `proxy_quantizable_now` | 开盘价在前日范围外，但开盘后震荡而非单向驱动。观察是否后续形成趋势。 | 区间外无方向感→潜在突破日。 |
| 20 | **响应买方 (Responsive Buying)** | 价格低于价值区间时，长线买方介入，使价格回升。 | `price_below_prev_va` + `buying_pressure_detected` + `price_returns_toward_va` | OHLCV + 前日数据 | 日级别 | `proxy_quantizable_now` | 价格低于前日价值区底部后，出现成交量放大或价格反弹→响应买方信号。 | 响应=价值回归力量。 |
| 21 | **响应卖方 (Responsive Selling)** | 价格高于价值区间时，长线卖方介入，使价格回落。 | `price_above_prev_va` + `selling_pressure_detected` + `price_returns_toward_va` | OHLCV + 前日数据 | 日级别 | `proxy_quantizable_now` | 价格高于前日价值区顶部后，出现抛压或回调→响应卖方信号。 | 响应=价值回归力量。 |
| 22 | **主动买方 (Initiative Buying)** | 在价值区内或价值区外推动价格上升，试图建立新价值。 | `price_breaks_above_prev_va` + `new_volume_cluster_above` + `acceptance_time > threshold` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 突破前日价值区顶部后，在新区间停留并形成新成交量聚集→主动买方确认。 | 主动=趋势延续力量。 |
| 23 | **主动卖方 (Initiative Selling)** | 在价值区内或价值区外推动价格下降，试图建立新价值。 | `price_breaks_below_prev_va` + `new_volume_cluster_below` + `acceptance_time > threshold` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 与主动买方对称。 | 主动=趋势延续力量。 |
| 24 | **31买入交易日 (3I Buying Day)** | 自发买入尾部 + 自发买入TPO + 自发买入价格幅度扩展。三个方向信号一致。 | `initiative_tail_buy` + `initiative_tpo_buy` + `initiative_range_extension_buy` | OHLCV + 分钟K线 | 日级别 | `needs_extra_data` | 检测三个自发信号同向：买入尾部（极端低单字母+反弹）+ 买入TPO（在价值区上方）+ 买入扩展（突破IB上沿）。 | 近似代理：统计次日94% 90分钟内好于前日VA；97%全日≥前日VA。日类型强依赖TPO形态，OHLCV只能近似。 |
| 25 | **31卖出交易日 (3I Selling Day)** | 自发卖出尾部 + 自发卖出TPO + 自发卖出价格幅度扩展。 | `initiative_tail_sell` + `initiative_tpo_sell` + `initiative_range_extension_sell` | OHLCV + 分钟K线 | 日级别 | `needs_extra_data` | 三个自发卖出信号同向。 | 近似代理：与31买入对称。日类型强依赖TPO形态，OHLCV只能近似。 |
| 26 | **价值区间规则 (Value Area Rule)** | 前日价值区顶部提供支持，底部提供阻力。重新进入价值区且被接受（双TPO）→可能突破。开市价越接近价值区，突破可能性越大。区间狭窄更易突破。 | `prev_va_top`/`prev_va_bottom` as key_levels + `breakthrough_after_re_entry` | OHLCV + 多日线 | 日级别 | `proxy_quantizable_now` | 次日价格相对于前日VA的位置判断。进入VA后是否被接受（停留时间+成交量）决定突破概率。 | 近似代理：跨日关键位系统。 |
| 27 | **剧变 (Spikes)** | 最后几个时段价格迅速偏离已形成的价值区。次日剧变区间内开市=确认；区间外同向=方向延续；反向=拒绝。 | `last_30min_spike_range` + `spike_deviation_from_va` + `next_day_open_vs_spike` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 尾盘30分钟价格偏离日内VA的程度。记录剧变区间[spike_low, spike_high]。次日开盘位置判断。 | 近似代理：剧变价位首次试探时有效；反复试探后失效。 |
| 28 | **平衡区突破 (Balance Area Breakout)** | 多个交易日价值区间重叠形成平衡区。突破后价格运动突然且剧烈。 | `multi_day_va_overlap` + `breakout_from_consolidation` + `volume_confirmation` | OHLCV + 多日线（5日+） | 多日线 | `proxy_quantizable_now` | 连续N日（如5日）VA重叠度>60%定义为平衡区。突破后成交量放大确认。 | 突破方向+止损设在突破点上下。 |
| 29 | **空跳缺口—突破型 (Break-Away Gap)** | 趋势早期，新长线参与者引起。缺口成为支持/阻力。 | `gap_size` + `trend_stage_early` + `gap_not_filled` | OHLCV | 日级别 | `proxy_quantizable_now` | 跳空发生在趋势初期（前日已有方向），缺口未被快速填补。 | 突破空跳=趋势启动确认。 |
| 30 | **空跳缺口—加速型 (Acceleration Gap)** | 趋势中途，再次确认方向。 | `gap_size` + `trend_stage_mid` + `gap_not_filled` | OHLCV | 日级别 | `proxy_quantizable_now` | 跳空发生在趋势中段，加速原有方向。 | 加速空跳=趋势延续确认。 |
| 31 | **空跳缺口—衰竭型 (Exhaustion Gap)** | 趋势最后阶段，几乎人人成为一方，趋势结束。 | `gap_size` + `trend_stage_late` + `gap_filled_quickly` | OHLCV | 日级别 | `proxy_quantizable_now` | 跳空发生在趋势末期，随后被快速填补→衰竭信号。 | 衰竭空跳=趋势结束预警。 |
| 32 | **TPO计数 (TPO Count)** | 控制点上方TPO总数 vs 下方TPO总数。比例估计价值区内买卖失衡。 | `volume_above_poc` / `volume_below_poc` 或 `periods_above_poc` / `periods_below_poc` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 日内POC上方成交量 vs 下方成交量。比例>1.2=卖方失衡；<0.8=买方失衡。 | 近似代理：分钟K线可替代TPO字母计数。 |
| 33 | **TPO图字母映射** | 每半小时一个字母：A=第一半小时，B=第二半小时... | A=9:30-10:00, B=10:00-10:30, C=10:30-11:00, D=11:00-11:30, E=13:00-13:30, F=13:30-14:00, G=14:00-14:30, H=14:30-15:00（A股无I，顺延） | OHLCV + 30分钟K线 | 日级别 | `proxy_quantizable_now` | 直接用30分钟K线生成8根K线，对应A-H。 | 近似代理：注意A股午休11:30-13:00与期货市场不同。 |
| 34 | **无趋势/不确定交易日 (Nontrend/Nonconviction)** | 无趋势：IB窄，无扩展，成交低。不确定：似乎有机会但无真正参考点。 | `nontrend`: `narrow_ib` + `no_extension` + `low_volume`。<br>`nonconviction`: `open_in_prev_va` + `random_oscillation` + `no_reference_point` | OHLCV | 日级别 | `needs_extra_data` | 两者都是“观望”信号。不确定日更容易诱多，因为似乎有驱动型态但实际无方向。 | 近似代理：不确定日=假的驱动型态。日类型强依赖TPO形态，OHLCV只能近似。 |
| 35 | **空头补仓止跌回稳 ("P"形)** | 价格狂跌后，空头回补（买回）引起反弹，无新买方。图形呈"P"字。补仓结束后价格返回原轨道。 | `rapid_rally_after_drop` + `rally_volume_anomaly` + `subsequent_selling_resumes` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 急跌后快速反弹，但反弹中买方力量逐波减弱（每半小时高点降低），之后卖方重新出现。 | 近似代理：图形识别需分钟级数据。可作为模式库。 |
| 36 | **多头斩仓狂跌 ("b"形)** | 上升趋势后，多头平仓（卖出）引起下跌，无新卖方。图形呈"b"字。 | `rapid_drop_after_rally` + `drop_lacks_selling_follow_through` + `buying_resumes` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 急涨后快速下跌，但下跌中卖方无持续力量，之后买方重新"完成"市场轮廓。 | 近似代理：图形识别需分钟级数据。 |
| 37 | **平衡板 (Ledge)** | 某价位区反复形成单字母/双字母停留，成为日内支撑/阻力。 | `repeated_price_halts` + `low_volume_zone` + `acceptance_vs_rejection` | OHLCV + 分钟K线 | 日级别 | `proxy_quantizable_now` | 日内某价位多次出现停留（TPO聚集），之后被接受或拒绝。 | 平衡板=日内关键位。 |
| 38 | **长线极端价位 / 价格偏离** | 长期趋势中的极端价位，远离已建立的价值。响应参与者在此介入。 | `price_vs_long_term_va` + `deviation_multiple` + `responsive_volume_surge` | OHLCV + 多日线 | 多日线/周线 | `proxy_quantizable_now` | 多日VA的移动平均。价格偏离多日VA超过1.5-2个标准差→价格偏离信号。 | 长线极端=中长线建仓/减仓点。 |

---

# FORMULAS_AND_ALGOS

## Formula 1: 价值区间计算（成交量法）—— 原文附录算法
**source_basis**: 附录"价值区间的计算方法"  
**proxy_formula_or_logic**:  
步骤清单：
1. 确定日内成交量最大的价位，将其成交量作为初始基数。
2. 分别计算该价位上方相邻两个价位的成交量之和，以及下方相邻两个价位的成交量之和；比较两侧和数，将较大一侧的和数与基数相加，形成新的基数，并将对应价位纳入价值区间。
3. 将新基数与全日总成交量比较；若未达到70%，则重复步骤2；若已达到或超过70%，则停止，当前纳入的所有价位即构成价值区间。

条件阈值：累加目标为全日总成交量的70%。  
所需数据：日内各价位成交量（分钟K线聚合或逐笔分桶）。  
**caveats**: 原文使用债券32分之1的离散价位。A股价格连续，需先分桶（如1分钱、1毛钱或固定tick）再聚合。分桶粒度直接影响VA宽度。  
**quant_status**: `proxy_quantizable_now` — 可用分钟K线成交量聚合实现。

---

## Formula 2: 价值区间计算（TPO法）—— 原文隐含算法
**source_basis**: 第一章第三节 + 第三章TPO计数法  
**proxy_formula_or_logic**:  
步骤清单：
1. 将交易日按固定时段划分（如每30分钟为一个时段，A股对应A–H共8个时段）。
2. 对每个时段，记录该时段内出现过的价格（可用OHLC范围内的所有价位，或仅取收盘/典型价作为代表）。
3. 每个价格每在一个时段中出现，记为一个TPO。
4. 找出TPO数量最多的价格，即为POC。
5. 从POC开始，分别向上和向下各取两个相邻价格，比较两侧TPO总数。
6. 将TPO较多的一侧加入价值区间，累加TPO数。
7. 重复步骤5–6，直到累计TPO数达到全日TPO总数的70%为止。

条件阈值：累加目标为全日TPO总数的70%。  
所需数据：分钟K线或30分钟K线的 open, high, low, close。  
**caveats**: 原文以债券的1/32离散价位计算。A股连续价格若直接取所有OHLC内价位，TPO数会过多。建议：用分桶聚合（如0.1%或固定档位），或仅用close/typical price作为每个时段的代表价。此方法是近似代理。  
**quant_status**: `proxy_quantizable_now` — 分钟K线可近似代理，但严格TPO需逐笔/时段数据。

---

## Formula 3: 控制点 (POC) 近似重建
**source_basis**: 第一章第三节"最长的且最接近价格幅度中部的TPOs称为控制点"  
**proxy_formula_or_logic**:  
步骤清单：
1. 计算日内各价位的成交量，找出成交量最大的价位。
2. 若多个价位成交量相同，则选择其中最接近日内价格中位数的价位作为POC。

条件阈值：成交量峰值应显著高于相邻价位；若存在多个并列峰值，需人工判断是否为异常。  
所需数据：日内各价位成交量分布（`volume_by_price`）。  
**caveats**: 原文要求"最长且最接近价格幅度中部"，同时考虑TPO长度和位置。纯成交量法只保证"最长"，不保证"最接近中部"。若成交量峰值出现在极端价位，需人工判断是否为异常。此方法是近似代理。  
**quant_status**: `proxy_quantizable_now` — 分钟K线聚合即可，但属近似代理。

---

## Formula 4: 日类型分类判定逻辑/条件清单
**source_basis**: 第二章七种日类型定义  
**proxy_formula_or_logic**:  
判定条件清单（按优先级逐一检验）：

1. 强趋势日判定条件：
   - 开盘位于全日价格幅度底部20%以上（开盘 > 最低 + 0.2 × 日幅）；
   - 收盘位于全日价格幅度顶部20%以下（收盘 < 最高 - 0.2 × 日幅）；
   - 开盘同时位于顶部30%以内（开盘 > 最高 - 0.3 × 日幅），收盘位于底部30%以内（收盘 < 最低 + 0.3 × 日幅）；
   - 当日成交量大于平均成交量的1.2倍。
   若全部满足，判为强趋势日。

2. 无趋势日判定条件：
   - IB区间 < 0.4 × 平均日幅；
   - 全日价格幅度 < 0.6 × 平均日幅；
   - 成交量 < 0.7 × 平均成交量。
   若全部满足，判为无趋势日。

3. 平衡日判定条件：
   - IB区间 > 0.6 × 全日价格幅度；
   - 最高价格未突破IB上沿的0.1%（最高 ≤ IB上沿 × 1.001）；
   - 最低价格未跌破IB下沿的0.1%（最低 ≥ IB下沿 × 0.999）。
   若全部满足，判为平衡日。

4. 变形平衡日判定条件：
   - IB区间 < 0.6 × 全日价格幅度；
   - 出现向上或向下扩展（最高 > IB上沿 或 最低 < IB下沿）；
   - 成交量大于平均成交量。
   若全部满足，判为变形平衡日。

5. 中立日（高/低收）判定条件：
   - 出现双向扩展（最高 > IB上沿 且 最低 < IB下沿，或突破前日最高/最低）；
   - 若收盘位于全日价格幅度中间50%区域（最低 + 0.4 × 日幅 < 收盘 < 最高 - 0.4 × 日幅），判为标准中立日；
   - 若收盘位于顶部20%以内（收盘 > 最高 - 0.2 × 日幅），判为高收中立日；
   - 若收盘位于底部20%以内（收盘 < 最低 + 0.2 × 日幅），判为低收中立日。

6. 弱趋势日/双重分布判定条件：
   - 日内成交量分布呈现双峰形态，且两个峰值之间有低成交量区（单字母/低成交带）。
   若满足，判为弱趋势日/双重分布。

7. 上述条件均不满足时，判为未分类。

条件阈值：所有比例阈值均为近似经验值，需根据标的波动率调整。  
所需数据：OHLCV + 前日数据 + 多日线统计（IB、平均成交量、平均日幅）。  
**caveats**: proxy/approximation。原文的日类型判断依赖于TPO图的完整形态（如"每个时段推向更高"、"TPO轮廓狭长"），仅用OHLCV和简化阈值是近似代理。准确率有限，需持续校准。本清单为判定逻辑，非综合判定引擎。  
**quant_status**: `needs_extra_data` — 日类型强依赖TPO形态，OHLCV只能近似代理，需更多数据或人工校验。

---

## Formula 5: 开市型态分类逻辑
**source_basis**: 第三章四种开市型态定义  
**proxy_formula_or_logic**:  
判定条件清单：

1. 驱动开市（Open-Drive）判定条件：
   - 开盘后30分钟内最高价同时高于开盘价和前日价格幅度上沿；
   - 开盘后30分钟内最低价同时高于开盘价和前日价格幅度下沿（或至少未显著跌破）；
   - 开盘后30分钟收盘价位于该时段振幅顶部10%以内（收盘 > 时段最高 - 0.1 × 时段振幅）。
   若满足，判为驱动开市。

2. 试探驱动开市（Open-Test-Drive）判定条件：
   - 开盘后30分钟内最高价突破前日范围上沿或开盘价上方显著位置；
   - 开盘后30分钟内最低价跌破前日范围下沿或开盘价下方显著位置；
   - 但收盘价最终回到开盘价上方。
   若满足，判为试探驱动开市。

3. 失败反转开市（Open-Rejection-Reverse）判定条件：
   - 开盘后30分钟内出现双向摆动（既突破开盘价上方又跌破开盘价下方）；
   - 收盘价与开盘价之差的绝对值 < 0.3 × 开盘后30分钟振幅。
   若满足，判为失败反转开市。

4. 无方向感开市判定条件：
   - 开盘后30分钟收盘价与开盘价之差的绝对值 < 0.2 × 开盘后30分钟振幅；
   - 若开盘价位于前日价格幅度内，判为"区间内无方向感"（Open-Auction in Range）；
   - 若开盘价位于前日价格幅度外，判为"区间外无方向感"（Open-Auction Out of Range）。
   若上述条件均不满足，判为未知型态。

条件阈值：30分钟为默认观察窗口，A股高波动标的建议缩短至15分钟。  
所需数据：开盘后30分钟OHLC + 前日价值区/价格幅度。  
**caveats**: proxy/approximation。原文判断依赖于TPO图的逐字母观察（如"A分区构成明显买入尾部"），上述逻辑用30分钟区间的简化规则替代。驱动开市和试探驱动的区分在A股中需要更细粒度（5/15分钟）才能准确。此方法是近似代理。  
**quant_status**: `proxy_quantizable_now` — 30分钟级可用，但属近似代理；5分钟级更准。

---

## Formula 6: 31交易日检测器
**source_basis**: 第八章第一节  
**proxy_formula_or_logic**:  
步骤清单：
1. 提取三个方向信号：
   - 尾部信号：检测日内是否出现买入尾部（极端低位单字母+反弹）或卖出尾部（极端高位单字母+回落）；
   - TPO偏向信号：比较POC上方与下方的TPO（或成交量）数量，若上方显著多于下方则为买方偏向，反之为卖方偏向；
   - 价格幅度扩展信号：判断价格是否突破IB上沿（向上扩展）或IB下沿（向下扩展）。
2. 方向一致性检验：
   - 若三个信号均为买方方向（买入尾部 + 买方TPO偏向 + 向上扩展），且收盘位于高位或中高位，则判为31买入交易日；
   - 若三个信号均为卖方方向（卖出尾部 + 卖方TPO偏向 + 向下扩展），且收盘位于低位或中低位，则判为31卖出交易日。
3. 若三个信号方向不一致，或收盘位置与方向不符，则判为非31交易日。

条件阈值：TPO偏向建议采用POC上方/下方成交量比例 > 1.2 或 < 0.8 作为显著失衡阈值。  
所需数据：日内TPO/成交量分布 + 尾部检测 + 扩展方向 + 收盘位置。  
**caveats**: proxy/approximation。原文要求"自发尾部/自发TPO/自发扩展"，需区分"自发"与"响应"。简化版本仅检测三个信号同向，不区分自发/响应。需结合主动/响应定义改进。此方法是近似代理。  
**quant_status**: `needs_extra_data` — 精确区分自发/响应及TPO形态需额外数据（Level2/订单簿/逐笔）。

---

## Formula 7: 价值区间规则（次日关键位判断）
**source_basis**: 第八章第三节  
**proxy_formula_or_logic**:  
步骤清单：
1. 判断次日开盘价相对于前日价值区的位置：
   - 若开盘价高于前日VA上沿：前日VA上沿转化为支撑位；若价格随后跌回VA上沿以下，则标记为"回返价值区，观察是否被拒"。
   - 若开盘价低于前日VA下沿：前日VA下沿转化为阻力位；若价格随后升回VA下沿以上，则标记为"回返价值区，观察是否被拒"。
   - 若开盘价位于前日VA内部：观察价格是否向上突破VA上沿并在上方停留超过阈值时间，若是则标记为"向上突破"；反之若向下跌破VA下沿并停留，则标记为"向下突破"；若未突破，则标记为"平衡"。
2. 评估VA宽度：
   - 计算前日VA宽度（VA上沿 - VA下沿）。
   - 若VA宽度 < 0.5 × 平均VA宽度，则标记为"窄VA"，突破概率较高。

条件阈值：突破后停留时间阈值建议至少30分钟（或对应2个30分钟TPO时段）；窄VA阈值为平均宽度的50%。  
所需数据：前日价值区 + 次日开盘/分钟价格 + 成交量分布。  
**caveats**: proxy/approximation。原文要求"双TPO字母"（进入VA后接受）来判断突破，简化版本用"时间和成交量"替代。此方法是近似代理。  
**quant_status**: `proxy_quantizable_now` — 标准跨日分析，但属近似代理。

---

## Formula 8: 剧变 (Spike) 检测与次日判断
**source_basis**: 第八章第四节  
**proxy_formula_or_logic**:  
步骤清单：
1. 剧变检测：
   - 计算尾盘30分钟价格区间（最高价 - 最低价）。
   - 若尾盘30分钟最低价低于日内VA下沿，且尾盘30分钟最高价低于VA下沿 + 0.5 × 剧变区间，则判为"卖出剧变"；
   - 若尾盘30分钟最高价高于日内VA上沿，且尾盘30分钟最低价高于VA上沿 - 0.5 × 剧变区间，则判为"买入剧变"。
   - 若未满足上述条件，则判为无剧变。
2. 次日判断：
   - 若检测到"卖出剧变"：
     - 次日开盘价低于剧变区间下沿 → 标记为"延续"；
     - 次日开盘价高于剧变区间上沿 → 标记为"拒绝"；
     - 次日开盘价位于剧变区间内 → 标记为"平衡"。
   - 买入剧变同理，方向相反。

条件阈值：剧变区间需显著偏离VA（至少有一端突破VA边界）。  
所需数据：日内VA + 尾盘30分钟OHLC + 次日开盘。  
**caveats**: proxy/approximation。原文中剧变可以是任意时段（不一定是尾盘），但尾盘剧变最常见且影响最大。此方法是近似代理。  
**quant_status**: `proxy_quantizable_now` — 尾盘检测直接可用，但属近似代理。

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

1. `initial_balance` (初期平衡) → 开盘后30/60分钟OHLC区间
2. `value_area_70pct` (价值区间) → 日内成交量分布70%区间（从POC向上下累加）
3. `point_of_control` (控制点) → 日内成交量峰值价或VWAP
4. `range_extension` (价格幅度扩展) → 突破IB后的延伸幅度和方向
5. `opening_type_classifier` (开市型态分类器) → 驱动/试探/失败反转/无方向感四类
6. `single_print_tail_proxy` (单字母尾部代理) → 分钟K线极端价位快速反转+低成交量
7. `tpo_count_proxy` (TPO计数代理) → 分钟/30分钟成交量在POC上方/下方的比例
8. `closing_range` (收市分区) → 尾盘30/15分钟区间
9. `prev_va_key_levels` (前日价值区关键位) → 前日VA_top/VA_bottom作为次日支持/阻力
10. `gap_detector` (缺口检测) → 隔夜跳空幅度+类型判断+回补检测
11. `spike_detector` (剧变检测) → 尾盘/盘中快速偏离VA的区间检测
12. `responsive_vs_initiative_proxy` (响应/主动代理) → 价格相对于前日VA的位置+突破后的接受度
13. `balance_area_detector` (平衡区检测) → 连续N日VA重叠度判断
14. `long_term_trend_proxy` (长线趋势代理) → 多日POC移动方向+VA重叠度

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
9. **day_type_classifier** (日类型分类器) → 基于OHLCV + 前日数据的七种日类型初步分类（日类型强依赖TPO形态，OHLCV只能近似代理，需更多数据或人工校验）
10. **3i_day_detector** (31日检测器) → 三个同向自发信号的简化版（精确区分自发/响应及TPO形态需额外数据）

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
*File: CUTPACK__A2__CN__市场轮廓理论__part2__v2_r1.md*


