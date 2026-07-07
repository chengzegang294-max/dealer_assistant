# GROUP_06 -> N02 对象候选清单 v1

## 目的

- 把 `GROUP_06_Auction_MarketProfile_价格行为` 中最贴近当前仓库的对象，正式接到 `N02` 后续候选层。
- 当前只做：
  - 对象候选定义
  - 输入/输出口径
  - 当前角色裁决
- 当前不做：
  - 直接写入现有 `N02 P0` 字段合同
  - 直接宣称已真实实现

## 候选对象

### G6-N02-O1: Initial Balance

- 来源：
  - `GROUP_06_market_profile_price_action_DEFINITIONS.md`
- 最小输入：
  - 分钟级或至少可重建 session 首小时区间的 OHLCV
  - `session_id`
  - `session_timezone`
- 最小输出：
  - `ib_high`
  - `ib_low`
  - `ib_range`
  - `ib_mid`
- 当前价值：
  - 是 `N02` 从 OR 扩展到 `IB context` 的最自然下一步
- 当前角色：
  - `可重开（N02 后续对象候选第一优先）`
  - 已新增更明确入口：
    - `..\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\REOPEN_B9_N02_IB_后续对象定义入口_v1.md`

### G6-N02-O2: Value Area

- 来源：
  - `GROUP_06_market_profile_price_action_DEFINITIONS.md`
- 最小输入：
  - 当日价格分布
  - TPO 或成交量分布
- 最小输出：
  - `vah`
  - `val`
  - `poc`
- 当前价值：
  - 可作为 session/日内结构环境锚点
- 当前角色：
  - `可重开（但数据要求高于 IB）`

### G6-N02-O3: POC

- 来源：
  - `GROUP_06_market_profile_price_action_DEFINITIONS.md`
- 最小输入：
  - 价格层级分布
- 最小输出：
  - `poc`
- 当前价值：
  - 比完整 Value Area 更轻，适合先作为对象化候选
- 当前角色：
  - `可重开（与 VA 配套）`

### G6-N02-O4: Balance vs Imbalance

- 来源：
  - `GROUP_06_market_profile_price_action_DEFINITIONS.md`
- 最小输入：
  - 当前价格
  - 前日 `VAH/VAL`
  - 当日/前日范围宽度
- 最小输出：
  - `balance_state`
    - `BALANCE`
    - `IMBALANCE_UP`
    - `IMBALANCE_DOWN`
    - `TRANSITION`
- 当前价值：
  - 适合做 session/auction context 的解释层
- 当前角色：
  - `future bucket（先定义保留）`

### G6-N02-O5: Day Type

- 来源：
  - `GROUP_06_market_profile_price_action_DEFINITIONS.md`
- 最小输入：
  - 当日 `IB`
  - 收盘位置
  - 当日总区间
  - 可能还需要 profile shape
- 最小输出：
  - `day_type`
    - `NORMAL_DAY`
    - `NORMAL_VARIATION`
    - `TREND_DAY`
    - `DOUBLE_DISTRIBUTION_TREND`
    - `NONTREND_DAY`
    - `NEUTRAL_DAY`
    - `NEUTRAL_EXTREME`
- 当前价值：
  - 对 `N02` 的日内环境解释有价值
  - 但工程复杂度高于 `IB`
- 当前角色：
  - `future bucket（先定义保留）`

## 当前排序

- 第一优先：
  - `G6-N02-O1 = Initial Balance`
- 第二优先：
  - `G6-N02-O2 = Value Area`
  - `G6-N02-O3 = POC`
- 第三优先：
  - `G6-N02-O4 = Balance vs Imbalance`
  - `G6-N02-O5 = Day Type`

## 当前原则

- 先对象化，再字段化。
- 先做 `IB`，不要一口气把 `VA/POC/Day Type` 全接进 `N02 P0`。
- `IB` 当前已从“候选清单”推进到“后续对象定义入口”，但仍不是当前 `N02 P0` 字段。
- 当前仍以：
  - `N02 sessions / open-range / time-window context`
  为主线。
- `IB / VA / POC / Day Type` 属于 `N02` 的后续扩展层，不反向污染当前 P0 合约。
