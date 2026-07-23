# YTC 分钟样本 provenance 模板

更新时间：2026-07-13

## 用途

- 这是一张模板页。
- 后续一旦拿到 `60m/5m` 真样本，直接复制这页并按实物填写。

## 模板

```md
# YTC intraday sample provenance

更新时间：<YYYY-MM-DD>

## 文件类型

- `INDEX_NOTE`

## 原路径

- `<source_path_or_provider>`

## 新路径

- `batch_147/00_raw_snapshot/<symbol>_<timeframe>_provenance_note__<date>.md`

## 生成入口

- `<producer_or_manual_export>`

## 适用对象

- `YTC`

## 当前作用

- `60m/5m` 真样本来源说明

## 证据强度

- `hard`
  - 若来自正式 provider 拉取
- `historical_recovered`
  - 若来自历史回收
- `weak_evidence`
  - 若只是临时外部手工导出

## 样本信息

- `symbol`: `<601991.SH>`
- `timeframe`: `<60m or 5m>`
- `date_range`: `<start ~ end>`
- `fields`: `trade_date/open/high/low/close/volume`

## 当前裁决

- 是否可作为 `YTC` 当前分钟样本：
  - `<yes/no>`
- 若否，原因：
  - `<...>`
```

## 当前推荐命名

- `601991_SH_60m_provenance_note__20260713.md`
- `601991_SH_5m_provenance_note__20260713.md`

## 当前结论

- 后续补分钟样本时，不再需要重新发明 provenance 写法。
- 直接按本模板落说明即可。
