# AGPro Family Invite-Only Access Note

更新时间：2026-07-15

## 文件类型

- `ARTIFACT`

## 原路径

- `https://www.tradingview.com/script/XJmX3p98-Trading-Suite-AGPro-Series/`

## 新路径

- `batch_146/00_raw_snapshot/AGPro_family_invite_only_access_note__20260715.md`

## 生成入口

- `manual_browser_probe`

## 适用对象

- `Batch9 N01 AG Pro family access-state evidence`

## 当前作用

- 把 `AGProLabs` 邀请制脚本页的访问状态正式落盘。
- 说明当前为什么还能继续补 `AG Pro` 参数与默认值证据，但无法把“完整 Pine 正文”误写成已拿到。

## 页面身份

- 页面标题：
  - `Trading Suite [AGPro Series] — Indicator by AGProLabs — TradingView`
- 页面性质：
  - `Invite-only script`
- 原文：
  - `Only users approved by the author can access this script. You'll need to request and get permission to use it. This is typically granted after payment.`

## Source Code 访问状态

- 页面标签：
  - `Chart`
  - `Source code`
- DOM 状态：

```json
[
  {"text":"Chart","selected":"true","disabled":"false"},
  {"text":"Source code","selected":"false","disabled":"true"}
]
```

- 当前解释：
  - `Source code` 标签存在，但当前页被禁用，不能打开源码窗口。
  - 这说明 `AGProLabs` 家族脚本存在“页面可见但源码不可见”的现实限制。

## Key Inputs 参数位

- `Visual Modules`
  - `trend ribbon`
  - `moving averages`
  - `anchored VWAP`
  - `session VWAP`
  - `directional labels`
  - `risk blocks`
  - `liquidity sweeps`
  - `FVG/BOS drawings`
  - `value zones`
  - `automatic support/resistance`
  - `dashboard`
  - `portfolio`
  - `Smart Swap panel`
- `SMC History Mode`
  - `Lite mode emphasizes recent structure and is the default for readability.`
- `Maximum S/R Levels and TP Levels`
  - `The default display is restrained: two support/resistance levels per side and two target levels.`
- `Use Confirmed Data for Smart Swap`
  - `Enabled by default.`
- `Realtime Refresh`
  - `Disabled by default.`
- `Smart Swap Strategy`
  - `Balanced is the neutral default.`

## 对 N01 主批次的可用价值

- 可补：
  - `AGPro family access_state`
  - `invite_only boundary`
  - `parameter_default_style`
  - `source_code_missing_reason`
- 不可冒充：
  - `AG Pro ATR Compression Map` 完整源码正文
  - `核心计算公式已直接见源码`

## 当前结论

- 当前已能正式写清：
  - `AGPro` 家族存在 invite-only 页面，且 `Source code` 可能被页面级禁用
  - 这类页面可继续贡献参数位、默认值与访问边界证据
- 当前仍不能写成：
  - `已拿到完整 Pine 正文`
