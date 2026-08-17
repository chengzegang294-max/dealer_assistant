# a_share_daily_tech_indicators — A股每日技术指标结构化家族（主线第一优先级，Cursor干脏活累活）

创建日期：2026-08-13
数据锚点：**东方财富网（eastmoney.com）Web 页面** = 和直播间、连板天梯同一套数据源锚点（都是你平时打开看的网页，不是东方财富PC客户端软件）。**两者没关系：直播间/连板天梯是从网站抓的，PC客户端是你看行情的独立软件，别混。**
零额外成本：不用注册新号（东财网本身免登录看全量行情表）、不用下载任何软件、不用申请 API key，直接开网页就能抓。
外汇/币圈/期货：**后续单独开家族，绝不混进本家族目录，不跟A股 T+1 混表**

---

## 一、你每天要做的事情（只有 1 件=10 秒说一句话，其他全是 Trae 脏活累活）

**收盘之后，对 Trae 说一句固定的开工话就行，不用你去打开东财网页、不用你去导 CSV、不用你手动操作任何东西：**
> `/a-tech-daily 交易日：YYYYMMDD --apply`
（例：`/a-tech-daily 交易日：20260813 --apply`）

Trae 会自动完成下面 6 件从东方财富网 Web 直接抓全量原始数据（和直播间/连板天梯一样，开网页取表/取接口）→ 计算均线/MACD/RSI/BOLL → 输出 6 份标准化 CSV：

| 数据 # | Trae 从东方财富网（Web）哪 6 页自动抓？（和直播间/连板天梯同一锚点，东财网免登录看全量） | 原始快照自动存档在哪？（你后面想重算直接用，不用再抓） | 输出什么结构化CSV？ |
|---|---|---|---|
| 1. 代码池日线（沪深300+中证500+中证1000+22房直播间TOP5命中） | 东财网「行情中心→沪深京A股」/ 各指数成分股页面 | `99_raw_snapshots_web/YYYYMMDD/01_bar_pool_raw.html/json` | `a_share_daily_bar_pool_YYYYMMDD.csv` |
| 2. 行业+概念板块资金流（涨跌幅+主力净流入净额） | 东财网「板块监测→行业板块/概念板块→主力净流入净额排序」 | `99_raw_snapshots_web/YYYYMMDD/02_sector_fund_flow_raw.html/json` | `a_share_sector_fund_flow_YYYYMMDD.csv` |
| 3. 涨跌停全量+连板晋级率（和连板天梯同一页面！） | 东财网「涨停板分析/连板天梯」→ 和你抓连板天梯的**同一个网页** | `99_raw_snapshots_web/YYYYMMDD/03_limit_up_ladder_raw.html/json` | `a_share_daily_limit_up_stats_YYYYMMDD.csv` |
| 4. 龙虎榜机构/北向/游资净买入TOP50 | 东财网「龙虎榜→每日龙虎榜→净额TOP50」 | `99_raw_snapshots_web/YYYYMMDD/04_dragon_tiger_raw.html/json` | `a_share_dragon_tiger_top50_YYYYMMDD.csv` |
| 5. 北向资金总额+沪/深分向 + 两融余额变动 | 东财网「数据中心→沪深港通北向每日净流入」+「融资融券两融余额」 | `99_raw_snapshots_web/YYYYMMDD/05_northbound_margin_raw.html/json` | `a_share_northbound_margin_YYYYMMDD.csv` |
| 6. 6大指数日线（上证/沪深300/中证500/中证1000/创业板指/科创50）+ 技术指标 | 东财网对应 6 大指数的 K线行情页 | `99_raw_snapshots_web/YYYYMMDD/06_index_bar_raw.html/json` | `a_share_index_daily_indicators_YYYYMMDD.csv` |

---

## 二、脚本自动输出的 6 份标准化结果（全部结构化，不用手动算）

| 输出文件（放在本家族根目录，YYYYMMDD自动按日） | 列字段合同（固定，不讨论不改动） | 谁用 |
|---|---|---|
| 1. `a_share_daily_bar_pool_YYYYMMDD.csv` | `stock_code_6d,stock_name,trade_date,open,high,low,close,vol_share,amt_yuan,turnover_rate_pct,change_pct,consecutive_limit_up_d,MA5,MA10,MA20,MA60,EMA12,EMA26,DIF,DEA,MACD,RSI_6,RSI_12,RSI_24,BOLL_UPPER,BOLL_MID,BOLL_LOWER` | 交叉验证直播间TOP5股票的T+1/T+2走势真值、分类器训练特征 |
| 2. `a_share_sector_fund_flow_YYYYMMDD.csv` | `sector_type(行业/概念),sector_name,change_pct,main_net_inflow_yuan,main_net_inflow_pct,lead_stock_code_6d,lead_stock_name,lead_stock_change_pct` | 交叉验证直播间TOP5关键词板块是不是市场真涨/真资金进 |
| 3. `a_share_daily_limit_up_stats_YYYYMMDD.csv` | `trade_date,limit_up_count_new,limit_up_count_total,limit_down_count,open_limit_up_blow_count,blow_rate_pct,board_pass_rate_1to2_pct,board_pass_rate_2to3_pct,board_pass_rate_3plus_pct,max_consecutive_days,sector_distribution_top5` | 交叉验证直播间情绪/风格判断（判多→涨停≥80？晋级率≥50%？） |
| 4. `a_share_dragon_tiger_top50_YYYYMMDD.csv` | `rank,seat_type(机构/北向/游资营业部),seat_name,net_buy_yuan,buy_yuan,sell_yuan,stock_code_6d,stock_name,change_pct,daily_turnover_pct` | 交叉验证直播间风格判断（打板→机构/游资净额>50亿？） |
| 5. `a_share_northbound_margin_YYYYMMDD.csv` | `trade_date,northbound_total_net_yuan,hgt_net_yuan,sgt_net_yuan,margin_total_balance_yuan,margin_daily_change_yuan,margin_daily_change_pct` | 交叉验证直播间宏观情绪（判多→北向净流入≥30亿？） |
| 6. `a_share_index_daily_indicators_YYYYMMDD.csv` | `index_code,index_name,trade_date,open,high,low,close,change_pct,amt_yuan,MA5,MA10,MA20,MA60,DIF,DEA,MACD,RSI_14,BOLL_UPPER,BOLL_MID,BOLL_LOWER,trend_vs_MA20(above/below),macd_cross(golden/dead/none)` | 大盘环境锚：直播间情绪判→是否在MA20以上？MACD金叉？ |

---

## 三、目录结构（外汇/币圈/期货 后面单独开家族，绝不混进本目录）

```
02_runtime/a_share_daily_tech_indicators/
├── 99_raw_snapshots_web/            Trae 自动抓取的东财网原始网页/JSON快照（按日分子目录，永久保留不删）
│   └── YYYYMMDD/
│       ├── 01_bar_pool_raw.html or .json
│       ├── 02_sector_fund_flow_raw.html or .json
│       ├── 03_limit_up_ladder_raw.html or .json
│       ├── 04_dragon_tiger_raw.html or .json
│       ├── 05_northbound_margin_raw.html or .json
│       └── 06_index_bar_raw.html or .json
├── README.md                        本文件（6份输入/6份输出/每日流程写死）
├── a_share_daily_bar_pool_YYYYMMDD.csv           ← 脚本输出1 代码池日线+技术指标
├── a_share_sector_fund_flow_YYYYMMDD.csv         ← 脚本输出2 行业/概念板块资金流
├── a_share_daily_limit_up_stats_YYYYMMDD.csv     ← 脚本输出3 涨跌停+连板晋级率
├── a_share_dragon_tiger_top50_YYYYMMDD.csv       ← 脚本输出4 龙虎榜TOP50
├── a_share_northbound_margin_YYYYMMDD.csv        ← 脚本输出5 北向+两融
└── a_share_index_daily_indicators_YYYYMMDD.csv   ← 脚本输出6 主要指数技术指标
```

**本家族红线：**
1. 只放A股结构化数据，外汇/币圈/期货数据绝不写进这里，后面单独开 `fx_* / crypto_* / futures_*` 家族；
2. 只写客观可量化的数值，不写主观情绪/判断，所有技术指标按公式算，不主观调；
3. **原始网页快照自动存档在 99_raw_snapshots_web/YYYYMMDD/，永久保留不删，后面重新算指标直接用，不用再开网页重抓，不反向覆盖原始。**
4. 【纠正之前的错误】：数据源锚点=东方财富网（eastmoney.com Web 页面）= 和直播间/连板天梯同一套，不是东方财富PC客户端；两者没有关系，直播间和连板天梯都是从网站抓的，不是从PC客户端导的。
