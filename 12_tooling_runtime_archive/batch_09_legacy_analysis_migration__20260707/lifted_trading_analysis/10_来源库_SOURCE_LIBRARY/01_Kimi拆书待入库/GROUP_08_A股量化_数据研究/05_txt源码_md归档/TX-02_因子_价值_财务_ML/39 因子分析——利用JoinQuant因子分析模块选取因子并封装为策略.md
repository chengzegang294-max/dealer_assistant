# 39 因子分析——利用JoinQuant因子分析模块选取因子并封装为策略

- source_type: txt_strategy_sample_raw
- project_role: A股 future research/data capability
- origin_path: D:\Stock\trading_assistant\12_tooling_runtime_archive\batch_09_legacy_analysis_migration__20260707\lifted_trading_analysis\10_来源库_SOURCE_LIBRARY\01_Kimi拆书待入库\GROUP_08_A股量化_数据研究__SOURCE_RAW\新的参考书\《Python股票量化交易从入门到实践》完整版\1.量化策略代码(99份)（赠品）\39 因子分析——利用JoinQuant因子分析模块选取因子并封装为策略.txt
- origin_encoding_guess: gb18030
- cluster_id: TX-02
- cluster_name: 因子/价值/财务/机器学习

```text
该策略由聚宽用户分享，仅供学习交流使用。
原文网址：https://www.joinquant.com/post/11044

原文一般包含策略说明，如有疑问建议到原文和作者交流讨论。


原文策略源码如下：

import pandas as pd
import jqdata

def initialize(context):
    g.index='000300.XSHG'
    set_option('use_real_price', True)
    set_order_cost(OrderCost(open_tax=0, close_tax=0, open_commission=0, close_commission=0, close_today_commission=0, min_commission=0), type='stock')
    set_benchmark('000300.XSHG')
    
def calalpha(context):
    stock_list=get_index_stocks(g.index)
    dt=context.previous_date
    df = get_price(stock_list,end_date=dt,count=1,fields=['money'])
    df = df['money'].T
    df.columns=['alpha']
    result=df.sort(['alpha'],ascending=False)
    return result
    
def before_trading_start(context):
    result=list((calalpha(context)['alpha'].iloc[0:40]).keys())
    g.result=result
    
def handle_data(context, data):
    tobuy_list=g.result
    holdings=context.portfolio.positions.keys()
    for stock in  holdings:
        if stock not in tobuy_list:
            print('----------')
            print(stock,'Shorting')
            order_target_value(stock,0)
        else:
            print('----------')
            print(stock,'Longing')
    cash=context.portfolio.cash
    num=len(tobuy_list)
    for eachsec in tobuy_list:
        order_value(eachsec,int(cash/num))
    
    
```
