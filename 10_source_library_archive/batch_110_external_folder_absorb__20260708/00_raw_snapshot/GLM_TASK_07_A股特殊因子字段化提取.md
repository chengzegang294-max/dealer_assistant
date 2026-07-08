# GLM_TASK_07 — A 股特殊因子字段化提取

> 任务编号：GLM_TASK_07  
> 主题：A 股特殊因子（资金流向 / 波动率 / 主动成交 / 机构行为）字段化对象卡  
> 阶段：结构化提取，不编码  
> 生产者：GLM（需基于 S_BUCKET 已有素材 + 搜索知识）  
> 交付格式：Markdown 对象卡，每因子一份，统一存于用户仓库

---

## 一、背景

用户仓库 `D:\Stock\trading_analysis` 中已有 **S_BUCKET** 素材库（券商研报 477 份），其中部分因子已完成 **round3 功能核心固化**，但尚未转化为可落地的字段化对象卡。

当前仓库已有指标：MT Probes、Volty/XBreaking、KD MTF、PV、RSJ、indicator_audit。已有外部体系：缠论（7 概念卡）、TK 外汇（7 对象卡）、Brooks/YTC/ICT。新补充：Volume Profile（VP）、Kelly Criterion（KELLY）、Volatility Targeting（VOLTARGET）。

**缺失**：A 股特殊因子（资金流向、波动率、主动成交占比、机构行为）尚未以"字段冻结"形式进入仓库。

---

## 二、素材来源（GLM 可基于以下素材，无需重新搜索外部论文）

### 2.1 S_BUCKET 已固化素材（Kimi 已提供索引）

**SBKT_F002** — 长江证券《基础因子研究（十二）：高频因子（七）分布估计下的主动成交占比》
- 已固化为："主动成交占比负向空头/多空 filter（置信正态/均匀 + 分段线性）"
- 升级决策：KEEP_AS_LIMITED_CANDIDATE（仅空头/多空可用，单向多头不纳入）
- 关键数据：全市场 IC=-7.22%, ICIR=-78.64%；中证800 IC=-6.43%, ICIR=-55.49%
- 2017 年后持续衰减，仅空头/多空可用
- 需要：分布估计（t分布/正态/均匀 CDF）、滑动窗口、收益率分位

**SBKT_F006** — 华泰证券《多因子系列 6：单因子测试之波动率类因子》
- 已固化为："波动率非冗余最小集合（id2_std_3m + hml_r_std_5m）"
- 升级决策：ENTER_FUNCTION_CORE_WITH_BOUNDARY
- 关键数据：8 个波动率因子 → 7 个高相关 → 收缩为 1 代表 + hml_r_std_5m（独立信息源）
- 样本期 3-5 个月最佳，2017/02 后样本外待核
- 需要：个股日收益率序列、市场收益率（中证全指）、日内 high/low/close（用于 hml_r_std）

**SBKT_F014** — 华泰证券《多因子系列 7：单因子测试之资金流向因子》
- 已固化为："资金流向短周期 alpha/filter 最小组合（mfd_sellord + mfd_volinflowrate_open_m）"
- 升级决策：ENTER_FUNCTION_CORE_WITH_BOUNDARY
- 关键数据：50 个因子按 8 类分类 → 后 4 类无效 → 前 4 类有效 → 收缩为 2 因子
- 持仓约 10 日，2018/03 后样本外待核，T+1 开盘信号受限
- 需要：Wind 资金流向数据（50 个因子）、委托流分层（小/中/大/超大单）、主动/被动成交标识

**SBKT_F007** — 国盛证券《多因子系列 13：基金重仓股研究》
- 已固化为："机构行为方向的选股池缩小工具（filter）"
- 升级决策：方法层（需筛选，不直接使用全部重仓股）
- 关键数据：基金季报前十大重仓股、Sharpe 资产因子模型、持仓特征因子（Topten_mean/max/count 等）
- 2017 年前小票/成长有效，2017 年后高估值有效
- 需要：基金季报、规模数据、Barra 风格因子

**SBKT_F008/F015/F016** — 广发/国盛多因子系列（均值回复、风险溢价时钟、非线性 Alpha）
- 已固化为：方法层/策略层
- 可作为因子择时/风格轮动参考，但非直接可落地字段

**SBKT_F009/F010** — 海通/国泰君安高频微观系列（持仓推断、机构动向监测）
- 需要 Level-2 数据，成熟度 `needs_extra_data`

### 2.2 搜索补充知识（Kimi 已搜索，GLM 可参考）

- 幻方/九坤等头部量化 A 股三大特色因子方向：
  1. 市场微观结构（Level-2，订单流失衡）→ needs_extra_data
  2. 行为金融异常（龙虎榜、游资席位、散户情绪反转）→ proxy_quantizable_now
  3. 另类数据（研报 NLP、舆情、互动易）→ needs_extra_data

- 聚宽/米筐等平台已支持的 A 股特色因子：
  - 涨跌停数量、涨停封单比、龙虎榜买入占比
  - 北向资金、主力净流入、大单/中单/小单拆分
  - 融资融券余额、股东人数变化
  - 雪球/股吧舆情热度（NLP 处理）

---

## 三、任务要求

### 3.1 交付物

为以下 **4 个 A 股特殊因子** 编写字段化对象卡（每因子一份 Markdown 文件），格式参考附件中的 `OBJECT_CARD_VP_P0_E__VolumeProfile_v1.0.md`：

| # | 因子名称 | 对象 ID | 功能层 | 成熟度 | 素材来源 |
|---|---------|--------|-------|-------|---------|
| 1 | 资金流向因子（Money Flow） | MFLOW_P0_A | P0_A（选股层） | proxy_quantizable_now | SBKT_F014 |
| 2 | 波动率因子（Volatility） | VOLFAC_P0_A | P0_A（选股层） | proxy_quantizable_now | SBKT_F006 |
| 3 | 主动成交占比（Active Trade Ratio） | ATRATIO_P0_A | P0_A（选股层） | proxy_quantizable_now（仅空头/多空） | SBKT_F002 |
| 4 | 机构行为因子（Institutional Behavior） | INSTB_P0_A | P0_A（选股层） | proxy_quantizable_now | SBKT_F007 + 搜索补充 |

### 3.2 每个对象卡必须包含的章节

1. **基本定义**：该因子描述什么，与现有指标的区别
2. **核心概念与字段冻结**：所有字段必须有类型、含义、取值范围
   - 基础字段（原始输入）
   - 派生字段（计算后）
   - 信号字段（如 `mflow_signal_type`、`volfac_filter_state`）
3. **计算逻辑（伪代码）**：基于 S_BUCKET 素材中的公式，写成 Python 风格的伪代码
   - 必须包含公式来源注释（如"来自 SBKT_F014 正文"）
   - 不要写实际可执行代码，用中文注释说明意图
4. **与现有指标的互锁逻辑**：
   - 与 KD MTF 的互锁（如：资金流向因子只在 KD 锁仓方向一致时生效）
   - 与 Volty 的互锁（如：高波动时资金流向因子可靠性下降）
   - 与 VP 的互锁（如：资金流向流入时若价格处于 VP 的 HVN，信号增强）
   - 与缠论 BSD 的互锁（如：1Buy 时若资金流入确认，可提升仓位）
   - 与 TK 的互锁（如：TK-R6 回撤时若资金持续流出，确认空头力量）
5. **失效模式**：什么时候该因子不可用，需要降级
6. **A 股特殊适配**：涨停/跌停、T+1、散户行为、交易成本等影响
7. **成熟度与数据需求**：所需数据类型、计算复杂度、A 股落地可行性

### 3.3 格式规范

- 文件名：`OBJECT_CARD_{ID}__{中文名}_v1.0.md`
- 文件头必须包含：功能层、成熟度、生产者、来源、状态
- 字段定义用 `字段名 类型 含义` 格式，类似 SQL 注释风格
- 所有公式必须标注来源（来自哪个 SBKT 或搜索来源）
- 所有产出必须携带：producer / source_path / status 元数据

### 3.4 特别注意

1. **不要编码**：只写伪代码和字段定义，不要写完整的 Python 可执行代码。
2. **保守标注**：只有常规 A 股数据（OHLCV、资金流向、龙虎榜）可直接落地的条目保留 `proxy_quantizable_now`；依赖 Level-2、NLP、另类数据的条目降级为 `needs_extra_data`。
3. **与现有对象的映射**：每个新因子必须明确说明"与现有仓库中的 X 对象是什么关系"（互补/重叠/替代/增强）。
4. **SBKT_F002 的特殊性**：该因子已明确"仅空头/多空可用，单向多头不纳入"。在对象卡中必须明确标注此限制，并给出"在单向多头策略中如何替代使用"的建议（如：用 SBKT_F014 替代）。

---

## 四、已提供的参考文件（Kimi 已写入）

请 GLM 在编写对象卡时参考以下文件的格式和风格：

1. `OBJECT_CARD_VP_P0_E__VolumeProfile_v1.0.md` — Volume Profile 执行层对象卡（格式模板）
2. `OBJECT_CARD_KELLY_P0_R__KellyCriterion_v1.0.md` — Kelly 风控层对象卡
3. `OBJECT_CARD_VOLTARGET_P0_R__VolatilityTargeting_v1.0.md` — Vol Targeting 风控层对象卡
4. `GLM_DELIVERY_04_CHANLUN_FULL_QUANT_v1.0.md` — 缠论全量化交付（字段冻结风格）
5. `GLM_DELIVERY_05_TK_FOREX_OPTIMIZED_v1.0.md` — TK 外汇优化交付（互锁逻辑风格）
6. `S_BUCKET_功能映射表_v1.tsv` — S_BUCKET 功能映射表（素材索引）

以上文件均位于 `E:\downloads\Desktop\找系统\特征\`（用户仓库工作目录）。

---

## 五、交付路径

GLM 完成后，将 4 个 Markdown 文件的内容直接写入回复中，或保存到指定路径。Kimi 会负责格式化、统一命名规范、并入仓库功能映射大表。

---

## 六、优先级与范围

**第一优先级（必须完成）**：
- MFLOW_P0_A（资金流向因子）— 基于 SBKT_F014，已有最完整的字段定义
- VOLFAC_P0_A（波动率因子）— 基于 SBKT_F006，已有明确的收缩结论

**第二优先级（尽量完成）**：
- ATRATIO_P0_A（主动成交占比）— 基于 SBKT_F002，但限制较多（仅空头/多空）
- INSTB_P0_A（机构行为因子）— 基于 SBKT_F007 + 搜索补充，需要更多判断

---

> 任务发起人：Kimi  
> 时间：2026-06-24  
> 状态：已发送，等待 GLM 交付
