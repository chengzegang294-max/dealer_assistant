# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = chapter15

---

CHAPTER 15
Performance Measurement and Attribution
There are two ways to spread light: to be the candle or the mirror that reflects it
.
—Abraham Lincoln
15.1 INTRODUCTION
Performance measurement and attribution are extremely important to the quantitative equity portfolio management (QEPM) process. Measurement of a portfolio’s return shows how much value the portfolio manager has added to the investment process overall. Performance attribution dissects the return in order to pinpoint the exact sources of value. QEPM is an ongoing process of analysis, implementation, and further analysis. An in-depth review of the portfolio’s performance at regular intervals is essential to honing the investment strategy. Yet portfolio management shops often fail to do this either because they focus exclusively on the bottom line (asking only, “Did our return beat the benchmark return?”) or because they put so much effort into building portfolios that little time or resources are left for performance analysis. Sometimes performance analysis, which is hardly the highest-paying job in a QEPM department, fails to attract the best talent.
Performance measurement, however, is a fundamental activity in portfolio management. It ensures that the returns of the portfolio
are understood accurately, according to an accepted standard. This reason may be quite obvious to many portfolio managers, but one cannot forget the scandal surrounding the
Beardstown ladies
in the late 1990s. The Beardstown ladies were a group of elderly women from the central Illinois town of Beardstown who created an investment club that, according to them, had generated returns of 23.4% from 1983 to 1993, beating the Standard & Poor’s (S&P) 500 by 8% per year, on average. They sold over 800,000 books on their investment technique and spoke publicly about their investing acumen. In 1998, Price Waterhouse performed an audit of the Beardstown ladies’ portfolio that revealed that their actual return over the 10-year period was a market-lagging 9.1%. It turned out that whenever there were inflows into their investment portfolio (e.g., when new money was invested in the portfolio), the ladies counted the inflows as part of the ultimate return.
1
,
2
A professional manager would be unlikely to make this sort of accounting error unwittingly, but the Beardstown ladies’ blunder serves as a reminder that accurate calculations of portfolio results are an important demonstration of transparency on the part of whoever manages the portfolio.
Another important function of performance measurement is to determine whether the portfolio manager outperformed or underperformed the benchmark and whether the difference was due to skill or luck. (We will see, though, that this unfortunately requires a substantial amount of data, and the time it takes to amass those data does not usually fit into the time period in which bonuses are awarded.) Another significant piece of information that comes from performance measurement is the risk of a portfolio. The risk levels of multiple portfolios can be aggregated into a general level of risk for an entire firm. Performance measurement lays out the portfolio’s results for marketing and eventually for the general public so that comparisons can be made between portfolios and managers.
Performance attribution is a vital follow-up to performance measurement. Attribution means taking the overall results and breaking them down into their underlying causes. This allows a portfolio manager to understand why the portfolio over- or under- performed the benchmark. If my portfolio performance was 10% and the benchmark’s performance was 8%, what was the primary cause for my extra 2% return? Was it that I picked stocks well over- all, or was it that I chose to overweight certain industries? Was it primarily that I bought stocks with substantial earnings revisions, or was it that I bought stocks with low analyst coverage? Answering these kinds of questions about the sources of excess returns is key to understanding how well and efficiently the factor model and all other parts of the investing strategy are working.
We begin this chapter by discussing performance measurement, including the basics of return and risk calculations. We explain risk-adjusted measures of performance, including the Sharpe ratio, Jensen’s
α
, and the information ratio. Then we dig a bit deeper into stock returns with standard performance attribution. Finally, we highlight issues of performance measurement and attribution related specifically to the quantitative portfolio manager.
3
15.2 MEASURING RETURNS
Accurately calculated returns are the clearest measure of the success of an actual portfolio or a yet-to-be implemented portfolio strategy. The return of the actual, managed portfolio is the manager’s grade for the quarter or the year. The return of a
paper portfolio
, or
hypothetical portfolio
, gives an idea of how the manager might do. Hypothetical returns are useful for backtesting a strategy on historical data, setting up factor portfolios going forward, or creating a model portfolio in real time. The techniques used to compute the performance of a paper or hypothetical portfolio differ slightly from the computation of real portfolio performance because they usually involve computing the weights and returns of each stock in the portfolio. For calculating the return on the actual portfolio, most firms typically have some kind of accounting system that keeps track of the market value of all the securities and the entire portfolio on a daily basis. The computational techniques we
describe may apply to either actual or hypothetical portfolios, although some are applied more commonly to one or the other.
15.2.1 No Cash Flows
Measuring the return of a portfolio is usually simple, but sometimes it can get “weird.” Consider an equity portfolio with only stocks. Suppose that the portfolio holds
N
securities such that the weight of each security is given by
w
i,t
, where the weights sum to 1 (that is,
). We are interested in measuring the return of the portfolio over some period, and our smallest interval of time is one day. We probably do not need to know the performance over an increment smaller than one day. (Tracking stock movements hour by hour is for day traders.) We can denote the return from day
t
to day
t
+1 as
r
t,t
+
1
. The return from day
t
to day
t
+
k
, where
k
can be many days (e.g., 10, 100, 250, etc.), will be denoted by
r
t,t
+
k
.
To determine the return of the entire portfolio, we first must determine the returns of each of the stocks within the portfolio. Most portfolio managers subscribe to databases that provide stock return data. To calculate the return on a stock over some period, we take the closing price
4
of the stock on day
t
+
k
divided by its closing price on day
t
to obtain the
gross price return
. We then subtract 1 from the gross price return to obtain the price return. Thus
The individual stocks in the portfolio might pay dividends during the return measurement period. Dividends have the effect of decreasing the stock price by the amount of the dividend. Thus, if dividends are paid during the return measurement period, one should modify the preceding formula to add the dividend back into the
price return
. The total return is the return that accounts for dividends:
Most data providers compute
total returns
.
5
For a performance analyst who does not rely on preadjusted data and instead calculates
his or her own dividend-adjusted returns, there is the issue of when to add the dividend to the stock price. If the analyst uses monthly data (i.e., month-end closing prices and monthly dividends), there is not much of a choice. The dividend should be added to the ending price of the stock, and the monthly return should be computed using the formula for total returns. This is equivalent to assuming that the portfolio manager kept the dividend under the mattress until reinvesting it in the stock at the end-of-month closing price. When the dividend yield is small, this technique does not distort returns very much. Remember, the cash held by the portfolio manager normally would earn interest.
If the analyst uses
daily data
, there are more choices of how to treat the dividend. The databases that he or she uses should tell him or her various things about the dividend, including the
payable date
, the day the dividend is paid out to owners of the security, and the
ex-dividend date
, the date before which one must buy the stock in order to receive the dividend. As long as the portfolio owned the security prior to the ex-dividend date, the dividend can be included in the return calculation.
With daily data, the portfolio analyst could compute the daily return of the stock including the dividend on the payable date. This would assume that the portfolio manager invested the dividend back into the stock at the closing price of that day.
An alternative is to assume that the portfolio manager waited until the end of the month to reinvest dividends (which is likely in practice). Until the last day of the month, the performance analyst could increase the cash in the portfolio by the dividend amount and accurately record interest on these dividends.
Yet another method is to compute the return including the dividend on the ex-dividend date. The idea is that, on this day, the price of the stock would have dropped by the amount of the dividend. Thus, adding the dividend amount back to the stock price removes distortion from the daily stock returns. Of course, this assumes that the manager reinvested the dividend on the ex-dividend date, which is unlikely in practice. These issues are primarily concerns for backtesting or for paper performance calculations. For the actual portfolio returns, the performance analyst will have accurate market values of the entire portfolio on a daily basis.
For most stocks, the price return and total return formulas are all that are needed to compute the performance of individual stocks, but there are some
corporate actions
that occasionally make
the return calculation more difficult. A company could go into bankruptcy, be acquired by another company, or have a stock split during the performance period. We leave discussions of the treatment of these sorts of events to other books. Analysts and portfolio managers should make sure that their data providers have adjusted stock return data to account for the effects of these events.
Once the returns of the individual stocks have been computed, it is possible to compute the return of the entire portfolio. The return of the entire portfolio will be given by a weighted sum of the returns of the individual stocks, where the weights are as of the beginning of the return measurement period. Thus
where
is the weight of security
i
in the portfolio at the close of business on day
t
.
6
The weights of each stock in the portfolio will change over time as prices change. Thus, to compute the performance of the portfolio for a subsequent period, the portfolio weights must be updated. The update formula is
Most of these steps are required for computing the performance of a hypothetical portfolio. To compute the returns of an actual portfolio, however, the performance analyst typically obtains individual securities’ weights by dividing closing market values for all securities in the portfolio by the sum of the market values of all securities in the portfolio. Similarly, the returns for the entire portfolio can be computed more easily just by dividing today’s closing market value by yesterday’s closing market value. That is, the return of the actual portfolio also can be calculated as the market value of the portfolio at time
t
+
k
divided by the market value of the portfolio at time
t
[that is,
r
P,t,t
+
k
= (
V
t
+
k
/
V
t
) − 1].
If the portfolio in question had no cash flows during the performance period, the foregoing calculations are enough to give an accurate measurement of the portfolio’s returns. The formulas assume that there are no buys or sells during the performance measurement period. This is fine for a paper portfolio, which is just a model without real customers. Actual portfolios, though, most likely will have experienced customer withdrawals or investments or other cash flows during any given period. As the Beardstown ladies’ mistake made embarrassingly clear, the effects of cash flows have to be removed from the calculations before a portfolio manager can claim some return figure as evidence of his or her superior stock-picking skills.
15.2.2 Inflows and Outflows
Movements of cash into or out of the portfolio complicate the calculations of actual returns. Cash inflows in particular demand a decision about how to allocate new money—whether to keep it in cash reserves, purchase additional shares of the portfolio’s stocks in proportion to their weights, or equitize the cash with futures. No matter how the manager decides to use the new cash, the inflows will distort return calculations performed on daily market values of the portfolio. This is a problem that the performance analyst cannot ignore. To tackle the problem, he or she can draw from the portfolio management system’s store of information, which typically records cash flows and end-of-day market values of the portfolio.
Simple calculations of return can distort performance quite severely. Consider portfolio
X
, which had a market value of $100,000 on day
t
− 1. On day
t
, some time after the market opened, a customer transferred $30,000 into the portfolio. As soon as the money came in, the portfolio manager invested the money in each of the portfolio’s stocks in proportion to its weight in the portfolio. Suppose that the weighted return, the true return, of all the stocks in the portfolio for day
t
was 5% and that the portfolio ended the day at a market value of $136,269.23. If a performance analyst were to use the typical calculation of return—the market value at the close of day
t
divided by the market value at the close of day
t
−1—he or she would calculate a return of
r
t
−
1,t
= (
V
t
/
V
t
−
1
) −1 = 0.3627, or 36.27%. This is clearly way off the 5% mark.
When there are cash flows into or out of the portfolio, the analyst must calculate the portfolio’s
time-weighted return
(TWR). The
TWR reduces the influence of cash flows on the calculated return so that the return reflects the return on the investments themselves. Ideally, the TWR would be calculated after every inflow or outflow, although the fact that some assets are priced only once a day often prevents exact intraday calculations. Other formulas, most popularly the Dietz method, must be used to approximate the actual TWR.
7
The Dietz method computes daily performance as
where
V
t
and
V
t
+
1
measure the portfolio value at the close of day
t
and day
t
+ 1, respectively, and
C
t
+
1
represents the net cash flows in the portfolio on day t + 1.
In the case of portfolio
X
, the Dietz method computes a daily return of 0.0545, or 5.45%, much closer to the 5% one-day return than the inflated 36.27% suggested by the simple return calculation. Analysts should be aware that the Dietz and other approximations of the TWR grow imprecise when the daily return is very large and when the cash flow represents a very high percentage of the underlying value of the portfolio prior to the flows.
8
The Dietz method should be adequate for portfolio management firms that price their portfolios daily because the daily flows and returns are probably not large enough to distort performance. Firms that value their portfolios less frequently, say, monthly, and that have flows throughout the month should use the more accurate
modified Dietz
method.
9
After calculating accurate daily returns, the performance analyst can compute returns for longer periods by
geometrically linking
the daily returns. The analyst gathers all the daily returns from a particular month (or year) and computes the one-month (or one-year) return as
where
k
is the total number of daily periods in the month (or year or whatever time period the analyst has chosen to look at), ∏ is the product sign indicating to multiply a group of variables, and
r
t,t
+
k
is the return of the portfolio over the
k
measured days of returns within the month (or year, etc.).
When it comes time to draft marketing reports or meet with clients, the general convention is to present
annualized
returns. It is fine to stick to this convention as long as the portfolio actually has existed—or has been monitored, in the case of a hypothetical portfolio—for at least a year.
10
To annualize the return, first calculate the preceding formula for geometrically linking daily returns, setting the value of
k
equal to the total number of daily returns on record for the entire lifetime of the portfolio. Second, take that geometrically linked return and compute the annualized return as follows:
where
k
is the number of calender days for which the portfolio has existed,
r
t,t
+
k
is the geometrically linked return over the entire life of the portfolio, and
D
equals the average number of days in a typical year.
D
can be computed by dividing the total number of days that the portfolio has existed by the number of years it has existed.
Suppose that a performance analyst obtained the daily returns of a portfolio that has existed for 2 years and 10 days. He or she computes the geometrically linked return as 26% (that is,
r
t,t
+
k
= 0.26). Suppose that the portfolio has existed for 740 days (
k
= 740) and that the average number of days in a year is 365 (
D
= 365). The annualized return will be:
r
annualized
= (1.26)
(365/740)
− 1 = 0.1207, or 12.07%.
15.2.3 Measuring Returns for Market-Neutral and Leveraged Portfolios
So far we have only shown how to assess the performance of a plain vanilla portfolio. Since we spent an entire section of this book extolling the benefits of
α
mojo, we assume that many managers will try something a little more daring than straight buying and selling. If a manager uses leverage or a market-neutral strategy, for instance, how will he or she be able to tell that the
α
mojo is working? This section explains how to accurately measure the results of leveraged and market-neutral portfolios. We focus on certain basic scenarios, but the techniques can be applied to more complicated versions of leverage and market neutrality as well.
The Leveraged Returns
We discussed many forms of leverage in
Chapter 12
, but here we focus on how to compute the return on a stock-and-cash portfolio that was leveraged with index futures.
11
We assume that this portfolio manager rebalances his or her portfolio every
k
days to achieve the desired
β*
of the portfolio. The value of his or her over- all equity at time
t
+
k
is given by
where
ξ
t
is the percentage of equity held in cash at time
t, V
t
is the value of the portfolio equity at time
t, r
s,t,t
+
k
is the return of the underlying stock portfolio from time
t
to time
t
+
k, N
f,t
is the number of futures contracts purchased or sold at time
t, q
is the contract multiplier, and
F
t
+
k
and
F
t
represent the futures price at the two respective times.
12
Since we have assumed that the quantitative manager rebalanced his or her portfolio at every rebalancing period to achieve the desired overall
β
of the portfolio
β *
, we can substitute the equation for
N
f,t
= {[
β
*+(
ξ
t
−1)
β
s,t
]/(
β
f,t
qS
t
)}
V
t
. Thus, making this substitution into
Eq. (15.8)
with some minor rearrangement of variables gives us the formula for the returns of the leveraged portfolio. Formally,
where
S
t
is the value of the futures contract index.
13
Thus, given a set of historical data, a quantitative analyst easily can compute the historical returns of a leveraged portfolio with rebalancing at a
k
-period interval by obtaining the underlying returns of the stock portfolio every period, the desired overall
β
, the percentage of equity held in cash each period, the value of the underlying index each period, the
β
of the underlying portfolio with respect to the underlying index, and the price of the index futures at each rebalancing point.
14
The Market-Neutral Returns
For a general market-neutral or long-short portfolio, the value of the account equity at time
t
+
k
can be expressed as
where
and
are the notional amounts of the long and short portfolios, respectively,
r
L,t,t
+
k
and
r
S,t,t
+
k
are the returns of the long-only part of the portfolio and the short-only part of the portfolio before shorting, respectively,
m
lb
is the additional liquidity buffer required on the short position (or total position) as a fraction of the total equity (which may take on any value including zero in certain cases depending on the positions taken), and
e
i
′
k
/360
and
e
ik
/360
represent the continuous compounded gross return on the margin deposit and the other cash in the portfolio including the proceeds from the short sale, respectively. We can simplify the notation by calling
r
lb
and
r
cash
the return on the margin deposit (
e
i
′
k
/360
−1) and the return on the other cash (
e
ik
/360
−1). Let’s also express the long-only part of the position as
and the short-only part of the position as
. These terms just represent the notional amounts of the long-only and short-only parts of the portfolio as fractions of the original equity.
We can express the return of the overall market-neutral or long-short portfolio as
This is a comprehensive formula for computing the returns of a market-neutral or long-short portfolio using historical or real-time data. One can simplify the equation for common situations. Suppose that the market-neutral portfolio manager is dollar-neutral (that is,
) and the return on the liquidity buffer equals the return on the cash (that is,
r
lb
=
r
cash
). Then
Thus, given a set of historical data, one can compute the returns of a hypothetical market-neutral (specifically, dollar-neutral) portfolio by computing the returns of the long-only part of the portfolio each period, the returns of the short-only portfolio each period (before shorting), the return on any cash (which is paid to the short proceeds, the liquidity buffer, and other cash), and the proportion of the original equity that is invested in the long-only and short-only parts of the portfolio.
15
15.3 MEASURING RISK
We have measured the return of portfolios, but return is only half the story. Risk matters, too. Perhaps some portfolio boasts an out-standing one-year return. The savvy investor will greet the return figure with a bit of skepticism because he or she knows that if the portfolio is very volatile, last year’s great returns easily could be followed by next year’s losses. The portfolio manager ought to be concerned with risk as well. A portfolio that goes through boom-and-bust cycles will scare away clients. The manager must strike some balance between the potential rewards of risk taking and the security of risk minimization.
There are a number of risk measurements: the standard deviation (or variance) of portfolio returns, the semivariance of returns, the tracking error of returns, the VaR (value at risk) of returns, the correlation and covariance of the portfolio, and the
β
of the
portfolio. These are not measures of all types of investment risk but of the risks inherent in market price fluctuations.
16
15.3.1 Standard Deviation
The standard deviation measures how much the returns of a portfolio move around the average return. The standard deviation grows as returns move further above or further below the average. As a measurement of risk, most investors only care about the standard deviation of a stock in one direction, above or below the mean. Investors who are long stocks do not want returns to dip below the mean, but they certainly would be happy with returns that exceed it. If the returns of the portfolio are normally distributed, then the standard deviation is a valid measure of returns that are below the mean. If returns are not normal but skewed, then the standard deviation is less meaningful—but we will talk about that in the next section.
A performance analyst would like to know the portfolio’s true future standard deviation. Unfortunately, this is not possible; he or she must estimate the standard deviation using past data.
17
To estimate the standard deviation of a series of portfolio returns, the performance analyst computes
where
r
P,t
represents the portfolio return for period
t
,
r
P
represents the average return of all the portfolio returns,
represents the sample variance, and
T
represents the number of portfolio returns.
This formula can be estimated using daily, monthly, or annual data. The performance analyst should be sure to have enough data.
15.3.2 Semi-Standard Deviation
When stock or portfolio returns are not normally distributed, the standard deviation of returns does not really measure risk the way that investors think of risk.
18
A better measure of risk as most investors define it—the chance of losing money—is one that only reflects the likelihood of poor returns.
For example, suppose that our distribution of returns or excess returns is log normal.
19
This distribution is not symmetric. It is
skewed
to the right. If we chose to find investments with low variances or standard deviations in this distribution, we actually would reduce disproportionately the upside of the distribution.
20
We would be better off by reducing the downside risk, which is measured by the
semivariance or semi-standard deviation
.
The general measure for downside risk is given by
where
k
is an arbitrary constant.
21
When
k
=
r
P
, then the measure is known as semi-standard deviation because it is measuring the deviations from the average return on the downside.
Although downside risk, or semi-standard deviation, is one of the most robust measures of risk, it presents computational difficulties that deter many practitioners. It does not work well, for instance, with standard quadratic optimization.
22
In any case, performance analysis software these days can easily compute the ex-post downside risk of any actual portfolio or model portfolio.
15.3.3 Tracking Error
Tracking error is a familiar concept to quantitative portfolio managers, index portfolio managers, and qualitative portfolio managers alike. Tracking error measures the deviation of a portfolio’s return from the return of the benchmark, be it a target asset class or a major index. The “perfect” index manager has a tracking error (
TE
) of 0. Real index managers do not track the benchmark perfectly owing to transactions costs, reinvestment of dividends, and sampling methods of replicating the benchmark, but they do try to get as close as possible. Quantitative portfolio managers, on the other hand, are not trying to eliminate tracking error. They purposefully choose stocks and/or weights so as to achieve a higher return than the benchmark. The point is to keep the tracking error stable. The portfolio manager typically has to operate under some sort of constraint, such as that the ex-ante tracking error cannot exceed 5%. This controls the risk of the portfolio versus the benchmark.
By
ex-ante tracking error
, we mean the tracking error that the portfolio manager attempts to build into the portfolio initially. The derivation of ex-ante tracking error was shown in
Chapter 9
. There is also
ex-post tracking error
, which is the actual or realized tracking
error over a given period. Performance measurement is mainly concerned with measuring the ex-post tracking error of the portfolio, but it also might involve measuring the difference between the ex-post and ex-ante tracking errors. Ex-post tracking error typically is defined as the standard deviation of the difference in returns of the portfolio and the benchmark (in other words, of the excess return). The formula is
where
x
t
=
r
P,t
−
r
B,t
and
. Tracking error typically is annualized. If the tracking error is measured using any particular interval of data, the performance analyst can annualize it by multiplying by the square root of the number of intervals required to make the measurement period a full year. Thus, if the tracking error has been computed using monthly data, one can annualize it by multiplying it by
.
15.3.4 CAPM
β
Modern portfolio theory and the capital asset pricing model (CAPM) gave birth to
β
. The
β
of the portfolio measures the risk of the portfolio in relation to the overall market, which is usually considered to be the S&P 500. A
β
of 1 indicates that the portfolio’s returns move one for one with the market returns. A
β
greater than 1 indicates that the portfolio amplifies the market’s return in both the positive and negative directions. A
β
of less than 1 represents a portfolio in which market swings are to some degree muted. A
β
of 0 means that the portfolio is not correlated with the market.
A performance analyst can find
β
either by taking the weighted average of the
β
’s of each stock in the portfolio or by running a linear regression of the portfolio’s returns against the market’s returns. For the first method, the performance analyst needs to estimate the
β
of each individual stock. In Appendix 15E we discuss one method, but here we will just say that stock
β
’s are available from most data providers.
23
The
β
of the overall portfolio is computed from the individual stock data as follows:
where
N
is the number of stocks in the portfolio,
is the weight of stock
i
in the portfolio at time
t
, and
β
i,t
is the
β
of stock
i
at time
t
.
The second way to find
β
P
is to run the following regression:
where
r
f,t
represents the risk-free rate, which can be monthly returns of the three-month Treasury bill, and
r
M,t
represents the monthly market return, with the S&P 500 typically used as a proxy for the market.
Here are some practical comments about
β
measurement: (1) The greater the number of stocks in the portfolio when estimating
β
, the more stable
β
is over time. Stability in the
β
estimate means that the analyst can rely on it as an accurate description of the portfolio’s relative market risk in the future. (2) Extreme
β
’s tend to regress toward the mean of 1. This had led many practitioners to construct an
adjusted β
, which is a function of both the measured
β
and the market
β
. Thus
β
adj
=
aβ
+ (1 −
a
)1. The parameter
a
is flexible. (3) Most data providers furnish similar stock
β
’s. (4) The
β
’s of individual companies usually are measured using monthly data over a three- or five-year horizon. Most data providers do not publish
β
’s for stocks that have less than three years’ worth of data. In Appendix 15E, we show one method of computing individual stock
β
’s when the data are limited. (5) If the performance analyst plots the measured
β
’s of individual stocks against the subsequent returns of the stocks and the market, he or she will find that the slope of the line is smaller than theory would predict.
24
Increases in
β
do not increase returns as much as the regression equation predicts, and decreases in
β
do not decrease returns as much as the regression equation predicts. This is, in part, related to observation (2). (6) Many practitioners have found that
β
does not adequately explain stock returns.
15.3.5 Value-at-Risk
Value-at-risk (VaR) is a concept that is mainly used to control the possibility for potential losses of an entire bank’s investment positions or to control the risk of an individual trading position. It is more of a short-term risk concept. VaR is defined as the maximum expected loss over a target horizon within a given confidence interval. There are many specialized techniques to compute VaR, but if the returns of the portfolio are normally distributed, then the calculation of VaR is straightforward.
25
Once the standard deviation and expected return of the portfolio have been estimated, then one uses the standard normal table to determine the critical value of the VaR calculation for the desired significance. For example, for a 95% significance, the critical value is 1.65. For 97.5%, 99%, and 99.5%, the critical values are 1.96, 2.33, and 2.58, respectively. Thus, if the estimated mean of the portfolio is
, the estimated standard deviation of the portfolio is given by
, and the confidence level critical value is given by
k
, then the VaR is
where
V
t
is the value of the portfolio at time
t
.
Suppose that our $100 million portfolio has an annualized mean of 10% and a standard deviation of 20%. Suppose, also, that we wish to have a confidence interval of 97.5%. Then the VaR of our portfolio is
VaR
t
= 100,000,000(0.10 − 1.96 · 0.20) = −29,200,000
We can be 97.5% confident that, in a given year, the worst loss that the portfolio could suffer is $29,200,000. Users of VaR often prefer to have a VaR measure over a shorter period of time, such as one day or one week, so that they can understand a bank’s exposure over a short period of time. The VaR calculation for any subperiod using annualized data is simply
where
s
is measured in fractions of a year. Thus, for a one-month VaR,
s
= 1/12. In our earlier example, using
s
= 1/24, we find that the VaR over a two-week period for the portfolio would be $7,584,999.
15.3.6 Covariance and Correlation
The covariance or correlation
ρ
of a portfolio with a major index indicates the risk of the portfolio with respect to the index. It also indicates the diversification benefits from combining the portfolio with other portfolios. The covariance of a portfolio ex ante or ex post can be constructed from the individual securities that make up the portfolio. We showed how to do this in
Chapters 6
and
7
. Here we show how to take a set of portfolio returns and compute the covariance and correlation.
The covariance of the portfolio with any other index is computed by gathering the returns of the portfolio and the index and computing the following:
The correlation between the portfolio and the index can be computed as follows:
where
and
are the standard deviations of the portfolio and the index over the sample period. The correlation is more pleasant to deal with than the covariance because it always must be between −1 and 1. A correlation of 1 represents two return streams that always move together. A correlation of −1 represents the other extreme, two return streams that move in opposite directions.
15.4 RISK-ADJUSTED PERFORMANCE MEASUREMENT
Many personal investors focus with tunnel vision on raw returns. This is why, each year, most mutual fund investments flow into the funds that had the best performances or highest returns in the previous year. It is absolutely a mistake, though, to look at returns out of the context of risk. Consider
Figure 15.1
.
FIGURE 15.1
Risk return of three portfolios.
Looking only at returns, one would conclude that portfolio manager
C
is the best. Manager
C
has the highest return over the
period, manager
B
has the second highest, and manager
A
has the lowest return over the period. Portfolio manager
A
would be considered the worst manager. One notices, though, that portfolio manager
C
is taking on a lot more risk than portfolio managers
A
and
B
. If we borrowed—using the risk-free asset of a margin account—at some given interest rate
r
f
, we could increase the returns and the risk of portfolio manager
A
. If we borrowed enough, we could increase his or her risk until it was equal to the risk of portfolio manager
C
. At that same risk level, portfolio manager
A
’s return actually would be much higher than portfolio manager
C
’s.
26
The most accurate comparison of portfolio managers, therefore, is a comparison not of returns but of risk-adjusted returns. One of the most important measures of risk-adjusted returns is the Sharpe ratio.
15.4.1 The Sharpe Ratio
William F. Sharpe won the Nobel Prize in Economic Sciences for his development of the CAPM.
27
Among the many things that came out of this work is a measurement for risk-adjusted returns that is appropriately called the
Sharpe ratio
. The Sharpe ratio (
SR
) measures the portfolio’s excess return above the risk-free rate per unit of risk. It is given by
where
SR
is the Sharpe ratio measured over the sample period,
r
P
is the average portfolio return,
r
f
is the average risk-free rate, and
is the estimated standard deviation of the portfolio returns.
28
In practice, this ratio is computed as follows: Suppose that one has the monthly returns of a portfolio. One should take the arithmetic average of those returns. Thus, if one has 25 months of monthly portfolio returns, one should compute the average as
. For the risk-free rate, the exact value actually does not matter for comparison purposes, as long as some consistent rate is chosen. Many people use the average monthly return on 1-month or 3-month United States Treasury bills as
r
f
.
29
Finally, one needs to compute the portfolio risk over the period by taking the monthly returns and computing the standard deviation of the monthly returns. One can use the basic formula:
The Sharpe ratio provides a basis for comparing portfolios. In isolation, it does not mean much. Even when managers speak of “good” and “bad” Sharpe ratios, they are speaking only in relative
terms.
30
If portfolio manager
A
has the highest Sharpe ratio of several managers, you can say that he or she has the highest risk-adjusted return of the managers for the period. If you actually believe that there is something inherently stable about portfolio manager
A
’s performance, then you could leverage portfolio manager
A
and achieve the return of any other manager with lower risk. Of course, there is no guarantee that the same risk-adjusted return will continue in the next period.
15.4.2 The Information Ratio
The information ratio (
IR
) measures the risk-adjusted performance of portfolio managers who manage to a benchmark. It is the ratio of the benchmark
α
they produced to the residual risk they took on with respect to the benchmark.
31
An index manager should have an
IR
of 0 because his or her
α
theoretically should be 0, and his or her residual risk theoretically should be 0. An active portfolio manager intentionally deviates from the benchmark weightings to outperform the
benchmark. This creates his or her
α
and also generates residual risk versus the benchmark. Thus the information ratio is defined as
where
is the estimate of
α
from the regression of the portfolio returns on the benchmark returns for the measurement period, and
is the estimate of the residual standard deviation of the regression.
32
As with the Sharpe ratio, the higher the value of the
IR
, the better the portfolio manager performed on a risk-adjusted basis. As with the Sharpe ratio, the correct
IR
is easy to compute over a period. All one needs is the returns of the portfolio and the returns of the benchmark.
The information ratio typically is computed by running a regression of the portfolio returns against the benchmark returns. The idea is that the portfolio manager is being measured against the benchmark, so we should consider his or her excess risk-adjusted return over the benchmark divided by his or her excess (residual) risk. A regression similar to the CAPM
α
(see subsection 15.4.3) is run over the relevant performance measurement period. The estimated
α
,
, is stored, as well as the residual standard deviation, which is given by
, where
. All the ingredients to measure the information ratio come directly from the CAPM
α
regression, with the benchmark replacing the market return.
15.4.3 The CAPM
α
and the Benchmark
α
In
Chapter 2
we discussed the various types of
α
relevant to quantitative equity portfolio management (QEPM). We also briefly discussed the distinction between ex-ante and ex-post
α
. When we measure the risk-adjusted performance of a portfolio, we are always measuring the ex-post
α
. We now discuss the CAPM
α
(
α
CAPM
) and the benchmark
α
(
α
B
) in this light. The CAPM implies the following relationship between the portfolio return and the market index return:
While the theory itself says that the value of
α
should be 0, practitioners nonetheless estimate
α
and use it as a measure of risk-adjusted return. If
α
is positive, then the portfolio manager has provided an extra return over the market portfolio that is not explained by the extra risk he or she is taking. If the
α
is negative, then the portfolio manager is losing value versus the market portfolio.
The CAPM
α
is a very popular method for measuring portfolio managers’ performance and for ranking portfolio managers. CAPM
α
is also called
Jensen’s α
after a paper that Michael Jensen wrote in 1968 that introduced a new method of determining whether mutual fund portfolio managers outperformed the market. Jensen was essentially trying to determine whether portfolio managers had positive
α
’s. Owing to the large number of mutual funds he studied, he could not determine the benchmark of each one. Instead, he used the market return as a proxy for each benchmark.
Given the popularity of the CAPM, it is not surprising that the CAPM equation or single-index model has been used for many other indices and benchmarks. When we estimate the CAPM equation replacing the market portfolio with the benchmark, we call the resulting
α
the
benchmark α
. The benchmark
α
is obtained from the following regression
33
:
If the
α
from this regression is positive, it is an indication that the portfolio manager is outperforming the respective index on a risk-adjusted basis, whereas if the value of
α
is negative, this is a sign that the portfolio manager is underperforming the index on a risk-adjusted basis. Both for CAPM
α
and for benchmark
α
, not only is the sign of the
α
important, but the analyst also must determine whether the
α
is statistically significant. Most regression analyses will supply the
t-statistic
of the estimate of
α
.
34
Generally, for a large enough sample (e.g., 40), a
t
-statistic greater than 2 will be sufficient for a 95% confidence level and 2.7 for a 99% confidence level.
35
These regressions can be corrected for heteroscedasticity and autocorrelation in the residuals if needed.
15.4.4 The Multifactor
α
Many studies have shown that the CAPM fails to explain security returns adequately. Thus multifactor models of stock returns have become more popular, especially in performance measurement.
36
In academic circles, two models have gained popularity. One is a three- factor model, which includes the market, the small-cap premium, and the book-to-market premium. The other is a four-factor model, which includes all the variables in the aforementioned three-factor model in addition to a momentum term.
To compute the multifactor
α
(
α
MF
), one needs to know the returns on the factors that are believed to represent security returns and the portfolio’s returns over time. The multifactor
α
is usually calculated by regressing the monthly or quarterly returns of the portfolio against the return on the market index or benchmark and other factors. The most commonly used multifactor models accepted by academics and many practitioners are the two written below
37
:
where
β
i
are the coefficients of each of the factor returns or factor exposures, (
r
M,t
−
r
f,t
) represents the stock market return minus the risk-free rate of return,
38
and
SMB
t
, HML
t
, RMW
t
, CMA
t
, MOM
t
are the value-weighted, zero-investment, factor-mimicking portfolios for market capitalization, book-to-market, profitability, investment, and momentum. These six factors can be constructed in a variety of ways. We discuss the most common academic constructions of these variables.
SMB
t
is the size or market capitalization factor,
which is constructed by subtracting a portfolio of equal-weighted small-cap stocks from a portfolio of equal-weighted large-cap stocks.
HML
t
is the value factor, which is constructed by subtracting a portfolio of high B/M (book-to-market) stocks from a portfolio with low B/M stocks.
RMW
t
is the profitability factor, which is constructed by subtracting a portfolio of high operating profitability stocks from a portfolio of low-profitability stocks.
CMA
t
is the investment factor, which is constructed by subtracting a portfolio of smaller asset growth (conservative) stocks from a portfolio with higher asset growth (aggressive) stocks.
MOM
t
is a portfolio of high-return stocks minus a portfolio of low-return stocks, where momentum is defined as the previous eleven-month returns lagged by one month (i.e., the returns from the month
t
− 12 to the end of month
t
− 2 when the ranking date is the end of month
t
− 1 for a portfolio in month
t
) and is updated monthly.
39
If
α
is positive, then the portfolio manager has provided an extra return that is not explained by the extra risk he or she is
taking, which is encapsulated by the
β
’s. If
α
is negative, then the portfolio manager is losing value. However, not only is the sign of the
α
important, but the analyst must determine whether the
α
is statistically significant. Most regression analyses will supply the
t
-statistic of the estimate of
α
.
When the multifactor
α
is used to judge the performance of a portfolio manager, it tends to rate him or her less favorably than CAPM
α
would because it considers additional risk factors. In fact, it is very common to find a negative value for multifactor
α
. However, there is still a debate over whether it is appropriate to use a multifactor
α
model to judge a portfolio manager’s performance. Some academics believe that the additional risk factors are not truly risk factors in the economy. They argue that the decision to load up on those factors is a decision that should in fact be rewarded. Other academics claim that a multifactor risk model is more appropriate as a surrogate for overall risks in the economy; although the typical Fama-French factors are not real economywide risks, they can act as proxies for them. One also could argue that since almost every commercial risk model is a multifactor model, it is inconsistent not to count these factors as risk factors for performance measurement yet include them in the risk model for managing the portfolio. A portfolio manager can outperform the benchmark by loading up on factors that have positive risk premiums or through individual stock picking. Loading up on factors that have a positive premium is a mechanical strategy that could be replicated by a machine.
40
Should bonuses be awarded for this? If you think so, then use a CAPM version for measuring
α
. If you believe that portfolio managers should be rewarded for their ability to pick individual stocks that have positive
α
’s after accounting for the multifactor risk in their portfolios, then use a multifactor model to measure
α
. Either way, the debate is sure to continue between defenders of the CAPM and proponents of the multifactor model.
41
15.4.5 Practical Issues with Risk-Adjusted Measures
Fund-of-fund managers and financial advisors look for good portfolio managers to include in their asset allocations, and CIOs look for good portfolio managers to hire. But what is the measure of a “good” portfolio manager? For an index manager, good means adequately tracking the benchmark; the closer the returns are to the benchmark, the better. For an enhanced index manager or an active manager, good generally means tracking the benchmark but consistently earning a higher return than the benchmark. Even if we know what we are looking for in a good manager, two obstacles get in the way of finding it. The first is that assessing a manager’s performance over an investment period requires a significant amount of data, which may not be available. The second is that we have to assume that past performance is somewhat indicative of future performance. We cannot resolve these problems, but we can look for the signs of a good manager.
Let’s start with benchmark
α
(i.e., Jensen’s
α
). The
t
-statistic generally is used to determine whether the
α
(or any other coefficient in a regression for that matter) of a manager is statistically different from a given value or not. The
t
-statistic is given by
, where
is the standard error of the estimate of
α
. This formulation is for testing whether the portfolio manager’s
α
is significantly different from the given value
α
0
. Typically, as performance analysts, we care whether or not a positive or negative
α
is significantly different from 0 rather than being concerned with some other value. Thus our
t
-statistics are simplified to
. Fortunately, most software programs that portfolio managers use produce all the values from a simple linear regression, including
, and the actual
t
-statistic. Thus this calculation is simple to perform. The performance analyst simply compares the calculated value of
t
with the
t
c
or critical
t
-statistic in the
t
-statistic table and determines whether the portfolio manager’s
α
is significant at the desired significance level. As we already stated, for most cases, this is a value greater than 2.
In the special case in which all the classical assumptions of linear regression apply, the
t
-statistic becomes
42
where
T
is the number of measurement periods (e.g., monthly returns for the portfolio manager and benchmark),
r
B
* is the average of the benchmark returns minus the risk-free rate,
IR
is the measured information ratio, and other variables are as defined previously.
With some minor manipulation, one will notice that the second term in the denominator is similar to the squared Sharpe ratio of the benchmark. That is,
Substituting this into
Eq. (15.28)
, we obtain
We can use this equation to tell us how many monthly returns we need for a given significance level and a given information ratio to obtain a significant estimate of
α
(and hence of the manager’s information ratio). Let us choose a value for the
IR
of our hypothetical manager and the
SR
of the benchmark. Then
t
c
will depend on the number of monthly returns.
43
The
t
value shown in
Eq. (15.30)
will also depend on the number of monthly returns. We can then choose the minimum number of time periods,
T
*, such that
t
>
t
c
.
Table 15.1
shows the minimum number of time periods,
T
*, for
a manager’s empirical
α
to be statistically significant for various portfolio manager information ratios and benchmark Sharpe ratios. Assuming a benchmark such as the S&P 500, one could estimate the Sharpe ratio at about 0.25. Thus, for a portfolio manager with an information ratio of 0.5, it takes at least 22 monthly returns to determine whether or not he or she had a significantly positive
α
or not. The number of months needed becomes less stringent as the
IR
of the portfolio manager increases. However, for most reasonable
IR
ranges, one can see the problem that a CIO faces. Bonuses typically are given biannually or annually. Clearly, for most portfolio managers, there will not be a sufficient amount of data available when it comes time to determine whether a bonus should be given or not.
TABLE 15.1
Months Required to Verify a Portfolio Manager’s
α
and Information Ratio
Although we used the more exact formula, some practitioners have become more familiar with the approximation that
. This comes from assuming that the
term is small and can be neglected. For those who are more familiar with this formula, you should just observe the column in
Table 15.1
where
SR
= 0. However, for large values of the
SR
for the benchmark, the number of monthly returns needed is much greater than the approximation would suggest.
In addition to the risk-adjusted measures we have mentioned, there are others. Which ones should an analyst use? We suggest using the ones that we have mentioned, but we realize that even among these the ranking of portfolios will not always be similar. The Sharpe ratio is equal to
.
44
That is, the Sharpe ratio
of a portfolio is equal to the sum of (1) the
α
of the portfolio divided by the portfolio’s standard deviation and (2) the correlation of the portfolio’s returns with the market multiplied by the Sharpe ratio of the market. Thus, depending on the various values, the ranking of portfolios by Jensen’s
α
and by the Sharpe ratio may differ. One might even ask a different question. Suppose that we begin with a portfolio that is perfectly indexed to the market, but then we alter it slightly so as to create a positive
α
. Will our new portfolio also have a higher Sharpe ratio than the market? It depends. Because
, it depends on whether the correlation with the market drops significantly from 1, and if it does, it also depends on the magnitude of the drop compared with the increase in
α
.
15.5 PERFORMANCE ATTRIBUTION
Performance attribution dissects a portfolio’s return into its components, yielding a valuable insight into the exact sources of gains and the effectiveness of the stock selection process. Performance attribution must be tailored to the specific investment process of a portfolio manager’s department. Not all processes fit the same department. Although many simple attribution systems exist for traditional qualitative equity portfolio managers, it is much more difficult to build a suitable system for a quantitative equity portfolio manager. We begin this section by discussing traditional attribution systems and then suggest methods that might be used to determine the sources of a quantitative manager’s performance.
15.5.1 Classical Attribution
Brinson, Beebower, and Hood (1986) showed how portfolio returns could be decomposed into various categories. Classical categories include the
security-selection effect
and the
sector-allocation effect
. The security-selection effect is the part of the excess return over the benchmark that is attributable to stocking-picking skill, whereas the sector-allocation effect reflects how well the manager allocated his or her equity portfolio among different stock sectors.
The first step of classical attribution is to compute the return of the portfolio and the return of the benchmark over the measurement period from the individual stock weights and returns. Thus
The second step is to decide the relevant sector breakdown. If there are 10 sectors in the investment universe, for instance, stocks in the benchmark and the portfolio should be divided into these sector buckets. The performance analyst then should compute the overall weight of the benchmark and portfolio in each of the sectors. Thus
where
and
are the weights of stock
i
in sector
j
of the benchmark and the portfolio, respectively, and
S
j
is the set of stocks in sector
j
. The performance analyst also should compute the contribution of return from each sector for the benchmark and the portfolio. Thus
This calculation simply computes the overall return of each sector from the benchmark and the portfolio. Thus it is the return as if the entire portfolio or benchmark was invested in only that sector.
With this information, we can perform the third step. The allocation effect (
AE
) then can be computed as
where
AE
is the allocation effect. One can see that it makes sense intuitively. The allocation effect is computed by using the
sector
returns
of the benchmark—this accepts the returns attributable to the sector—but assigning them the weights given to sectors in the portfolio. This value minus the value of the overall benchmark return
r
B
represents the excess return of the portfolio owing to sector allocation.
The fourth step is to compute the security-selection effect (
SSE
). It is computed as
where
SSE
represents the security-selection effect. One can see that this also makes sense intuitively. The difference between the actual portfolio return
r
P
and the return of the portfolio with benchmark returns in every sector (with exactly the same weighting in every sector as the actual portfolio) will be due to the differential returns in each sector between the benchmark and the portfolio. But this differential can only be due to the difference between the individual stock selections and weights within each sector. Thus it represents the portion of the excess returns attributable to the
stock-selection effect
.
As a final check on this type of attribution scheme, we make sure that all the components add up. The excess return of the portfolio over the benchmark should be explained fully by the sector- allocation effect and the security-selection effect. In fact, it is. After canceling terms,
r
P
−
r
B
=
AE
+
SSE
. This classical attribution can be done in a variety of ways, but it helps us understand the source of the portfolio manager’s excess returns over the benchmark. What portion of the returns was due to efficient sector allocation, and what portion was due to security selection within the sectors? If the portfolio manager uses a model to predict all stock returns with no restriction on sector weights and finds that the sector-allocation bets are not performing well, he or she might want to consider running his or her quantitative stock-picking model while completely eliminating sector deviations from the benchmark. It thus helps the portfolio manager to uncover shortcomings in the investment process.
Suppose, for example, that we divide the stock universe into three sectors: technology, financial, and other. Suppose that we have already computed the weights and returns of the portfolio and benchmark in each sector as listed in
Table 15.2
.
TABLE 15.2
Performance of Portfolio and Benchmark in Selected Sectors
From this table we can compute the return of the portfolio
r
P
= 15.4%, the benchmark return
r
B
= 14.2%, the excess returns of the portfolio over the benchmark
r
P
−
r
B
= 1.2%, the allocation effect
AE
= −1.8%, and the security-selection effect
SSE
= 3%. From this simple example we can state that over the measurement period, the portfolio manager’s models did well at selecting individual securities within sectors but did not do so well at selecting sectors. If this type of bias continues in future attribution reports, the portfolio manager might consider optimizing his or her portfolio with the constraint that portfolio sector weights equal the benchmark sector weights.
15.5.2 Multifactor QEPM Attribution
Quantitative portfolio managers usually build the kind of stock models we described in
Chapters 5
,
6
, and
7
. In
Chapter 9
we discussed the importance of creating a model that generates security returns in order to produce risk estimates of the portfolio and optimize the portfolio against a benchmark. These concepts are used to construct the ex-ante optimal portfolio, which is optimized with a tracking- error constraint.
These same concepts can be used in turn to produce the ex-post performance attribution of the portfolio. In multifactor performance attribution, we use our multifactor risk model to understand the sources that generated the excess returns of our portfolio for the performance measurement period, whether it be a month, a quarter, or a year. Typically, performance attribution is performed
monthly. In this subsection we revisit some of the basic concepts and illustrate some of the typical multifactor attribution reports that could be produced for quantitative portfolios.
We begin with our model for security returns used in the risk model. It is of the form
When we use this model to construct the portfolio, we must estimate or forecast various components of the equation, as discussed in previous chapters. For performance attribution, we will have realized values of these variables. For the fundamental factor model, we can measure the factor premiums with a cross-sectional regression over all the stocks for the past month of performance. For the factor exposures of each stock, we already know the beginning-period values of those. For the economic factor model, we will have realized values of the factor premiums for the month, and we will use previously estimated factor exposures for each stock. In both cases we have the realized values for the month of attribution that we are concerned with. The
α
of each stock can be determined as
in the case of the fundamental factor model, and
in the case of the economic factor model. That is, for attribution purposes, whatever is not explained by the stock return model in the month we leave as
α
. Thus this completes the circle for return attribution. At this point, we can perform multifactor attribution. We are concerned with the sources of excess returns over the benchmark. Thus, for a given return period,
t
, using the notation for the economic factor model,
45
where
. Depending on which model we are using, either the fundamental or economic factor model, we will have the corresponding realized values of the appropriate variable during the month of attribution. Each component in this reduced equation makes up our performance attribution of various components as measured by our risk model. The performance attribution report can be presented in a table such as
Table 15.3
.
TABLE 15.3
The Multifactor Attribution of the Portfolio
In this attribution report, one also will notice a risk decomposition of the variance of the portfolio. Some portfolio managers may wish to view this in their attribution report as well. Technically, though, this report is not a risk attribution report because in a period
of one month, there is only one observable factor realization in that particular month for each factor. The factor variances and covariances, as well as the variance of the residuals, typically are estimated from historical data.
46
Thus this risk decomposition is really an ex-ante decomposition rather than a risk attribution analysis.
47
The reader also will notice that in the risk decomposition, we use only the variance of each factor multiplied by the squared active exposure of the portfolio over the benchmark to explain the risk contributed to the tracking error by that particular factor exposure. Technically, this is not the entire story; we are leaving out the cross correlation among factor premiums. Some portfolio managers would choose to have the cross correlations of each factor added to the overall contribution of the risk attributable to that factor (especially when the correlation among factor returns is quite high), whereas other portfolio managers may choose not to have it added (especially when the correlation among factor returns is quite low). We chose to separate it out in a distinct area called “Adjustment for factor correlation” that appears at the bottom of the table. This represents all the cross-correlation effects of the factor returns. Unfortunately, there is no absolutely correct method to decompose this part of the overall risk.
The performance analyst may wish to provide portfolio managers with an individual stock report as well. A report listing mul
tiple securities would be quite long, but it could follow the format of
Table 15.4
. In this table,
r
i
represents the return of the security for the given performance measurement period,
represents the portfolio weight of the security at the beginning of the performance period,
represents the benchmark weight of the particular security at the beginning of the performance period,
x
i
represents the excess return contributed by that particular security, which is equal to (
)
r
i
or
is the estimated multifactor of the historical stock return model, and the exposures on each factor represent the excess exposure to each factor given by the portfolio weights (that is,
).
TABLE 15.4
Inside a Portfolio
A complementary report might be organized like
Table 15.5
. In this table, many of the variables are similar, except that the
represents the individual stock attribution
α
that is the part of return not explained in the performance period by the multifactor model; the contributions of factor exposure returns are also in this table, describing how each factor contributed to the excess return of the portfolio from the weight differential in that particular stock (that is,
for security
i
, where
f
1
is the period realization of factor 1); and the marginal risk is given by the effect on risk of increasing that particular security’s weight by a small amount. If the tracking error (
TE
) is given by
TABLE 15.5
The Multifactor Attribution of a Portfolio’s Individual Stocks
then the marginal contribution of risk to the total portfolio tracking risk is given by
There are some conceptual details that the performance analyst may wish to think about. First of all, this type of multifactor attribution usually is done with the risk model of the commercial software or the in-house risk model. Although the risk model presumably encompasses and explains security returns quite well, is such a decomposition very meaningful to the quantitative portfolio manager? A manager might be more interested in obtaining the performance attribution with respect to his or her
α
factor model, whether it be an aggregate Z-score model, an economic factor model, or a fundamental factor model. When the risk model is already built and used for the creation of optimized portfolios, this makes it simpler to use the risk model for multifactor attribution. For portfolio managers who use commercial software, there really is no other choice. However, a performance analyst might consider taking the quantitative factors used to forecast
α
by the portfolio manager and use those to construct some type of risk model that runs parallel to the firm’s risk model. Thus, for performance attribution, the performance analyst can present attribution with respect to the factors that the quantitative manager actually uses to pick his or her stocks.
15.6 CONCLUSION
In this chapter we examined various techniques used in performance measurement and attribution. Conceptually, these techniques are straightforward. When they are actually applied to the real world, though, numerous complications arise. There are many answers even to seemingly simple questions such as, “What was the portfolio’s return?” When the question becomes, “What was the portfolio’s risk (and risk-adjusted return)?” almost every analyst can come up with a different solution. The proliferation of methods for measuring “good” performance simply means that a performance analyst must be careful to pick the technique that best
fits the particulars of the situation and states the portfolio’s performance clearly and honestly.
1
Source
: Karen Hube. “How to Sidestep a ‘Beardstown Blunder’ When Calculating Portfolio Performance,”
Wall Street Journal
, March 25, 1998.
2
For example, suppose that a portfolio began with $10,000 in it and that over one year the true portfolio return on the investment was about 8%. Then the ending value would be $10,800. Suppose that just prior to the last day of the year, a new investor placed $10,000 in the portfolio. The end-of-year value of the portfolio would be $20,800. If you did not account for this cash inflow appropriately, you might be led to compute the performance of the portfolio as (20,800/10,000) −1 = 108%. Clearly, this would be an incorrect measurement of performance because the new investor’s money should not be part of the portfolio’s return.
3
For a discussion of performance presentation standards in the industry, please see the Global Performance Investment Standards (GIPS), which can be found at
www.gipsstandards.org
.
4
Closing prices are the most commonly available data on stock prices.
5
Even
finance.yahoo.com
allows the user to download “adjusted prices” for stocks, which are prices that include the dividend. The adjusted prices let you compute the return in the normal way.
6
The formulas are easiest for equal-weighted and value-weighted portfolios. For an equal-weighted portfolio, the formula is
For a value-weighted portfolio, the formula is
or
, where
V
i,t
+
k
and
V
i,t
are the market value of security
i
at
t
+
k
and
t
, respectively, and
V
t
is the market value of the portfolio at time
t
.
7
The Dietz method is named after Peter Dietz. See Dietz (1966). Another method very similar to Dietz is known as the ICAA method. ICAA stands for the Investment Council Association of America.
8
This is a more significant issue for separate account platforms, in which advisors or investors tend to move a substantial amount of assets from one portfolio to another over the course of a day. Modified Dietz and other TWR approximations mitigate the effect of these sorts of large flows.
9
The modified Dietz method weights the cash flows at the times they actually occurred during the performance period rather than at the midpoint of the period, as the normal Dietz method does. For portfolios priced on a monthly basis, this distinction greatly improves the approximation. Each movement of cash is weighted in proportion to the number of days in the portfolio. The formula for multiple cash flows in a month is given by
, where
is the modified Dietz weight, with
n
i
being the number of days between the beginning of the period and the timing of cash flow
i
, and
N
being the number of days in the whole performance measurement period.
CF
i
represents the net cash flow
i
during the period, and
n
cf
is the number of cash flows. For more details, see Dietz and Kirschman (1983).
10
For returns of less than 1 year, the convention is to not annualize the returns.
11
In our formulas we will ignore issues related to the rollover of the futures contracts. We also assume that margin requirements can be settled through use of the underlying stock portfolio.
12
All this notation is described in more detail in
Chapter 12
.
13
This formula simplifies for many backtests. If the index futures are on the underlying benchmark,
β
f
will be equal to 1 and can be removed from the equation. Also, if
ξ
= 0 and
I
t,t
+
k
= 1, then the formula reduces to
r
s,t,t
+
k
+ [(
β*
−
β
s,t
)/
S
t
] (
F
t
+
k
−
F
t
).
14
Of course, this formula is not exact because it assumes that the portfolio manager can purchase fractional amounts of the futures contract, which is not possible in practice. Nevertheless, this computation will be quite close and satisfactory for historical backtests.
15
In the case of a maximum leveraged dollar-neutral portfolio,
κ
L
=
κ
S
= (1 −
m
lb
).
16
A nonfinancial friend of ours once asked us, “Why should I care about the variance if in the long run the stock market goes up?” It was a good question, but then we realized it was based on an investor fallacy in thinking, which is that the stock market always goes up over the long run. Variance of returns means that there is the probability, however small, that the market potentially could go down over the long run. This probability is the basis for the portfolio insurance business. If you wish to insure your portfolio even over many years, it usually costs anywhere from 5% to 10% of your investment. Someone else once criticized portfolio insurance as “ridiculous—since we know stocks always go up over the long term, this insurance should be free.” A few months later, the internet bubble burst and, along with it, his portfolio, which fell by 80%. This may have been an unfortunate lesson in the fact that depending on what years you look at, the stock market sometimes may decline over a longer time frame.
17
Implied volatilities from the option prices of stocks are also used to forecast future volatility.
18
A performance analyst may wish to test for the normality of the distribution of portfolio returns. A popular test, known as the
Jarque-Bera test
, is based on two central moments of the distribution of stocks returns, called
skewness
and
kurtosis
. The test is based on the sample skewness and kurtosis of stock returns. The Jarque-Bera test statistic is given by
, where
is the chi-square distribution with 2 degrees of freedom,
and
Most popular software packages have some variant of this test built directly into their software. For example, in STATA, you can use the function SUMMARIZE to get skewness and kurtosis and then compute the Jarque-Bera (JB) statistic or use the command VECNORM to conduct the Jarque-Bera Test. You can also conduct the JB test in R, using the function JARQUE.BERA.TEST; in MATLAB, using the function JBTEST; and in RATS, using the function STATISTICS.
19
When a random variable,
X
, has a normal distribution, then
Y
=
e
X
has a log-normal distribution. If
μ
and
σ
are the mean and standard deviation of
X
, then the probability density function for
Y
is
20
Now, had the distribution been negatively skewed, or skewed left, the variance/standard deviation analysis would have placed too little weight on the downside risk.
21
There are alternative methods of computing this, including dividing by the total number of downside observations rather than the total number of observations.
22
See
Chapter 9
.
23
Appendix 15E can be found under Chapter Appendices at
https://ludwigbc.com/books/qepm/exclusive_qepm_content_2020/
or at
www.ludwigbc.com
under QEPM Exclusive Content.
24
See Friend and Blume (1970), Black, Jensen, and Scholes (1972), and Stambaugh (1982). Chincarini et al. (2020) found that the relationship is much stronger if one accounts for the ages of firms.
25
For more details on VaR, see Jorion (1997) or Dowd (1998).
26
Mathematically, one can observe that if the expected leveraged return of portfolio
A
is
E
[
r
Al
] = (1+
α
)
μ
A
−
αr
f
, and the risk of the leveraged portfolio
A
is
σ
Al
= (1+
α
)
σ
A
, then a leveraged portfolio
A
with the same risk as portfolio
C
always will have a higher expected return if (
μ
A
−
r
f
)/
σ
A
> (
μ
C
−
r
f
)/
σ
C
. This condition is that the slope of the line through the risk-free rate and portfolio
A
is greater than the slope of the line through the risk-free rate and portfolio
C
.
27
Jan Mossin, John Linter, and Jack Treynor also did work at the same time as Sharpe to develop the CAPM. Some people refer to this as the Linter-Mossin-Sharpe-Treynor CAPM. Harry Markowitz told us that the most elegant paper to read on the topic was written by Mossin (1966).
28
When returns are non-normal, it is better to divide the numerator by the semi-standard deviation. This modified Sharpe ratio is also known as the
Sortino ratio
. Risk-adjusted hedge fund returns are sometimes measured with the Sterling and Calmar ratios, which are ratios of the annualized returns of the portfolio over some period divided by a type of downside risk measure known as drawdown.
Drawdown
measures the absolute value of the return loss from the peak to trough of the portfolio value. The peak and trough are recognized, once a new peak is reached by the portfolio. The Calmar ratio uses the absolute maximum drawdown over the measurement period, while the Sterling ratio uses the absolute average drawdown minus some constant.
29
When total returns are not available for Treasury bills, some people just use the time-series average of the Treasury yields as a proxy for the Treasury bill return.
30
For example, some portfolio managers say that a Sharpe ratio above 0.5 is really good. What they are really saying is, “Of all the portfolios I’ve seen managed, I haven’t seen a Sharpe ratio above 0.5 too often.”
31
The ex-ante information ratio is used to described the expected portfolio information ratio, while the ex-post information ratio is used to measure actual risk-adjusted performance. Some portfolio managers measure the ex-post information ratio as
where
is the average return of the portfolio, and
is the average return of the benchmark over the measurement period.
is the tracking error (i.e., the standard deviation of the difference in returns between the portfolio and the benchmark). Portfolio managers often use this measure as it is easier to compute. However, this measure can lead to misleading conclusions about the respective information ratios of different managers with different exposures to the benchmark (i.e., their
β
). To understand this, note that
where
is the residual variance of the portfolio. Thus, the two measures of information ratio,
IR*
and
IR*
, are only equal when the measured
β
of the portfolio versus the benchmark is equal to 1; otherwise, they are different. If you take the derivative of
IR*
with respect to
β
, you will find that
. Thus,
, whenever
, and
. Thus, for upward-drifting markets (
), among portfolio managers with a similar positive
α
, a less aggressive portfolio manager (smaller
β, β
< 1) will look worse (i.e., lower
IR*
). Whenever
, the higher manager will have a lower
IR*
. In both of these cases, the
IR*
measure leads to erroneous interpretation of the managers, while
IR
does not. In fact, in both of these cases, the
IR
of the managers is the same.
32
Some practitioners use the notation
instead of
.
33
Some practitioners estimate this regression without subtracting the risk-free rate.
34
The
t
-statistic is discussed in Section 15.4.5.
35
The critical
t
-statistic can be found for any specific situation after determining the degrees of freedom. However, for most circumstances, this rule of thumb is sufficient.
36
See Fama and French (1993) and Carhart (1997).
37
When we published the first edition of this book, the most commonly used academic model was the three-factor Fama-French model plus momentum. In recent years, many researchers have extended the three-factor model into a five- or six-factor model, including Eugene Fama and Kenneth French. Thus, we present the Fama-French six-factor model or five-factor model plus momentum. That there has been so much change over the years in the accepted factor models and the growing literature on data mining of factors (which always concerned Fischer Black) remind us how difficult it is to precisely quantify the behavior of asset prices.
38
Academics typically use a value-weighted portfolio of New York Stock Exchange (NYSE), American Stock Exchange (AMEX), and National Association of Securities Dealers Automated Quotations (NASDAQ) stocks to proxy for the market.
39
Fama and French construct it as
SMB
t
=
(
Small Value
+
Small Neutral
+
Small Growth
) −
(
Big Value
+
Big Neutral
+
Big Growth
), where the six portfolios in the equation are constructed by dividing the NYSE, AMEX, and NASDAQ stocks into two buckets on either side of the median market capitalization of the NYSE stocks. The small and big buckets are further divided into three buckets based upon the 70% and 30% breakpoints of book-to-market ratios of NYSE stocks. These six portfolios then correspond to the names listed prior, with value being high B/M and growth being low B/M. To construct the
HML
t
factor, Fama-French use
HML
t
=
(
Small Value
+
Big Value
) −
(
Small Growth
+
Big Growth
). The first factor weights the portfolios so that both the small portfolio and big portfolio have about the same average B/M ratio. The second factor weights the portfolios so that the high B/M portfolio and low B/M portfolio have the same weighted-average size, to remove the size effect. The profitability (
RMW
t
) and investment (
CMA
t
) factors are constructed similarly to the value factor. Thus, once sorts are complete,
RMW
t
=
(
Small Robust
+
Big Robust
)−
(
Small Weak
+
Big Weak
), where
Robust
is for high operating profitability and
Weak
is for low operating profitability.
CMA
t
=
(
Small Conservative
+
Big Conservative
) −
(
Small Aggressive
+
Big Aggressive
). Operating profitability is defined as annual revenues minus COGS minus interest expense minus SGA divided by book equity. Investments are defined as change in total assets divided by total assets.
Robust
profitability firms are firms with higher profitability, and
Conservative
firms are the firms with the lowest change in investments. The momentum (
MOM
t
) factor is also constructed similarly to the value factor. Thus, once sorts are complete,
MOM
t
=
(
Small High
+
Big High
) −
(
Small Low
+
Big Low
), where the high and low return portfolios are separated by the previous eleven-month cumulative returns lagged by one month (i.e.,
t
− 12 to
t
− 2). For
MOM
t
, portfolios are formed monthly rather than annually. For more details, see Fama and French (1993, 2015). The portfolio manager can create his own factor portfolios using similar concepts. There is no need to follow the Fama-French methodology.
40
In fact, since we wrote the first edition of this book, many practitioners have created what are known as
smart-beta strategies
. These factor strategies are based on a formula and are offered to investors in the form of a mutual fund or ETF or separate account.
41
The joke we make to our students is that if you’re a portfolio manager, you want to convince the performance measurement department to use a CAPM-based or Jensen’s
α
measurement. If you’re the CIO, you want to use the multifactor model.
42
The reader should be aware that this formulation for the standard error of
does not apply when standard errors are corrected for heteroscedasticity, autocorrelation, or other effects.
43
To construct the number of monthly returns, we had to consider the relationship between
IR, SR
, and the
t
-statistic as well as the relationship between
t
c
and
T
. To make this exercise meaningful, we are assuming that
IR
and
SR
do not change as we vary the number of months. Also, it should be remembered that the number of months minus 2 is the appropriate degrees of freedom.
44
This can be derived by starting with the CAPM equation and making a substitution of variables.
45
The derivations work for the fundamental factor model as well, only instead of “estimation hats” over the
β’s
, there are hats over the factor premiums,
f
.
46
With an economic factor model, the factor variance and covariances (or correlations) can be estimated as well as the variance of the error terms on a time series. With the fundamental factor model, the historical variances and covariances (or correlations) of the factors can be estimated with a series of cross-sectional regressions on historical data.
47
One method to get a risk attribution analysis would be to estimate the daily factor premiums and then compute the daily variances and covariances (or correlations) of the factor premiums during the month and multiply these by 20 to get an estimate of the volatility and correlations of the factors for the month. Although this would be closer to an actual attribution of the portfolio for the particular month, more biases may creep in owing to the noise associated with measurements of daily volatility and issues of non-normality in the data that may arise. For more information, see DiBartolomeo (2003).
