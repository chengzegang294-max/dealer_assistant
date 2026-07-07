# OUTBOUND: strictMode vs close-overlap v1

## Task

- 目标：只基于下面证据，判断 `strictMode` 更像：
  - 一个比 `close-overlap behavior sensitivity` 更总括的 filtering/gating 开关
  - 还是本质上就等于 `close-overlap sensitivity`
- 额外判断：
  - `strictMode` 是否更可能和 `close-overlap sensitivity` 一起，在 `pocket qualify` 之前或之内起作用

## Hard Rules

- 只能使用 EVIDENCE PACK。
- 如果证据不足，必须写 `NEED_EVIDENCE`，不要猜。
- 不允许编造源码行号、参数名、触发公式。
- 不允许把 `releaseUp / releaseDown` 倒推成主状态条件。

## EVIDENCE PACK

### Evidence 1: page excerpt

Path:
- `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\N01_波动率状态机\AG_Pro_ATR_Compression_Map__page_excerpt.md`

Key excerpt:

```text
Instead of treating every quiet market phase as equally meaningful, the script separates loose and unstable contraction from cleaner, more contained compression conditions.

The script combines four internal components into a unified compression score
1) ATR contraction
2) Range tightness
3) Noise evaluation
4) Containment structure

Advanced options allow stricter filtering and additional sensitivity controls for wick behavior and close-overlap behavior

Compression Active alert is triggered when compression conditions become active according to the script's scoring logic
Compression Mature alert is triggered when the current state reaches Mature
Compression State Change alert is triggered when the internal compression state changes

It does not attempt to forecast direction
```

### Evidence 2: Kimi structured note

Path:
- `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\batch9_sources_kimi\N01\03_ag_pro_atr_compression_map_tradingview.md`

Key excerpt:

```text
- noiseWindow: 10
  - Window to evaluate wick behavior, direction flips, close-to-close noise

- containmentWindow: 24
  - Window to evaluate price clustering inside contained volatility pocket

- compressionThreshold: 62.0
  - Minimum score required for qualified compression state

- matureThreshold: 80.0
  - Higher score for mature compression when noise and containment confirm

- strictMode: false
  - Applies tighter score gates for more selective compression pockets
```

### Evidence 3: methodology order

Use this ordering only:

```text
Noise evaluation
Structural containment
compressionScore -> state bucket -> isMature/isTight/isBuilding -> action labels
```

## Questions

Q1:
- 更稳妥的裁决是什么？
  - A = `strictMode` 本质上就是 `close-overlap sensitivity`
  - B = `strictMode` 更像总括 filtering/gating，`close-overlap` 是同组但相对独立的 sensitivity input
  - C = 证据不足，只能停在“同方向”

Q2:
- 当前更可能的顺序是什么？
  - A = `strictMode -> close-overlap sensitivity -> pocket qualify -> contained pocket -> Mature`
  - B = `close-overlap sensitivity + strictMode broader gating -> pocket qualify -> contained pocket -> Mature`
  - C = `strictMode` 主要只作用在 `Mature` 末端 gating

Q3:
- 哪条结论现在绝对不能写死？
  - A = 不能写死 `strictMode == close-overlap sensitivity`
  - B = 不能写死 `strictMode` 只改 `Mature` 阈值
  - C = 以上两条都不能写死

## Output Contract

- 先输出一行：

```text
VOTE: Q1=<A/B/C>; Q2=<A/B/C>; Q3=<A/B/C>
```

- 再输出 3-6 条 bullet：
  - 每条都必须引用 EVIDENCE PACK 里的原句或路径
  - 若证据不足，明确写：
    - `NEED_EVIDENCE: <缺什么>`

- 最后只补 1 小段：
  - `NEXT_ACTIONS:` 后面最多 2 条可验证动作



VOTE: Q1=B; Q2=B; Q3=C

---

**Evidence-based reasoning:**

- **Q1 → B**: Evidence 1 states "Advanced options allow **stricter filtering** and **additional sensitivity controls** for wick behavior and **close-overlap behavior**" — the phrasing uses "and" to connect "stricter filtering" (the gating dimension) with "sensitivity controls for close-overlap" (a specific input dimension), treating them as coexisting rather than equivalent. Evidence 2 further clarifies `strictMode` "Applies **tighter score gates** for more selective **compression pockets**" — this describes a broad gating function over pocket qualification, not a single-parameter sensitivity knob.

- **Q2 → B**: Evidence 2 positions `strictMode` as "tighter score gates for more selective compression pockets," placing its effect at or before pocket qualification. Evidence 3 shows the pipeline runs `compressionScore -> state bucket -> isMature/isTight/isBuilding`. `strictMode` as a "score gate" must act at the pocket-qualify boundary (where compressionThreshold of 62.0 is applied per Evidence 2), not downstream at Mature alone. Close-overlap sensitivity, per Evidence 1, is an "additional sensitivity control" operating alongside this gating layer.

- **Q3 → C**: 
  - (A) Cannot equate `strictMode` to close-overlap: Evidence 1 explicitly separates "stricter filtering" from "sensitivity controls for...close-overlap behavior" — they are grammatically and functionally distinct.
  - (B) Cannot lock `strictMode` to Mature-only gating: Evidence 2 says it makes "compression pockets" more selective — this points to the qualification gate (compressionThreshold 62.0), not exclusively the Mature threshold (80.0). Evidence does not specify whether `strictMode` also shifts `matureThreshold`.

- **NEED_EVIDENCE**: `strictMode`具体的实现方式——是压低`compressionThreshold`/`matureThreshold`的数值、增加额外的必要条件、还是改变`compressionScore`的计算公式？目前Evidence 2只给了语义描述，没有源码级行为确认。

- **NEED_EVIDENCE**: `close-overlap sensitivity`在pipeline中的确切注入位置——是在Noise evaluation阶段作为close-to-close noise的子组件，还是在Structural containment阶段评估containment structure，还是作为独立的第五维score modifier？

- **NEED_EVIDENCE**: `strictMode`与`close-overlap sensitivity`之间是否存在交互（additive, multiplicative, or mutually exclusive gating），还是两条完全独立的控制路径？

---

NEXT_ACTIONS:
1. 获取`AG_Pro_ATR_Compression_Map`的源码或更详细的参数文档，确认`strictMode`对`compressionThreshold`和`matureThreshold`的具体影响方式（是直接修改阈值、添加额外条件、还是调整score计算权重）。
2. 定位文档中关于`close-overlap sensitivity`的独立描述，确认其在四组件（ATR contraction / Range tightness / Noise evaluation / Containment structure）中的归属与注入阶段。