# TK外汇核心概念对象卡（Kimi 自制版）

> 制作人：Kimi
> 来源路径：`D:/Stock/trading_analysis/10_来源库_SOURCE_LIBRARY/00_TK外汇`
> 制作时间：2026-06-19
> 版本：v1.0
> 状态：供 GLM 审阅 / 仓库字段冻结预备

---

## 阅读说明

本文档是 Kimi 在读取 `00_TK外汇` 文件夹全部素材后，自行制作的 TK 外汇系统核心概念对象卡。供 GLM 后续优化、补充和正式入库使用。

素材已读取：
- `20231219TK外汇交易系统学习资料整理(6)_吸收结论_v1.md`
- `TK_Batch1_新增对象入口索引_v1.md`
- `外汇交易课程第一集-信号_导出.md` (IB/DB/CB 定义)
- `外汇交易课程第八集-让我稳定获利的开单工具_导出.md` (XBreaking + FEtp)
- `外汇交易课程第九集-如何让Xbreaking在小周期正常运作_导出.md` (XBreaking 小周期排障)

---

# 第一部分：TK 信号基础层（3 个对象）

## [01] TK-IB — Initial Break（初始突破）

| 字段 | 内容 |
|------|------|
| **object_id** | TK_IB |
| **object_name** | 初始突破（IB） |
| **source_anchor** | 第一集：最高/最低收盘价蜡烛的开盘与收盘区间 |
| **function_bucket** | 结构层 / 原始特征 |
| **process_layer** | 特征 |
| **scope_tags** | 单资产 / 单时间框架 |
| **maturity_level** | 已摘公式 |
| **input_requirement** | 标准 OHLC + 收盘价序列；找出最高收盘价（上涨趋势）或最低收盘价（下跌趋势）的蜡烛 |
| **output_form** | `struct {ib_high, ib_low, ib_direction, parent_candle_idx}` |
| **best_use_case** | 所有后续信号（DB、CB）成立的先决条件；信号失效的判定基准 |
| **cannot_do_yet** | 无法自动判断"最高收盘价"是否属于当前波段（需排除更早波段干扰） |
| **combines_with** | TK-DB（>=3根蜡烛突破IB）、TK-CB（IB左侧收盘价突破） |
| **overlaps_with** | 传统支撑阻力区、缠论中枢（都是价格重叠区域） |
| **failure_modes** | IB 区域被反向突破 = 信号失效（唯一标准）；急涨急跌中 IB 频繁被反向击穿 |
| **evidence_note** | 上升趋势：最高收盘价蜡烛的 [open, close] 区间；下跌趋势：最低收盘价蜡烛的 [open, close] 区间 |
| **proxy_quantizable_now** | yes |

### 关键公式（伪代码）

```python
def identify_ib(candles, trend_direction):
    if trend_direction == "up":
        # 找最高收盘价的蜡烛
        target_candle = max(candles, key=lambda c: c.close)
    else:  # down
        # 找最低收盘价的蜡烛
        target_candle = min(candles, key=lambda c: c.close)
    
    ib_high = max(target_candle.open, target_candle.close)
    ib_low = min(target_candle.open, target_candle.close)
    
    return {
        "ib_high": ib_high,
        "ib_low": ib_low,
        "direction": trend_direction,
        "parent_idx": target_candle.index
    }
```

---

## [02] TK-DB — Dominant Break（主导突破）

| 字段 | 内容 |
|------|------|
| **object_id** | TK_DB |
| **object_name** | 主导突破（DB） |
| **source_anchor** | 第一集：至少3根或以上蜡烛共同完成IB突破 |
| **function_bucket** | 结构层 / 信号 |
| **process_layer** | 信号 |
| **scope_tags** | 单资产 / 单时间框架 |
| **maturity_level** | 已摘公式 |
| **input_requirement** | TK-IB 已识别 + 后续蜡烛序列 |
| **output_form** | `struct {db_triggered(bool), db_candle_count, db_confidence}` |
| **best_use_case** | 出现在关键支撑/阻力区域时，可直接作为入场信号 |
| **cannot_do_yet** | 无法自动判断"关键支撑/阻力区域"（需人工/外部工具标定） |
| **combines_with** | TK-IB（前提）、TK-FEtp（执行工具） |
| **overlaps_with** | Brooks 多蜡烛突破、YTC BOF/BPB、缠论中枢突破 |
| **failure_modes** | IB 区域被反向突破 = 信号失效；假突破（3根突破后迅速回踩） |
| **evidence_note** | IB 区域被 >=3 根连续蜡烛完全突破（close > ib_high 或 close < ib_low） |
| **proxy_quantizable_now** | yes |

### 关键公式（伪代码）

```python
def identify_db(candles_after_ib, ib_struct):
    count = 0
    for candle in candles_after_ib:
        if ib_struct.direction == "up" and candle.close > ib_struct.ib_high:
            count += 1
        elif ib_struct.direction == "down" and candle.close < ib_struct.ib_low:
            count += 1
        else:
            break  # 连续性中断
    
    return {
        "db_triggered": count >= 3,
        "db_candle_count": count,
        "db_confidence": min(count / 5, 1.0)  # 5根以上视为高置信度
    }
```

---

## [03] TK-CB — CanBreak（趋势突破/确认突破）

| 字段 | 内容 |
|------|------|
| **object_id** | TK_CB |
| **object_name** | 确认突破（CB） |
| **source_anchor** | 第一集：IB 左侧前一根蜡烛的收盘价突破 |
| **function_bucket** | 执行层 / 触发器 |
| **process_layer** | 执行约束 |
| **scope_tags** | 单资产 / 单时间框架 |
| **maturity_level** | 已摘公式 |
| **input_requirement** | TK-IB 已识别 + IB 左侧前一根蜡烛的收盘价 |
| **output_form** | `struct {cb_triggered(bool), cb_price_level, cb_candle_idx}` |
| **best_use_case** | 最安全的入场信号之一；发生在支撑/阻力区域时可直接执行 |
| **cannot_do_yet** | 无法自动判断 CB 位置是否"左侧前一根"（需确认不是 IB 本身） |
| **combines_with** | TK-IB（前提）、TK-DB（同向确认）、TK-FEtp（执行） |
| **overlaps_with** | Brooks Breakout Pullback、YTC TST、缠论三类买卖点（第三类） |
| **failure_modes** | CB 突破后迅速回落 = 假突破；IB 被反向突破 = 信号失效；CB 与 IB 开盘价重合 = 定位错误（学生常见错误） |
| **evidence_note** | IB 蜡烛左侧紧邻的前一根蜡烛的收盘价，被后续蜡烛突破 |
| **proxy_quantizable_now** | yes |

### 关键公式（伪代码）

```python
def identify_cb(candles, ib_struct, ib_idx):
    # ib_idx: IB 蜡烛在序列中的索引
    if ib_idx <= 0:
        return {"cb_triggered": False}
    
    # CB 点位 = IB 左侧前一根蜡烛的收盘价
    cb_level = candles[ib_idx - 1].close
    
    # 等待后续蜡烛突破
    for i, candle in enumerate(candles[ib_idx + 1:], start=ib_idx + 1):
        if ib_struct.direction == "up" and candle.close > cb_level:
            return {
                "cb_triggered": True,
                "cb_price_level": cb_level,
                "cb_candle_idx": i
            }
        elif ib_struct.direction == "down" and candle.close < cb_level:
            return {
                "cb_triggered": True,
                "cb_price_level": cb_level,
                "cb_candle_idx": i
            }
    
    return {"cb_triggered": False}
```

### 常见错误（学生常犯）
- **错误**：将 IB 蜡烛的开盘价当作 CB 点位
- **正确**：CB 点位 = IB 左侧前一根蜡烛的收盘价
- **工程注意**：代码中必须检查 `cb_level != ib_struct.ib_open`，否则标注 `INVALID_CB_PLACEMENT`

---

# 第二部分：TK 工具层（XBreaking 正式对象化）

## [04] TK-XBreaking — CB/DB 信号识别指标

| 字段 | 内容 |
|------|------|
| **object_id** | TK_XBREAKING |
| **object_name** | XBreaking 信号识别器 |
| **source_anchor** | 第八集：自动识别 CB/DB 信号；第九集：小周期排障 |
| **function_bucket** | 执行层 / 辅助触发器 |
| **process_layer** | 执行约束 |
| **scope_tags** | 单资产 / 多时间框架（1H以上稳定，1H以下需手动加载历史数据） |
| **maturity_level** | 已知IO（Known Input-Output） |
| **input_requirement** | 标准 OHLC + 参数：计算K线个数（默认200）、灵敏度（16）、剔除无效信号（默认True） |
| **output_form** | `struct {signal_type(enum: CB/DB/CB+DB/none), signal_box_price, signal_size_pips, is_valid(bool)}` |
| **best_use_case** | 新手辅助识别信号；复盘中快速标记所有历史信号（含失败信号） |
| **cannot_do_yet** | 1分钟周期无法显示（数据源物理极限）；信号框偶尔错位（最低/最高点位不准） |
| **combines_with** | TK-IB/DB/CB（人工验证）、TK-FEtp（执行） |
| **overlaps_with** | 所有手动识别方法（XBreaking 是自动化封装） |
| **failure_modes** | 小周期数据加载不足导致无信号；信号框与真实最低/最高点位偏差；历史数据加载导致卡顿 |
| **evidence_note** | buffer 0 对应 CB/DB 信号标记；参数 `calc_bars=200` 控制回检范围 |
| **proxy_quantizable_now** | yes |

### XBreaking 参数冻结建议

```yaml
TK_XBREAKING:
  parameters:
    calc_bars: 200        # 计算K线个数，复盘可增至2000/5000
    sensitivity: 16       # 灵敏度，默认不动（开发者未解释含义）
    alert_enabled: true   # 系统预警
    wechat_alert: false   # 微信预警（需额外配置）
    show_notes: true      # 显示分析备注（方框+文字）
    remove_invalid: true  # 剔除无效信号（保持图表简洁）
    
  colors:  # 可自定义，但不影响逻辑
    cb_long: "青色"
    db_long: "指定色"
    cb_db_combined: "指定色"
    db_short: "红色"
    
  output_buffers:
    buffer0: signal_type  # CB/DB/DB+CB/none
    # 信号框大小：信号成立到止损位置的点数（括号内数字）
```

### XBreaking 语义确认（解决 NEED_PROBE）

此前仓库中 `XBreaking` 标注为 `NEED_PROBE`（buffer 0 可读但语义未知）。

**经 TK 素材确认：**
- `buffer0` 对应 **CB/DB 信号类型**（做多信号/做空信号）
- XBreaking 的核心功能是 **自动识别 TK-IB/DB/CB 信号体系中的信号**
- 不是独立的新信号类型，而是现有信号体系的 **自动化探测器**

**因此，建议将 `XBreaking` 对象升级：**
- object_id: `TK_XBREAKING`（替代原 `XBREAKING`）
- maturity: `已知IO` → `可进入候选组合`
- 映射：TK_XBREAKING.signal_type ↔ 人工识别的 TK-IB/DB/CB

---

# 第三部分：TK 后续对象层（R6/R7/R8 当前状态）

## [05] TK-R6 — IB 回撤阻挡 → TP3 概率增强

| 字段 | 内容 |
|------|------|
| **object_id** | TK_R6 |
| **object_name** | IB 回撤阻挡到 TP3 概率增强 |
| **source_anchor** | 吸收结论：IB 是信号最后关口；回撤到 IB 后被强力阻挡 → TP3 概率增强 |
| **function_bucket** | 执行层 / 后续对象入口 |
| **process_layer** | 执行约束 |
| **maturity_level** | 后续对象入口（next_object_entry） |
| **input_requirement** | TK-IB 已识别 + 价格回撤到 IB 区域 + 蜡烛阻挡行为 |
| **output_form** | `enum {touch_only, reject_weak, reject_clear, inside_ib, break_through}` |
| **best_use_case** | 主信号成立后，判断 IB 区域是否提供有效支撑/阻力，增强 TP3 延伸信心 |
| **cannot_do_yet** | `reject_clear` 的最少价格行为特征未标准化；`inside_ib` 的最小触达距离未冻结 |
| **combines_with** | TK-R1（TP3 延伸骨架）、TK-R8（B 区域 qualify） |
| **overlaps_with** | Brooks pullback、LBR Holy Grail、缠论二类买卖点 |
| **failure_modes** | IB 被直接突破（无阻挡）= 信号失效；弱阻挡后价格继续穿透 |
| **evidence_note** | 已有 `tkr6_manual_audit_sheet_v1.tsv` 和 `tkr6_manual_audit_summary_v1.md` |
| **proxy_quantizable_now** | no（需人工标注样本） |

### 当前待冻结字段草案

```yaml
TK_R6:
  fields:
    ib_retest_status:   # 枚举: touch_only / reject_weak / reject_clear / break_through
    reject_strength:    # 0-1 浮点，基于影线/实体比例
    tp3_probability:  # 标签: enhanced / normal / reduced
    min_distance_pips:  # IB 附近最小距离口径（待定义）
```

---

## [06] TK-R7 — AO 背离风险调整标签

| 字段 | 内容 |
|------|------|
| **object_id** | TK_R7 |
| **object_name** | AO 动量背离风险调整标签 |
| **source_anchor** | 吸收结论：AO 作为风险调整/背离辅助，不升独立硬信号 |
| **function_bucket** | 能量层 / 风险调整标签 |
| **process_layer** | 过滤器 |
| **maturity_level** | 风险调整标签入口（risk_adjust_label_entry） |
| **input_requirement** | AO 指标 + 价格新高/新低 + AO 柱状图 |
| **output_form** | `enum {divergence_present, no_divergence, momentum_fade}` |
| **best_use_case** | 主信号成立后，如果 AO 背离存在，降低仓位或提前止盈 |
| **cannot_do_yet** | AO 参数未标准化；背离确认延迟 |
| **combines_with** | 所有 TK 执行层对象（作为风险修正标签） |
| **overlaps_with** | RSJ（情绪冷暖）、CHZL_BC（缠论背驰） |
| **failure_modes** | AO 背离后价格继续加速（趋势太强） |
| **evidence_note** | 已有 `tkr7_manual_audit_sheet_v1.tsv` |
| **proxy_quantizable_now** | needs_extra_data（AO 参数需校准） |

---

## [07] TK-R8 — B 区域 Qualify 壳

| 字段 | 内容 |
|------|------|
| **object_id** | TK_R8 |
| **object_name** | B 区域资格判定壳 |
| **source_anchor** | 吸收结论：不是所有回撤区都算 B；需维持 ABC 波段结构成立 |
| **function_bucket** | 执行层 / 过滤器 |
| **process_layer** | 过滤器 |
| **maturity_level** | Qualify 壳入口（qualify_shell_entry） |
| **input_requirement** | ABC 波段结构 + 回撤深度 + 结构未破坏 |
| **output_form** | `enum {valid_b_zone, invalid_b_zone, structure_broken, continuation_lost}` |
| **best_use_case** | 细化 ABC/B 位挂单的条件，避免在无效回撤区入场 |
| **cannot_do_yet** | `structure_break` 最小可见价格行为特征未定义；`b_zone_miss` 最小距离口径未冻结 |
| **combines_with** | TK-R1（TP3 延伸）、TK-R6（IB 阻挡验证） |
| **overlaps_with** | Brooks BPB、YTC BPB、缠论中枢内部（都是"回撤区"） |
| **failure_modes** | ABC 结构失效（C 点未创新高/低）；B 区域后价格继续反向穿透 |
| **evidence_note** | 已有 `tkr8_manual_audit_sheet_v1.tsv` 和 `tkr8_manual_audit_summary_v1.md` |
| **proxy_quantizable_now** | no（需结构判定的主观规则） |

### 当前待冻结字段草案

```yaml
TK_R8:
  fields:
    abc_valid:          # bool: C 点是否创新高/低
    b_zone_depth:       # float: 回撤占 AB 段的比例（如 0.382, 0.5, 0.618）
    structure_status:   # 枚举: valid / broken / extending
    b_zone_qualify:     # bool: 是否满足最小判据
```

---

# 第四部分：TK 外汇 vs KD MTF P0 映射关系

## 1. 结构层映射

| KD MTF P0 字段 | TK 对应概念 | 映射说明 |
|---------------|------------|---------|
| `kd_week_bias` | TK-IB 的波段方向 | 周线 KD 方向 ≈ IB 所在的大趋势方向 |
| `kd_day_signal` | TK-CB 触发时机 | 日线 KD 金叉/死叉常发生在 CB 突破前后 |
| `kd_4h_confirm` | TK-DB 确认 | 4H 出现 DB 信号 ≈ 4H KD 同向确认 |
| `kd_alignment_tier` | TK 信号链完整性 | `s` = IB+DB/CB 完整；`a` = 只有 IB；`b` = 等待 CB |
| `kd_direction_filter` | TK 信号方向 | long_preferred = CB做多/DB做空信号 |
| `kd_week_extreme_zone` | TK 信号位置评估 | overbought = 信号出现在高位，需更严的 qualify |

## 2. 执行层映射

| KD MTF P0 状态 | TK 执行动作 | 互锁决策 |
|---------------|------------|---------|
| `alignment = s` + `direction = long` | TK-CB 做多触发 | **最强信号**：共振 + 结构确认 |
| `alignment = a` + `day = cross_up` | 等待 TK-CB 或 TK-DB | **观察**：有动能但无结构确认 |
| `alignment = conflict` + `week = up` | TK-IB 被反向突破 | **强制止损**：结构失效，KD 信号无效 |
| `week_extreme = overbought` | TK-CB 出现在高位 | **降低仓位**：即便信号成立，RRR 变差 |

## 3. 能量层映射（TK-R7 对接）

| KD MTF P0 字段 | TK-R7 对接 | 说明 |
|---------------|-----------|------|
| `kd_week_extreme_zone` | `ao_divergence` | 周线超买 + AO 背离 = 强反转预期 |
| `kd_day_signal` | `momentum_fade` | 日线 KD 金叉但 AO 走弱 = 假突破风险 |

---

# 第五部分：工程建议与字段冻结清单

## 立即可冻结（可进入候选组合）

```yaml
# TK-IB / TK-DB / TK-CB 核心字段
TK_IB:
  - ib_high: float
  - ib_low: float
  - ib_direction: enum(up, down)
  - ib_parent_idx: int
  - ib_valid: bool  # 是否被反向突破

TK_DB:
  - db_triggered: bool
  - db_candle_count: int
  - db_confidence: float(0-1)

TK_CB:
  - cb_triggered: bool
  - cb_price_level: float
  - cb_candle_idx: int
  - cb_placement_valid: bool  # 检查是否 != IB 开盘价
```

## 后续对象入口（待 GLM/Kimi 继续推进）

```yaml
TK_R6:
  status: next_object_entry
  needs: 人工标注 100+ 个 IB 回撤样本，训练 reject_weak vs reject_clear 分类

TK_R7:
  status: risk_adjust_label_entry
  needs: AO 参数标准化（周期设置）；与 KD MTF P0 的联合回测

TK_R8:
  status: qualify_shell_entry
  needs: ABC 结构失效的精确量化规则（如 C 点回撤超过 AB 的 80%？）
```

## XBreaking 升级建议

- **原对象**：`XBREAKING`（NEED_PROBE）
- **建议升级为**：`TK_XBREAKING`（已知IO → 可进入候选组合）
- **字段映射**：
  - `buffer0` → `signal_type`（CB/DB/CB+DB/none）
  - 信号框大小 → `signal_size_pips`（止损到信号点的距离）
- **注意事项**：
  - 1H 以下周期需手动加载历史数据（向左拖动图表）
  - 1 分钟周期存在物理极限，无法显示
  - 信号框偶有错位，需人工校验

---

# 附录：素材来源索引

| 文件 | 内容摘要 | 在本文档中的引用位置 |
|------|---------|-------------------|
| `吸收结论_v1.md` | TK-R6/R7/R8 的优先级裁决；四分流 | 第三部分、第四部分 |
| `Batch1_新增对象入口索引_v1.md` | R6/R7/R8 的入口文件清单 | 第三部分 |
| `第一集-信号_导出.md` | IB/DB/CB 定义、失效条件、CB 定位错误 | 第一部分 |
| `第八集-开单工具_导出.md` | XBreaking 参数、FEtp 工具、风控一致性 | 第二部分 |
| `第九集-Xbreaking小周期_导出.md` | 小周期排障、数据加载限制、CB/DB 信号识别 | 第二部分 |

---

> **给 GLM 的备注**：
> 本文档是 Kimi 基于原始素材自行整理的一版。重点解决了 XBreaking 的 `NEED_PROBE` 状态（已确认为 CB/DB 信号探测器）。
> GLM 可在此基础上：
> 1. 优化 TK-IB/DB/CB 的伪代码，补充边界条件（如 IB 被反向突破的实时检测）
> 2. 为 TK-R6/R7/R8 设计更精确的量化判据
> 3. 补充 TK 外汇系统与缠论对象卡（CHZL_xxx）的交叉映射
