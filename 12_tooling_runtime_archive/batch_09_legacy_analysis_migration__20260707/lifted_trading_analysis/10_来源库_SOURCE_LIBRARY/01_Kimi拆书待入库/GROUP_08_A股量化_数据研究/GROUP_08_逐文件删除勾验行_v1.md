# GROUP_08 逐文件删除勾验行 v1

更新时间：2026-06-22

## 本表作用

- 这张表把 `research pdf` 从“逐条映射”推进到“逐文件删除勾验行”。
- 每一行都只回答四件事：
  - 仓库内侧现在能不能删
  - 外部 `D:\Stock\cut_file\S\03_券商研报` 对应子集现在能不能删
  - 当前总裁决是什么
  - 还差什么
- 自 2026-06-22 起，外部侧的“精确路径/复制入 staging/最终删除勾选条目清单”改为台账驱动：
  - 精确路径与复制真值：`GROUP_08_前后路径台账_v1.tsv`
  - 条目级最终删除勾选：`GROUP_08_research_pdf_最终删除勾选_逐条清单_v1.tsv`
  - 引用扫描证据：`GROUP_08_repo_refscan_summary_v1.tsv`
  - 因而本表的“外部侧/还缺什么”不再强制逐行同步，避免手工维护反复偏离真值

## 勾验状态口径

- `REPO_PENDING_TICK`
  - 仓库内已有 `v2 md`
  - 但还没做最终删除勾选
- `REPO_DELETE_RECHECK_READY`
  - 仓库内 `v2 md` 已完成删除级别重核
  - 可进入最终删除勾选候选
- `S_PENDING_EXACT_PATH`
  - 外部 `S` 已确认属于 `03_券商研报` 子树
  - 但还没落成精确文件路径和删除勾选
- `SERIES_MANUAL_CONFIRMED / SHARED_SERIES_SOURCE_CONFIRMED / TOPIC_MANUAL_CONFIRMED / EXACT_LIKE_MATCH`
  - 外部 `S\03_券商研报` 已补到精确路径层
  - 且已生成（或复用）仓库内 staging 副本
- `BOOKDIR_EXACT_PATH_CONFIRMED`
  - 已在 `D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）` 下确认精确原始 `pdf`
  - 但当前只代表“可回溯原件”，不代表立即可删
- `DUPLICATE_KEEP_ONE`
  - 重复源，不单开独立删除动作
- `NOT_DELETE_READY`
  - 当前不能删

## 择时组

| paper_id | 标题锚点 | 仓库内侧 | 外部侧 | 当前总裁决 | 还缺什么 |
|---|---|---|---|---|---|
| `T-001` | `度量市场"恐惧与贪婪"的量化择时指标` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 外部精确路径 + 双侧勾选 |
| `T-002` | `通过产业资本增减持数据构建的量化择时指标` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 外部精确路径 + 双侧勾选 |
| `T-003` | `量化择时——度量市场"恐惧与贪婪"的量化择时指标` | `DUPLICATE_KEEP_ONE` | `DUPLICATE_KEEP_ONE` | `NOT_DELETE_READY` | 仅保留重复对照 |

## 资产配置组

| paper_id | 标题锚点 | 仓库内侧 | 外部侧 | 当前总裁决 | 还缺什么 |
|---|---|---|---|---|---|
| `A-001` | `华夏上证行业ETF风格轮动策略之一：利用债券YTM打造行业风格导航仪` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 外部精确路径 + 双侧勾选 |
| `A-002` | `华夏上证行业ETF风格轮动策略之二：强弱趋势捕捉组合投资机会` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `A-003` | `华夏上证行业ETF风格轮动策略之三：基于涨跌比择时的绝对收益动量策略` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `A-004` | `华夏上证行业ETF风格轮动策略之四：基于残差动量的相对收益动量策略` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `A-005` | `基于涨跌比的行业轮动与择时研究` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `A-006` | `妙用涨跌比，小盘指数巧择时` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `A-007` | `基于板块效应动量反转特征的alpha策略研究` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `A-008` | `行业动量策略进阶之一：间隔期、系统性风险及换手率的影响` | `REPO_PENDING_TICK` | `BOOKDIR_EXACT_PATH_CONFIRMED` | `MOVE_READY_NOT_DELETE` | 最终删除勾选（已入条目级清单） |
| `A-009` | `板块持仓测算在创业板风格轮动中的应用` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `A-010` | `海通AK行业轮动策略——结构性行情必杀技` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `A-011` | `如虎添翼，两融带给ETF的投资机会——海通ETF风格轮动模型实证分析` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `A-012` | `行业基本面预测——在工程机械行业的实证` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `A-013` | `行业基本面预测——在煤炭行业的实证` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `A-014` | `行业基本面预测——在电力行业的实证` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `A-015` | `行业基本面预测——在钢铁行业的实证` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `A-016` | `衍生产品及量化组合管理策略介绍` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |

## 选股组

| paper_id | 标题锚点 | 仓库内侧 | 外部侧 | 当前总裁决 | 还缺什么 |
|---|---|---|---|---|---|
| `S-001` | `A股全市场选股策略研究` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 外部精确路径 + 双侧勾选 |
| `S-002` | `A股上市公司毛利率的均值回归及选股实证` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-003` | `A股市场特征研究（一）——沪深300样本股尾部相关性观察` | `REPO_PENDING_TICK` | `SHARED_SERIES_SOURCE_CONFIRMED` | `MOVE_READY_NOT_DELETE` | 最终删除勾选（已入条目级清单） |
| `S-004` | `A股市场特征研究（二）——波段划分新方法及应用展望` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-005` | `从极值角度进行选股因子有效性的确认——在换手率上的实证` | `REPO_PENDING_TICK` | `BOOKDIR_EXACT_PATH_CONFIRMED` | `MOVE_READY_NOT_DELETE` | 最终删除勾选（已入条目级清单） |
| `S-006` | `分析师荐股能力评定与跟踪` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-007` | `高估值，你是否师出有名？` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-008` | `工欲善其事，必先利其器——选股因子深度解析` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-009` | `极值视角下的多因子选股策略` | `REPO_PENDING_TICK` | `EXACT_LIKE_MATCH` | `MOVE_READY_NOT_DELETE` | 最终删除勾选（已入条目级清单） |
| `S-010` | `利用分析师盈利预测数据挖掘投资机会` | `REPO_PENDING_TICK` | `TOPIC_MANUAL_CONFIRMED` | `MOVE_READY_NOT_DELETE` | 最终删除勾选（已入条目级清单） |
| `S-011` | `量化选股之事件驱动策略` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-012` | `如何捕捉短线反弹机会？` | `REPO_PENDING_TICK` | `BOOKDIR_EXACT_PATH_CONFIRMED` | `MOVE_READY_NOT_DELETE` | 最终删除勾选（已入条目级清单） |
| `S-013` | `商业贸易行业选股策略` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-014` | `上市公司动量反转以及市值因子的选股识别度` | `REPO_DELETE_RECHECK_READY` | `BOOKDIR_EXACT_PATH_CONFIRMED` | `MOVE_READY_NOT_DELETE` | 最终删除勾选（已入条目级清单） |
| `S-015` | `上市公司估值指标的稳定性与选股识别度` | `REPO_PENDING_TICK` | `BOOKDIR_EXACT_PATH_CONFIRMED` | `MOVE_READY_NOT_DELETE` | 最终删除勾选（已入条目级清单） |
| `S-016` | `事件驱动策略之一——业绩预告之一——把握扭亏、预减公告，获取短期超额收益` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-017` | `事件驱动策略之二——关注主板预减快报后的短期反弹机会以及中小板盈利公告` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-018` | `事件驱动策略之三——指数样本股调整` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-019` | `事件驱动策略之四——ETF事件套利研究` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-020` | `事件驱动策略之五——大股东增减持——关注增持比例较大的事件机会` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-021` | `事件驱动策略之六——规避预案陷阱，把握实施收益` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-022` | `事件驱动策略之七——高送转行情下的事件性投资机会` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-023` | `事件驱动策略之九——股权激励续篇` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-024` | `事件驱动策略之十一——事件驱动组合止损机制设计` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-025` | `事件驱动策略之十二——重要股东持股结构变化蕴含的信息分析` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-026` | `事件驱动策略之十三——定增事件投资——甄别市场，把握买点` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-027` | `现金流量市值比因子的极值效应` | `REPO_DELETE_RECHECK_READY` | `BOOKDIR_EXACT_PATH_CONFIRMED` | `MOVE_READY_NOT_DELETE` | 最终删除勾选（已入条目级清单） |
| `S-028` | `相关性选股策略——全市场选股方法改进` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-029` | `相关性选股策略——在房地产行业上的实证` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-030` | `相关性选股策略——在纺织服装行业上的实证` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-031` | `相关性选股策略——在公用事业行业上的实证以及选股因子权重的再讨论` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-032` | `相关性选股策略——在化学工业行业上的实证` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-033` | `相关性选股策略——在有色金属行业上的实证` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-034` | `行业内股票业绩弹性分析——在钢铁行业上的实证` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-035` | `行业内选股策略——钢铁行业` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-036` | `行业内选股策略——有色金属行业` | `REPO_PENDING_TICK` | `S_PENDING_EXACT_PATH` | `NOT_DELETE_READY` | 同上 |
| `S-037` | `选股因子研究系列（一）——动量反转效应研究` | `REPO_PENDING_TICK` | `SERIES_MANUAL_CONFIRMED` | `MOVE_READY_NOT_DELETE` | 最终删除勾选（已入条目级清单） |
| `S-038` | `选股因子研究系列（二）——因子模型的尾部相关性研究` | `REPO_PENDING_TICK` | `SERIES_MANUAL_CONFIRMED` | `MOVE_READY_NOT_DELETE` | 最终删除勾选（已入条目级清单） |
| `S-039` | `选股因子研究系列（三）——Kalman Filter模型在因子选择中的应用` | `REPO_PENDING_TICK` | `SERIES_MANUAL_CONFIRMED` | `MOVE_READY_NOT_DELETE` | 最终删除勾选（已入条目级清单） |
| `S-040` | `选股因子研究系列（四）——多因子选股模型的有效与失效` | `REPO_PENDING_TICK` | `SERIES_MANUAL_CONFIRMED` | `MOVE_READY_NOT_DELETE` | 最终删除勾选（已入条目级清单） |
| `S-041` | `选股因子研究系列（五）——寻找股价驱动新因子之净换手率` | `REPO_PENDING_TICK` | `SERIES_MANUAL_CONFIRMED` | `MOVE_READY_NOT_DELETE` | 最终删除勾选（已入条目级清单） |

## 当前批量结论

- 当前共形成：
  - `2` 条择时候选删除勾验行
  - `1` 条重复源保留行
  - `16` 条资产配置删除勾验行
  - `41` 条选股删除勾验行
- 也就是说，`research pdf` 这批当前已经不再缺“逐文件勾验骨架”。
- 其中本轮已额外推进：
  - `S-014`
  - `S-027`
  从“待找外部精确路径”收紧为“删除级别重核通过，但仍未到直接删除”。

## 主链外附加裁决

- `事件驱动策略之十——如何刻画股票热度以及寻找“潜在热门股”`
  - 当前保持：`KEEP_OUTSIDE_MAINCHAIN`
  - 原因：
    - 已确认属于 `62份赠品` 的有效研究条目
    - 但尚未进入稳定 `paper_id` 主链
    - 当前不应为了补一条额外条目而扰动现有删除勾验表编号

## 下一步只剩什么

- 仓库内侧：
  - 给每条 `REPO_PENDING_TICK / REPO_DELETE_RECHECK_READY` 补最终删除勾选
- 外部侧：
  - 把 `D:\Stock\cut_file\S\03_券商研报` 的精确文件路径逐条落下
  - 给 `BOOKDIR_EXACT_PATH_CONFIRMED` 这类已落到直接真值目录的条目补前后路径台账
  - 再补最终删除勾选
