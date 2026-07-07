# OUTBOUND: strictMode vs close-overlap v2

## TASK

- 只基于 EVIDENCE PACK，判断下面这条更稳妥：
  - `close-overlap behavior` 更像 feature-level sensitivity
  - `strictMode` 更像 policy-level gating / qualify strictness
  - 二者可能共同汇入 `shared pocket qualify`
- 这次不要只回答“同方向”，要尽量判断：
  - 二者是并列能力
  - 还是一个只是另一个的别名/展开

## HARD RULES

- 只能使用 EVIDENCE PACK。
- 如果证据不足，必须写 `NEED_EVIDENCE`。
- 不允许编造源码、公式、行号、变量名。
- 不允许把 `releaseUp / releaseDown` 倒推成主状态条件。
- 不允许把 `strictMode` 直接写死为只改 `Mature` 阈值，除非证据明确支持。

## EVIDENCE PACK

### Evidence 1

Path:
- `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\N01_波动率状态机\AG_Pro_ATR_Compression_Map__page_excerpt.md`

Quoted lines:

```text
Advanced options allow stricter filtering and additional sensitivity controls for wick behavior and close-overlap behavior

Instead of treating every quiet market phase as equally meaningful, the script separates loose and unstable contraction from cleaner, more contained compression conditions.

The script combines four internal components into a unified compression score
1) ATR contraction
2) Range tightness
3) Noise evaluation
4) Containment structure
```

### Evidence 2

Path:
- `12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\10_来源库_SOURCE_LIBRARY\00_外部公开资料与方法论参考\01_外部公开指标资料_Batch9\batch9_sources_kimi\N01\03_ag_pro_atr_compression_map_tradingview.md`

Quoted lines:

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

### Evidence 3

Use this structure order only:

```text
Noise evaluation
Structural containment
compressionScore -> state bucket -> isMature/isTight/isBuilding -> action labels
```

## QUESTIONS

Q1:
- 哪个判断更稳妥？
  - A = `strictMode == close-overlap sensitivity`
  - B = `strictMode` 与 `close-overlap` 是并列能力，但职责不同
  - C = 证据不足，只能停在“同方向”

Q2:
- 如果选 B，更可能是哪种职责拆分？
  - A = `close-overlap = feature-level sensitivity`; `strictMode = policy-level gating`
  - B = `close-overlap = pocket qualify`; `strictMode = Mature gating`
  - C = NEED_EVIDENCE

Q3:
- 当前更可能的链路是什么？
  - A = `close-overlap(feature sensitivity) + strictMode(policy gating) -> shared pocket qualify -> contained pocket -> Mature`
  - B = `strictMode -> Mature only`
  - C = `strictMode == close-overlap -> pocket qualify`

Q4:
- 现在绝对不能写死的结论是什么？
  - A = 不能写死 `strictMode == close-overlap sensitivity`
  - B = 不能写死 `strictMode` 只改 `Mature`
  - C = A 和 B 都不能写死

## OUTPUT CONTRACT

先输出一行：

```text
VOTE: Q1=<A/B/C>; Q2=<A/B/C>; Q3=<A/B/C>; Q4=<A/B/C>
```

然后输出 3-6 条 bullets：
- 每条必须引用 EVIDENCE PACK 的原句或路径
- 若证据不足，明确写：
  - `NEED_EVIDENCE: <缺什么>`

最后输出：

```text
NEXT_ACTIONS:
- <最多 2 条可验证动作>
```
VOTE: Q1=B; Q2=A; Q3=A; Q4=C

---

- **Evidence 1 语法并列区分**：原文 `"Advanced options allow stricter filtering and additional sensitivity controls for wick behavior and close-overlap behavior"` 使用 `and` 将 `stricter filtering` 与 `additional sensitivity controls for...close-overlap` 并列列出，二者不是同义词，而是同一组 Advanced options 下的两个独立维度。路径：`AG_Pro_ATR_Compression_Map__page_excerpt.md`

- **`strictMode` 作用于 pocket qualify 而非仅 Mature**：Evidence 2 明确描述 `strictMode` — `"Applies tighter score gates for more selective compression pockets"`，目标词是 `compression pockets`（整体口袋资格），不是 `mature` 单一状态。路径：`03_ag_pro_atr_compression_map_tradingview.md`

- **`close-overlap` 被定性为 sensitivity control 而非 gating**：Evidence 1 将 `close-overlap behavior` 归入 `additional sensitivity controls` 范畴，与 `stricter filtering`（即 policy-level gate）形成语义对照。路径：`AG_Pro_ATR_Compression_Map__page_excerpt.md`

- **`strictMode` 的 gating 位置在 score qualify 阶段**：Evidence 2 给出 `compressionThreshold: 62.0` 作为 `"Minimum score required for qualified compression state"`，而 `strictMode` 描述为 `"tighter score gates"`，语义上最直接对应 qualify 入口的收紧，不限于下游 `matureThreshold: 80.0`。路径：`03_ag_pro_atr_compression_map_tradingview.md`

- **NEED_EVIDENCE: `strictMode` 具体实现机制** — 缺乏源码或文档说明 `strictMode` 是（a）抬高 `compressionThreshold` 数值、（b）增加额外必要条件、还是（c）修改 `compressionScore` 计算公式中的权重。Evidence 2 仅有语义描述，无机制细节。

- **NEED_EVIDENCE: `close-overlap sensitivity` 在四组件中的注入位置** — 缺乏明确说明该 sensitivity 属于 `Noise evaluation`（ Evidence 2 提到 `close-to-close noise` 可能相关）、`Containment structure`、还是独立 score modifier。Evidence 1 四组件列表与 sensitivity controls 的映射关系未明确。

---

NEXT_ACTIONS:
- 获取 `AG_Pro_ATR_Compression_Map` 的源码或技术白皮书，确认 `strictMode` 是修改阈值、添加条件、还是调整 score 计算权重。
- 在同一文档中定位 `close-overlap` 的完整参数定义，确认它是独立参数还是 `noiseWindow` / `containmentWindow` 下的子属性，及其在四组件 pipeline 中的注入点。