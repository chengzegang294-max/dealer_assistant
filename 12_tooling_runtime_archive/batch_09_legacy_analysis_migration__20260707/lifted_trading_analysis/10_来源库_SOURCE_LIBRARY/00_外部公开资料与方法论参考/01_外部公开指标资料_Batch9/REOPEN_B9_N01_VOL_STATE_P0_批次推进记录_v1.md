# REOPEN_B9_N01_VOL_STATE_P0 批次推进记录 v1

## 作用

- 这份文档专门记录 `Batch9` 第二项重开是怎样一步步从“来源收集”推进到“可实施”的。
- 它不是字段定义文档，也不是运行说明，而是给主线回看时用的推进索引。

## 推进链路

### 第 1 步：类型裁决

- 在 `Batch9` 开题阶段，先把外部指标类型拆成：
  - `N01`
  - `N02`
  - `N03`
  - `N04/N05/N06`
- 其中 `N01 vol regime / squeeze-shock / realized vol` 被裁定为立即收集类型。

### 第 2 步：公开来源收集

- 已收：
  - `TTM_Squeeze__Alorse.pine`
  - `TTM-Squeeze-Pro__vijankush.pine`
  - `TTM_Squeeze_Pro__TradingView_page_excerpt.md`
  - `AG_Pro_ATR_Compression_Map__page_excerpt.md`
  - `ATR_Regime_Study__CHE__page_excerpt.md`
  - `Volatility_Regimes__GainzAlgo__page_excerpt.md`
- 结论：
  - `N01` 已具备最小字段合同所需的主要证据，但仍未收集完全。

### 第 3 步：字段合同化

- 已形成：
  - `N01_字段草案_v1.md`
  - `N01_P0_字段落盘草案_v1.md`
  - `Batch9_P0_统一字段_CSV草案_v1.csv`
- 结论：
  - `N01` 已具备最小 `P0` 字段合同。

### 第 4 步：批次收口与四分流

- 已新增：
  - `Batch9_批次收口与四分流_v1.md`
- 裁决：
  - `REOPEN_B9_N01_VOL_STATE_P0`
  - 进入 Batch9 首批量化重开第二优先项

### 第 5 步：最小实施草案

- 已新增：
  - `REOPEN_B9_N01_VOL_STATE_P0_最小实施草案_v1.md`
- 固定内容：
  - 第一版只做 `8` 个 `N01 P0` 字段
  - 不混入 `compression_state / vol_regime_code / breakout`
  - 不做硬门控

### 第 6 步：第一版输出证据

- 已新增：
  - `n01_p0_field_sample_v1.csv`
  - `n01_p0_field_header_v1.txt`
  - `n01_p0_contract_notes_v1.md`
- 结论：
  - 已从“只有草案”推进到“已有表头、空值、默认值、枚举样本证据”。

### 第 7 步：真实输出路径草案

- 已新增：
  - `REOPEN_B9_N01_VOL_STATE_P0_真实字段输出路径草案_v1.md`
- 结论：
  - 下一阶段真实运行产物应落到哪里、叫什么、各自承担什么角色，已经固定。

### 第 8 步：工具运行时空壳落地

- 已新增目录：
  - `12_工具运行时_TOOLING_RUNTIME\Batch9_reopen_n01_vol_state_p0_v1\`
- 已新增：
  - `n01_p0_fields_runtime_v1.csv`
  - `n01_p0_fields_runtime_header_v1.txt`
  - `n01_p0_runtime_notes_v1.md`
  - `n01_p0_runtime_gaps_v1.md`
  - `n01_p0_runtime_append_protocol_v1.md`
- 结论：
  - `REOPEN_B9_N01_VOL_STATE_P0` 已正式跨过来源库样本证据阶段，进入工具运行时阶段。

### 第 9 步：params template + append stub + dry-run

- 已新增：
  - `n01_p0_runtime_params_template_v1.json`
  - `n01_p0_runtime_append_stub_v1.py`
- 已验证：
  - 默认 `dry-run` 会读取 params
  - 会校验运行时 CSV 表头
  - 会清理 placeholder 后在内存中追加 `1` 条示例行
  - 不会写回 CSV
- 当前结果：
  - `REOPEN_B9_N01_VOL_STATE_P0` 已具备参数模板与追加脚本 stub
  - 并已完成一次可复现 dry-run 验证

### 第 10 步：stub 的 persist 示例行验证

- 已验证：
  - 可选 `--persist` 会先清理 placeholder 与旧示例行，再只保留 `1` 条示例行写回
- 当前结果：
  - `n01_p0_fields_runtime_v1.csv` 里的 placeholder 已被示例行替换
  - 但这条示例行仍不是“真实 runtime 数据”

### 第 11 步：关键参数从占位说明推进到冻结口径

- 已推进：
  - `atr_baseline_length = 50`
    - 已从 `stub_only_default` 升级为 `source_excerpt_or_open_source`
    - 依据：`Volatility_Regimes__GainzAlgo__page_excerpt.md` 中明确写到 baseline ATR 默认 `50 bars`
  - `atr_percentile_window = 252`
    - 已从 `stub_only_default` 升级为 `project_contract_default`
    - 依据：`ATR_Regime_Study__CHE__page_excerpt.md` 明确需要 rolling window，但未冻结唯一默认长度；因此 Batch9 v1 先把 `252` 冻结成比较窗口
- 当前结果：
  - `N01` 的关键参数不再都停留在工程占位层
  - 已区分“来源页可支撑参数”与“Batch9 v1 冻结参数”

### 第 12 步：ATR 核心输入长度补到来源页支撑

- 已推进：
  - `atr_length = 14`
    - 已从 `project_contract_default` 升级为 `source_excerpt_or_open_source`
    - 依据：`Volatility_Regimes__GainzAlgo__page_excerpt.md` 中明确写到 `ATR = SMA(True Range, default 14)`
- 当前结果：
  - `atr_length / atr_baseline_length` 现在都已有来源页支撑
  - `N01` 的 ATR 参数骨架更接近可审计实现口径

### 第 13 步：真实接入前 ATR 计算验收清单落地

- 已新增：
  - `n01_p0_runtime_atr_calculation_checklist_v1.md`
- 当前作用：
  - 在第一份真实 runtime 数据接入前，固定 ATR / baseline / percentile / squeeze 的最小验收顺序
- 当前结果：
  - `N01` 已不只是“参数冻结”
  - 还具备了真实接入前的固定 checklist

### 第 14 步：真实数据接入前最小输入映射草案

- 已新增：
  - `n01_p0_real_input_mapping_draft_v1.md`
- 当前作用：
  - 固定 `OHLC + ATR 参数骨架` 如何映射到当前 N01 P0 输出字段
- 当前结果：
  - `N01` 已具备真实接入前的输入映射草案
  - 后续第一份真实数据可以直接按草案做 proof-of-mapping

## 当前状态

- 当前角色：`in_progress`
- 当前准确描述：
  - 已完成类型裁决
  - 已完成来源收集
  - 已完成字段合同化
  - 已完成第一版样本证据
  - 已完成真实输出路径草案
  - 已完成工具运行时空壳
  - 已完成 params template 与 append stub
  - 已完成 dry-run 可复现验证
  - 已完成 persist 示例行验证
  - 已完成关键参数冻结口径升级
  - 已完成 ATR 核心输入长度来源绑定升级
  - 已完成真实接入前 ATR 计算验收清单
  - 已完成真实数据接入前最小输入映射草案
  - 已完成第二品种真实 runtime append 证据（`XAUUSD H1`）
  - 已把 runtime 样本从单品种推进到最小跨品种覆盖（`EURUSD H1 + XAUUSD H1`）
  - 已完成第二周期真实 runtime append 证据（`EURUSD M15 + XAUUSD M15`）
  - 已把 runtime 样本推进到最小跨品种 + 跨周期覆盖（`EURUSD/XAUUSD` × `H1/M15`）
  - 已完成第三周期真实 runtime append 证据（`EURUSD H4 + XAUUSD H4`）
  - 已完成原油类新资产类别真实 runtime append 证据（`XBRUSD H1 + XBRUSD H4`）
  - 已完成股票类新资产类别真实 runtime append 证据（`AAPL.NAS H1 + AAPL.NAS H4`）
  - 已完成指数类新资产类别真实 runtime append 证据（`USTEC H1 + USTEC H4`）
  - 已完成指数分支扩样真实 runtime append 证据（`US500 H1/H4`、`DE40 H1/H4`）
  - 已完成亚洲指数分支真实 runtime append 证据（`JP225 H1/H4`）
  - 已完成港股指数分支真实 runtime append 证据（`HK50 H1/H4`）
  - 已完成 `squeeze` 首批跨变体审计证据（`tier!=off` 对比 `mid-only`，20 组样本）
  - 已完成 `compression_quality_score` 首批跨变体审计与 `range_score` 去退化修正（20 组样本）
  - 已完成 `compression_quality_score` 结构级源码等价审计（参数/权重/阈值骨架已对齐 AG Pro）
  - 已完成 `compression_quality_score` 核心计算段细化审计（四项子评分逐项拆成“当前实现 / 来源语义 / 已锁定不等价项”）
  - 已完成 `compression_state` 影子分箱审计（`62/80` 阈值，20 组样本）
  - 已完成 `compression_state` 不等价项清单固化（`70` 仍是影子切点，`noise/containment confirm` 与 `strictMode` 仍待绑定）
  - 已补 `strictMode` / `Action Engine` 的新增来源边界：已确认 `strictMode` 的作用方向是“收紧 score gates”，且 `Action Engine` 存在 `Watch Edge / Monitor Mature / Track Compression / Build Context` 建议层分支
  - 已补公开页正文边界：`strictMode` 还伴随 `stricter filtering + wick/close-overlap sensitivity`，且存在 `Compression Mature / Compression State Change` 告警语义
  - 已完成 `strictMode` 的首版优先核对清单：若后续真接代码，优先核对 `noiseScore(wick)`、`containment/close-overlap`、`compression_active/Mature gating`
  - 已补源码结构层级边界：`Pocket detection` 在 `Lines 201-300`，`Action Engine + Event Labels` 在 `Lines 426-540`，因此 `nearEdge / releaseUp / releaseDown` 更像位置事件后处理分支，不应先并入核心评分
  - 已补 `Action Engine` 条件优先级边界：`releaseUp/releaseDown` 优先于 `isMature and nearEdge`，而 `nearEdge` 仅出现在 `Mature` 分支
  - 已补 `State Change` 与 `release` 的边界：`Compression State Change` 是独立告警语义，因此 `releaseUp/releaseDown` 更像状态后的事件标签，不应直接等同通用 state change 或 breakout 信号
  - 已补 Alerts 层边界：公开页明确暴露 `Compression Active / Mature / State Change`，但没有把 `Review Upside / Review Downside` 作为 alerts；因此 `strictMode` 更优先怀疑落在 `active/mature gating`，而不是 Action Engine 文案层
  - 已补展示层边界：公开页还直接展示 `active compression zone`、mini panel 的 `active state` 与 `compression window length`，因此 `active pocket / active state` 属于主状态层 first-class 输出，`release` 更像后处理标签
  - 已补 resolved 边界：更新日志单独提到 `resolved compression areas`，因此 `releaseUp/releaseDown` 更值得优先怀疑与 resolved/exit 事件相关，而不只是任意 state change
  - 已补 archive 边界：`archivePockets / archiveCount` 说明 resolved 更可能属于 pocket/归档展示链路，`release` 更像 active pocket 结束后的事件解释层
  - 已补 preview 边界：更新日志明确写出 preview labels 可在非 active 时继续显示，且不能视为 active confirmation，因此展示标签层与 active 状态层必须分开
  - 已补参数面板边界：`strictMode` 位于 `Core Engine`，而 `showPocket / archivePockets / projectPocketBars` 位于 `Compression Pocket Visuals`，因此 `strictMode` 更像核心资格/过滤层输入
  - 已补总述边界：公开页把 `display controls` 与 `advanced options` 分开描述，因此当前没有证据表明 `strictMode` 与 labels/panel/theme 共用显示链路
  - 已补 `strictMode` 参数语义：`more selective compression pockets` 再结合 `cleaner, more contained compression conditions` 与 `matureThreshold -> noise and containment confirm`，使其更值得优先怀疑会前移到 contained pocket / pocket qualify，而不只是 active/mature 后置 gating
  - 已把 `strictMode` 的 first landing 再收窄一层：当前更优先怀疑先收紧 `close-overlap / pocket qualify`，再影响 `contained pocket`，最后才传导到 `active/Mature gating`
  - 已把这层关系再拆细：原始页面把 `local overlap behavior` 放在 `Noise evaluation`，把 `Structural containment` 单列为后一项；因此当前更优先怀疑 `close-overlap` 是前置敏感度子门，`contained pocket` 是其筛选后的结构结果
  - 已补 `Key Inputs` 边界：公开页写的是 `stricter filtering + additional sensitivity controls for ... close-overlap behavior`；因此当前更优先把 `close-overlap` 视为可调 sensitivity input，而不是 `pocket qualify` 条件名本体
  - 已把这层口径再收紧：当前不直接写成 `strictMode == close-overlap sensitivity`；更保守的解释是二者同属 `advanced options`，其中 `strictMode` 更像总括 filtering/gating，`close-overlap behavior` 更像局部 sensitivity control
  - 已补句式结构证据：`stricter filtering and additional sensitivity controls ...` 更像两类并列能力，而不是同一个旋钮的重述；因此当前更优先怀疑 `strictMode` 与 `close-overlap sensitivity` 会并列存在，并可能共同进入 `pocket qualify`
  - 已再细分一层职责：当前更优先把 `close-overlap` 视为 feature-level sensitivity，把 `strictMode` 视为 policy-level gating / qualify strictness；两者不是互相替代，更像共同汇入 `shared pocket qualify`
  - 已完成 `strictMode v3` 多 AI 批次收口：
    - 多数票型当前收在：
      - `Q1 = A = threshold shift`
      - `Q2 = C = score formula / weights rewrite` 最不优先
      - `Q3 = A = pocket/state qualify strictness`
    - 当前 durable 口径因此从：
      - `threshold shift`
      - vs `additional qualify conditions`
      再压窄一层为：
      - `threshold shift / tighter score gates` 更优先
      - `additional qualify conditions` 继续保留为次优残余可能
      - `score formula / weights rewrite` 继续最不优先
    - 当前仍不写满的部分：
      - 具体抬的是哪个 threshold
      - 是否同时叠加 qualify 条件
      - `delta` 数值与分层方式
  - 已并入 `strictMode_kimi_followup` 的 v1 回帖：
    - `VOTE: Q1=B; Q2=B; Q3=C`
    - 外部回帖继续支持：
      - `strictMode != close-overlap sensitivity`
      - `close-overlap sensitivity + strictMode broader gating -> pocket qualify -> contained pocket -> Mature`
      - `strictMode` 不应先锁死为 `Mature` only
    - 外部回帖同时继续保留缺口：
      - `strictMode` 的具体实现方式仍不明
      - `close-overlap sensitivity` 的注入位点仍不明
      - 二者交互方式仍不明
  - 本轮再往前压一层：
    - 因为参数区直接写了 `noiseWindow = wick behavior, direction flips, close-to-close noise`
    - 而公开页又把 `wick behavior` 与 `close-overlap behavior` 并列为 sensitivity controls
    - 因此当前更优先怀疑 `close-overlap sensitivity` 先挂在 `Noise evaluation` 一侧，而不是先挂 `Structural containment`
    - 然后再通过 `shared pocket qualify` 间接影响 `contained pocket / containment quality`
  - 已继续并入 `strictMode_kimi_followup` 的 v2 回帖：
    - `VOTE: Q1=B; Q2=A; Q3=A; Q4=C`
    - 这把当前判断又收窄为：
      - `close-overlap = feature-level sensitivity`
      - `strictMode = policy-level gating / qualify strictness`
      - 更可能链路：`close-overlap(feature sensitivity) + strictMode(policy gating) -> shared pocket qualify -> contained pocket -> Mature`
    - 同时继续保留缺口：
      - `strictMode` 具体是抬阈值、加必要条件，还是改总分/权重，仍无源码证据
  - 当前又再收紧一层：
    - 在这三类机制里，`score formula / weights rewrite` 是当前最不优先
    - 更优先顺序暂写为：
      - `threshold shift / qualify strictness`
      - `additional qualify conditions`
      - `score formula / weights rewrite`
  - 已补 `projectPocketBars` 边界：它更像 pocket 区域向右投影/延伸的展示控制，不宜直接当成 `release` 触发证据
  - 已补源码顺序边界：`Scoring engine + State machine` 在 `Pocket detection` 与 `Action Engine` 之前，因此 `releaseUp / releaseDown` 更像状态机之后的下游解释层，不宜反推成 state/pocket qualify 前置条件
  - 已补章节顺序边界：`batch9_sources_kimi` 明确先写 `State 判定`，后写 `Action Engine 输出`；因此当前顺序进一步固定为 `compressionScore -> state bucket -> isMature/isTight/isBuilding -> action labels`
  - 已补 confirm 顺序边界：`noise + containment -> Mature confirm` 应位于 `release/nearEdge` 之前，`releaseUp / releaseDown` 不应倒推成 `Mature` 的前置条件
  - 已补方向边界：页面明确写 `It does not attempt to forecast direction`，因此 `releaseUp / releaseDown` 不宜解释成 breakout direction prediction，更像 resolved/exit 后的复核建议标签
  - 已把后续追索顺序进一步收紧：先追 `strictMode -> contained pocket / close-overlap / pocket qualify`，再追 `noise/containment confirm -> Mature`，最后再追 `releaseUp / releaseDown` 与 resolved pocket 退出事件
  - 已完成 `compression` 等价矩阵固化（`runtime_notes` 中明确已对齐 / 半对齐 / 缺源码无法判定）
  - 已把 runtime 样本推进到多周期 + 多资产类别覆盖（`EURUSD/XAUUSD` × `H1/M15/H4` + `XBRUSD H1/H4` + `AAPL.NAS H1/H4` + `USTEC/US500/DE40/JP225/HK50 H1/H4`）
- 当前还没完成：
  - 真实运行脚本接入
  - `strictMode` 的精确 gating 规则
  - `compression_state` 的 confirm 门槛与 `nearEdge / releaseUp / releaseDown` 判定
  - 四项 compression 子评分是否正式落盘
  - 更多地区指数/个股分支、港股/日股更细分支或第四周期覆盖
  - `compression_state / vol_regime_code / breakout` 条件层

## 为什么先做到这一步

- `N01` 是环境状态层，不是执行层。
- 它对后续分桶、环境过滤和解释变量研究有共用价值。
- 先固定运行时目录与文件角色，可以避免后续接脚本时反复改名。

## 对主线的意义

- `Batch9` 现在已经不只是“收网页资料”。
- `REOPEN_B9_N01_VOL_STATE_P0` 证明：
  - Batch9 可以像前几批一样，先收口，再选首批重开项，再逐步形成实现证据。

## 下一步

- 若继续推进同一条线，下一步应是：
  - 先继续做 `strictMode` 在 `close-overlap(feature-level sensitivity) + strictMode(policy-level gating) -> shared pocket qualify -> contained pocket -> active/Mature gating` 这一更窄顺序里的精确落点证据，并保持 `state 判定在前、Action Engine 在后` 的顺序口径不漂移
  - 再继续确认 `close-overlap sensitivity` 是否真的先进入 `Noise evaluation`，还是源码里仍落在 `containment`/独立 modifier
  - 再继续确认 `strictMode` 更像：
    - 阈值门（threshold shift）
    - 额外 qualify 条件（additional conditions）
    - 还是总分/权重改写（score formula / weights）
  - `strictMode_kimi_followup` 的 v3 问题包本轮再次检查仍无回帖，因此当前只继续冻结：
    - `threshold shift`
    - vs `additional qualify conditions`
    这一最小缺口
  - 当前仍不把两者先后顺序写死成源码级结论
  - 再继续补 `Pocket detection -> Action Engine` 之间 `nearEdge / releaseUp / releaseDown` 的判定证据
  - 期间继续维持四项子评分“只审计，不落盘”
  - 再决定是否补更多地区指数/个股分支、港股/日股更细分支或第四周期样本
- 若暂时不接代码，也应保持：
  - `N01 in_progress`
  - `N02` 继续领先一小步
