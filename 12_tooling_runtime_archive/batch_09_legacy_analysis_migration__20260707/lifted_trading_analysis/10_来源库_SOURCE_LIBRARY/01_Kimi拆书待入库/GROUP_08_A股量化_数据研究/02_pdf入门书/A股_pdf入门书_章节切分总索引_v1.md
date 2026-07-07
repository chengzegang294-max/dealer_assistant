# A股 pdf 入门书 章节切分总索引 v1

- source_type: pdf_book
- project_role: A股 future research/data capability
- current_status: 待入库
- book_title: 量化交易之路：用Python做股票量化分析
- book_author: 阿布
- book_publisher: 机械工业出版社
- book_year: 2017
- github_repo: https://github.com/bbfamily/abu

---

## 章节目录

| chapter_id | chapter_title | chapter_role | main_theme | go_to_file |
|------------|---------------|--------------|------------|------------|
| CH-01 | 量化引言 | 仅来源库保留 | 量化交易概念科普 | 章节卡片_v1.md |
| CH-02 | 量化语言——Python | 仅来源库保留 | Python基础语法与数据结构 | 章节卡片_v1.md |
| CH-03 | 量化工具——NumPy | future bucket | NumPy基础操作与统计分布 | 章节卡片_v1.md |
| CH-04 | 量化工具——pandas | 可重开 | pandas金融数据处理、异动阈值、星期效应、跳空缺口 | 章节卡片_v1.md |
| CH-05 | 量化工具——可视化 | future bucket | Matplotlib/Bokeh/Seaborn可视化、黄金分割线、技术指标可视化 | 章节卡片_v1.md |
| CH-06 | 量化工具——数学 | future bucket | 回归插值、蒙特卡罗、凸优化、线性代数 | 章节卡片_v1.md |
| CH-07 | 量化系统——入门 | 可重开 | 趋势跟踪与均值回复策略、凯利公式仓位管理 | 章节卡片_v1.md |
| CH-08 | 量化系统——开发 | 可重开 | abu量化系统择时与选股、买卖因子、滑点、并行回测 | 章节卡片_v1.md |
| CH-09 | 量化系统——度量与优化 | 可重开 | 回测度量体系、Grid Search最优参数、资金管理 | 章节卡片_v1.md |
| CH-10 | 量化系统——机器学习·猪老三 | 仅来源库保留 | 机器学习基础概念、回归/分类预测股价、深度学习尝试 | 章节卡片_v1.md |
| CH-11 | 量化系统——机器学习·abu | 可重开 | 主裁边裁拦截模式、角度/跳空/价格/波动信号集成 | 章节卡片_v1.md |
| APP-A | 附录A：量化环境部署 | 仅来源库保留 | Python量化环境安装配置 | 章节卡片_v1.md |
| APP-B | 附录B：量化相关性分析 | future bucket | 相关性分析方法补充 | 章节卡片_v1.md |
| APP-C | 附录C：量化统计分析及指标应用 | future bucket | 统计分析与技术指标补充 | 章节卡片_v1.md |

---

## 章节统计

| chapter_role | 数量 | 章节 |
|--------------|------|------|
| 可重开 | 5 | CH-04, CH-07, CH-08, CH-09, CH-11 |
| future bucket | 4 | CH-03, CH-05, CH-06, APP-B, APP-C |
| 仅来源库保留 | 5 | CH-01, CH-02, CH-10, APP-A |

---

## 按功能域分组

| 功能域 | 覆盖章节 |
|--------|----------|
| 数据获取与清洗 | CH-04（pandas数据操作） |
| 回测框架 | CH-08（abu系统开发）、CH-09（度量与优化） |
| 因子/策略研究 | CH-07（趋势跟踪/均值回复/仓位管理）、CH-11（主裁边裁信号） |
| 可复用Python工具链 | CH-04（pandas）、CH-08（abu框架） |
| 基础科普/入门 | CH-01（引言）、CH-02（Python语言）、CH-03（NumPy） |
| 数学与统计工具 | CH-05（可视化）、CH-06（数学工具）、APP-B/C |
| 机器学习 | CH-10（ML基础）、CH-11（ML信号集成） |
