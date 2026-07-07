# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = chapter17

---

CHAPTER 17
The Portfolios’ Performance
Beneath the good so far—but far above the great
.
—Thomas Gray
17.1 INTRODUCTION
In this chapter we present the historical performance results of the selected portfolio strategies that we discussed in
Chapter 16
. Our baseline strategy was to create an optimized tracking portfolio that maximized the excess expected return of the portfolio subject to a tracking-error constraint of 5%. In addition to the tracking-error constraint, we imposed three additional constraints: a full-investment constraint, a no-short-selling constraint, and a trading-volume constraint. We implemented our baseline strategy using the economic factor model, the fundamental factor model, and the aggregate Z-score model.
In addition to the baseline strategy, we also performed backtests on 11 additional strategies. These alternative strategies that created our portfolios were based on different levels of tracking error, sector weight and factor exposure matching; transactions costs and tax management; leverage; and market neutrality. The performance statistics of the strategies will give readers an idea of the types of statistics that are relevant to quantitative equity portfolio management (QEPM) and how to interpret them properly. Of course, the reader also may be interested in how these specific
strategies worked with our particular historical data set. The first section of the chapter discusses the results of the baseline strategy plus the first four variations implemented with the fundamental factor model, the aggregate Z-score model, and the economic factor model. It also includes a detailed performance attribution for one of the portfolios. The remaining four sections of the chapter look at the remaining portfolios.
17.2 THE PERFORMANCE OF THE BASELINE PORTFOLIO AND VARIATIONS
In this section we present the performance statistics of the baseline strategy and four variations that alter either the tracking error, sector weight matching, or factor exposure matching.
17.2.1 The Fundamental Factor Model Performance
Table 17.1
shows the historical performance of the portfolio strategies based on the fundamental factor model. Five portfolios were created at the end of each month between December 2010 and November 2020. The portfolios came from the same model and the same set of factors but were subject to different constraints. The first three portfolios were subject to the tracking-error constraints of 2%, 5%, and 10% per annum, respectively. The fourth portfolio was subject to the tracking-error constraint of 5%; in addition, it was constrained to have the sector weights identical to those of the benchmark.
1
The fifth portfolio was also subject to the tracking-error constraint of 5%; in addition, it was constrained to have the factor exposures identical to those of the benchmark.
TABLE 17.1
Historical Performance of the Fundamental Factor Model
The first row in the table shows the average return of each portfolio. Return figures are annualized monthly returns. For example, the portfolio with a target tracking error of 2% per annum has an average monthly return of 1.44975%, which translates to an average annualized monthly return of 17.397%. That is, an investment in this portfolio at the beginning of the investment period would have
provided the investor with an average return of about 17.397% per year. We can see that, as expected, the average return of the portfolio increases when the target tracking error increases because we are taking more risk in constructing the portfolio.
The fifth row shows the average excess return of the various portfolios. In all cases, the average excess return is positive, which is reassuring because our goal was to create portfolios with the
highest possible excess return subject to the tracking-error constraint. The minimum average excess return of 0.34% came from the factor-matched portfolio. The other portfolios have an even higher excess return.
The second and the sixth rows show the standard deviation of the portfolio return and the ex-post (i.e., realized) tracking error of the portfolio, respectively. All standard deviations have been annualized. Thus the standard deviation of 15.309% reflects a standard deviation of monthly returns of 4.419% (15.309/
). Roughly speaking, there is less than a 2.5% probability that the annual return of this particular portfolio will be worse than −13.22% (=17.40 − 2 × 15.31). One also will notice that an increasing average return of the portfolio is accompanied by an increasing standard deviation of returns, which confirms the basic idea of financial theory that risk and return are positively related to each other. For quantitative portfolio managers, the most important measure of risk is the risk versus the benchmark, summed up by the tracking error. Although our portfolios had ex-ante tracking errors of 2%, 5%, or 10%, their ex-post tracking errors were 5.020%, 10.275%, and 15.850%, respectively. Although there are discrepancies because the model cannot exactly describe future stock returns, as our ex-ante tracking error increases, so does our ex-post tracking error. We have some degree of control over the ex-post tracking error of our optimized portfolios.
2
The worst and best monthly returns over the entire backtesting period are also given in the table. These statistics supplement the standard deviation risk measure and can be useful in explaining the amount of risk in the portfolio to nonquantitative investors.
The rows titled
and
show the estimated
α
and
β
of the tracking portfolios with respect to the benchmark. They are the constant (
α
) and coefficient (
β
) in a regression of the tracking portfolio returns on the benchmark returns. The key variable for portfolio managers is the
α
with respect to the benchmark (
α
B
). Except for the factor-matched portfolio, all the portfolios have positive values of
α
B
. The portfolio with a 2% tracking error has a
β
B
close to 1, so most of its excess return over the benchmark is coming from stock picking, not from increased risk vis-à-vis the benchmark. Quantitative managers also focus on the information ratio (
IR
), which measures the
excess return of the portfolio, as measured by
α
B
divided by the residual risk of the portfolio. The information ratios of all the portfolios, except for the factor-matched portfolio, are very similar, even though their
α
B
values differ.
There are many sources of a positive benchmark
α
. One of these is the multifactor
α
,
, which is the part of the excess return that is not due to any of the pricing factors that the stock return model identified. It is possible that the multifactor
α
of a portfolio is larger than its benchmark
α
since factor exposures and factor premiums may have a negative sign.
The last row shows the Sharpe ratio, another measure of the risk-adjusted average return. All our portfolios, except for the factor-matched portfolio, have a higher Sharpe ratio than the benchmark does, which suggests that they are more efficient than the benchmark. The sector-matched portfolio is the most efficient according to the Sharpe ratio.
Overall, the following conclusions can be drawn from the results of our historical backtests:
1.
The optimized tracking portfolios achieve positive average excess returns over the benchmark, ranging from 0.3% to 11.1% per annum.
2.
Using multifactor stock return models can control the ex-post tracking error to some extent by optimizing the ex-ante target tracking error.
3.
Much of the average excess return of the portfolios over the benchmark is attributable to benchmark
α
.
4.
The information ratios of the portfolios can be as high as 0.5 on an annualized basis. Thus, for every 1% additional excess risk per year, the portfolios provide more than 0.5% in additional excess returns.
5.
The Sharpe ratios of many of our portfolios are higher than that of the benchmark, indicating that our stock-selection methodology may create portfolios that earn more than the benchmark on a risk-adjusted basis.
17.2.2 The Aggregate Z-Score Model Performance
Table 17.2
shows the historical performance of the portfolio strategy based on the aggregate Z-score model. The format of this
table is identical to the preceding table, so we will just comment briefly on the salient results.
TABLE 17.2
Historical Performance of the Aggregate Z-Score Model
In terms of the average return and the average excess return, the portfolios based on the aggregate Z-score model perform similarly to the portfolios based on the fundamental factor model. The average excess return ranges from 14.324% per annum to 25.008%
per annum, which is not very different from what we obtained from the fundamental factor model.
The standard deviation of returns and the ex-post tracking error also remain at about the same level. Given the similarities in average returns and standard deviations, the information ratio and Sharpe ratio are also comparable to those of the fundamental factor model.
While the overall performance of the aggregate Z-score model portfolios is comparable to that of the fundamental factor model portfolios, some differences can be noticed when we look at the individual portfolios more carefully. For example, the sector-matched portfolio has a higher Sharpe ratio in the case of the aggregate Z-score model, whereas the 2% tracking-error portfolio achieves a slightly better risk-return combination in the case of the fundamental factor model.
17.2.3 The Economic Factor Model Performance
Table 17.3
shows the historical performance of the portfolio strategies based on the economic factor model.
TABLE 17.3
Historical Performance of the Economic Factor Model
Compared with the portfolios built with the fundamental factor model and aggregate Z-score model, the performance of the portfolios based on the economic factor model are somewhat disappointing. Take, for instance, the portfolio with a tracking-error constraint of 2%. Using the economic factor model, this portfolio’s average excess return is comparatively small at 1.006% per annum. Its ex-post tracking error, at 4.869%, is not much smaller than it is using the other models. All the economic factor model portfolios’
α
B
values are close to zero or negative, suggesting that the portfolio strategy actually performed quite poorly at stock picking vis-à-vis the benchmark. The information ratios are all close to zero or negative, and the Sharpe ratios are below that of the benchmark. In summary, our economic factor model portfolios underperformed our benchmark on a risk-adjusted basis over the backtesting period.
17.2.4 Performance Reports for Distribution
In addition to the raw performance results produced for each model in the preceding subsections, portfolio departments may wish to produce other performance reports for internal or external
distribution.
3
Below we provide examples of those types of reports for our backtested portfolios.
Table 17.4
compares the various period returns and the annual returns together with risk measures for three tracking portfolios with a 5% target tracking error.
TABLE 17.4
Summary Portfolio Performance
The period returns were calculated counting the years of the period backward. Thus the one-year return is the return for the
year 2020, the three-year return is the return for years 2018 through 2020, and so on. For all selected periods, the returns of the three tracking portfolios are higher than the benchmark return. This is a very significant result. We already learned that all our optimized portfolios provided average excess returns, but what is more impressive is that they consistently obtain higher returns over various return horizons (one-, three-, five-, and ten-year periods). There are some individual years in which the portfolios do not beat the benchmark, but these are the exception rather than the rule. For many years, each of the tracking portfolios outperforms the benchmark. The portfolios based on the fundamental factor model and the Z-score model outperform the benchmark for eight and seven of the 10 years, respectively. The portfolio based on the economic factor model outperforms the benchmark five of nine years.
The last three rows of the table display different measures of risk. In terms of the total risk (measured by the standard deviation of the return) and the tracking error, the fundamental factor model is the riskiest. However, in terms of the systematic risk (represented by
), the portfolio based on the economic factor model is the riskiest.
Although we have already considered the ex-ante and ex-post tracking error, we provide a table specifically dedicated to examining how well our models controlled the ex-post tracking error (
Table 17.5
). As stated before, the ex-ante and ex-post tracking errors do not exactly match because the model cannot anticipate returns exactly. The ex-post tracking error is much higher than we expected. Nevertheless, the ex-ante and ex-post values are related, and by lowering the ex-ante tracking error, we also can lower the ex-post tracking error.
TABLE 17.5
Tracking-Error Analysis
Comparing the performance of the three optimized tracking portfolios, we can make the following conclusions:
1.
The tracking portfolios achieve a positive average excess return over the benchmark for the period we examined. Also, the tracking portfolios achieve a positive excess return over the benchmark for each of the one-, three-, five-, and 10-year period returns.
2.
Most of the positive average excess return is due to benchmark
α
rather than benchmark
β
.
3.
The tracking portfolios based on the fundamental factor model and the Z-score model perform better than the tracking portfolio based on the economic factor model for the period we examined.
4.
The ex-post tracking error is closest to the ex-ante tracking error for the portfolio based on the economic factor model.
5.
While the ex-post tracking error is positive, the actual risk faced by the benchmark manager may be lower than the ex-post tracking error suggests because each period’s excess return is positive.
17.2.5 Performance Attribution for the Fundamental Factor Model Baseline Portfolio
In this subsection we look in detail at the results of the portfolio based on the fundamental factor model for December 2020, applying performance attribution techniques discussed in
Chapter 15
. The classical performance attribution, shown in
Table 17.6
, identifies
the portfolio return in each economic sector and then breaks down the excess return into its two parts: the part due to the sector weights and the part due to the within-sector security weights. We chose to use the two-digit sector breakdown according to Standard & Poor’s Global Industry Classification Standard (GICS).
TABLE 17.6
Classical Performance Attribution for a December 2020 Portfolio
Looking at the table, we see that in absolute terms the information technology sector has the highest sector weight of 30.2% in our portfolio. Relative to the benchmark, however, the health care sector has the highest active weight (19.3% for the portfolio versus 13.6% for the benchmark). The return of the health care sector in the benchmark was not small, but not much higher than the other sectors’ returns, so on first inspection it is unclear whether our overweighting of the health care sector was a good choice. The returns from the particular health care sector stocks in our portfolio are quite high (6.99%) compared with the returns of the health care stocks included in the benchmark (3.98%). This shows that our quantitative model was able to select superior stocks within the health care sector for the month of December 2020. Of course, the tracking portfolio sometimes selects “wrong” sectors and “wrong” stocks. For example, the tracking portfolio gave a higher weight to the underperforming utility sector than the benchmark did. Overall, though, our optimized tracking portfolio outperformed the benchmark in December 2020 by 2.726%. The table also shows the overall asset allocation effect (
AE
) and the security selection effect (
SSE
). The former effect, −0.284%, reflects our model’s poor performance in terms of selecting good sectors of the stock market, but the latter effect, 3.010%, shows our model to be quite capable of picking good stocks within a sector.
Quantitative equity portfolio managers may be more concerned with multifactor performance attribution than with the classical attribution, as discussed in
Chapter 15
. In
Table 17.7
we present the multifactor performance attribution. The excess total returns of the portfolio over the benchmark for December 2020 are mainly due to a positive
attribution α
. Attribution
α
is the residual error in that month (i.e., the part of the return that is not explained by the factors).
4
During the month of December 2020, the portfolio achieved an excess return over the benchmark of 2.726%, of which 2.266% was due to attribution
α
. The remainder is attributed to the
exposure to five factors. The exposure to EBITDAEV and SUE had a positive contribution to the excess return, while the exposure to BB, PSL, and TP3M had a negative contribution to the portfolio excess return. Most of the overall risk also was attributable to portfolio-specific diversifiable risk rather than to risk caused by exposure to certain factors.
TABLE 17.7
Multifactor Performance Attribution of a December 2020 Portfolio
Sometimes quantitative portfolio managers want to be able to attribute the portfolio’s performance to the returns of the individual stock holdings. In Tables 17.8 and 17.9 we produce the weights and returns of 10 stocks whose weights are highest compared with the benchmark weights and 10 stocks whose weights are lowest compared to the benchmark weights, all as of December 2020.
5
TABLE 17.8
Inside a December 2020 Portfolio
TABLE 17.9
The Multifactor Attribution of a December 2020 Portfolio’s Individual Stocks
For example, Kimberly Clark (KMB) has a weight of 0.036 in the tracking portfolio and a weight of 0.002 in the benchmark. Our portfolio’s excess weight in KMB is therefore 0.034, or 3.4%. On the other hand, Berkshire Hathaway (BRK.B) has a zero weight in the tracking portfolio and a weight of 0.017 in the benchmark. Thus, the excess weight in BRK.B is −0.017, or −1.7%. Not all
overweighted stocks contributed to the excess return, as can be seen from the negative values of
x
i
. Certain picks such as Adapthealth (AHCO) and Erie Indemnity (ERIE) turned out to be good ones, adding 0.227% and 0.129% to the excess return, respectively. In the end, the total gains from the overweighted stocks exceeded the total
losses from the underweighted stocks. This confirms what we already showed elsewhere—that, overall, the tracking portfolio managed to assign greater weights to the “right” stocks.
The table also shows the active exposures to the five factors in December 2020.
6
For example, the active position in KMB has a positive exposure to the standardized unanticipated earnings (SUE) and Pastor-Stambaugh liquidity (PSL) factors and a negative exposure to the EBITDA-to-price ratio (EBITDAP), Bollinger bands (BB), and ten year–three-month term premium (TP3M) factors.
Table 17.9
shows the returns of the active positions attributable to the five factors for December 2020.
7
We find that the return of the active position in KMB attributable to all of the five factors is 0.011% − 0.002% + 0.002% − 0.008% − 0.001% = 0.002%. The attribution
α
for KMB is − 0.088% for December 2020. Given the returns and estimates of the factor premiums for December 2020, we might have expected a return for KMB equal to 0.126%, rather than − 0.086%.
8
The reason for the difference is the random nature of financial markets. Thus, in any given month, the fluctuations of the error term in our model, and also the effect of the misspecification of our stock return model, can lead to differences in what is expected ex ante and what might happen in any given month. The realized
α
for this stock in December 2020 is just the actual return of the stock minus the factor exposures multiplied by the realized factor estimates. That is,
.
17.3 THE TRANSACTIONS COST–MANAGED PORTFOLIO PERFORMANCE
The analysis so far has ignored the transactions costs of buying and selling stocks. The incorporation of realistic transactions costs into our analysis changes the performance reports for the portfolios. We rebalanced these portfolios on a monthly basis, so to account for transactions costs, we computed the necessary
costs to rebalance our portfolios using the Abel Noser data, as mentioned in
Chapter 16
. By subtracting these costs from the returns of our portfolios, we obtained the after-transactions-costs returns.
We present the performance statistics that account for transactions costs in
Table 17.10
. The optimized tracking portfolio is based on the fundamental factor model and has a target tracking error of 5%. The tracking portfolio still outperforms the benchmark after accounting for the transactions costs, but the average excess return
is significantly lower at 4.337% per annum compared with the 6.839% per annum when we ignored transactions costs. In terms of the Sharpe ratio, however, the tracking portfolio fails to outperform the benchmark when transactions costs are accounted for.
TABLE 17.10
Historical Performance Considering Transactions Costs
This table also shows the performance of the portfolio that was optimized for transactions costs. That is, we created this portfolio using the fundamental factor model while explicitly accounting for the effects of transactions costs, as discussed in
Chapters 10
and
16
. This transactions cost-optimized portfolio increases the average return by about 0.5% per annum, while the standard deviation goes up by about 0.2%. Relative to the benchmark, the transactions cost–optimized portfolio achieves an excess return of about 5% with a realized tracking error of about 10%. However, its
SR
is not higher than that of the benchmark in this period.
9
Practitioners should include transactions costs in their backtests of models; otherwise, the portfolios that implement the models may have too much turnover and fall short of expected results.
17.4 THE TAX-MANAGED PORTFOLIO PERFORMANCE
Table 17.11
presents the after-tax performance statistics of the tracking portfolio and the tax-managed portfolio. We made adjustments for capital gains and losses. We did not make adjustments for the dividend tax because the tax rates vary for different types of investors. We examined trading at the time of reestimation (the end of each month), calculated the realized capital gains and losses that would occur according to the trades we would have to make, computed the tax burden (applying a 15% tax rate on long-term capital gains and a 37% tax rate on short-term capital gains), and subtracted this value from the return.
TABLE 17.11
Historical Performance Considering Taxes
In
Table 17.11
we consider five portfolios. The first portfolio, Tracking FIFO, is the standard fundamental factor model optimized for a 5% tracking error, but accounting for tax effects. Security lots are sold according to the first in, first out (FIFO) method. The second portfolio, Tracking Optimized, rebalances the portfolio
according to the tax optimization rules presented in
Chapter 11
on which tax lots to sell. The third portfolio, Tax-Managed Optimized, uses tax-harvesting techniques to generate losses and reduce the tax burden, as explained in
Chapter 11
and
Chapter 16
, Section 16.8.2. The fourth and fifth portfolios are benchmark portfolios where stocks are bought and sold using either the FIFO method or the optimized method of selling tax lots as we do for the Tracking Optimized portfolio.
The average excess return of the tracking portfolio is reduced almost by 5% per annum when we properly account for the tax burden. That is, when we compare the fundamental factor model with 5% tracking error from
Table 17.1
to the Tracking FIFO portfolio in this table, the performance difference is almost 5% (20.881% to 15.946%), reflecting the losses from taxes. The reduction in performance due to taxes is smaller, about 3% (20.881% to 17.507%), if the optimal tax-lot selection technique, Tracking Optimized, is applied. The benchmark is less affected by taxes, since there is less turnover in the benchmark.
When tax-loss-harvesting techniques were applied to the portfolio optimizations, Tax-Managed Optimized, we were able to outperform the benchmark by 5% per annum with a tracking error of 8.883%. That is, our loss-harvesting technique generated almost 2% extra return every year without adding significant tracking error compared to the simple tax strategies. Along with tax harvesting comes an implicit strategy that tends to overweight recent “winners” (stocks whose prices have risen) and tends to underweight recent “losers.” To the extent that stock prices exhibit positive autocorrelation, then past winners will outperform past losers, adding to the gains of a loss-harvesting strategy. This aspect of tax-loss-harvesting depends on the rebalancing frequency; if the “wrong” frequency is chosen, the beneficial returns associated with tax loss harvesting may be substantially smaller.
17.5 THE LEVERAGED PORTFOLIO PERFORMANCE
Some quantitative portfolio managers choose to leverage their equity portfolios in order to enhance returns, as we discussed in detail in
Chapter 12
and a bit in
Chapter 16
. To increase the average return, we created leverage by purchasing S&P 500 futures. The amount of futures was determined so that the
β
with respect to the S&P 500 was exactly 2 at the beginning of every month. Given a high
α
, increasing the
β
of the overall portfolio results in an even higher average return, provided that the stock market returns are generally positive.
Table 17.12
shows the performance statistics of the leveraged portfolio, the tracking portfolio, and the benchmark. For this and the following sections, we present the S&P 500 return figures provided by Compustat. These figures are different from our own
S&P 500 benchmark calculations in prior sections due to our exclusion of certain REIT stocks. The average return of the leveraged portfolio is higher than the return of the tracking portfolio by almost 15% per annum. Since the increase in the average return comes from the high
β
, the risk also increases from 18.8% per annum to 33% per annum. For the same reason, the information ratio and the Sharpe ratio are slightly reduced.
TABLE 17.12
Historical Performance of Portfolio Strategies in a Leveraged Form
This leveraged portfolio was rebalanced monthly to achieve an ex-ante
β
of 2. Our ex-post
β
(calculated with respect to the
S&P 500 total return index) is very near 2 at 2.043.
10
As for the benchmark , we do not control it directly.
11
17.6 THE MARKET-NEUTRAL PORTFOLIO PERFORMANCE
Table 17.13
presents the performance statistics of the two market-neutral portfolios, along with the returns on cash (1-month Treasury bill returns) and the S&P 500. One of the market-neutral portfolios, the sector-neutral portfolio, is composed of a long position in the sector-weight-matched tracking portfolio and a short position in the benchmark. The factor-neutral portfolio is composed of a long position in the factor-exposure-matched tracking portfolio and a short position in the benchmark.
TABLE 17.13
Historical Performance of Portfolio Strategies in Market-Neutral Form
It is not always clear what the appropriate benchmark for a market-neutral portfolio is. In a sense, it is the risk-free rate of return because we have attempted to eliminate market risk. From another perspective, it is the market return, because we want our portfolio to have a low correlation with the market. We therefore have included both benchmarks in the performance tables. Both the sector-neutral portfolio and the factor-neutral portfolio are dollar-neutral as well, and their returns are calculated as the tracking portfolio return minus the benchmark return plus the risk-free rate. The average returns of these two portfolios are higher than the cash return, which is the risk-free rate. The standard deviation of the returns (SD) is significantly lowered given the low market exposure of the market-neutral portfolios.
The correlation between the market-neutral portfolios and the S&P 500
ρ
B
is quite low, which is the aim of market neutrality. Both market-neutral portfolios have a relatively low
β
B
. We did not impose neutrality with respect to the benchmark
β
. However, the sector neutrality or multifactor neutrality affects
β
B
as well.
Table 17.14
presents the performance of two additional market-neutral portfolios. These portfolios were created directly from the
optimization by imposing two new constraints, while maximizing expected excess return. The dollar-neutrality constraint required that all weights in the portfolio sum to 0. The weights of long positions summed to 1, and the weights of short positions summed to 1 as well. The second additional constraint imposed either factor neutrality or sector neutrality. The factor neutrality constraint required the portfolio to have zero exposure to each factor in the model. The sector-neutrality constraint required the portfolio to have a zero weight for each sector. We dropped the full-investment constraint, the no-short-sale constraint, and the tracking-error constraint. We modified the diversification constraint and the trading-volume
constraint so as to limit absolute weights rather than weights. Once the market-neutral portfolio was created, we separated it into a long portfolio (the stocks with positive weights) and a short portfolio (the stocks with negative weights). The figures for the short portfolio are presented as if the investor had a long position in the short portfolio.
TABLE 17.14
Historical Performance of Optimized Market Neutral Portfolios
The optimized market-neutral portfolios recorded much higher returns than the two previous market-neutral portfolios where we simply shorted the S&P 500. The short sides of the optimized market-neutral portfolios had relatively small returns of 6.688% and 9.328%. By shorting these low-return positions rather than shorting the high-return S&P 500, the long-short portfolios produced returns as high as 13.057% and 11.202%. These returns are particularly impressive given the low values of
ρ
B
and
β
B
. This suggests that the optimization was quite successful at identifying the stocks that would underperform as well as the stocks that would outperform.
17.7 CONCLUSION
In this chapter we examined the results of our backtests of various types of portfolio strategies described throughout this book. From a backtesting point of view, our primary interest was the average excess returns and the ex-post tracking errors of our portfolios. Many quantitative equity portfolio managers focus on these statistics because they manage their portfolios with respect to a benchmark. For the time period we examined, and from the perspective of these two statistics, the portfolio strategy based on the fundamental factor model performed better than did the strategy based on the economic factor model. Of course, this should not be taken as proof of the superiority of the fundamental factor model in general. Our statistics represent the probable results of specific portfolios from 2011 to 2020. Choosing a model requires consideration of various models’ theoretical strengths and appropriateness to current and future conditions. Overall, we were quite satisfied with the performance of the models. We achieved a positive excess return over the benchmark while constraining our tracking error to some degree. In most cases, we achieved a positive
α
B
over the benchmark with a relatively high information ratio.
The analysis of after-transactions-cost performance and aftertax performance showed that a quantitative portfolio manager can do much more for an investor than just pick the right stocks. Managing transactions costs and tax costs quantitatively is also somewhat more predictable than selecting outperforming stocks. Portfolio managers can and should harness the power of cost and tax management. Our tax-managed portfolios performed much better than the basic tracking portfolio, not only in average return
but also in terms of risk-adjusted return. The transactions cost-optimized portfolio did not make a noticeable improvement on the regular tracking portfolio in this particular analysis, but in other data periods it most likely would. It generally makes sense to minimize the portfolio’s tax giveaways as much as possible.
12
We found that leveraging an equity portfolio produced much higher returns and higher risk when the market moved upward. We also showed that it is quite practical to create market-neutral portfolios using a variety of strategies that are relatively uncorrelated with the S&P 500 and yet produce a modest excess return over cash. The results of our example strategies hopefully will aid novices in the field and be of comparative interest to experts.
QUESTIONS
17.1.
(a)    How effective were the optimizations at creating portfolios with the desired tracking error?
(b)    What does this suggest about practical methods of risk control?
17.2.
Discuss the following constraints in practical portfolio optimization. In particular, explain what each constraint means in layperson’s terms and why a portfolio manager might choose to use it.
(a)
w
> 0
(b)
w′
ι
= 1
(c)
w
≤ 0.05
(d)
17.3.
Did the portfolios with a tracking error of 2% for the fundamental, economic, and Z-score models achieve the following objectives?
(a)    Positive
α
B
(b)    A Sharpe ratio higher than the benchmark’s
(c)    The desired tracking error
17.4.
In the backtests documented in this chapter, which model exhibited the smallest difference between ex-ante and ex-post tracking errors?
17.5.
Referring to the December 2020 performance attribution using the fundamental factor model, please respond to the following statements.
(a)    The portfolio strategy did well at asset allocation.
(b)    The portfolio strategy did well at stock selection.
(c)    The portfolio strategy was better at asset allocation than at stock selection.
17.6.
These questions relate to the tables on multifactor attribution (
Tables 17.7
,
17.8
, and
17.9
).
(a)    In
Table 17.7
, which factor contributed most to the excess return?
(b)    In
Table 17.7
, which factor contributed most to the excess risk? What is the important contributor to risk?
(c)    In Tables 17.8 and 17.9, which stock contributed most to the excess return, and by how much? What was the main source of this stock’s contribution to the return?
(d)    In Tables 17.8 and 17.9, which stock contributed the least to the excess return, and by how much? What was the main source of this stock’s contribution to the return?
17.7.
In the backtests that explicitly considered transactions costs,
(a)    How much higher was the average return owing to considering the transactions costs directly in the optimization?
(b)    Was the risk any higher as a result?
17.8.
The following questions concern the results of the tax-optimized portfolio versus the portfolios that mildly consider taxes.
(a)    What was the difference in average returns between the Tracking Optimized and the simple Tracking FIFO method?
(b)    Did loss harvesting improve the after-tax returns as illustrated by the Tax-Managed Optimized portfolio?
(c)    Based on the evidence in this chapter, is it important to explicitly consider taxes or not? State your answer and support with evidence.
(d)    How would you have done the backtest better?
17.9.
The following questions pertain to the leveraged portfolio results.
(a)    Decompose the leveraged portfolio return into three components:
α
B
, the part attributable to the S&P 500, that is,
β
B
r
B
, and the part attributable to the error term.
(b)    How much did the leverage increase the return? How much did it increase the risk? How much did it increase the Sharpe ratio of the portfolio?
17.10.
What is the most appropriate benchmark for a market-neutral portfolio?
17.11.
The following questions pertain to the information contained in
Table 17.13
about the market-neutral portfolios.
(a)    Did the sector-neutral portfolio achieve its objective?
(b)    Did the factor-neutral portfolio achieve its objective?
(c)    Using only the information in the table, was there a better portfolio that could have been constructed over this investment period? If so, what was it?
17.12.
The following questions pertain to the information contained in
Table 17.14
about the market-neutral optimized portfolios.
(a)    Did the market-neutral optimized portfolios achieve their objective?
(b)    Would you have bought these portfolios? Why or why not?
(c)    What was the main cause of the ex-post average returns of the portfolios?
17.13.
Respond to the following statements with regard to the empirical results of our backtests.
(a)    Market-neutral portfolios are pointless. Holding a portfolio of cash and equities is preferable.
(b)    Tax-management strategies offer no room for the improvement of after-tax returns because the relative gains on the tax side are offset by the relative losses on the investment side.
(c)    Accounting for transactions costs that consist of commissions, market impact, and delay does not really affect the average returns of a portfolio. Since you are going to have to buy some and sell some, on balance, the costs even out.
(d)    Leverage is like magic. It boosts the portfolio’s average returns.
1
It is standard practice among many quantitative portfolio managers to add a sector constraint to the portfolio. However, since we are already controlling the ex-ante tracking error of our portfolio versus the benchmark, to the extent that our modeling procedure is reasonable, we should not expect a further reduction in the ex-post tracking error from this additional constraint.
2
In the 1st Edition of this book, we warned of the problems with ex-ante and ex-post tracking error. Since then, new techniques have been suggested for how to deal with this. See Bruno et al. (2018), Menchero et al. (2012), and Menchero and Ji (2019).
3
These reports provide information that is suggested by the Association for Investment Management and Research’s Global Investment Performance Standards (AIMR-GIPS).
4
Since attribution
α
is realized errors of the stock return model, we do not define it elsewhere in the book. Some practitioners may prefer to call it the
unexplained excess return
.
5
For the readers who have forgotten the definitions of the components in this table, please refer back to
Chapter 15
.
6
Remember, the active exposure is given by
as explained in
Chapter 15
. To obtain the actual factor exposures of each stock, one can easily divide the active exposures by
. They will not be exactly the same due to rounding issues, but they will be close. For KMB, the division results in factor exposures of −0.147, −0.529, 0.059, 0.265, and −0.029, while the actual factor exposures are −0.146, −0.529, 0.054, 0.255, and −0.04.
7
Remember, the returns of the factors are given by
, where
is the realized factor premium during that month, as estimated by a cross-sectional regression. For more information, see
Chapter 15
.
8
This is assuming that our ex-ante
α
for KMB remained the same in December 2020 at 0.124%.
9
Some of the transactions cost-optimized portfolios that we examined (with a different list of factors) and not presented to the reader did achieve a higher
SR
than the benchmark during this period. Nonetheless, the not-so-impressive performance shown in
Table 17.10
illustrates the difficulty of beating the benchmark when aggressive transactions costs are applied, as we do in our analysis.
10
The
β
B
is not exactly 2 because it is calculated from the portfolio return rather than from the
β
B
of the individual stocks and weights. Also, it is equal to 2 only at the beginning of every month and consequently can diverge throughout the month because we did not rebalance daily.
11
In a perfect world, the
α
of the leveraged portfolio would be identical to the
α
of the tracking portfolio. In reality, the risk-free rate is not completely independent of the S&P 500.
12
Of course, we used one set of transactions costs assumptions. Readers should make assumptions most appropriate to their own trading practices.
