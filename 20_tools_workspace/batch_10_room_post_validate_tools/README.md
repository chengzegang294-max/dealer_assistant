# batch_10 直播间后验真值 + 多AI准确率验证 工具家族

创建日期：2026-08-13
工作仓：`d:\Stock\dealer_assistant`（正式主线，脚本明确结论后落这里）

---

## 作用

把用户说的「多AI讨论3格判断 → 用T+1/T+2实际走势验证谁准 → 沉淀100条经验 → 训练本地化分类器」5步工程化落地。

**本家族只做客观工具，不做主观判断：**
- 第0步真值数据录入：客观后验涨跌幅，是人录入的事实，不是AI猜的
- 第2步准确率打分：只按公式算分，不偏AI不黑AI
- 第4步本地化分类器训练：纯 sklearn 本地训练，不用外部 API，不用 key

---

## 一、现在已经有的文件（你可以直接打开，不用找文件夹）

| 文件 | 路径（直接点打开） | 作用 | 你要做什么 |
|---|---|---|---|
| 22房TOP5代码预填CSV模板 | [post_truth_20260811_TEMPLATE_prefilled.csv](file:///D:/Stock/dealer_assistant/20_tools_workspace/batch_10_room_post_validate_tools/post_truth_20260811_TEMPLATE_prefilled.csv) | 22房*5=110行；前3列已预填（房名/Top5排名/代码，抓不全的手动补） | 填后面4列客观真值（T+1收盘涨跌幅 / T+2收盘涨跌幅 / T+1日内最高冲高涨跌幅 / 连板天数） |
| 第2步AI准确率打分脚手架（空壳，等你填完CSV+AI输出就直接算） | [validate_ai_vs_post_truth_v1.py](file:///D:/Stock/dealer_assistant/20_tools_workspace/batch_10_room_post_validate_tools/validate_ai_vs_post_truth_v1.py) | 输入：填完的真值CSV + 每家AI的3格输出（旧仓90区02目录）→ 输出：每家AI 3格的准确率分 + 哪类房最准 | 填完真值+AI出完3格判断后，直接跑 |
| 第4步本地化分类器训练脚手架（空壳，等Step3凑够50条经验后用） | [train_room_3style_local_classifier_v1.py](file:///D:/Stock/dealer_assistant/20_tools_workspace/batch_10_room_post_validate_tools/train_room_3style_local_classifier_v1.py) | sklearn随机森林/决策树本地训练3个分类器（情绪/风格/节奏），完全本地化不调用外部API | 凑够50条经验后直接跑 |

---

## 二、你每天填真值CSV的4列怎么填（T日=直播间当日；这里T=2026-08-11）

1. `T_plus_1_close_pct`：2026-08-12（T+1日）收盘价相对2026-08-11（T日）收盘价的涨跌幅，单位：百分比数值，直接写数字不要写%，例如涨 3.24% 就写 `3.24`，跌 1.5% 就写 `-1.5`
2. `T_plus_2_close_pct`：2026-08-13（T+2日，今天）收盘价相对T日收盘价的涨跌幅，同样填数字
3. `T_plus_1_intraday_high_pct`：2026-08-12（T+1）日内最高价格相对T日收盘价的涨跌幅（=直播间提过这只股票后，次日冲高涨多少，用来验证风格/节奏判断的兑现）
4. `consecutive_limit_up_days`：从T日收盘后开始算的连续涨停板天数（整数，1=次日1板，2=2连板，0=没涨停）

**CSV前3列预填的 stock_code_6d 如果是空的（正则没抓全复盘哥/独家5号的TOP5代码），直接去对应房的Prefill看TOP5股票代码那行手动补。**

---

## 三、第2步AI准确率打分规则（客观公式，不偏不黑，脚本就是按这个算的）

先把你要验证的每家AI的3格判断输出，复制成 JSON 模板（`validate_ai_vs_post_truth_v1.py` 里有）：每家AI每间房3格写成一条记录。

### 3.1 情绪格（情绪偏多空）准确率怎么算
- 算某间房的TOP5平均T+1收盘涨跌幅，记为 avg_pct
- AI判 = 多 / 稍多  →  avg_pct > +0.5% → 判对；avg_pct < -0.5% → 判错；中间算半对
- AI判 = 空 / 稍空  →  avg_pct < -0.5% → 判对；avg_pct > +0.5% → 判错；中间算半对
- AI判 = 中性 / 震荡 → avg_pct 落在 [-0.5%, +0.5%] → 判对，否则判错半对
- 最后3间样板房平均一下，就是这家AI「情绪格准确率」

### 3.2 风格格（打板/低吸/埋伏/轮动）准确率怎么算
- T+1日内最高冲高涨跌幅（T+1冲高涨多少）按档分组，每档对应期望风格：
  - 冲高涨 +8% 以上 or 连板天数≥2 → 期望风格=打板
  - 冲高涨 +3%~+7% 且收盘拉回（T+1收盘 - T收盘 < +2%）→ 期望风格=低吸
  - 冲高涨 < +3% 且 T+2 收盘 > +3% → 期望风格=埋伏
  - 冲高涨分散，5只TOP5有3只以上不同档 → 期望风格=轮动
- AI判和期望风格相同 → 判对；不同 → 判错；相关但不完全一致 → 半对

### 3.3 次日节奏格（高位接力/中位/首板/观望）准确率怎么算
- 看TOP5代码的「T日前1日收盘- T日最高 - T+1日最高」是拉板加速还是底部首板：
  - 连续2板以上（连板天数≥2）且T日之前已经有1板 → 期望节奏=高位接力
  - T日首板，T+1二板 → 期望节奏=中位
  - T日没板，T+1首板 → 期望节奏=首板
  - T日T+1都没板，冲高涨都<+2% → 期望节奏=观望
- AI判和期望节奏一致→判对，否则判错/半对

### 3.4 总分=（情绪准确率×0.4 + 风格准确率×0.3 + 节奏准确率×0.3）
按总分从高到低排AI名次，得分高的AI后面我们优先参考它的3格草稿，得分低的直接丢掉不发包。

---

## 四、当前进度 / 下一步启动点（记3件事就够）

1. ✅ Step0+1 骨架已搭：真值CSV预填模板已出（110行，22房*5）+ 验证打分脚手架已出 + 本地化分类器训练脚手架已出
2. ✅ Step1 多AI发包输入已复制到旧仓90区（3间样板房的Prefill+人读摘要6件MD全拷过去了，直接打开看）
3. 🚀 下一次最小启动点：
   ① 你先花15分钟，把真值CSV里的T+1/T+2 4列客观涨跌幅填完（空代码去Prefill手补TOP5）
   ② 复制旧仓90区01_ai_inputs/ 里的3间样板房MD，发给3~5家AI独立填3格+写1句判断理由，每家AI输出 JSON/Markdown 都行，放旧仓90区02_ai_outputs_per_vendor/<厂商名>/
   ③ 都齐了之后对我开工：`跑batch_10 validate AI准确率` → 我直接跑脚本算每家AI 3格的准确率分

---

## 五、旧仓90区多AI讨论发包点（试验/草稿/待裁决区，不污染新仓正式主线）

多AI发包目录直接点打开：
[batch_10_multi_ai_room_classifier__20260813/](file:///D:/Stock/trading_assistant/90_SCRATCH_AND_TEST_ZONE/batch_10_multi_ai_room_classifier__20260813)
- `01_ai_inputs/` = 3间样板房的Prefill+人读摘要MD（直接复制给AI的输入）
- `02_ai_outputs_per_vendor/` = 每家AI输出放这里，每个厂商一个子目录，比如 02_ai_outputs_per_vendor/GPT4o/ 或 Claude35/
- 发包规则 README：[README.md](file:///D:/Stock/trading_assistant/90_SCRATCH_AND_TEST_ZONE/batch_10_multi_ai_room_classifier__20260813/README.md)
