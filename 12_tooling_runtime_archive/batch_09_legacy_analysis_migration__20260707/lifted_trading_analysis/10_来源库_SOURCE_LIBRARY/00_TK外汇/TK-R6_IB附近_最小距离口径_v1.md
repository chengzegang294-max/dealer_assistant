# TK-R6 IB 附近 最小距离口径 v1

## 作用

- 作为 `TK-R6` 的第二份最小条件草案。
- 用于先回答：
  - 什么叫“回到 `IB` 附近”
  - 以便后续 `retest_touch_only / retest_reject_*` 有统一口径

## 适用对象

- 上游入口：
  - `TK-R6_IB回撤阻挡到TP3_后续对象定义入口_v1.md`
- 配套标签草案：
  - `TK-R6_IB_retest_rejection_最小标签定义_v1.md`

## 当前目标

- 先把“接近 `IB`”写成最小三档，而不是一上来冻结复杂数值系统。
- 当前最小三档：
  - `far_from_ib`
  - `near_ib`
  - `inside_ib`

## 最小距离口径

### 1. `far_from_ib`

- 含义：
  - 当前回撤还没有真正回到 `IB` 观察区
- 当前作用：
  - 不计入 `IB retest`

### 2. `near_ib`

- 含义：
  - 当前价格已经回到 `IB` 附近观察带
  - 但还不能直接认定为“已经打进 `IB` 核心区”
- 当前作用：
  - 可记为候选 retest 观察状态

### 3. `inside_ib`

- 含义：
  - 当前价格已经进入 `IB` 核心区或贴近 `IB level`
- 当前作用：
  - 才更适合作为正式 `IB retest` 的最小前提

## `inside_ib` 的最小 candle 触达定义

- 当前先不冻结精确 pip / ATR 数值。
- 当前先冻结最小可见触达语义：
  - `candle_touch_ib_edge`
  - `candle_body_enters_ib`
  - `candle_close_inside_ib`

### 1. `candle_touch_ib_edge`

- 含义：
  - 当前 K 线至少有高低点之一触碰到 `IB` 边界
- 当前角色：
  - 只能算最弱触达
  - 还不够单独定义为 `inside_ib`

### 2. `candle_body_enters_ib`

- 含义：
  - 当前 K 线实体已有一部分进入 `IB` 核心区
- 当前角色：
  - 更适合作为 `inside_ib` 的最低可接受触达
  - 比单纯影线触碰更强

### 3. `candle_close_inside_ib`

- 含义：
  - 当前 K 线收盘已落入 `IB` 核心区
- 当前角色：
  - 是更强的 `inside_ib` 触达
  - 也更适合作为后续判断 `touch_only / reject_*` 的起点

## 当前保守裁决

- 当前更稳的最小写法是：
  - `candle_touch_ib_edge` 只算 `near_ib` 或最弱触达提示
  - `candle_body_enters_ib` 起，才更像真正 `inside_ib`
  - `candle_close_inside_ib` 是更强 `inside_ib`
- 因而当前不建议把：
  - 单根影线碰边
  直接写成正式 `inside_ib retest`

## 当前保守定义方式

- 现在先不冻结精确 pip 数、百分比或 ATR 倍数。
- 当前先冻结判定顺序：
  - 先有一个可引用的 `IB zone / IB level`
  - 再判断当前价格相对该区是：
    - `far`
    - `near`
    - `inside`
- 当前更稳的保守写法是：
  - `near_ib` 只代表“接近观察带”
  - `inside_ib` 才更像真正的 retest 候选

## 与 TK-R6 标签的关系

- `no_retest`
  - 默认对应：
    - `far_from_ib`
- `retest_touch_only`
  - 更优先对应：
    - `inside_ib`
    - 但尚未出现明确 rejection
- `retest_reject_weak / clear`
  - 更优先要求：
    - 先 `inside_ib`
    - 再出现不同强度的拒绝迹象

## `inside_ib -> label` 的更细映射

- 当前先不冻结数值化 candle 比例。
- 当前先冻结保守映射顺序：
  - `inside_ib + no clear reclaim/reject`
    - 更优先记为 `retest_touch_only`
  - `inside_ib + partial reclaim or weak reject hint`
    - 更优先记为 `retest_reject_weak`
  - `inside_ib + close_back_to_signal_side + visible_rejection_hint`
    - 更优先记为 `retest_reject_clear`

### 1. `inside_ib -> retest_touch_only`

- 更常见于：
  - `candle_body_enters_ib`
  - 或 `candle_close_inside_ib`
  - 但没有清晰收回
  - 也没有明显拒绝痕迹
- 当前角色：
  - 代表“已触达，但没有足够 rejection 证据”

### 2. `inside_ib -> retest_reject_weak`

- 更常见于：
  - 已 `inside_ib`
  - 有一定回收
  - 但回收力度不够稳定
  - 或只有局部影线拒绝/实体收回，仍不够干净
- 当前角色：
  - 代表“已有 rejection 倾向，但不宜写满”

### 3. `inside_ib -> retest_reject_clear`

- 更常见于：
  - 已 `inside_ib`
  - 且 `close_back_to_signal_side`
  - 且存在 `visible_rejection_hint`
- 当前角色：
  - 代表“已满足更强 rejection 结构”

## 当前保守裁决补充

- 当前不把：
  - `inside_ib`
  直接等同于：
  - `reject_clear`
- 当前更稳的最小写法是：
  - `inside_ib` 只是 retest 前提
  - `touch_only / reject_weak / reject_clear` 仍要看回收与拒绝强度

## 当前不做的事

- 不直接把：
  - `near_ib`
  写成已经完成 retest
- 不直接冻结：
  - `多少 pip`
  - `多少百分比`
  - `多少 ATR`
- 不直接把距离口径升级成：
  - entry gate
  - 胜率结论

## 下一步

- 若继续推进：
  - 再补 `reject_weak` 的最小降级条件
  - 再补 `close_back_to_signal_side` 的更细 candle 提示
