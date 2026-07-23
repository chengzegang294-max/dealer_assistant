# Batch149 Formula Semantics To Batch1 Field Bridge v1

更新时间：2026-07-20

## 一、用途

- 这页把 `batch_149` 当前首批对象卡的输出语义，压到 `A股 P0 Batch1` 已冻结的：
  - `EventSummary`
  - `ExplanationPayload`
- 这页不是前端实现文档。
- 这页只做：
  - 让 `Batch1` 后续实现不再重造 mock 字段

## 二、上游来源

- 当前接完整 `6` 张核心对象卡：
  - `沪深涨跌停`
  - `打板资金`
  - `上榜资金`
  - `HYDB行业对比`
  - `ZSDB指数对比`
  - `启动点`
- 当前不接：
  - 花哨主图样式
  - 复杂画线参数
  - 终端专有图标与色彩语义

## 三、Batch1 已冻结接口

### 3.1 EventSummary

- 固定字段：
  - `eventId`
  - `title`
  - `subject`
  - `occurredAt`
  - `holdingRelation`
  - `processStatus`
  - `disclosureFlag`

### 3.2 ExplanationPayload

- 固定字段：
  - `eventId`
  - `title`
  - `subject`
  - `logic`
  - `impact`
  - `historyAnalogy`
  - `nextReviewPoint`

## 四、统一桥接规则

- `eventId`
  - 用规则化 id：
    - `market-limit-board-<date>`
    - `market-board-capital-<date>`
    - `market-top-list-capital-<date>`
- `title`
  - 必须写成一句事件标题
  - 不直接写公式名
- `subject`
  - 当前固定允许：
    - `全市场`
    - `全市场打板`
    - `全市场榜单资金`
- `occurredAt`
  - 用当次触发时间
- `holdingRelation`
  - 当前默认：
    - `其它`
  - 只有后续能稳定映射到持仓/关注对象时，才允许升到：
    - `持仓相关`
    - `关注相关`
- `processStatus`
  - 初始固定：
    - `pending`
  - 进入记录提交回显后，才允许被首页实现更新
- `disclosureFlag`
  - 当前固定：
    - `still_need_evidence`
  - 禁止把公式信号伪写成确定性投资建议

## 五、六张核心对象卡字段桥

| 对象卡 | EventSummary.title | EventSummary.subject | ExplanationPayload.logic | ExplanationPayload.impact | ExplanationPayload.historyAnalogy | ExplanationPayload.nextReviewPoint |
|---|---|---|---|---|---|---|
| `沪深涨跌停` | `涨停/连板热度出现异常变化` | `全市场` | 当日涨停家数、连板家数、跌停家数出现突变，说明热点情绪与风险偏好发生切换 | 用于解释今日事件流偏热、偏冷还是分化加剧 | 可与近几次题材情绪高点/退潮阶段做轻类比，不强制必填 | 下一次复查：收盘前涨停家数、连板高度、跌停扩散是否继续同向 |
| `打板资金` | `封板资金强弱发生变化` | `全市场打板` | 封板成功资金、封单额与封板失败资金的相对变化，说明打板承接与封板质量变化 | 用于解释热点为何强化、炸板为何增多、事件热度是否具备持续性 | 可选填：与上一轮活跃题材日做比较 | 下一次复查：封板成功资金是否继续放大，封板失败资金是否同步恶化 |
| `上榜资金` | `榜单资金出现异动` | `全市场榜单资金` | 上榜资金净额明显变化，说明有主动资金在榜单层面集中出现 | 用于解释某类事件是否具备资金背书，而非单纯价格波动 | 可选填：与近期榜单净流入/净流出强度做比较 | 下一次复查：次日榜单净额是否延续，同题材是否出现扩散 |
| `HYDB行业对比` | `所属行业强弱出现明显偏移` | `相关行业` | 行业指数走势与行业涨幅出现明显偏移，说明当前事件更可能处在行业顺风或逆风环境中 | 用于解释事件更像行业共振还是个股独立异动 | 可选填：与近期同类行业活跃/退潮阶段做比较 | 下一次复查：行业涨幅、行业方向与事件所在个股是否继续同向 |
| `ZSDB指数对比` | `指数环境强弱发生变化` | `全市场指数环境` | 指数涨幅与指数走势方向发生明显变化，说明当前事件所处的大盘环境正在顺风、转弱或逆风 | 用于解释事件为何更容易扩散、承接不足或逆势独立 | 可选填：与近期市场风险偏好阶段做比较 | 下一次复查：指数涨幅、指数方向与事件热度是否继续同向 |
| `启动点` | `个股出现启动候选信号` | `相关个股` | 个股出现启动买点或 MACD 启动信号，说明走势有转强候选，但仍需结合环境与事件背景复核 | 用于解释为什么当前事件值得跟踪、观察或准备进入记录 | 可选填：与近期同类启动后是否延续做轻类比 | 下一次复查：量价延续、环境是否顺风、信号是否失效 |

## 六、禁止照搬项

- 禁止把原公式名直接当首页事件标题。
- 禁止把多组原始数值全部塞进 `ExplanationPayload.logic`。
- 禁止在 `impact` 里直接写成买卖建议。
- 禁止在 `historyAnalogy` 里伪造历史胜率。
- 禁止把终端里的配色、箭头、火焰山、柱体样式搬成产品字段。

## 七、给 Batch1 的直接使用口径

- 首页 `今日事件流`
  - 只消费压缩后的事件标题与解释短文
- `SelectedEventSummaryBar`
  - 只显示：
    - `title`
    - `subject`
    - `occurredAt`
    - `holdingRelation`
    - `processStatus`
- `ExplanationCard`
  - 只显示：
    - `logic`
    - `impact`
    - `historyAnalogy`
    - `nextReviewPoint`
- `DecisionRecordForm`
  - 不直接消费原公式值
  - 只在对象卡下沉后消费解释结论

## 八、六卡最小闭环裁决

- 当前 `6` 张卡已经覆盖：
  - `市场热度`
  - `资金承接`
  - `资金背书`
  - `行业环境`
  - `指数环境`
  - `个股动作候选`
- 这已经足够支持 `Batch1` 做第一轮真实 mock。
- 后续若切回代码实现，应以这 `6` 张卡为上游唯一真值。

## 九、主负责人裁决

- 当前这张字段桥一旦冻结，就应作为：
  - `Batch1 mock 唯一真值`
- 下一手不再回头重开合同页。
- 下一手只允许：
  - 继续补对象卡
  - 或切回 `Batch1` 开写实现
