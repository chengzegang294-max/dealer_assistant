# quicktiny / 连板天梯 Capture Tools Batch 08

## 用途

- 这里放 `连板天梯 / quicktiny` 的最小抓取摸底工具。
- 当前先不宣称“已经完成正式抓取”。
- 当前只做两件事：
  1. 先盘清桌面端安装物与 `EBWebView` 本地数据面
  2. 给后续 `Cursor` 或人工继续做网络请求观察、缓存抽样、页面级留样提供稳定起点

## 当前文件

- `inventory_quicktiny_webview_state_v1.py`
  - 输入：
    - 安装目录
    - `EBWebView` 本地目录
  - 输出：
    - JSON 盘点
    - Markdown 摘要
  - 当前作用：
    - 先回答“本机到底有什么”
    - 不直接回答“已经抓到哪些业务字段”

- `extract_min_day_sample_v1.py`
  - 输入：batch_04 最小字段合同 + batch_03 slim/raw（若 slim 截断则同接口补拉完整 raw）
  - 输出：`batch_05_min_day_sample__{date}` 下 min json/tsv + sample_acceptance
  - 只处理 `ladder/day` 与 `sector-capital-flow/snapshot`，不找新接口

- `capture_sector_snapshot_daily_v1.py`
  - 输入：已捕获的当日 sector snapshot JSON + 输出目录 + `YYYYMMDD`
  - 输出：`sector_capital_flow_snapshot__{date}.json/.tsv/.meta.json`
  - 只做当日快照存档；日期不一致直接拒绝；不请求历史日

- `prefill_p1_day_facts_v1.py`
  - 输入：交易日 + 可选 ladder/sector 当日 JSON
  - 输出：`daily/p1_day__{date}.md`（事实预填，判断格留空）并更新月日志 TSV
  - 不自动填写偏强/偏弱、资金是否仍在、够用/不够用

## 推荐执行方式

```powershell
python "d:\Stock\dealer_assistant\20_tools_workspace\batch_08_quicktiny_capture_tools\inventory_quicktiny_webview_state_v1.py" `
  --install-dir "D:\Stock\连板天梯" `
  --webview-dir "C:\Users\91883\AppData\Local\cn.quicktiny.sectorcapital\EBWebView" `
  --output-json "d:\Stock\dealer_assistant\02_runtime\quicktiny_capture\batch_01_inventory__20260808\derived\quicktiny_webview_inventory__20260808.json" `
  --output-md "d:\Stock\dealer_assistant\02_runtime\quicktiny_capture\batch_01_inventory__20260808\derived\quicktiny_webview_inventory__20260808.md"
```

## 当前一句话口径

- 这批工具先做摸底，不跳步宣布“正式抓取已稳定”；先把目录、缓存、存储位置盘清，再决定下一手是看网络请求、看本地存储，还是继续页面留样。
