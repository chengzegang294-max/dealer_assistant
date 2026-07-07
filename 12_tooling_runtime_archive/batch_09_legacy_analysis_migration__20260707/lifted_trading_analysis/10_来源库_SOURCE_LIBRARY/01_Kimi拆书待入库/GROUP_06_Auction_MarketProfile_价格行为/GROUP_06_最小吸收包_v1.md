# GROUP_06 最小吸收包 v1

更新时间：2026-06-21

## 本次只解决什么

- 把 `GROUP_06_Auction_MarketProfile_价格行为` 从“大对象定义库”收成当前仓库可直接继续推进的最小吸收层。
- 本轮只产出三件事：
  - 最小对象表
  - 最小判定树
  - `N02` 标签映射草案
- 本轮不做：
  - 直接改 `N02 P0` 字段合同
  - 直接写新回测脚本
  - 直接宣称 A 股端已经实现

## 进入条件

- 已有统一定义文件：
  - `GROUP_06_market_profile_price_action_DEFINITIONS.md`
  - `GROUP_06_market_profile_price_action.md`
- 已有 `N02` 候选入口：
  - `..\GROUP_06_to_N02_对象候选清单_v1.md`
- 已有批次摘要说明哪些对象属于 `proxy_quantizable_now`：
  - `01_A2_cutpack_v2\BATCH_SUMMARY__A2__v2.md`

## 退出条件

- 写清楚首批只吸收哪些对象。
- 写清楚先后顺序和停点。
- 写清楚哪些对象仍留在 `future bucket / extra data`。

## 最小对象表

| 对象 | 最小输入 | 最小输出 | 当前角色 | 当前备注 |
|---|---|---|---|---|
| `Opening Type` | 前日区间/前日价值区、开盘价、开盘后分钟K线 | `open_type` | `DIAG_ONLY_CANDIDATE` | 最贴近 A 股集合竞价与开盘结构 |
| `Initial Balance` | session 首 30/60 分钟分钟K线 | `ib_high` `ib_low` `ib_range` `ib_mid` | `DIAG_ONLY_CANDIDATE` | 当前第一优先对象 |
| `POC` | 分钟K线成交量分布或价位分布 | `poc` | `DIAG_ONLY_CANDIDATE` | 比完整 `VA` 更轻，可单独先做 |
| `Value Area` | 分钟K线 + 价位分布近似 | `vah` `val` `poc` | `DIAG_ONLY_CANDIDATE` | 需要日内价位分布重建 |
| `Balance vs Imbalance` | 前日 `VAH/VAL`、当日价格、当日/前日范围 | `balance_state` | `DIAG_ONLY_CANDIDATE` | 更像解释层标签，不应先变硬门控 |
| `Day Type` | `IB`、日内总区间、收盘位置、可能的 profile shape 近似 | `day_type` | `CONDITIONAL_KEEP_CANDIDATE` | 工程复杂度高于 `IB/POC/VA` |

## 最小判定树

### Step 1：先判数据够不够

- 只有日线或小时线：
  - 停止在“来源吸收层”，不进入实现层。
- 有分钟级数据，但没有 session 边界：
  - 先只能做近似 `POC / VA`，不做严格 `IB / Opening Type`。
- 有分钟级数据 + session 边界：
  - 才进入首批实现候选。

### Step 2：先做开盘与首小时

- 第一优先：`Opening Type`
  - 目标不是复刻全部拍卖理论，而是先分：
    - `OPEN_WITHIN_VALUE`
    - `OPEN_OUTSIDE_VALUE`
    - `OPEN_OUTSIDE_RANGE`
- 第二优先：`Initial Balance`
  - 先只做首 `30/60` 分钟区间，不扩成完整 TPO 工程。

### Step 3：再做日内价格分布锚点

- 第三优先：`POC`
- 第四优先：`Value Area`
- 这一步只接受 `proxy` 近似，不要求逐笔 / DOM / Level2。

### Step 4：最后再做解释层

- 第五优先：`Balance vs Imbalance`
- 第六优先：`Day Type`
- 这两项当前只保留成标签候选，不应先变成硬交易门控。

## A 股适配口径

- `Opening Auction`
  - 对应 A 股 `9:15-9:25` 集合竞价结果。
- `Initial Balance`
  - 对应 A 股 `9:30-10:00` 或 `9:30-10:30` 的首段连续竞价区间。
- `POC / Value Area`
  - 当前只按分钟级近似重建，不假装已有逐笔与完整价位分布。
- `Day Type`
  - 先按 `Normal / Trend / Neutral / Nontrend` 粗分，不提前扩到完整 7 类自动化。

## N02 标签映射草案

| G06 对象 | N02 候选标签 | 当前层级 | 说明 |
|---|---|---|---|
| `Opening Type` | `n02_open_type` | `DIAG_ONLY_CANDIDATE` | 对接开盘环境，不直接进硬门控 |
| `Initial Balance` | `n02_ib_state` | `DIAG_ONLY_CANDIDATE` | 承接当前 `OR -> IB context` 最自然 |
| `POC` | `n02_poc_context` | `DIAG_ONLY_CANDIDATE` | 先做价格分布锚点 |
| `Value Area` | `n02_value_context` | `DIAG_ONLY_CANDIDATE` | 先做日内价值区解释层 |
| `Balance vs Imbalance` | `n02_balance_state` | `DIAG_ONLY_CANDIDATE` | 适合做状态解释，不先做门控 |
| `Day Type` | `n02_day_type` | `CONDITIONAL_KEEP_CANDIDATE` | 先保留为日结构解释标签 |

## 当前冻结区

- `TPO` 的精细字母矩阵实现：暂不做。
- `Single Prints / Tails / Excess` 的严格识别：需要更细粒度数据或人工补锚点。
- `DOM / Level2 / Order Book`：明确属于 `needs_extra_data`，不在本轮最小吸收范围。
- Brooks 价格行为的主观信号条目：继续留在定义层，不在本轮落成对象标签。

## 当前结论

- `GROUP_06` 已从“可重开”推进到“最小吸收包已成形”。
- 当前最稳顺序已经固定：
  - 先 `Opening Type + Initial Balance`
  - 再 `POC + Value Area`
  - 最后 `Balance vs Imbalance + Day Type`
- 本轮完成后，`GROUP_06` 的角色应表述为：
  - `N02 上游对象定义层 + A 股开盘结构解释层`
