# GROUP_08 research pdf 逐条映射清单 v1

更新时间：2026-06-22

## 本表作用

- 把 `GROUP_08` 里的 `research pdf` 进一步收成：
  - `source_pdf(标题锚点)`
  - `v2 md`
  - `当前状态`
  - `删源边界`
- 本表当前采用“双真值源”：
  - 仓库内真值锚点：`GROUP_08_A股量化_数据研究__SOURCE_RAW\新的参考书`
  - 外部补充真值锚点：`D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）`
- 截至本轮，仓库内 `SOURCE_RAW` 已恢复关键源头书：
  - `《Python股票量化交易从入门到实践》完整版`
  - 其中 `research pdf` 的原始承载父目录已确认是：
    - `2.其他量化资料(62份)（赠品）`
- 本轮新增硬结论：
  - `62份赠品` 当前磁盘实际是 `62` 份 `pdf`
  - 其中 `1` 份是物理重复件
  - 因而当前有效研究条目数仍按 `61 pdf` 记
  - 另有 `1` 份 `UNMAPPED_EXTRA` 当前保持主链外保留，不并入现有 `paper_id` 主链
- 当前不满足以下两条前，不删源：
  - 仓库内 `source_raw -> v2 md` 映射成立
  - 外部 `cut_file` 仍可回溯到这批 research pdf 的原始来源目录

## 删源状态口径

- `MAPPED_NOT_DELETE_READY`
  - 已有 `source_pdf(标题锚点) -> v2 md`
  - 但外部 `D:\Stock\cut_file\S` 还没做逐文件删除验收
- `DUPLICATE_SOURCE_ONLY`
  - 重复源，只保留来源对照，不新增独立 v2 产物

## 择时组

| paper_id | source_pdf(标题锚点) | v2 md | 当前状态 | 删源边界 |
|---|---|---|---|---|
| `T-001` | `度量市场"恐惧与贪婪"的量化择时指标` | `CUTPACK__G08__择时__恐惧与贪婪择时指标__v2.md` | `MAPPED_NOT_DELETE_READY` | 需继续保留仓库内 `source_raw` 与外部 `D:\Stock\cut_file\S` 对照 |
| `T-002` | `通过产业资本增减持数据构建的量化择时指标` | `CUTPACK__G08__择时__产业资本增减持择时__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `T-003` | `量化择时——度量市场"恐惧与贪婪"的量化择时指标` | `复用 T-001 对应 v2` | `DUPLICATE_SOURCE_ONLY` | 当前只保留重复源对照，不单开删源 |

## 资产配置组

| paper_id | source_pdf(标题锚点) | v2 md | 当前状态 | 删源边界 |
|---|---|---|---|---|
| `A-001` | `华夏上证行业ETF风格轮动策略之一：利用债券YTM打造行业风格导航仪` | `CUTPACK__G08__资产配置__华夏ETF风格轮动之一_YTM导航仪__v2.md` | `MAPPED_NOT_DELETE_READY` | 需继续保留仓库内 `source_raw` 与外部 `D:\Stock\cut_file\S` 对照 |
| `A-002` | `华夏上证行业ETF风格轮动策略之二：强弱趋势捕捉组合投资机会` | `CUTPACK__G08__资产配置__华夏ETF风格轮动之二_强弱趋势__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `A-003` | `华夏上证行业ETF风格轮动策略之三：基于涨跌比择时的绝对收益动量策略` | `CUTPACK__G08__资产配置__华夏ETF风格轮动之三_涨跌比择时__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `A-004` | `华夏上证行业ETF风格轮动策略之四：基于残差动量的相对收益动量策略` | `CUTPACK__G08__资产配置__华夏ETF风格轮动之四_残差动量__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `A-005` | `基于涨跌比的行业轮动与择时研究` | `CUTPACK__G08__资产配置__涨跌比行业轮动择时__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `A-006` | `妙用涨跌比，小盘指数巧择时` | `CUTPACK__G08__资产配置__涨跌比小盘指数择时__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `A-007` | `基于板块效应动量反转特征的alpha策略研究` | `CUTPACK__G08__资产配置__板块效应动量反转_alpha策略__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `A-008` | `行业动量策略进阶之一：间隔期、系统性风险及换手率的影响` | `CUTPACK__G08__资产配置__行业动量策略进阶_间隔期风险换手率__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `A-009` | `板块持仓测算在创业板风格轮动中的应用` | `CUTPACK__G08__资产配置__板块持仓测算_创业板轮动__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `A-010` | `海通AK行业轮动策略——结构性行情必杀技` | `CUTPACK__G08__资产配置__海通AK行业轮动策略__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `A-011` | `如虎添翼，两融带给ETF的投资机会——海通ETF风格轮动模型实证分析` | `CUTPACK__G08__资产配置__两融ETF投资机会_海通轮动__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `A-012` | `行业基本面预测——在工程机械行业的实证` | `CUTPACK__G08__资产配置__行业基本面预测_工程机械__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `A-013` | `行业基本面预测——在煤炭行业的实证` | `CUTPACK__G08__资产配置__行业基本面预测_煤炭__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `A-014` | `行业基本面预测——在电力行业的实证` | `CUTPACK__G08__资产配置__行业基本面预测_电力__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `A-015` | `行业基本面预测——在钢铁行业的实证` | `CUTPACK__G08__资产配置__行业基本面预测_钢铁__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `A-016` | `衍生产品及量化组合管理策略介绍` | `CUTPACK__G08__资产配置__衍生产品量化组合管理__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |

## 选股组

| paper_id | source_pdf(标题锚点) | v2 md | 当前状态 | 删源边界 |
|---|---|---|---|---|
| `S-001` | `A股全市场选股策略研究` | `CUTPACK__G08__选股__A股全市场选股策略__v2.md` | `MAPPED_NOT_DELETE_READY` | 需继续保留仓库内 `source_raw` 与外部 `D:\Stock\cut_file\S` 对照 |
| `S-002` | `A股上市公司毛利率的均值回归及选股实证` | `CUTPACK__G08__选股__毛利率均值回归选股__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-003` | `A股市场特征研究（一）——沪深300样本股尾部相关性观察` | `CUTPACK__G08__选股__A股市场特征_尾部相关性__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-004` | `A股市场特征研究（二）——波段划分新方法及应用展望` | `CUTPACK__G08__选股__A股市场特征_波段划分__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-005` | `从极值角度进行选股因子有效性的确认——在换手率上的实证` | `CUTPACK__G08__选股__极值角度_换手率因子有效性__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-006` | `分析师荐股能力评定与跟踪` | `CUTPACK__G08__选股__分析师荐股能力评定__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-007` | `高估值，你是否师出有名？` | `CUTPACK__G08__选股__高估值师出有名__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-008` | `工欲善其事，必先利其器——选股因子深度解析` | `CUTPACK__G08__选股__选股因子深度解析__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-009` | `极值视角下的多因子选股策略` | `CUTPACK__G08__选股__极值视角多因子选股__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-010` | `利用分析师盈利预测数据挖掘投资机会` | `CUTPACK__G08__选股__分析师盈利预测选股__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-011` | `量化选股之事件驱动策略` | `CUTPACK__G08__选股__量化选股_事件驱动策略__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-012` | `如何捕捉短线反弹机会？` | `CUTPACK__G08__选股__捕捉短线反弹机会__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-013` | `商业贸易行业选股策略` | `CUTPACK__G08__选股__商业贸易行业选股__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-014` | `上市公司动量反转以及市值因子的选股识别度` | `CUTPACK__G08__选股__动量反转市值因子选股识别度__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-015` | `上市公司估值指标的稳定性与选股识别度` | `CUTPACK__G08__选股__估值指标稳定性选股识别度__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-016` | `事件驱动策略之一——业绩预告之一——把握扭亏、预减公告，获取短期超额收益` | `CUTPACK__G08__选股__事件驱动_业绩预告扭亏预减__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-017` | `事件驱动策略之二——关注主板预减快报后的短期反弹机会以及中小板盈利公告` | `CUTPACK__G08__选股__事件驱动_预减快报反弹__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-018` | `事件驱动策略之三——指数样本股调整` | `CUTPACK__G08__选股__事件驱动_指数样本股调整__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-019` | `事件驱动策略之四——ETF事件套利研究` | `CUTPACK__G08__选股__事件驱动_ETF套利__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-020` | `事件驱动策略之五——大股东增减持——关注增持比例较大的事件机会` | `CUTPACK__G08__选股__事件驱动_大股东增减持__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-021` | `事件驱动策略之六——规避预案陷阱，把握实施收益` | `CUTPACK__G08__选股__事件驱动_规避预案陷阱__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-022` | `事件驱动策略之七——高送转行情下的事件性投资机会` | `CUTPACK__G08__选股__事件驱动_高送转__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-023` | `事件驱动策略之九——股权激励续篇` | `CUTPACK__G08__选股__事件驱动_股权激励续篇__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-024` | `事件驱动策略之十一——事件驱动组合止损机制设计` | `CUTPACK__G08__选股__事件驱动_组合止损机制__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-025` | `事件驱动策略之十二——重要股东持股结构变化蕴含的信息分析` | `CUTPACK__G08__选股__事件驱动_股东持股结构变化__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-026` | `事件驱动策略之十三——定增事件投资——甄别市场，把握买点` | `CUTPACK__G08__选股__事件驱动_定增事件投资__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-027` | `现金流量市值比因子的极值效应` | `CUTPACK__G08__选股__现金流量市值比极值效应__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-028` | `相关性选股策略——全市场选股方法改进` | `CUTPACK__G08__选股__相关性选股_全市场改进__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-029` | `相关性选股策略——在房地产行业上的实证` | `CUTPACK__G08__选股__相关性选股_房地产__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-030` | `相关性选股策略——在纺织服装行业上的实证` | `CUTPACK__G08__选股__相关性选股_纺织服装__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-031` | `相关性选股策略——在公用事业行业上的实证以及选股因子权重的再讨论` | `CUTPACK__G08__选股__相关性选股_公用事业__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-032` | `相关性选股策略——在化学工业行业上的实证` | `CUTPACK__G08__选股__相关性选股_化学工业__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-033` | `相关性选股策略——在有色金属行业上的实证` | `CUTPACK__G08__选股__相关性选股_有色金属__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-034` | `行业内股票业绩弹性分析——在钢铁行业上的实证` | `CUTPACK__G08__选股__行业内业绩弹性_钢铁__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-035` | `行业内选股策略——钢铁行业` | `CUTPACK__G08__选股__行业内选股_钢铁__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-036` | `行业内选股策略——有色金属行业` | `CUTPACK__G08__选股__行业内选股_有色金属__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-037` | `选股因子研究系列（一）——动量反转效应研究` | `CUTPACK__G08__选股__选股因子_动量反转效应__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-038` | `选股因子研究系列（二）——因子模型的尾部相关性研究` | `CUTPACK__G08__选股__选股因子_尾部相关性__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-039` | `选股因子研究系列（三）——Kalman Filter模型在因子选择中的应用` | `CUTPACK__G08__选股__选股因子_Spearman_KalmanFilter__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-040` | `选股因子研究系列（四）——多因子选股模型的有效与失效` | `CUTPACK__G08__选股__选股因子_有效与失效__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |
| `S-041` | `选股因子研究系列（五）——寻找股价驱动新因子之净换手率` | `CUTPACK__G08__选股__选股因子_净换手率__v2.md` | `MAPPED_NOT_DELETE_READY` | 同上 |

## 当前删源规则

- 当前只说明“已映射”，不说明“可删完毕”。
- 真正进入“整理后可删”，至少再满足两条：
  - `GROUP_08_A股量化_数据研究__SOURCE_RAW\新的参考书` 中对应 `research pdf` 已完成逐条删除验收
  - `D:\Stock\cut_file\S` 中对应外部源目录完成复核，不再作为唯一真值源

## 当前新增锚点

- 本轮已能在项目内直接定位下列关键原始 PDF：
  - `S-005` 对应：
    - `从极值角度进行选股因子有效性的确认——在换手率上的实证.pdf`
  - `S-012` 对应：
    - `如何捕捉短线反弹机会？.pdf`
  - `S-014` 对应：
    - `上市公司动量反转以及市值因子的选股识别度.pdf`
  - `S-027` 对应：
    - `现金流量市值比因子的极值效应.pdf`
- 本轮已补出的精确原始路径：
  - `S-014`
    - `D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\财务指标选股研究系列\上市公司动量反转以及市值因子的选股识别度.pdf`
  - `S-027`
    - `D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\选股因子研究系列\现金流量市值比因子的极值效应.pdf`
- 本轮已新增归属审计表：
  - `GROUP_08_research_pdf_61_vs_62归属审计_v1.md`
- 本轮已新增删除级别重核表：
  - `GROUP_08_S-014_S-027_删除级别重核_v1.md`
- 因而当前下一步不再是“继续猜父目录”，而是：
  - 给 `S-014 / S-027` 补最终删除勾选与前后路径台账
  - 继续保持 `UNMAPPED_EXTRA` 主链外保留，后续若要正式吸收再单开编号

## 当前一句话结论

- `GROUP_08` 的 `research pdf` 现在已经从“源线级总表”推进到“逐条标题锚点 -> v2 md”清单。
- 但离“整理后可删”还差最后一步：
  - 给仓库内 `source_raw`
  - 和外部 `D:\Stock\cut_file\S`
  - 各补一轮真正的删除验收表
