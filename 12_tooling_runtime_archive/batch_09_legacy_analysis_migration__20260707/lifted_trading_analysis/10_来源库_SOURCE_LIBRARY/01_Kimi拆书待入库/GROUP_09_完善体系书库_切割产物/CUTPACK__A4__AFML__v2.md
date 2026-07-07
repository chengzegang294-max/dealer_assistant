### MATERIAL_CARD
- title: Advances in Financial Machine Learning
- author_or_source: Marcos López de Prado
- material_type: 书
- domain_tags: [金融机器学习, 量化策略, 回测, 资产配置, 市场微观结构, 过拟合控制]
- file_scope: 全书 393 页（Part 1–5，含 22 章 + 附录）

### ROUTING_DECISION
- current_repo_role: DATA_ENGINEERING_GUARD
- is_worth_deep_cut_now: yes
- deep_cut_priority: P0
- reason: 本书是金融 ML 的'工厂蓝图'，直接定义了数据清洗、标注、采样、回测、组合优化的工业标准。大量概念（triple-barrier、meta-labeling、purged CV、deflated Sharpe、HRP）已被社区验证，必须立即转化为可量化对象和状态模板。

### CONTENT_CLUSTERS
- cluster_name: 数据结构与采样
  what_it_is: 金融原始数据→结构化 bars（标准 bars / 信息驱动 bars），ETF trick、单产品滚动、事件采样。
  keep_level: 高
  repo_mapping: data_engineering_guard / object_definition_shell

- cluster_name: 标签系统
  what_it_is: Fixed-time horizon 的缺陷、triple-barrier method、meta-labeling 解耦方向与仓位、动态阈值。
  keep_level: 高
  repo_mapping: object_definition_shell / state_template_shell

- cluster_name: 样本权重与非 IID 处理
  what_it_is: 重叠 outcome、并发标签数、平均唯一性、sequential bootstrap、时间衰减。
  keep_level: 高
  repo_mapping: data_engineering_guard / state_template_shell

- cluster_name: 分数差分特征
  what_it_is: 整数差分抹除记忆的问题、fracdiff 的迭代估计、固定宽度窗口、ADF 最优 d。
  keep_level: 高
  repo_mapping: object_definition_shell

- cluster_name: 集成与交叉验证
  what_it_is: Bagging vs Boosting、随机森林、purged K-fold + embargo、sklearn bug 规避。
  keep_level: 高
  repo_mapping: data_engineering_guard / state_template_shell

- cluster_name: 特征重要性
  what_it_is: MDI（IS，树专属）、MDA（OOS，置换检验）、orthogonal features、substitution effect。
  keep_level: 中
  repo_mapping: state_template_shell

- cluster_name: 仓位管理
  what_it_is: 预测概率→仓位、active bets 平均、离散化、动态限价单仓位。
  keep_level: 中
  repo_mapping: state_template_shell

- cluster_name: 回测与过拟合控制
  what_it_is: 回测不是研究工具、组合 purged CV、合成数据回测、deflated Sharpe ratio。
  keep_level: 高
  repo_mapping: data_engineering_guard / state_template_shell

- cluster_name: 策略风险与资产配置
  what_it_is: 对称/非对称赔付、策略失败概率、HRP（树聚类+递归二分）替代马科维茨。
  keep_level: 高
  repo_mapping: state_template_shell / object_definition_shell

- cluster_name: 结构突变与熵特征
  what_it_is: CUSUM 检验、SADF、爆炸性检验、Shannon/Lempel-Ziv 熵、编码方案。
  keep_level: 中
  repo_mapping: object_definition_shell / future_bucket

- cluster_name: 微观结构特征
  what_it_is: Tick rule、Roll model、Kyle/Amihud/Hasbrouck lambda、VPIN、订单流序列相关。
  keep_level: 中
  repo_mapping: future_bucket / orderflow_future_bucket

### QUANTIZATION_TABLE
| concept | type | minimal_definition | observable_proxy | min_data_requirement | confirmation_timing | quant_status | repo_target | leakage_risk | notes |
|---|---|---|---|---|---|---|---|---|---|
| Triple-Barrier Label | label | 以三个障碍（上止盈/下止损/时间失效）判定事件结果，替代固定时间 horizon | 事件触发后记录哪一障碍先被触碰，标注为 +1/-1/0 | OHLCV | 事件闭合后（障碍触碰或到期） | proxy_quantizable_now | object_definition_shell | low | 需定义障碍宽度；若用日 K 则时间障碍为收盘 |
| Meta-Labeling | label | 第一层模型预测方向；第二层模型预测第一层是否成功 | 第一层预测命中与否作为第二层标签；第二层输出概率用于仓位 | OHLCV/session_calendar | 第一层预测周期结束后 | proxy_quantizable_now | state_template_shell | med | 两层必须不同特征集，避免泄露 |
| Sequential Bootstrap | feature | 按重叠程度动态调整抽样概率，减少冗余样本被重复抽取 | 计算每个标签的并发数 c_t 与平均唯一性 u_t，作为样本权重 | OHLCV/session_calendar | 训练前计算 | proxy_quantizable_now | data_engineering_guard | low | 需知道标签时间区间 [t_i0, t_i1] |
| Fractionally Differentiated d | feature | 通过分数阶差分 d∈(0,1) 使序列平稳同时保留最大记忆 | ADF 检验 p-value < 0.01 的最小 d 值；或固定宽度窗口 fracdiff | OHLCV | 每日收盘后重新估计（若用 expanding window） | proxy_quantizable_now | object_definition_shell | low | A 股必须考虑停牌导致窗口不连续 |
| Purged K-Fold CV | risk_guard | 在交叉验证中清除训练集与测试集之间的重叠区间，防止泄露 | CV 分割时训练集删除与测试集时间重叠的样本，并加 embargo | OHLCV/session_calendar | 模型训练阶段 | proxy_quantizable_now | data_engineering_guard | low | embargo 长度必须 ≥ 策略持有期 |
| Mean Decrease Impurity (MDI) | feature | 随机森林中每个特征对不纯度下降的总贡献，IS 解释性重要性 | sklearn RF 的 feature_importances_ 平均，0 值替换为 np.nan | OHLCV/cross_section | 模型训练后 | proxy_quantizable_now | state_template_shell | med | max_features=1 避免 masking |
| Mean Decrease Accuracy (MDA) | feature | 置换某特征列后 OOS 性能下降幅度，预测性重要性 | purged CV 下置换列并计算负对数损失或 F1 的下降 | OHLCV/cross_section | purged CV 完成后 | proxy_quantizable_now | state_template_shell | med | 对完全相关特征会判定为冗余 |
| Deflated Sharpe Ratio | risk_guard | 用多个独立检验修正后，估计真实 Sharpe 为 0 条件下观察到该 Sharpe 的概率 | 根据试验次数 N、策略间相关性、非正态性调整，计算 PSR 阈值 | OHLCV/session_calendar | 回测完成后 | proxy_quantizable_now | data_engineering_guard | high | 必须准确估计历史尝试次数，否则防御失效 |
| Hierarchical Risk Parity (HRP) | execution_rule | 基于树聚类与递归二分的协方差矩阵不变式资产配置 | quasi-diagonalization 后递归分配权重，不要求协方差可逆 | cross_section/PIT_fundamental | 再平衡时点 | proxy_quantizable_now | state_template_shell | low | A 股行业/风格聚类天然适配 |
| Bet Sizing from Probabilities | execution_rule | 将预测概率通过反凯利或 sigmoid 映射为仓位比例 | active bets 的预测概率 p 加权平均后，sigmoid 转换为 m ∈ [0,1] | OHLCV | 每次预测更新后 | proxy_quantizable_now | state_template_shell | med | 需区分模型概率与真实概率（calibration） |
| CUSUM Filter (Event Sampling) | filter | 累积和超过阈值时触发事件采样，替代均匀时间采样 | 计算收益或波动率的累积偏离，突破 h 时产生 t1 事件 | OHLCV | 盘中实时 | proxy_quantizable_now | object_definition_shell | low | 阈值 h 需根据标的波动率标度化 |
| Supremum ADF (SADF) | feature | 向后扩展窗口的 ADF 上确界，检测周期性崩溃泡沫 | 滚动计算 SADF_t，超过临界值时标记爆炸性状态 | OHLCV | 滚动窗口更新后 | needs_extra_data | object_definition_shell | high | 临界值对样本长度敏感，需蒙特卡洛模拟确定 |
| VPIN (Volume-Synchronized PIN) | feature | 在成交量钟下估计知情交易概率，用订单流不平衡的期望近似 | 成交量 bar 内的 |2vB-1| 滚动平均，vB 为买方体积占比 | tick_trade | 每个成交量 bar 闭合后 | needs_extra_data | orderflow_future_bucket | high | A 股无逐笔成交公开数据，需 level2 或付费终端 |
| Kyle's Lambda | feature | 价格变化对单位订单流的敏感度，反映市场深度/流动性 | 回归 Δp = λ·(S·V) + ε，S 为买卖方向，V 为成交量 | tick_trade/level2_orderbook | 日内交易后 | needs_extra_data | orderflow_future_bucket | high | A 股最小数据为逐笔，且需识别主动买卖方向 |
| Amihud's Lambda | feature | 价格变化对单位美元成交量的敏感度，低流动性代理 | |日收益率| / (成交额 × 收盘价) | OHLCV | 每日收盘后 | proxy_quantizable_now | object_definition_shell | low | A 股可直接用日 K 计算，但横截面可比性需货币单位一致 |

### RETAINED_EXCERPTS
- excerpt_id: EX-02
  source_hint: Chapter 3: Labeling / Meta-Labeling
  quote: >
    
    CHAPTER 2
    Financial Data Structures
    2.1 MOTIV A TION
    In this chapter we will learn how to work with unstructured financial data, and from
    thattoderiveastructureddatasetamenabletoMLalgorithms.Ingeneral,youdonot
    wanttoconsumesomeoneelse’sprocesseddataset,asthelikelyoutcomewillbethat
    you discover what someone else already knows or will figure out soon. Ideally your
    starting point is a collection of unstructured, raw data that you are going to process
    in a way that will lead to informative features.
    2.2 ESSENTIAL TYPES OF FINANCIAL DATA
    Financial data comes in many shapes and forms. Table 2.1 shows the four essential
    typesoffinancialdata,orderedfromlefttorightintermsofincreasingdiversity.Next,
    
  why_kept: 解耦方向预测与仓位预测：第一层学 side，第二层学 size（第一层是否成功）。这是处理低信噪比金融序列的关键设计。
  quant_link: Meta-Labeling

- excerpt_id: EX-03
  source_hint: Chapter 4: Sample Weights / Overlapping Outcomes
  quote: >
    
    36 FINANCIAL DATA STRUCTURES
    inverse variance allocation. Almost all principal components contribute risk, includ-
    ing those with highest variance (components 1 and 2). In contrast, for the PCA port-
    folio, only the component with lowest variance contributes risk.
    Snippet 2.1 implements this method, where the user-defined risk distribution
    R is passed through argumentriskDist (optional None). If riskDist is None,
    the code will assume all risk must be allocated to the principal component with
    smallest eigenvalue, and the weights will be the last eigenvector re-scaled to match
    𝜎(riskTarget).
    SNIPPET 2.1 PCA WEIGHTS FROM A RISK DISTRIBUTION R
    def pcaWeights(cov,riskDist =None,riskTarget=1.):
    #
  why_kept: 金融标签非 IID 的根源：同一收益率被多个标签区间共享。必须保留此段作为样本权重设计的边界条件。
  quant_link: Sequential Bootstrap

- excerpt_id: EX-04
  source_hint: Chapter 4: Sequential Bootstrap
  quote: >
    
    36 FINANCIAL DATA STRUCTURES
    inverse variance allocation. Almost all principal components contribute risk, includ-
    ing those with highest variance (components 1 and 2). In contrast, for the PCA port-
    folio, only the component with lowest variance contributes risk.
    Snippet 2.1 implements this method, where the user-defined risk distribution
    R is passed through argumentriskDist (optional None). If riskDist is None,
    the code will assume all risk must be allocated to the principal component with
    smallest eigenvalue, and the weights will be the last eigenvector re-scaled to match
    𝜎(riskTarget).
    SNIPPET 2.1 PCA WEIGHTS FROM A RISK DISTRIBUTION R
    def pcaWeights(cov,riskDist =None,riskTarget=1.):
    #
  why_kept: 动态抽样概率公式：u_tj^(2) = 1 / (1 + sum 1_tk)。保留公式与实现逻辑，用于重建样本权重模块。
  quant_link: Sequential Bootstrap

- excerpt_id: EX-05
  source_hint: Chapter 5: Fractionally Differentiated Features
  quote: >
    
    THE QUANTAMENTAL WAY 53
    Meta-labelingwillincreaseyourF1-scorebyfilteringoutthefalsepositives,where
    the majority of positives have already been identified by the primary model. Stated
    differently,theroleofthesecondaryMLalgorithmistodeterminewhetherapositive
    from the primary (exogenous) model is true or false. It isnot its purpose to come up
    with a betting opportunity. Its purpose is to determine whether we should act or pass
    on the opportunity that has been presented.
    Meta-labeling is a very powerful tool to have in your arsenal, for four additional
    reasons. First, ML algorithms are often criticized as black boxes (see Chapter 1).
    Meta-labelingallowsyoutobuildanMLsystemontopofawhitebox(likea
  why_kept: 核心论证：整数差分使序列平稳但抹除记忆，导致残差信噪比进一步恶化。fracdiff 保留记忆的论证必须保留。
  quant_link: Fractionally Differentiated d

- excerpt_id: EX-06
  source_hint: Chapter 7: Cross-Validation
  quote: >
    
    78 FRACTIONALLY DIFFERENTIATED FEATURES
    1 .00
    0.75
    0.50
    0.25
    0.00
    –0.25
    –0.50
    –0.75
    –1 .00
    012
    0.0
    0.25
    0.5
    0.75
    1. 0
    345
    FIGURE 5.1 𝜔k (y-axis) ask increases (x-axis). Each line is associated with a particular value ofd ∈
    [0,1], in 0.1 increments.
    When d is a positive integer number,∏ k−1
    i=0
    d−i
    k! = 0,∀k > d, and memory beyond
    that point is cancelled. For example, d = 1 is used to compute returns, where∏ k−1
    i=0
    d−i
    k! = 0,∀k > 1, and𝜔={ 1,−1,0,0, …} .
    5.4.2 Iterative Estimation
    Lookingatthesequenceofweights, 𝜔,wecanappreciatethatfor k = 0,… ,∞,with
    𝜔0 = 1, the weights can be generated iteratively as:
    𝜔k =−𝜔k−1
    d−k+1
    k
    Figure 5.1 plots the sequence of weights used to compute each value o
  why_kept: 标准 K-Fold 在金融数据失效的原因：序列相关特征 + 重叠标签导致训练集向测试集泄露信息。
  quant_link: Purged K-Fold CV

- excerpt_id: EX-07
  source_hint: Chapter 8: Feature Importance / MDI
  quote: >
    
    STATIONARITY WITH MAXIMUM MEMORY PRESERVATION 87
    EO1 Index −0.6561 −1.0567 −1.7409 −2.6774 −3.8543 −5.5096 −7.9133 −10.5674 −15.6442 −21.3066 −35.1397
    ER1 Comdty −0.1970 −0.3442 −0.6334 −1.0363 −1.5327 −2.2378 −3.2819 −4.4647 −7.1031 −10.7389 −40.0407
    ES1 Index −0.3387 −0.7206 −1.3324 −2.2252 −3.2733 −4.7976 −7.0436 −9.6095 −14.8624 −21.6177 −46.9114
    FA1 Index −0.5292 −0.8526 −1.4250 −2.2359 −3.2500 −4.6902 −6.8272 −9.2410 −14.1664 −20.3733 −41.9705
    FC1 Comdty −1.8846 −2.1853 −2.8808 −3.8546 −5.1483 −7.0226 −9.6889 −12.5679 −17.8160 −23.0530 −31.6503
    FV1 Comdty −0.7257 −0.8515 −1.0596 −1.4304 −1.8312 −2.5302 −3.6296 −4.9499 −7.8292 −12.0467 −49.1508
    G 1 Comdty 0.2326 0.0026 −0.4686 −1.0590
  why_kept: MDI 是 IS 解释性方法，必须设置 max_features=1 避免 masking；0 重要性应替换为 np.nan 而非参与平均。
  quant_link: Mean Decrease Impurity (MDI)

- excerpt_id: EX-08
  source_hint: Chapter 8: Feature Importance / MDA
  quote: >
    
    STATIONARITY WITH MAXIMUM MEMORY PRESERVATION 87
    EO1 Index −0.6561 −1.0567 −1.7409 −2.6774 −3.8543 −5.5096 −7.9133 −10.5674 −15.6442 −21.3066 −35.1397
    ER1 Comdty −0.1970 −0.3442 −0.6334 −1.0363 −1.5327 −2.2378 −3.2819 −4.4647 −7.1031 −10.7389 −40.0407
    ES1 Index −0.3387 −0.7206 −1.3324 −2.2252 −3.2733 −4.7976 −7.0436 −9.6095 −14.8624 −21.6177 −46.9114
    FA1 Index −0.5292 −0.8526 −1.4250 −2.2359 −3.2500 −4.6902 −6.8272 −9.2410 −14.1664 −20.3733 −41.9705
    FC1 Comdty −1.8846 −2.1853 −2.8808 −3.8546 −5.1483 −7.0226 −9.6889 −12.5679 −17.8160 −23.0530 −31.6503
    FV1 Comdty −0.7257 −0.8515 −1.0596 −1.4304 −1.8312 −2.5302 −3.6296 −4.9499 −7.8292 −12.0467 −49.1508
    G 1 Comdty 0.2326 0.0026 −0.4686 −1.0590
  why_kept: MDA 是 OOS 预测性方法；对完全相同的两个特征，MDA 会判定两者均冗余——这是 substitution effect 的陷阱。
  quant_link: Mean Decrease Accuracy (MDA)

- excerpt_id: EX-09
  source_hint: Chapter 10: Bet Sizing
  quote: >
    
    FEATURE IMPORTANCE WITH SUBSTITUTION EFFECTS 115
    decreased. Therefore, we can derive for each decision tree how much of the overall
    impuritydecreasecanbeassignedtoeachfeature.Andgiventhatwehaveaforestof
    trees,wecanaveragethosevaluesacrossallestimatorsandrankthefeaturesaccord-
    ingly. See Louppe et al. [2013] for a detailed description. There are some important
    considerations you must keep in mind when working with MDI:
    1. Masking effects take place when some features are systematically ignored
    by tree-based classifiers in favor of others. In order to avoid them, set
    max_features=int(1)whenusingsklearn’sRFclass.Inthisway,onlyone
    random feature is considered per level.
    (a) Every feature is giv
  why_kept: 将预测概率转化为仓位的公式：m = 2Z[p] - 1，其中 Z[p] 是标准正态 CDF。保留公式用于仓位状态模板。
  quant_link: Bet Sizing from Probabilities

- excerpt_id: EX-10
  source_hint: Chapter 14: Backtest Statistics / Deflated Sharpe
  quote: >
    
    EXPERIMENTAL RESULTS 177
    are represented in grayscale (lighter indicating better performance; darker indicat-
    ing worse performance), in a format known as a heat-map. Performance (𝜋i,Ti)i s
    computed per unit held (mi = 1), since other values ofmi would simply re-scale per-
    formance,withnoimpactontheSharperatio.Transactioncostscanbeeasilyadded,
    but for educational purposes it is better to plot results without them, so that you can
    appreciate the symmetry of the functions.
    13.6.1 Cases with Zero Long-Run Equilibrium
    Cases with zero long-run equilibrium are consistent with the business of market-
    makers,whoprovideliquidityundertheassumptionthatpricedeviationsfromcurrent
    levelswillcorrectthemse
  why_kept: 修正选择偏差后的 Sharpe：DSR = PSR(π0, π*, σ_FSR, T, N...)。保留公式与参数定义用于回测护栏。
  quant_link: Deflated Sharpe Ratio

- excerpt_id: EX-11
  source_hint: Chapter 16: Machine Learning Asset Allocation
  quote: >
    
    GENERAL CHARACTERISTICS 197
    trades,ifeverytradeinvolvesflippingthepositionbetweenmaximumlongand
    maximum short.
    r Correlation to underlying:This is the correlation between strategy returns
    and the returns of the underlying investment universe. When the correlation is
    significantly positive or negative, the strategy is essentially holding or short-
    selling the investment universe, without adding much value.
    Snippet14.1listsanalgorithmthatderivesthetimestampsofflatteningorflipping
    trades from a pandas series of target positions (tPos). This gives us the number of
    bets that have taken place.
    SNIPPET 14.1 DERIVING THE TIMING OF BETS FROM A SERIES
    OF TARGET POSITIONS
    # A bet takes place between f
  why_kept: HRP 解决马科维茨三大问题：不稳定性、集中性、样本内表现差。不要求协方差矩阵可逆。
  quant_link: Hierarchical Risk Parity (HRP)

- excerpt_id: EX-12
  source_hint: Chapter 16: HRP Algorithm
  quote: >
    
    GENERAL CHARACTERISTICS 197
    trades,ifeverytradeinvolvesflippingthepositionbetweenmaximumlongand
    maximum short.
    r Correlation to underlying:This is the correlation between strategy returns
    and the returns of the underlying investment universe. When the correlation is
    significantly positive or negative, the strategy is essentially holding or short-
    selling the investment universe, without adding much value.
    Snippet14.1listsanalgorithmthatderivesthetimestampsofflatteningorflipping
    trades from a pandas series of target positions (tPos). This gives us the number of
    bets that have taken place.
    SNIPPET 14.1 DERIVING THE TIMING OF BETS FROM A SERIES
    OF TARGET POSITIONS
    # A bet takes place between f
  why_kept: 树聚类→准对角化→递归二分。保留距离度量 d = sqrt(0.5(1-ρ)) 与链接准则定义。
  quant_link: Hierarchical Risk Parity (HRP)

- excerpt_id: EX-13
  source_hint: Chapter 17: Structural Breaks / SADF
  quote: >
    
    FROM GEOMETRIC TO HIERARCHICAL RELATIONSHIPS 225
    10
    9
    8
    7
    6
    5
    4
    3
    2
    1
    0
    49
    48
    47
    46
    45
    44
    43
    42
    41
    40
    39383736
    35
    34
    33
    32
    31
    30
    29
    28
    27
    26
    25
    24
    23
    22
    21
    20
    19
    18
    17
    16
    15 14 13 12 11
    (a)
    (b)
    13
    18
    14
    15
    4
    5
    17
    31
    10
    33
    32
    38
    37
    39
    36
    35 34
    11
    12 3
    16 1
    0
    6
    21
    20
    19
    2
    7
    23 22
    24
    8
    9
    28
    29
    30
    26
    2527
    FIGURE 16.2 The complete-graph (top) and the tree-graph (bottom) structures
    Correlation matrices can be represented as complete graphs, which lack the notion of hierarchy: Each
    investment is substitutable with another. In contrast, tree structures incorporate hierarchical relationships.
    
    --- PAGE 253 ---
    226 MACHINE LEARNING ASSET ALLOCATION
    in {1,… ,i,… ,N}. This allows us to compute an NxN d
  why_kept: SADF 通过向后扩展窗口的上确界检测周期性崩溃泡沫。保留回归设定与统计量定义。
  quant_link: Supremum ADF (SADF)

- excerpt_id: EX-14
  source_hint: Chapter 19: Microstructural Features / VPIN
  quote: >
    
    EXPLOSIVENESS TESTS 259
    if constant! ='nc':
    x=np.append(x,np.ones((x.shape[0],1)),axis=1)
    if constant[:2] =='ct':
    trend=np.arange(x.shape[0]).reshape(-1,1)
    x=np.append(x,trend,axis=1)
    if constant =='ctt':
    x=np.append(x,trend**2,axis=1)
    return y,x
    Snippet17.3listsfunction lagDF,whichappliestoadataframethelagsspecified
    in its argumentlags.
    SNIPPET 17.3 APPLY LAGS TO DATAFRAME
    def lagDF(df0,lags):
    df1=pd.DataFrame()
    if isinstance(lags,int):lags =range(lags+1)
    else:lags=[int(lag) for lag in lags]
    for lag in lags:
    df_=df0.shift(lag).copy(deep=True)
    df_.columns=[str(i)+'_'+str(lag) for i in df_.columns]
    df1=df1.join(df_,how='outer')
    return df1
    Finally, Snippet 17.4 lists function getBetas, which
  why_kept: VPIN = E[|2vB-1|] 在成交量钟下的知情交易概率近似。保留公式与订单流不平衡定义。
  quant_link: VPIN (Volume-Synchronized PIN)

- excerpt_id: EX-15
  source_hint: Chapter 19: Tick Rule
  quote: >
    
    EXPLOSIVENESS TESTS 259
    if constant! ='nc':
    x=np.append(x,np.ones((x.shape[0],1)),axis=1)
    if constant[:2] =='ct':
    trend=np.arange(x.shape[0]).reshape(-1,1)
    x=np.append(x,trend,axis=1)
    if constant =='ctt':
    x=np.append(x,trend**2,axis=1)
    return y,x
    Snippet17.3listsfunction lagDF,whichappliestoadataframethelagsspecified
    in its argumentlags.
    SNIPPET 17.3 APPLY LAGS TO DATAFRAME
    def lagDF(df0,lags):
    df1=pd.DataFrame()
    if isinstance(lags,int):lags =range(lags+1)
    else:lags=[int(lag) for lag in lags]
    for lag in lags:
    df_=df0.shift(lag).copy(deep=True)
    df_.columns=[str(i)+'_'+str(lag) for i in df_.columns]
    df1=df1.join(df_,how='outer')
    return df1
    Finally, Snippet 17.4 lists function getBetas, which
  why_kept: 用价格变动方向判定成交主动方：Δp>0 为买发起，Δp<0 为卖发起，Δp=0 继承前一 tick 方向。
  quant_link: Tick Rule (Event Sampling)

- excerpt_id: EX-16
  source_hint: Chapter 1: Meta-Strategy Paradigm
  quote: >
    Every successful quantitative firm I am aware of applies the meta-strategy paradigm. Accordingly, this book was written as a research manual for teams, not for individuals. Through its chapters you will learn how to set up a research factory, as well as the various stations of the assembly line.
  why_kept: 全书的方法论根基：量化研究必须以工厂/团队方式组织，个体'单兵作战'必然失败。决定 repo 的组织方式（data/object/state 分层）。
  quant_link: Meta-Labeling

- excerpt_id: EX-17
  source_hint: Chapter 11: Dangers of Backtesting
  quote: >
    Backtesting Is Not a Research Tool. A common misconception is to view backtesting as a tool for researching the markets. Backtesting is not a research tool. It is a way to verify a discovery that has been made through other scientific methods.
  why_kept: 回测不是研究工具，而是验证工具。这个边界条件决定了策略开发流程：feature→model→paper trading→backtest，而不是 backtest-driven research。
  quant_link: Deflated Sharpe Ratio

- excerpt_id: EX-18
  source_hint: Chapter 12: Backtesting through CV
  quote: >
    The Combinatorial Purged Cross-Validation Method. The goal of CPCV is to generate multiple backtest paths, each with a different combination of training and testing sets. This allows us to estimate the distribution of the strategy's performance under different scenarios.
  why_kept: CPCV 生成多条回测路径，每条路径使用不同的训练/测试组合。保留算法逻辑用于回测状态模板。
  quant_link: Purged K-Fold CV

- excerpt_id: EX-19
  source_hint: Chapter 7: Embargo
  quote: >
    
    78 FRACTIONALLY DIFFERENTIATED FEATURES
    1 .00
    0.75
    0.50
    0.25
    0.00
    –0.25
    –0.50
    –0.75
    –1 .00
    012
    0.0
    0.25
    0.5
    0.75
    1. 0
    345
    FIGURE 5.1 𝜔k (y-axis) ask increases (x-axis). Each line is associated with a particular value ofd ∈
    [0,1], in 0.1 increments.
    When d is a positive integer number,∏ k−1
    i=0
    d−i
    k! = 0,∀k > d, and memory beyond
    that point is cancelled. For example, d = 1 is used to compute returns, where∏ k−1
    i=0
    d−i
    k! = 0,∀k > 1, and𝜔={ 1,−1,0,0, …} .
    5.4.2 Iterative Estimation
    Lookingatthesequenceofweights, 𝜔,wecanappreciatethatfor k = 0,… ,∞,with
    𝜔0 = 1, the weights can be generated iteratively as:
    𝜔k =−𝜔k−1
    d−k+1
    k
    Figure 5.1 plots the sequence of weights used to compute each value o
  why_kept: Embargo 在测试集后追加一段禁入期，防止因时间邻近导致的隐形泄露。
  quant_link: Purged K-Fold CV

- excerpt_id: EX-20
  source_hint: Chapter 4: Time Decay
  quote: >
    Return Attribution and Time Decay. Observations that are far in the past should be given less weight than recent observations, because the market regime may have changed.
  why_kept: 时间衰减：旧样本权重下降，因市场 regime 可能已切换。用于样本权重状态模板。
  quant_link: Sequential Bootstrap

### FORMULAS_AND_ALGOS

**1. Triple-Barrier Labeling (Chapter 3)**
```
For each event i starting at t_i0:
  upper_barrier = p_t0 + g × σ(t0)   [profit taking]
  lower_barrier = p_t0 - g × σ(t0)   [stop loss]
  time_barrier  = t0 + ΔT            [max holding]
  y_i = +1 if upper touched first
  y_i = -1 if lower touched first
  y_i =  0 if time barrier expires first (or vertical)
```
- g: user-defined width (e.g., 2× daily volatility)
- σ(t0): realized volatility estimated at t0
- 失效条件：障碍宽度 g 若用未来信息估计，则产生前视偏差（future function）

**2. Meta-Labeling (Chapter 3)**
```
Primary model M1: predicts side (long/short) → signal s_t ∈ {+1, -1}
Secondary model M2: predicts whether M1's bet is successful
  X2 uses different features from X1
  y2 = 1 if M1's bet hits the profit-taking barrier before stop-loss
  y2 = 0 otherwise
Bet size m_t = 2 × Z[p2] - 1, where Z is standard normal CDF
```
- M1 与 M2 必须特征隔离，否则 M2 直接复制 M1 的预测
- 适用条件：M1 有方向性优势但胜率 < 1；M2 提升 calmar 而非 sharpe

**3. Sequential Bootstrap Uniqueness (Chapter 4)**
```
1_t,i = 1 if [t_i0, t_i1] overlaps [t-1, t]
c_t = Σ_i 1_t,i          [number of concurrent labels at t]
u_t,i = 1_t,i / c_t      [uniqueness of label i at t]
ū_i = (Σ_t u_t,i) / (Σ_t 1_t,i)   [average uniqueness of label i]
```
- 使用 max_samples = mean(ū_i) 在 sklearn BaggingClassifier 中控制冗余
- 失效条件：若未记录每个标签的 [t0, t1] 区间，则无法计算 u_t,i

**4. Fractionally Differentiated d (Chapter 5)**
```
X_t^(d) = Σ_{k=0}^{∞} w_k X_{t-k}
w_k = w_{k-1} × (k - 1 - d) / k
with w_0 = 1

Fixed-width window: keep only τ coefficients where |w_k| > threshold
Optimal d: smallest d such that ADF test on X_t^(d) rejects unit root at 1%
```
- 迭代估计避免计算阶乘；窗口固定防止历史漂移
- 失效条件：序列存在结构突变时，单一 d 不足以描述全样本

**5. Deflated Sharpe Ratio (Chapter 14)**
```
DSR = PSR(SR*, SR0, σ_FSR, T, N)
where:
  SR*  = observed Sharpe ratio
  SR0  = expected Sharpe under null (often 0)
  σ_FSR = standard deviation of SR estimates across N trials
  T    = number of returns observations
  N    = number of independent trials / backtests conducted
```
- N 必须准确估计所有尝试的策略数，包括未报告的失败实验
- 失效条件：若策略间存在相关性，σ_FSR 需用相关性矩阵修正

**6. HRP Recursive Bisection (Chapter 16)**
```
Stage 1: Tree Clustering
  d_i,j = sqrt(0.5 * (1 - ρ_i,j))
  linkage: argmin_{i≠j} d̃_i,j → form cluster u
  update d̃ using nearest-point algorithm (single linkage)

Stage 2: Quasi-Diagonalization
  reorder columns of covariance matrix by cluster leaves

Stage 3: Recursive Bisection
  for each cluster [left, right]:
    V_left  = diag(Σ_left)^-1
    V_right = diag(Σ_right)^-1
    α_left  = V_left / (V_left + V_right)
    w_left  *= α_left; w_right *= (1 - α_left)
```
- 不要求 Σ 可逆；对 singular cov matrix 仍可分配
- 失效条件：若输入为价格序列而非收益率，距离度量需调整

### NOT_QUANT_YET
1. **Quantum Combinatorial Optimization (Chapter 21)** — 当前量子计算硬件尚未成熟到可执行金融组合优化；记录为 future_bucket，不做对象壳。
2. **非均匀快速傅里叶变换（NUFFT）在闪崩检测中的应用** — 依赖 sub-millisecond 时间戳与原始撮合数据，A 股无公开数据源；标为 future_bucket。
3. **Kyle/Hasbrouck Lambda 的日内估计** — 需要 level2 orderbook 与逐笔委托/成交数据，A 股当前仅对付费终端开放；标为 needs_extra_data。
4. **Order Size Distribution / Cancellation Rates** — 需要完整 FIX 消息流或交易所原始归档数据，A 股 level2 切片不完整；标为 needs_extra_data。
5. **Lempel-Ziv 熵的实时计算** — 需要高频符号序列（tick rule 编码），在日线/分钟线粒度下信息含量过低；标为 shell_only（有公式但缺数据）。

### NEXT_ACTION
1. 立即生成 `triple_barrier_label` 对象定义壳（含 t0, t1, upper, lower, time_barrier 字段与闭合判定逻辑）。
2. 立即生成 `meta_labeling_state` 模板（M1 方向层 + M2 成功概率层 + bet_size 输出层）。
3. 补全 A 股交易日历与停牌标记数据，用于 sequential bootstrap 的并发区间计算。
4. 生成 `purged_kfold_cv` 护栏代码（embargo 长度参数化、训练集重叠删除逻辑）。
5. 生成 `deflated_sharpe_guard` 模块：输入回测 Sharpe 与试验次数 N，输出 boolean 通过/拒绝。
6. 生成 `hrp_allocator` 对象壳：输入协方差矩阵，输出权重向量（支持树聚类+递归二分）。
7. 收集 A 股 level2 数据供应商清单（如 Wind、同花顺 iFinD、交易所数据文件），评估逐笔/VPIN 可行性。
8. 继续切割 Algorithmic Trading (E. Chan) 作为方向性策略与均值回复策略的对比素材。