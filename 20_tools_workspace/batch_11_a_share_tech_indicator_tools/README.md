# batch_11 A股每日技术指标工具家族（主线第一优先级， Cursor/Trae 干脏活累活）

创建日期：2026-08-13
数据源：**东方财富网（eastmoney.com）Web 页面=和直播间、连板天梯同一套数据源锚点**（不是东方财富PC客户端软件，两者没关系，你搞错了我纠正）。东财网本身免登录看全量行情表，不用注册新号/不用下软件/不用API key，Trae 直接开网页抓。
命令入口：`/a-tech-daily`

---

## 一、6 件脚本空壳 + 字段合同（全部搭好，Trae 开东方财富网 6 页抓全量→自动算→输出6件CSV）

| # | 工具脚本 | Trae 自动从东方财富网 Web 哪页抓（和直播间/连板天梯同一套锚点，东财网免登录） | 输出：6份标准化结果CSV（见02_runtime家族README表） | 脏活累活（脚本干，你不用干） |
|---|---|---|---|---|
| 1 | `calc_daily_bar_pool_with_indicators_v1.py` | 「行情中心→沪深京A股」/ 沪深300、中证500、中证1000 指数成分股页面 + 22房直播间命中的 TOP5 代码池合并 | `a_share_daily_bar_pool_YYYYMMDD.csv` | 对齐交易日/补前复权价格/算MA5/MA10/MA20/MA60/算EMA12-EMA26→MACD/算RSI6/12/24/算BOLL上中下轨 全算好 |
| 2 | `calc_sector_fund_flow_clean_v1.py` | 「板块监测→行业板块/概念板块→主力净流入净额TOP排序」页 | `a_share_sector_fund_flow_YYYYMMDD.csv` | 清洗行业+概念板块分开/主力净流入元换算/匹配龙头股代码和涨跌幅 |
| 3 | `calc_limit_up_stats_and_pass_rate_v1.py` | 「涨停板分析 / 连板天梯」→ 和你抓连板天梯的**同一个网页** | `a_share_daily_limit_up_stats_YYYYMMDD.csv` | 统计涨停/跌停/炸板数/算炸板率/算1进2/2进3/3板以上晋级率/板块分布TOP5 |
| 4 | `clean_dragon_tiger_list_v1.py` | 「龙虎榜→每日龙虎榜→机构席位/北向资金/游资营业部 净买入净额TOP50」页 | `a_share_dragon_tiger_top50_YYYYMMDD.csv` | 分机构/北向/游资营业部/算净买/买/卖额/匹配股票涨跌幅换手 |
| 5 | `clean_northbound_and_margin_v1.py` | 「数据中心→沪深港通北向每日净流入（沪分向/深分向）」+「融资融券两融余额变动」 | `a_share_northbound_margin_YYYYMMDD.csv` | 合并北向总额/沪分向/深分向/两融余额变动元+百分比 |
| 6 | `calc_index_daily_indicators_v1.py` | 6大指数 K线行情页：上证指数 / 沪深300 / 中证500 / 中证1000 / 创业板指 / 科创50 | `a_share_index_daily_indicators_YYYYMMDD.csv` | 算均线/EMA/MACD/RSI/BOLL/判断MA20上方还是下方/判断MACD金叉死叉 |

**每个子脚本内部执行顺序（固定不讨论）：**
1. 用 Trae 内置 Browser 工具 / 或东财网公开行情 HTTP 接口 → 抓对应页面原始 HTML / JSON 快照
2. 原始快照**自动存档**到 `02_runtime/a_share_daily_tech_indicators/99_raw_snapshots_web/YYYYMMDD/`（永久保留不删，后面重算不用再抓）
3. 解析快照 → 按字段合同输出标准化 CSV → 存家族根目录

---

## 二、一个汇总脚本：`run_a_tech_daily_v1.py`（对应 `/a-tech-daily` 命令，一口气全跑 6 件）

### 用法（和/live-md 一样，一句命令全跑完）
```powershell
# 收盘后你只需要对 Trae 说：/a-tech-daily 交易日：YYYYMMDD --apply
# Trae 内部会执行：
python 20_tools_workspace/batch_11_a_share_tech_indicator_tools/run_a_tech_daily_v1.py `
  --snapshot-root 02_runtime/a_share_daily_tech_indicators/99_raw_snapshots_web `
  --out-root 02_runtime/a_share_daily_tech_indicators `
  --trade-date 20260813 `
  --apply
# 自动依次跑 1→6 件脚本：抓Web→存快照→算指标→出CSV
# 某件抓失败自动SKIP，不杀其他件，容错优先
```

**注意（现在是空壳脚手架，填充抓取+计算逻辑后面慢慢加不影响骨架）：** 现在 7 件脚本都实现了最小空壳：字段合同读入原始→输出空NA。先把骨架和流程跑通，`--snapshot-root` 里面有对应01~06的原始快照文件（Trae Browser 抓完会自动存）就会自动解析，抓网页的具体 selector / 接口 URL 后面填充不用改骨架。

---

## 三、当前进度 & 下一最小启动

1. ✅ 家族目录建好：02_runtime/a_share_daily_tech_indicators/（含 99_raw_snapshots_web/ 按日快照目录 + 6 件输出路径）
2. ✅ 命令建好：`.trae/commands/a-tech-daily.md`（写死 6 件顺序 + 东财网 Web 抓，不用你手动导CSV/不用你开网页）
3. ✅ 6件工具脚本空壳+汇总脚本：7个脚本全落好，字段合同和家族 README 完全对齐
4. 🚀 下一最小启动（收盘后你只用说 1 句话，不用你动手其他）：
   ① **你做的=10 秒**：对 Trae 说 `/a-tech-daily 交易日：YYYYMMDD --apply`
   ② **Trae 做的（脏活累活）**：自动开东财网 6 页抓 → 存快照 → 解析 → 算指标 → 出 6 件CSV → 回写交接
   ③ 任一网页抓失败 → 自动 SKIP，不杀其他件，后面补抓就行

## 四、外汇/币圈/期货 后面分开做

按你说的「都会分开做」，本家族只承接 A 股，外汇/币圈/期货路径/脚本/字段/锚点全独立绝不混：
- 外汇 → 后面新开 `02_runtime/fx_daily_rates_and_indicators/` + 新 batch
- 币圈 → 新开 `02_runtime/crypto_daily_rates_and_indicators/` + 新 batch
- 期货 → 新开 `02_runtime/futures_daily_indicators/` + 新 batch
绝不写进本目录混表。
