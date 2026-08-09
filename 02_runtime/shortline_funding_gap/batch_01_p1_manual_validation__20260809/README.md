# batch_01_p1_manual_validation__20260809

更新时间：2026-08-09  
状态：脚手架已铺好，可开始日填

## 一、这批只服务什么

1. `P1` 人工验证每日记录
2. `sector` 当日快照累积（不碰历史日）

不做：新接口、权限购买讨论、金融判断、历史回补抓取。

## 二、每天谁填、什么时候填

| 事项 | 谁 | 何时 |
|---|---|---|
| P1 竞价段 | 主负责人 / 指定观察人 | 9:25 后立刻补“竞价期判断” |
| P1 盘中时点 | 同上 | 建议 10:00、13:30；可选 14:30 |
| P1 收盘回看 | 同上 | 收盘后 30 分钟内 |
| sector 当日快照存档 | Cursor / 工具执行人 | 收盘后拿到**当日** snapshot JSON 后立刻归档 |

原则：

- 没看到就留空
- 一项最多一句话
- 先连续记 5 个交易日

## 三、P1 模板在哪

- [p1_manual_validation_template__20260809.md](file:///d:/Stock/dealer_assistant/02_runtime/shortline_funding_gap/batch_01_p1_manual_validation__20260809/derived/p1_manual_validation_template__20260809.md)
- [p1_manual_validation_template__20260809.tsv](file:///d:/Stock/dealer_assistant/02_runtime/shortline_funding_gap/batch_01_p1_manual_validation__20260809/derived/p1_manual_validation_template__20260809.tsv)

日填建议目录：

`daily/p1_day__{YYYYMMDD}.md`

## 四、sector 当日快照怎么累积

脚本：

- [capture_sector_snapshot_daily_v1.py](file:///d:/Stock/dealer_assistant/20_tools_workspace/batch_08_quicktiny_capture_tools/capture_sector_snapshot_daily_v1.py)

输入：

1. 已经拿到的**当日** `sector-capital-flow/snapshot` 原始 JSON
2. 输出目录
3. 交易日标签 `YYYYMMDD`

输出：

- `sector_capital_flow_snapshot__{date}.json`
- `sector_capital_flow_snapshot__{date}.tsv`
- `sector_capital_flow_snapshot__{date}.meta.json`

示例：

```powershell
python "d:\Stock\dealer_assistant\20_tools_workspace\batch_08_quicktiny_capture_tools\capture_sector_snapshot_daily_v1.py" `
  --input-json "D:\path\to\today_sector_snapshot.json" `
  --output-dir "d:\Stock\dealer_assistant\02_runtime\quicktiny_capture\sector_daily_snapshots" `
  --trade-date 20260809
```

硬限制：

- 若 JSON 内 `actualTradeDate/tradeDate` 与 `--trade-date` 不一致，脚本直接拒绝
- 不请求历史日
- 不新开接口

建议存档根目录：

`02_runtime/quicktiny_capture/sector_daily_snapshots/`

## 五、哪些地方仍然是人工

1. 竞价判断、异动标的、高标表现
2. 盘中“资金是否仍在”
3. 收盘“够用/不够用”
4. 何时打开连板天梯拿到当日 sector JSON（抓包/导出仍靠人）
5. 是否把当日 JSON 丢给归档脚本

自动化只做：把已有当日 JSON 规范命名并拆 TSV。

## 六、执行回报

- [A5_Cursor执行回报_P1模板与sector当日快照脚手架__20260809.md](file:///d:/Stock/dealer_assistant/02_runtime/shortline_funding_gap/batch_01_p1_manual_validation__20260809/A5_Cursor执行回报_P1模板与sector当日快照脚手架__20260809.md)
