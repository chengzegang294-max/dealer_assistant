# REOPEN_B9_N02_SESSION_OR_P0 真实字段输出路径草案 v1

## 目标

- 把 `REOPEN_B9_N02_SESSION_OR_P0` 从“样本证据”推进到“真实字段输出路径已定义”。
- 先固定第一版真实产物应放哪里、叫什么、各文件承担什么角色。
- 这一步仍然不写实现代码，只收口路径合同，避免后面真实落盘时再次乱命名。

## 不变量

- 只覆盖 `N02 P0` 的 `12` 个字段。
- 不提前混入：
  - `IB`
  - `acceptance`
  - `ib_failed_breakout_event`
  - `session_bias`
- 不把样本文件误记成真实运行产物。
- 第一版仍然是：
  - `diagnostic/context layer`
  - 不是策略门控
  - 不是实盘执行产物

## 第一版真实产物建议目录

- 建议以 `12_工具运行时_TOOLING_RUNTIME` 作为未来真实输出根目录。
- 第一版建议路径：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n02_session_or_p0_v1\`

## 第一版真实产物清单

### 1. 主产物

- `n02_p0_fields_runtime_v1.csv`
- 角色：
  - bar-level 真实字段输出
- 说明：
  - 每一行对应一个 bar
  - 用于后续和 entry/trade 级别输出做 join

### 2. 表头冻结文件

- `n02_p0_fields_runtime_header_v1.txt`
- 角色：
  - 冻结真实输出的当前表头
- 说明：
  - 若未来升级为 `v2`，旧版 header 不覆盖

### 3. 运行说明

- `n02_p0_runtime_notes_v1.md`
- 角色：
  - 记录 session 参数、OR 窗口、字段空值口径、当前未实现内容
- 说明：
  - 这里写“运行口径”
  - 不重复大段字段定义

### 4. 缺口与审计说明

- `n02_p0_runtime_gaps_v1.md`
- 角色：
  - 记录当前没做什么，以及为什么没做
- 说明：
  - 要明确：
    - `IB` 未接入
    - `close` vs `wick` 未拆
    - `width_error_day` 阈值仍需运行后核对

### 5. 追加协议

- `n02_p0_runtime_append_protocol_v1.md`
- 角色：
  - 约束第一批真实数据行怎样从占位状态过渡到真实追加
- 说明：
  - 明确是否删除占位样本行
  - 明确何时需要起 `v2`

## 文件命名规则

- 统一小写下划线风格，不混中文文件名到运行产物目录。
- 固定前缀：
  - `n02_p0_`
- 版本号固定放文件名末尾：
  - `_v1`
- 不在文件名里携带：
  - `date_tag`
  - `symbol`
  - `timeframe`
- 这些运行维度应体现在文件内容列里，而不是拆成大量碎文件。

## 真实输出表头

- 运行时主键列：
  - `symbol`
  - `timeframe`
  - `bar_time`
- `N02 P0` 字段列：
  - `session_id`
  - `session_timezone`
  - `opening_range_window_minutes`
  - `opening_range_high`
  - `opening_range_low`
  - `opening_range_mid`
  - `opening_range_width`
  - `opening_range_width_pct_open`
  - `session_open_price`
  - `opening_range_defined`
  - `first_break_direction`
  - `width_error_day`

## 产物职责分层

- `sample/header/notes`
  - 现在已经在来源库里落地
  - 用于合同演示和表头冻结
- `runtime csv/header/notes/gaps/append_protocol`
  - 下一步进入工具运行时目录
  - 用于真实脚本输出与审计

## 第一版验收口径

- 真实输出目录已固定，后续不再来回改名。
- 主 CSV 表头必须和当前样本表头一致。
- 运行说明必须写清：
  - 默认 `session_id`
  - 默认 `session_timezone`
  - 默认 `opening_range_window_minutes`
- 缺口文件必须写清：
  - 还未做 `IB`
  - 还未做 `target_trigger_source`
  - 还未做 `close` vs `wick`

## 当前不做

- 不拆 `symbol` 单文件输出
- 不拆 `timeframe` 单文件输出
- 不加 `trade_id`
- 不加 `entry_id`
- 不加 `signal_id`
- 不加 `or_break_high / or_break_low`
- 不加任何 `IB` 字段

## 下一步

- 按本路径草案，把 `REOPEN_B9_N02_SESSION_OR_P0` 的下一阶段定义为：
  - 真实字段输出文件路径已固定
  - 运行时目录空壳已创建
  - 占位样本行与追加协议已落地
  - 后续接入脚本或运行链路时，先处理占位行，再往该目录追加真实产物
