# TK-R6 IB 回踩 / 拒绝 最小标签定义 v1

## 作用

- 作为 `TK-R6` 的第一份最小标签草案。
- 用于先把 `IB retest / rejection` 写成可审计的诊断标签，而不是直接写成策略规则。

## 适用对象

- 上游入口：
  - `TK-R6_IB回撤阻挡到TP3_后续对象定义入口_v1.md`
- 当前只服务于：
  - `IB 回撤阻挡 -> TP3 概率增强`
  这条结构补充对象

## 标签目标

- 先把当前价格行为分成 4 类最小状态：
  - `no_retest`
  - `retest_touch_only`
  - `retest_reject_weak`
  - `retest_reject_clear`

## 最小输入

- 方向：
  - `long / short`
- `IB` 区域：
  - 已有一个可引用的 `IB zone` 或 `IB price level`
- 回撤后的 K 线：
  - 至少能判断是否触碰、是否收回、是否留出拒绝痕迹

## 最小标签定义

### 1. `no_retest`

- 含义：
  - 主信号后价格没有明显回撤到 `IB` 附近
- 当前用途：
  - 作为对照组

### 2. `retest_touch_only`

- 含义：
  - 价格已回到 `IB` 附近
  - 但只看到了接触，没有看到明确“被拒绝/被阻挡”
- 当前用途：
  - 与 `retest_reject_*` 区分

### 3. `retest_reject_weak`

- 含义：
  - 价格回到 `IB` 附近后有初步拒绝迹象
  - 但拒绝力度不够稳定
- 最小可见迹象：
  - 有回收
  - 但实体不强
  - 或影线/收盘位置不够清晰

#### `reject_weak` 的最小降级条件

- 当前先不冻结点数、实体比例或连续 bars 数。
- 当前先冻结最小降级条件：
  - `inside_ib_present`
  - `partial_reclaim_only`
  - `rejection_hint_not_stable`

##### 1. `inside_ib_present`

- 含义：
  - 当前已经满足：
    - `candle_body_enters_ib`
    - 或 `candle_close_inside_ib`
- 当前角色：
  - 没有这一步，优先还是留在：
    - `retest_touch_only`

##### 2. `partial_reclaim_only`

- 含义：
  - 价格有一定回收
  - 但没有明确回到更支持原主信号的一侧
- 当前角色：
  - 是 `weak` 与 `clear` 的第一道分界

##### 3. `rejection_hint_not_stable`

- 含义：
  - 只能看到局部拒绝痕迹
  - 但还不够清晰、连续或干净
- 当前角色：
  - 用来解释为什么不升级成：
    - `retest_reject_clear`

## 当前保守裁决补充

- 当前更稳的最小写法是：
  - 先 `inside_ib`
  - 再出现 `partial_reclaim_only`
  - 并伴随 `rejection_hint_not_stable`
- 三者同时出现时，更优先记为：
  - `retest_reject_weak`
- 若只有 `inside_ib`，没有回收或拒绝痕迹：
  - 更优先记为：
    - `retest_touch_only`
- 若已经出现：
  - `close_back_to_signal_side`
  - 且 `visible_rejection_hint`
  则更优先升级为：
  - `retest_reject_clear`

### 4. `retest_reject_clear`

- 含义：
  - 价格回到 `IB` 附近后，出现较明确的“被阻挡/被拒绝”结构
- 最小可见迹象：
  - 触碰后收回
  - 且收盘方向支持原主信号
  - 且至少有一处明显的拒绝痕迹

#### `reject_clear` 的最少价格行为特征

- 当前先不冻结点数、ATR、实体比例。
- 当前先冻结最小组合特征：
  - `inside_ib_confirmed`
  - `close_back_to_signal_side`
  - `visible_rejection_hint`

##### 1. `inside_ib_confirmed`

- 含义：
  - 当前 K 线已至少达到：
    - `candle_body_enters_ib`
    - 或 `candle_close_inside_ib`
- 当前角色：
  - 没有这一步，不优先记为 `reject_clear`

##### 2. `close_back_to_signal_side`

- 含义：
  - 触达 `IB` 后，收盘重新回到更支持原主信号的一侧
- 当前角色：
  - 是“不是单纯触碰”的最小确认

###### `close_back_to_signal_side` 的更细 candle 提示

- 当前先不冻结绝对点数、实体比例或连续 bars 数。
- 当前先冻结 3 类最小 candle 提示：
  - `close_reclaims_ib_edge`
  - `body_recovers_signal_side`
  - `close_holds_beyond_mid_hint`

####### 1. `close_reclaims_ib_edge`

- 含义：
  - K 线先进入或触达 `IB`
  - 随后收盘重新回到更支持原主信号的一侧边界外
- 当前角色：
  - 是 `close_back_to_signal_side` 的最小可见版本

####### 2. `body_recovers_signal_side`

- 含义：
  - 不只是影线回收
  - 至少实体也明显回到更支持原主信号的一侧
- 当前角色：
  - 用来区分“只有尾巴收回”与“真实收盘回到信号侧”

####### 3. `close_holds_beyond_mid_hint`

- 含义：
  - 若当前还能看到收盘不只回到边缘，而是至少越过 `IB` 中线提示位
  - 则更支持“已真正回到 signal side”
- 当前角色：
  - 作为 `reject_clear` 的增强提示
  - 当前不是必需条件

##### 3. `visible_rejection_hint`

- 含义：
  - 当前至少还能看到一处清晰拒绝痕迹，例如：
    - 明显拒绝影线
    - 明显收回实体
    - 强势 reclaim 收盘
- 当前角色：
  - 用于把 `reject_clear` 与 `reject_weak` 区分开

## 当前保守裁决

- 当前更稳的最小写法是：
  - 先 `inside_ib`
  - 再 `close_back_to_signal_side`
  - 再配合 `visible_rejection_hint`
- 三者同时出现时，才更优先记为：
  - `retest_reject_clear`
- 若只有其中 `1-2` 项：
  - 仍更保守地留在：
    - `retest_touch_only`
    - 或 `retest_reject_weak`
- 当前对 `close_back_to_signal_side` 的更细保守写法是：
  - 先有 `close_reclaims_ib_edge`
  - 若再出现 `body_recovers_signal_side`
    - 则更像清晰回到 signal side
  - 若还能看到 `close_holds_beyond_mid_hint`
    - 则更支持升级到 `retest_reject_clear`

## 最小辅助标签

- `ib_retest_present`
  - `0 / 1`
- `ib_retest_quality`
  - `none / touch_only / weak / clear`
- `ib_rejection_candle_hint`
  - `none / wick_reject / close_back / strong_reclaim`

## 当前保守判法

- 现在先不冻结数值阈值。
- 当前只先冻结语义顺序：
  - 先判断有没有回到 `IB`
  - 再判断有没有拒绝
  - 再区分弱拒绝和清晰拒绝

## 当前不做的事

- 不直接写：
  - `clear reject = 必到 TP3`
- 不直接写：
  - `weak reject = 无效`
- 不直接把标签升级成：
  - entry gate
  - 出场规则
  - 胜率结论

## 下一步

- 若继续推进：
  - 再补 `visible_rejection_hint` 的最小示例集合
  - 再补 `wick_reject / strong_reclaim` 与 `reject_clear` 的更细映射
- 当前已补：
  - `TK-R6_IB附近_最小距离口径_v1.md`

## `visible_rejection_hint` 最小示例集合 v1

### 目标

- 给 `retest_reject_clear` 提供最小可审计“可见拒绝痕迹”集合。
- 当前不冻结：
  - 数值阈值
  - 连续 bars 数
  - ATR 倍数

### 示例族 1：`wick_reject`

- long：
  - 已 `inside_ib`
  - 触达/打进 `IB` 后出现下影线拒绝
  - 且收盘相对更支持原 `long` 主信号（配合 `close_back_to_signal_side`）
- short：
  - 已 `inside_ib`
  - 触达/打进 `IB` 后出现上影线拒绝
  - 且收盘相对更支持原 `short` 主信号（配合 `close_back_to_signal_side`）

### 示例族 2：`strong_reclaim`

- long：
  - 已 `inside_ib`
  - 收盘不仅回到 `IB` 边缘外，还更像“强势回到 signal side”
  - 常见外观：
    - 实体明显回收（不是只有影线回收）
    - 形态更接近“回收后继续延伸”的干净结构
- short：
  - 同理，方向镜像

### 示例族 3：`reject_clear` 的最小组合提示

- long：
  - `inside_ib_confirmed`
  - `close_back_to_signal_side`
  - `visible_rejection_hint in {wick_reject, strong_reclaim}`
- short：
  - 同理，方向镜像

### `ib_rejection_candle_hint` 的保守映射 v1

- `none`
  - `retest_touch_only`
- `wick_reject`
  - `retest_reject_weak` 或 `retest_reject_clear`（取决于是否同时满足 `close_back_to_signal_side`）
- `close_back`
  - 满足 `close_reclaims_ib_edge`，但 `visible_rejection_hint` 不清晰时
- `strong_reclaim`
  - 更优先支持 `retest_reject_clear`
