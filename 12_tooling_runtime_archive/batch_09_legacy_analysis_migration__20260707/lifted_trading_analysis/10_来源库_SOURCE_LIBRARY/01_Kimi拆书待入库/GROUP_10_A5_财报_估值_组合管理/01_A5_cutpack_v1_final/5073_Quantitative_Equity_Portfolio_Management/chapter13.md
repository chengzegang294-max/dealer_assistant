# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = chapter13

---

CHAPTER 13
Market Neutral
Not being able to govern events, I govern myself
.
—Michel de Montaigne
13.1 INTRODUCTION
Market-neutral strategies have gained popularity over the last few years. From 2000 to 2020, the equity market-neutral strategy declined from 2.57% of the hedge-fund universe to 1.51%.
1
The first known hedge fund was market neutral. It was founded in 1949 by Alfred W. Jones, an Australian-born Harvard graduate who believed that he had an ability to predict individual stock returns but no ability to time the market or predict its general direction. Jones realized that if he could, in the right proportion, short the securities that he thought would lose value and buy the securities that he thought would gain value, he would effectively eliminate the impact of the overall market return on his portfolio. His portfolio’s return would equal the difference in returns between the winners and losers, reflecting only his ability to pick the stocks. Jones’s track record was quite impressive. In fact, a 1966
Fortune
article entitled, “The Jones That Nobody Can Keep Up With,” reported that his fund beat the best-performing mutual fund of that year by 44%.
Jones’s market-neutral strategy took hold in the investment community, and although people today apply a variety of techniques and designs to it, the goal remains the same: to reduce the sensitivity of the portfolio to market movements by taking long and short positions in individual securities or market indices that offset the effects of the market. One of those effects is market risk.
Table 13.1
shows that over the last 25 years, a market-neutral portfolio would have earned a return a little less than half of the Standard & Poor’s (S&P) 500 but with about half of the volatility. In fact, the market-neutral portfolio had less risk than any other major index except for the money market index. By taking a big slice of risk out of the portfolio, market-neutral strategies clear the path for a manager who is good at stock picking to focus on his or her strength. This can boost
α
above the
α
of the traditional long portfolio. In other words, market neutral is a good source of
α
mojo.
TABLE 13.1
Statistics of a Market-Neutral Portfolio versus Other Major Indices
Market-neutral strategies can work for index managers too. Combined with a long exposure to the equity index, buying favorable stocks and shorting unfavorable ones adds the
α
from stock picking to the benchmark return. Market-neutral portfolios also can help to diversify an investor’s overall portfolio because they have very low correlations with the market.
Table 13.1
shows that
the correlations between the market-neutral portfolio and various indices are all less than 0.36.
2
In this chapter we discuss the basics of equity market-neutral strategies of portfolio management. We show the various methods for constructing a market-neutral portfolio, go over the basic mathematics, and discuss the advantages of the strategy.
13.2 MARKET-NEUTRAL CONSTRUCTION
The market-neutral concept applies to a variety of investment strategies, including convertible arbitrage, fixed-income arbitrage, and risk arbitrage. Here we focus on applying it to an equity portfolio run by a stock-picking manager.
A manager can construct a market-neutral position by purchasing stocks that he or she thinks are “buys” and shorting ones that he or she thinks are “sells.” He or she can separate the buys from the sells with an aggregate Z-score model, a fundamental factor model, or an economic factor model—any of these will help to rank the stocks by expected return. He or she also can sort these stocks using other methods, including directly through an optimization. Then, to achieve market neutrality, the manager must use some mechanism for controlling risk so that the entire portfolio has
zero net exposure
to the market even as it captures the excess return from stock picking. Risk-control mechanisms run the gamut from very simple to quite complex. We discuss a number of them in this section.
13.2.1 Security Selection
In order to construct the portfolio, the manager must identify the buys and sells. With a quantitative model, he or she can estimate the expected returns or
α
’s of the stocks in his or her investment universe. Stocks with low expected returns or
α
’s go in the “sell” pile; the rest are “buys.” We will assume that the manager already has forecasted the expected returns of stocks, or their
α
’s, from either an aggregate Z-score model or a factor model.
13.2.2 Dollar Neutrality
The simplest market-neutral strategy is
dollar neutrality
, which means that the dollar amount of the long positions equals the dollar amount of the short positions. Suppose that the portfolio manager has identified 10 stocks that are buys and 10 stocks that are sells and that he or she has $100 million with which to trade. He or she can weight the group of buys and sells in any manner he or she chooses as long as the ratio of the weights of the longs to the weights of the shorts is 1:1. The short positions also will require margin collateral from the broker, but we take up this issue in a later section. If
V
L
represents the notional amount invested in the long positions and
V
S
represents the notional amount invested in the short positions, then dollar neutrality implies that
The weights of the long and short stocks each total 1. Thus
and
, where
represents the relative weights of stocks in the long portfolio and
represents the relative weights of stocks in the short portfolio prior to shorting, and
N
L
and
N
S
represent the number of stocks in the long and short portfolios, respectively. It is convenient to think of the short portfolio as simply a long portfolio in which the stocks are sold in certain proportions rather than purchased.
3
Suppose that we have an equity value of $90 million. In
Table 13.2
we identify 10 stocks we would like to buy and 10 stocks that we would like to short.
TABLE 13.2
Example of a Dollar-Neutral Portfolio
The weights in each portfolio were chosen according to some relative Z-score weighting. The sum of the weights in both portfolios equals 1. The
β
’s are reported with respect to the S&P 500. The weighted-average
β
for the long portfolio is 1.78, whereas the weighted-average
β
of the short portfolio is 2.36. The number of shares to go long and short, also listed in the table, are a function of the value of the portfolio and the current price of the stocks. This is a dollar-neutral portfolio, but it is not neutral to market risk. In fact, the
β
of the overall portfolio is roughly
A portfolio neutral to market risk would display a
β
P
of 0. This dollar-neutral portfolio’s
β
of −0.58 exhibits some market risk.
13.2.3 Beta Neutrality (a.k.a. Risk-Factor Neutrality)
The dollar-neutral portfolio is relatively uncorrelated with the market. Whenever one side of the portfolio (long or short) rises, the other side drops. However, dollar neutrality does not guarantee
that the overall portfolio is neutral with respect to many of the risk factors in the economy. A dollar-neutral portfolio may have very low exposure to risk factors, but there is no guarantee that the exposure will be zero. Generally, it could even be quite high or negative. Thus it is better to create a market-neutral portfolio that is not only dollar neutral but also neutral with respect to market risk factors according to some risk model of equities.
The market-neutral portfolio should be, at the very minimum, both dollar neutral and neutral to market risk. For the portfolio to be neutral to market risk, the weighted-average capital asset pricing model (CAPM)
β
of its long and short sides must equal 0.
4
Thus
where
N
L
and
N
S
represent the number of stocks in the long and short portfolios, respectively, and
β
i
is the
β
of stock
i
with respect to the market index return.
5
One should remember that in the short portfolio, the stocks will be shorted; thus the actual exposure will be the negative of the overall
β
of the short portfolio.
With this method, the manager achieves a simple yet effective market-neutral portfolio. Some managers may want to make the portfolio neutral to many more factors—perhaps all the factors—contained in some risk model. This can be done by building the entire portfolio with a constraint that sets all the factor exposures to zero. More generally, the optimization would be run such that
where
k
represents the
k
th factor. With no exposure to any of the risk factors, the portfolio theoretically should return the risk-free rate and have an
α
of 0. However, to the extent that markets are not efficient, the portfolio may have a positive
α
.
Continuing with our example from the preceding section, we use an optimizer
6
to construct a dollar-neutral and
β
-neutral portfolio.
Table 13.3
contains the portfolios, which are both dollar neutral and
β
neutral. Notice that we have allowed a relatively high
β
of 2.0 for the long and short portfolios because if we had tried to keep their
β
’s lower, it would have been difficult to achieve a
β
-neutral portfolio without excluding many stocks. Even with such a high
β
, on the long side we end up having to altogether forgo purchasing two of our preferred stocks, AMD and CDNS. On
the short side, in order to achieve the high
β
, we have to assign a 65.5% weight to UAL. This means shorting $59 million of UAL. Here we run into some practical limitations of the optimization. Shorting so much of one stock might not be feasible from a liquidity point of view, and it would reduce the overall diversification of the portfolio. We will discuss these sorts of practical issues in more detail in the last part of this book (
Chapters 16
and
17
), which covers empirical examples of quantitative equity portfolio management (QEPM). In this case, a better way to achieve the
β
neutrality might have been to relax the dollar-neutrality constraint.
TABLE 13.3
Example of a Dollar-Neutral and
β
-Neutral Portfolio
13.2.4 Market-Neutral Portfolio Out of a Long-Only Portfolio
An alternative way to create a dollar-neutral portfolio or a
β
-neutral portfolio is to create one out of two existing portfolios. A dollar-neutral portfolio can be created easily as long as we have two portfolios with different expected returns. Suppose that we have two portfolios,
A
and
B
. Portfolio
A
’s expected return is higher than portfolio
B
’s expected return. A simple way to create a dollar-neutral portfolio with a positive return is to take a long position in portfolio
A
and a short position of the same size in portfolio
B
.
For a
β
-neutral portfolio, we need two portfolios with identical factor exposures.
7
Suppose that portfolio
A
has factor exposures identical to benchmark
B
’s factor exposures. The portfolio manager could have constructed portfolio
A
using the technique of factor exposure targeting described in
Chapter 9
. Then, taking a long position in portfolio
A
and a short position of the same size in benchmark
B
results in a
β
-neutral portfolio. If the benchmark is also traded as a futures contract, this market neutrality can be achieved easily by shorting the futures contract.
8
13.3 MARKET NEUTRAL’S MOJO
Suppose that a portfolio manager creates a market-neutral portfolio hedged against all risk factors. It is then possible to compute the expected return of this strategy. Assuming that stock returns are
driven by some multifactor model, the excess return of stock
i
can be represented as
where there are
K
factors representing security returns,
β
i,k
is the sensitivity of stock
i
to factor
k, f
k
is the factor excess return, and
ϵ
i
is the residual return of security
i
. The excess return to a marketneutral portfolio when all risk factors are set to be neutral is
Thus the expected excess return of the market-neutral portfolio is
According to the arbitrage pricing theory (APT), the market-neutral portfolio should have no expected excess return, but we are assuming that the market is not completely efficient and/or that the portfolio manager is good at picking outperforming and underperforming stocks. If you make a further assumption that
α
L
= −
α
S
=
α
(i.e., that the long portfolio’s
α
and the short portfolio’s
α
have the same absolute value but opposite signs), then the market-neutral portfolio achieves its
2α
, that is,
This is the market-neutral strategy’s hidden source of
α
mojo. It is one of the advantages of the market-neutral portfolio over a long-only portfolio, which can achieve only 1
α
. It is important to point out, though, that this
α
mojo comes purely from the leverage in the market-neutral portfolio, in which the full capital is invested both on the long side and on the short side.
9
Without the leverage,
the
α
would be no greater than the long-only portfolio’s
α
unless very big, unexploited opportunities existed on the short side.
In addition to the expected return, it is possible to calculate the variance of the market-neutral portfolio:
If we make the assumption that
V
(
ϵ
L
) =
V
(
ϵ
S
) =
ω
2
, then the variance of the market-neutral portfolio reduces to
where
ρ
is the correlation coefficient between
ϵ
L
and
ϵ
S
.
Though
α
mojo is by itself a benefit, extra
α
comes at a price, and this should matter to the portfolio manager. The manager should be concerned with attaining a higher
information ratio
than the long-only portfolio.
10
The information ratio (
IR
) of a long-only portfolio is
whereas the information ratio of the market-neutral portfolio we considered earlier is
Thus the ratio of information ratios of a market-neutral to a long-only portfolio is
One can immediately see the benefits of a market-neutral strategy in the information ratio. Since the correlation between
ϵ
L
and
ϵ
S
is always less than or equal to 1, the market-neutral strategy improves on the long-only portfolio. In the extreme case of perfect correlation, the ratio of information ratios tends toward infinity.
11
In this case, the long and short portfolios (after shorting) move in opposite directions, reducing the overall portfolio variance.
Market neutral’s advantage, however, does not come only from the correlation between the long and short portfolios. The mere ability to short securities itself offers a distinct advantage. A long-only manager cannot take any particular action on a stock that he or she expects will crash; all he or she can do is not buy it. These constraints may actually cause greater mispricings and make
α
S
>
α
L
. With a long-short portfolio, the portfolio manager can have an outright negative weight on the stock and take advantage of this.
13.4 THE MECHANICS OF MARKET NEUTRAL
This section guides you through the mechanics of creating long and short positions in the securities markets.
13.4.1 Margin and Shorting
Equity securities in the United States can be purchased on margin. This allows an investor to invest more in securities than he or she has in cash. The Federal Reserve Board regulates margin and margin requirements through Regulation T.
12
For some time now, Regulation T has required that a customer deposit at least 50% of the current market value (CMV) of a marginable security. This is known as the
initial margin
, which is the margin required on first purchase of the equity security. For example, if a portfolio manager purchases 20,000 shares at $10 per share, the customer technically could borrow up to $100,000 from the broker for this $200,000
purchase of securities. Of course, the broker-dealer will charge interest on the margin, often the broker
call rate
(the rate the bank charges the broker-dealer) plus some markup. We will call this margin rate
i
M
.
13
There is margin for both going long and shorting stocks. However, because of the interest cost of trading on margin, the portfolio manager should trade on margin only with a specific objective in mind.
Suppose that a portfolio manager buys 200 shares of
ABC
at a price per share of $50 and on 50% margin. This would be $10,000 of security
ABC
. His or her CMV is $10,000, his or her debit balance
D
is $5,000, and his or her equity
E
is $5,000 (
E
= CMV−
D
). These are broker-dealer terms. Clearly, as each day passes and the brokerage firm marks to market, the CMV, and hence the equity, will change. Marking to market means the broker-dealer obtains the current value of the security each day and monitors whether the funds deposited by the portfolio manager are sufficient to cover the risks of a margined position. For example, if the price of
ABC
drops to $30 the next day, the account equity will drop to $1,000. This is worrisome because the manager has only $1,000 in equity and a loan of $5,000. To address this sort of problem, the Financial Industry Regulatory Authority (FINRA) and the stock exchanges have established rules that require a
minimum maintenance margin
. If a customer’s equity value falls below some threshold, the broker-dealer makes a
margin call
that requires the customer to deposit extra securities or cash. The current threshold value is 25% of the CMV.
14
If a customer receives a margin call, he or she must deposit enough funds to reach the minimum maintenance margin, or the broker-dealer may sell securities to achieve this minimum.
When a portfolio manager shorts a stock, he or she is effectively borrowing the stock from someone (the broker-dealer arranges this) and then selling it. Since this is like trading on margin, the manager must deposit margin for the stock. Regulation T therefore
applies to short sales of equity securities as well. With a short account, the initial margin is also 50%, but the minimum maintenance margin is 30%.
15
Accounting for a short position differs slightly from accounting for long margin trades, but the concepts are basically the same. On shorting the security, the broker-dealer receives the value of the short sale in cash plus additional cash (or some other deposit) representing the 50% margin. We call this initial cash balance
C
. The CMV of the securities is computed daily. The equity
E
of the account is equal to the cash deposit less the CMV, that is,
C
− CMV. For example, to short 200 shares of a stock at a price per share of $50, using a 50% margin, the portfolio manager deposits $5,000 as cash. The proceeds from the short sale are $10,000. The cash in the account is therefore $15,000. The CMV is $10,000, so the equity in the account is $5,000. As with long positions, if the stock price rises, the broker-dealer may require additional deposits as the minimum maintenance margin is reached.
16
When a portfolio manager has both long positions and short positions with a broker-dealer, the broker-dealer computes the margin requirements of the long and short accounts separately and then nets them to determine the total equity in the account.
13.4.2 The Margin and Market Neutral
With Regulation T in mind, a market-neutral portfolio manager with $
V
in capital can invest $
V
in a long portfolio and then short $
V
of the short portfolio. A margin account will be required for every security sold short in the short portfolio, so the manager will have to post margin. In this case, though, the long positions can be used as margin collateral. Given the 50% margin requirement, the portfolio manager either could deposit $
V/
2 in cash with the broker to cover the shorts or could just deposit $
V
of long securities.
17
Theoretically, the portfolio manager could purchase $
V
of the long portfolio and short $
V
of the short portfolio and satisfy the Regulation T margin requirements.
In practice, however, a broker or prime broker usually requires an additional
liquidity buffer
to meet mark to markets on the short portfolio and to satisfy dividend payments on the short portfolio.
18
Thus the broker may require an additional 10% of the value of the capital. In our example, this would be an additional 0.10
V
. Let’s call this extra liquidity buffer requirement
m
lb
. For any amount of capital
V
, the maximum that can be invested on one side in a fully leveraged market-neutral portfolio is
V
* =
V
(1−
m
lb
). Thus the total maximum amount invested would be 2
V
*. Of course, the portfolio manager can choose to leverage to a lesser degree. He or she could invest
V
/2 in the long portfolio and
V
/2 in the short portfolio, and this would achieve the same degree of gross leverage as a long-only portfolio, but zero net leverage.
19
13.4.3 Sources of the Return
Suppose that a portfolio manager has identified a basket of securities to go long and a basket of securities to sell short. Call these portfolios
L
and
S
. A quantitative model has predicted excess returns for the long portfolio and negative or relatively lower excess returns for the short portfolio. The manager’s equity capital is
V
, and the additional margin required by the broker is 10% (
m
lb
= 0.10). Let’s assume that the manager has $100 million in equity capital (
V
= $100 million). Given the margin requirement, he or she will purchase $90 million of the long portfolio and sell short $90 million of the short portfolio. Thus the portfolio manager has chosen to fully leverage the market-neutral portfolio (i.e.,
V
* invested in the long and short sides). He or she also has chosen to be dollar neutral.
Figure 13.1
illustrates the pattern of flows to create this market-neutral portfolio.
FIGURE 13.1
Flows in creating a market-neutral portfolio.
Ignoring any margin calls, we can dissect the returns that will accrue to the market-neutral portfolio. The first source of return is the difference in total return between the long portfolio and the short portfolio,
r
L
−
r
S
, where
r
S
is the return
before shorting
, the actual return of the weighted short portfolio.
20
The expected
α
of the overall portfolio, if the hedging is done perfectly, equals
α
L
−
α
S
. In practice, it may differ slightly from this value, but it can be measured exactly.
The second source of return is the interest on the proceeds of the short sale that are used as collateral. It usually will be a haircut to competitive short-term investment opportunities available in the marketplace. One should expect to receive, over a period of
k
days and using continuous compounding,
.
21
The third source of return is the interest paid by the broker on the liquidity buffer. We shall assume that the liquidity buffer rate is
i
′. Thus, over a period of
k
days, one would receive
.
The value of the portfolio after
k
days (assuming we close all positions) would be
22
Suppose that we hold the market-neutral portfolio for one month (
k
=30). Portfolio
L
increases by 7%, whereas portfolio
S
decreases by 4%. Suppose that the interest on the collateral and liquidity buffer is 2% per annum at a continuously compounded rate. In our example, the new value of the portfolio would be $110,066,805.63. This is composed of the long P/L of $6,300,000.00 plus the short P/L of $3,600,000.00 plus the interest on the collateral of $150,125.07 and finally the interest on the liquidity buffer of $16,680.56. The return is 10.07% for the one-month period. This calculation is summarized in
Table 13.4
.
TABLE 13.4
Sources of Return from Example Market-Neutral Portfolio
13.5 THE BENEFITS AND DRAWBACKS OF MARKET NEUTRAL
Market-neutral portfolios offer a host of benefits for quantitative portfolio managers who wish to select specific stocks with their quantitative models. They allow the portfolio manager to focus his or her ability on stock selection with few disruptions from movements of the overall market. There are also some minor drawbacks to a market-neutral portfolio, including, of course, the
transactions costs of creating it.
Table 13.5
lists more of the benefits and drawbacks.
TABLE 13.5
Benefits and Drawbacks of a Market-Neutral Portfolio
Perhaps the most return-enhancing benefit of a market-neutral portfolio is the ability to short stocks. There tends to be a long bias in the market. Many money managers, including mutual fund managers, are restricted to long-only positions by institutional rules, and a majority of investors are either not aware of or just plain wary of shorting strategies. A wide variety of stocks may be overpriced owing to the lack of adequate shorting in the market. Thus the very act of shorting may exploit market inefficiencies.
A closely related advantage of a market-neutral portfolio is that in a long-only portfolio the worst view of a stock results in only a 0% weighting of that stock, whereas in a market-neutral portfolio, the manager can express a negative view with an outright negative weighting.
A third benefit is that the market-neutral portfolio is more flexible than the long-only portfolio. The long-only portfolio cannot stray too far from the benchmark owing to risk constraints, so it’s stock weightings must match more closely those of the benchmark. The market-neutral portfolio is not bound to the benchmark, so its stock weightings can follow many different patterns.
Extra diversification is another big benefit of the market-neutral portfolio when the stocks in the long and short portfolios are not very correlated. We know from basic portfolio theory that combining two securities with less than perfect correlation results in diversification. That is, by combining the two securities, the portfolio manager obtains a portfolio with returns similar to but with risk less than what either security in isolation would achieve. Since most stocks tend to be somewhat positively correlated, a long-only manager can get only so much of this diversification kick. However, since the stocks in the short portfolio are sold short, the manager effectively creates a negative correlation between the short and long portfolios. Depending on the extent of this negative correlation, the market-neutral portfolio can achieve greater diversification than can the long-only portfolio.
The benefit of diversification is truly amazing. Consider
Table 13.6
, which describes two portfolios if they are both held long. One is the “good” portfolio because its expected return is high, and the other is the “bad” portfolio because its expected return is low. Both portfolios have similar risk.
TABLE 13.6
Return and Risk Characteristics of Good and Bad Stock Portfolios
Now consider the possible ways of owning the two portfolios. For an overall portfolio that is long only, the weightings of the long and short portfolios must sum to 1. That is, we could own 100% of the good portfolio and 0% of the bad portfolio or 0% of the good portfolio and 100% of the bad portfolio or some combination in between those two extremes. From the perspective of diversifica
tion, it is better to own a bit of both portfolios.
Figure 13.2
illustrates the idea. As we move from the point at which 100% is invested in the bad portfolio to the point at which 55% is invested in the good and 45% in the bad, we improve our risk-return combination. The frontier between 100% in the good portfolio and 55%–45% represents the efficient portfolios for a long-only manager, and we would pick an investment point along this frontier.
FIGURE 13.2
Diversification enhancement from a long-short portfolio.
However, if we could short stocks, we could do better. By allowing for shorting the bad portfolio, the efficient frontier actually moves to the left. There is a whole area, ranging from 100% long the good portfolio to 100% long the good portfolio and 71% short the bad portfolio, where we actually achieve lower risk for the same return that we could earn with the long-only portfolio. This risk reduction demonstrates the power of market-neutral investing.
In addition to the low correlation between the long and short sides of the portfolio, the market-neutral portfolio is relatively uncorrelated with market movements. This offers a benefit to investors who wish to invest in equities but do not wish to be exposed to overall market risk.
A final benefit of market-neutral portfolios is that they allow the portfolio manager to focus on stock picking without having to worry about market timing or exposure to a poorly performing market. During the internet bubble, a market-neutral manager would not have been outright long internet stocks. He or she would have been long certain stocks while shorting others so that his or her portfolio probably would have fared well even when the bubble burst.
Most of the drawbacks of the market-neutral portfolio are not terribly detrimental. Shorting stocks is subject to certain restrictions that make shorting stocks sometimes difficult.
23
This means that one cannot always short quite as easily as one can go long. Interest rates on the proceeds from the short sale may be less than current
market rates, causing a slight loss in potential return. Prime brokers typically require an additional cash liquidity buffer to handle the short portfolio for things such as dividend payments and margin calls. This takes some of the portfolio out of the market, but it is not a big problem because the market-neutral portfolio is usually leveraged anyway.
24
In a bull market, market-neutral portfolios will usually underperform all equity portfolios. This is the price of avoiding market collapses. Finally, a market-neutral portfolio focuses the returns on stock picking. Thus, while it aids a manager who is good at stock picking, it only magnifies the losses of a manager who, either for lack of a good model or simply because of bad luck, does not pick stocks well. There is no market-neutral strategy to disguise a poor model.
13.6 REBALANCING
Market-neutral portfolios need to be rebalanced as time passes to maintain market neutrality. At the same time, the market-neutral portfolio must meet margin requirements. We shall briefly discuss these two rebalancing needs.
Let’s start with the case of dollar neutrality. Suppose that we create a dollar-neutral portfolio at time
t
. At time
t
+ 1, the weights of the long portfolio and short portfolio will have changed. In particular, dollar neutrality at time
t
implies that
At time
t
+ 1, this will no longer be true because
Only if the long portfolio and short portfolio had performed identically during the period would the overall portfolio have remained perfectly balanced. In all but the rarest of cases, therefore, the dollar
neutrality must be reestablished. If the long portfolio has grown larger than the short portfolio, then selling stocks (in amounts proportional to their weights) from the long portfolio and keeping the funds in cash will reestablish the dollar neutrality. If the short portfolio has grown larger than the long portfolio, then buying back or covering some of the shorts will reestablish the dollar neutrality.
For the case of
β
neutrality, at time
t
, we have
However, at time
t
+ 1, we have
At time
t
+ 1, rebalancing reestablishes
β
neutrality. The rebalancing process is simpler for
β
neutrality than it is for dollar neutrality. You can restore
β
neutrality by reducing the dollar value of the portfolio that now has the larger
β
, as in the case of dollar neutrality. You also can adjust the weights of the stocks within one of the portfolios, either the long or the short, so that the average weighted
β
is the same as it was originally. Or, in lieu of either of these methods, the portfolio manager simply can use index futures to alter the entire portfolio
β
. If the overall
β
has become slightly positive (or slightly negative), the portfolio manager can use concepts from
Chapter 12
on leverage to reduce (or increase) the
β
to 0.
25
13.7 GENERAL LONG-SHORT
This chapter has focused on the construction of market-neutral portfolios in which the securities that the portfolio manager goes long exactly offset the securities that he or she shorts. Some portfolio managers bias the portfolio toward either the long or short sides either by design or as a consequence of their investment processes. This style of managing the portfolio not to be perfectly market neu
tral is known as
long-short
. In this section we discuss the general concept of partially hedging the portfolio this way. We also discuss the concept of
equitization
, or using index futures contracts to alter the portfolio’s exposure to the overall market. Finally, we discuss
pair trading
, which is a bit like market neutrality on a pair of stocks.
13.7.1 Long-Short
Up to this point in the chapter we have looked at market-neutral portfolios that are either dollar neutral or risk factor neutral. Some portfolio managers want to construct their portfolios so that they are not entirely market neutral but retain some bias toward either the long or the short side. All of the concepts that we have explored thus far still apply, except that in the
long-short
portfolio there is some difference between either the dollar values or the risk exposures of the long and short sides. For example, the portfolio may have an overall
β
of 0.4 with respect to the market portfolio. It is not really market neutral, although it certainly has less risk than an all-equity index such as the S&P 500.
Long-short is a common portfolio style. It represents about 5% of the hedge fund world.
26
A long-short manager who is bearish on the equity market might be slightly short, whereas another who is optimistic might be slightly long. Along with the additional risk, the long-short strategy lets a manager benefit from overall market movements and
α
mojo.
13.7.2 Equitization
Equitization
is the process of converting cash into a synthetic equity position with equity futures, forwards, or options. Through equitization, a portfolio manager with a market-neutral portfolio can keep his or her
α
and also have full exposure to the equity market. To alter the portfolio’s exposure to the market, the manager can use equity index futures to go long the index an amount equal to 100% of the equity capital.
27
The return on the new portfolio will equal the return from the market-neutral side plus the return on the index
futures. The market risk of the portfolio will be 1 (that is,
β
P
= 1). The portfolio will have all the attributes of a long-only portfolio, as well as the advantages of a market-neutral portfolio.
Equitization is especially useful to a portfolio manager who must maintain a significant exposure to a specific equity benchmark but has views on the relative performance of stocks. To take one example, if the manager feels that certain sectors of the economy are the most mispriced, he or she can focus on making many trades in those sectors. If he or she finds great opportunities in, say, the consumer staples sector, he or she can create a market-neutral position within consumer staples, leaving other sector exposures long-only, as dictated by the long index futures position. The resulting portfolio will still behave very much like the benchmark, but benefit from the hidden
α
of the market-neutral position in consumer staples.
13.7.3 Portable
α
Equitization can be taken a step further via the concept of
portable α
.
28
Portable
α
is
α
that can be transported from the portfolio to another asset class or subclass entirely. This allows plan sponsors, financial advisors, pension fund managers, and other investors the flexibility to separate decisions relating to
α
from the asset-allocation decision. For portfolio managers, portable
α
makes it possible to separate the
α
from the
β
of the portfolio. The construction of portable
α
combines concepts from leverage (
Chapter 12
) and market neutrality (this chapter).
For example, suppose that a portfolio manager is very good at managing small-cap stocks but thinks that large-cap stocks will outperform small-cap stocks. He or she always has had a positive
α
B
when it comes to managing small-cap stocks against a small-cap benchmark such as the Russell 2000. He or she believes that his or her success is due to many inefficiencies in the small-cap universe that he or she is able to exploit with quantitative models. His or her models are less successful in the large-cap universe, perhaps because there are fewer inefficiencies there. He or she tends to manage mainly small-cap stocks, but given that his or her benchmark is the S&P 500 (not the Russell 2000), he or she realizes that if
he or she is correct about large-cap stocks performing better than small-cap stocks, this will hurt his or her relative performance tremendously. This is a perfect situation for the manager to transport his or her small-cap
α
. The manager can continue to manage his or her portfolio as he or she wishes, choosing small-cap stocks that he or she feels are relatively mispriced, but he or she also should short the Russell 2000 futures in order to achieve
β
neutrality vis-à-vis the Russell 2000 and purchase S&P 500 futures so as to achieve a
β
equal to 1 versus the S&P 500. This leaves the manager with a portfolio that has the overall market risk of the S&P 500 plus the
α
B
of his or her portfolio over the Russell 2000.
29
Below we describe the steps of transporting
α
in this example and the resulting overall portfolio:
Step 1:
Find the
β
of the small-cap portfolio versus the Russell 2000:
.
30
Step 2:
Short the required amount of Russell 2000 futures to achieve a
β
* = 0 for the overall portfolio. Then the excess return of the new portfolio becomes
.
Step 3:
Find the
β
of the new portfolio versus the S&P 500. This is done by regressing
against the excess returns of the S&P 500 (
). The new beta estimate will be given by
. The constant term, or alpha intercept, will be given as
.
Step 4:
Go long the required amount of S&P 500 futures to achieve a
. The new
excess return of the portfolio will be
.
Step 5:
The
α
of the new portfolio with respect to the S&P 500 is
. Thus, this method gives the portfolio manager a
β
exposure of 1 to the S&P 500 with an
α
of
. This means that the portfolio manager achieves a perfect
α
transport when
. Depending on other values, his transported
α
might be larger or smaller than his original Russell 2000
α
.
Portable
α
creates a host of possibilities for transporting
α
in the manager’s portfolio. Given that there is no strict mandate on the portfolio’s base exposure, the manager even could transport
α
from an equity universe to a bond universe. For example, the portfolio manager in the preceding example has a positive
α
versus the Russell 2000 equity benchmark by managing a portfolio of smallcap stocks. He or she could short the Russell 2000 futures in the same proportion so as to neutralize his or her overall
β
. He or she then could use the proceeds to invest in either 10-year bond futures or bond exchange-traded funds (ETFs) to acquire a market exposure to the bond markets.
The concept of portable
α
is quite useful, although there are some problems associated with it. First, derivatives, swaps, and even liquid futures do cost money to buy and sell. Second, index futures may not perfectly track the underlying portfolio, even if the
β
versus the index has been measured. The resulting residual risk may be larger than the
α
that the portfolio manager is trying to transport. Third, futures may not exist for a particular portfolio or asset class. In other cases, the futures may exist but be insufficiently liquid. For example, there are some futures for certain sector indices, but they are extremely illiquid and thus not practical. Fourth, while quantitative portfolio managers have the expertise to transport
α
, many pension fund committees and other investors simply do not have the expertise to handle
α
mojo. Fifth, margin may need to be posted for the futures trading, so a slightly lower interest rate is received than with alternative investment vehicles. Sixth, index futures have roll-over risk and basis risk,
and swaps have counterparty risk. For the most part, these risks are small.
Despite the minor problems associated with portable
α
, it is a low-cost mechanism to use capital efficiently and separate the
α
from the
β
of the portfolio so as to achieve the best of both worlds for the investor.
13.7.4 Pair Trading
Pair trading
means creating a market-neutral balance between two securities that are similar except that one is undervalued and one is overvalued (according to a quantitative model of stock returns). The pair trade involves buying the undervalued security and shorting the overvalued security. Just as a market-neutral portfolio removes exposure to market risk and solidifies the connection between the portfolio’s return and its
α
, a pair trade removes market risks from the pair and brings out the
α
’s of the individual securities. Pair trades can be very useful for quantitative portfolio managers for a variety of reasons. They allow the portfolio manager to make trades that focus on
α
without the complications of market or industry risk. Second, they expand the investment universe to stocks in otherwise overlooked sectors. Even if the manager considers the consumer discretionary sector extremely overvalued as a whole, he or she may find good picks within that sector. Pair trading takes advantage of picking these stocks while still avoiding exposure to the overvalued sector. A long-only portfolio simply would avoid the sector altogether. Another useful aspect of pair trading is that it uses equity capital efficiently. The pair trade involves using margin on the short side, so every dollar invested in the pair trade is equivalent to $2 invested in a long-only portfolio without leverage. This is the same efficient use of capital that a leveraged long-only portfolio would provide.
A pair trade can occur when the portfolio manager believes that there is a difference between either the
absolute values
or the
relative values
of the two securities. It could be that the securities are both expected to have a positive
α
, but one of them is expected to have a much higher
α
. In this case, buying the security with the higher
α
and shorting the one with the lower
α
is still a reasonable pair trade because there is a difference in the relative expected movements of the securities. Or it could be the case that a portfolio manager finds two securities that are similar, but one is expected to
have a negative
α
and the other a positive
α
. This is an absolute pair trade, the ideal case.
The first step in pair trading is to identify similar stocks, and
similar
has more than one meaning. One is that the stocks are in the same industry. The manager can apply his or her quantitative model to stocks within an industry and then rank them by aggregate Z-score, or
α
, or expected return. The pair could be two stocks at opposite ends of the ranked list.
Similar stocks also can be found with
characteristic matching
, as discussed in
Chapter 7
. The manager looks for stocks with close fundamental ratios. One should be careful to look at fundamental ratios that are not factors in the quantitative model of stock returns because those factors already drive the expected
α
’s.
Statistical analysis can help to identify stocks that have behaved similarly over time. One test is take the historical returns of stocks and estimate their correlations with each other (their
β
coefficients).
31
Two stocks whose returns are highly correlated, or whose
β
with respect to one another is close to 1 and statistically significant, have behaved very similarly in the past and may tend to in the future. The problem with this sort of analysis is that it applies a relationship gleaned from past data to future expected returns. The value of the analysis, though, comes from the fact that the daily relative volatility of a pair of stocks will be under control if the stocks are highly correlated.
Another way to find similar stocks is to run a regression of stock
A
’s returns against stock
B
’s returns using daily data for a period of one year. The manager runs a series of regressions for every month of the past year and stores the
α
’s of the regression. He or she looks for pairs in which the
β
is close to 1 and the
α
of one stock versus the other is significant and related over time. This kind of similarity would show up in the autoregressive behavior of the
α
of two stocks relative to each other. If the pattern appears, there is a potential pair trade. The risk of one stock offsets the risk of the other, but one stock has an excess return over the other that seems to persist.
It is also possible to take a contrarian view of pair trades. Historical statistical data show whether or not two stocks that are similar have diverged in return movement. If they have, one might believe that they eventually must converge. In the contrarian pair
trade, one would short the stock that has had the higher return over some period and purchase the one that has had the lower return.
Many portfolio managers spend a lot of time researching the fundamentals of the companies before enacting the pair trade. A quantitative portfolio manager, however, relies on his or her quantitative models and statistical techniques. Once a pair-trade candidate has been identified, the next step is to determine how much to trade. There are a number of methods for this, as well. Some managers want to be a bit long or a bit short on one side of a pair trade. We will focus on the case in which the portfolio manager wants to eliminate as much risk as possible and focus on the relative
α
’s of the stocks. As with a market-neutral portfolio, this sort of pair trade can be dollar-neutral or risk-factor-neutral—although, unlike the market-neutral portfolio, it cannot be both at once. Dollar-neutral pair trades are common, although they may be flawed if one stock is much more volatile than the other. Dollar neutrality implies that
w
A
=
w
B
, where the same dollar amount is placed in stock
A
and stock
B
. Risk-factor neutrality adjusts for the risk-factor
β
. The
β
of each stock is measured against some index,
w
B
=
w
A
(β
A
/
β
B
) , where
β
A
and
β
B
are the measured
β
’s of each stock over the same time horizon with respect to some industry index or the market index. You can use
w
A
= 1 and get the appropriate risk-adjusted weight for stock
B
for the pair trade. Since a pair trade is ever undiversified, a portfolio manager may wish to use volatility instead of
β
to determine the relative sizes of the stock trades. In this case, the weights would be determined as
w
B
=
w
A
(
σ
A
/
σ
B
).
Suppose that a quantitative portfolio manager ran his or her quantitative model on the pharmaceutical industry. From the model, he or she has determined that Johnson & Johnson is relatively more attractive than Merck. Since the companies are similar in that they come from the same industry and specialize in drug manufacturing, the manager wants to make a pair trade on these two stocks from January 2021 onward.
The manager already has completed the first step of identifying the stocks to pair trade. The next step is to determine the weights to hold in each security. Using historical data from December 31, 2014, to December 31, 2020, the portfolio manager estimates
β
JNJ
= 0.717 and
β
MRK
= 0.513 versus the S&P 500. For
β
neutrality, he or she will short $1.40 times Merck for every $1.00 exposure to Johnson & Johnson. Another way of saying this is that the relative normalized weights (weights that sum to 1) should be 0.417 and 0.582 for JNJ and MRK, respectively. If, instead, the portfolio manager wants to be
dollar neutral, he or she should short $1 of Merck for every $1 of Johnson & Johnson so that the relative weights are 0.50 and 0.50.
The performance of such a pair trade from December 31, 2020, to August 31, 2021, appears in
Table 13.7
. From this table we can see that owning JNJ outright would have provided a decent return over the period of 10.01%, but with an annualized volatility of 10.79%. Shorting Merck also would have produced a positive 2.19% return but with higher annualized volatility of 17.42%. Together, though, the dollar-neutral pair trade produced an unleveraged return of 6.10% with a lower volatility of 9.77%. Thus, for an average return similar to that of either trade on its own, the pair trade produced a volatility that was less than the volatility of either of the individual securities. The correlation with the S&P 500 was −0.41 compared to −0.38 and 0.23. The
β
-neutral pair trade did not perform quite as well as the dollar-neutral one, but both accomplished the desired goal of maintaining return while reducing risk.
TABLE 13.7
Example of a Pair Trade
13.8 CONCLUSION
Where leverage multiplies a portfolio’s exposure to the market, the market-neutral strategy insulates the portfolio from market winds. Market-neutral strategies reduce or eliminate an investor’s exposure to the volatility of the marketplace while still producing substantial returns. In fact, these strategies even can boost the relative contribution of a portfolio’s
α
and be used to transport
α
across asset classes. In this chapter we discussed the two main variants of market neutrality: dollar neutrality, in which the long and short positions equal each other in dollar value, and
β
neutrality, in which the long and short positions have similar
β
’s with respect to certain risk factors.
We showed that market-neutral investing is a great source of
α
mojo because, by letting the portfolio manager sell bad stocks short, it boosts
α
and the information ratio. We also discussed cousins of the market-neutral strategy, including long-short strategies, equitization of a market-neutral strategy, portable
α
, and pair trading.
We have not exhausted the wellsprings of
α
mojo quite yet. In the next chapter we uncover the third major source of investing mojo, a rigorous statistical theory that boosts the value of
α
by quantifying qualitative information.
1
Source
: BarclayHedge. The actual assets under management grew from $5.5 billion to $57.8 billion. The broader category of long-short funds and market-neutral funds declined from 19.45% to 6.07% over the same period.
2
For more details, see Patton (2004). He uses various definitions of market neutrality and finds that while some market-neutral funds do not behave neutrally with respect to the market, most do. He also finds that market-neutral funds are clearly less affected by the market than are other types of hedge funds.
3
In terms of writing a computer program, however, it may be more convenient to remove the short-sale constraint in the optimization and treat the weights of stocks in the short portfolio as the stocks that produce negative weights. An additional constraint can be added that the negative weights sum to −1 and the positive weights sum to positive 1 to maintain the dollar neutrality.
4
To leave some exposure to market risk, the portfolio can be set with a
β
not exactly equal to 0. Even if
β
P
is not exactly equal to 0, it is sometimes possible to achieve
β
neutrality with a futures overlay. At this point, though, we are not considering the use of futures.
5
Of course, the portfolio manager can construct the market-neutral portfolio to be neutral with respect to the market index of his or her choice (e.g., S&P 500, RusseII 1000, and NASDAQ 100).
6
We discuss optimizers in
Chapter 9
.
7
In general, we can create a
β
-neutral portfolio if we have two portfolios whose factor exposure profiles are a multiple of one another.
8
In Part V of this book we implement this technique as well as the more direct construction of market-neutral portfolios, as explained earlier.
9
We will see in the margin section of this chapter that in practice the maximum
α
mojo that can be achieved is 1.8 owing to additional cash requirements by the brokers. Theoretically, though, a market-neutral portfolio can achieve two times the
α
of a long-only portfolio. Hedge funds that use prime brokers can increase their leverage beyond a leverage of two, depending on the relationship with the prime broker.
10
The information ratio is a common performance-measurement criterion for active managers. It is the ratio of active return to active risk. A higher ratio implies a better portfolio manager, one who achieves more return for the same amount of risk. This is described in more detail in
Chapter 15
on performance measurement.
11
These arguments were presented in Michaud (1993). Michaud argues, however, that additional costs associated with the short side of the strategy actually may reduce this efficiency of the portfolio. He also worries about the true ability to perfectly hedge all the additional risk factors. It should be mentioned that the ratio in
Eq. (13.13)
holds even without any additional leverage in the market-neutral over the long-only portfolio.
12
The Securities Exchange Act of 1934 granted the Federal Reserve Board this authority.
13
Broker-dealers make a large amount of their profits from margin lending.
14
There are other rules as well. The customer must have a minimum equity of $2,000. (This is mostly a concern for individual investors, not usually for managers who run portfolios with millions of dollars in assets.) Some firms also have higher maintenance margins than the minimum requirement. For example, during the internet bubble of 2000, many brokerages placed especially high maintenance margins on certain internet stocks.
15
The minimum maintenance margin is only 5%, though, if the portfolio manager shorts against the box (i.e., shorts the same security that he or she is long).
16
The value of the stock position that will result in a margin call can be figured out by dividing the cash balance by (1 +
m
MM
), where
m
MM
is the minimum maintenance margin requirement.
17
Unmargined securities are worth half the equity of cash. Many hedge funds achieve greater leverage than described here due to their relationships with prime brokers.
18
When someone shorts a stock, all dividend payments from the shorted stocks must be paid to the stock’s owner.
19
In
Chapter 12
, we defined leverage to be net leverage or leverage with respect to market exposure. Gross leverage is also used by practitioners and is the sum of the absolute positions of a trade or portfolio divided by equity capital.
20
While the differences in dividend payments for stocks in the long portfolio and the short portfolio can be considered as a source of return as well, this is already reflected in the return formula.
21
Interest rates from the broker are not continuously compounded rates, but they can be converted to continuously compounded rates, and this makes the math more presentable. Also, one may wish to alter the day count convention from
k
/360 to something else. For a discussion on conversions between rates and general conventions, see Steiner (1998).
22
For the actual computation of historical returns of a market-neutral portfolio, we briefly discuss these calculations in
Chapter 15
on performance measurement. The formula is
r
P
=
r
L
−
r
S
+
r
cash
.
23
For many years, stocks were subject to the uptick rule, which stated that a listed security could only be sold short at a price above the price of the preceding sale (plus tick) or at the last sales price if higher than the previous sale. Short sales were not permitted on minus ticks or zero-minus ticks. Since many practitioners believed these rules did very little for markets, they were removed in 2007. However, in 2010, after the great financial crisis of 2008, the SEC modified the rule, which is now known as the
alternative uptick rule
or the
short-sale restriction
. The rule only prohibits the execution of a short sale order at a price that is less than or equal to the current national best bid if the price of that covered security decreases by 10% from the prior day. This prohibition stays in effect the rest of that trading day plus the next trading day.
24
Many investors believe that market-neutral portfolios must be leveraged. This is not true. Leverage is the choice of the portfolio manager. One can create a market-neutral portfolio that has the same leverage as a long-only portfolio.
25
In addition to rebalancing needs for dollar and
β
neutrality, there are also rebalancing needs owing to the management of short positions.
26
Source
: BarclayHedge and author’s calculations.
27
This example assumes that the
β
of the market-neutral portfolio is equal to 0. While there will be a requirement by the futures broker for margin on the index futures, this amount can be supplied through the liquidity buffer used for the short positions. Since the long futures contract will implicitly hedge the short positions, less is required on both sides of the deal to meet margin requirements.
28
Some people refer to this as
α transport
.
29
The portfolio manager will achieve perfect
α
transport only under certain conditions discussed in the detailed steps to create portable
α
.
30
We use double subscripts (
P,R
) to indicate the regression of the portfolio excess return (“
P
”) on the Russell 2000 excess return (“R”), where
, and
(i.e., the excess return of the portfolio or of the Russell 2000 over the risk-free rate). We also use (“S”) to represent the S&P 500. The user can do the entire analysis with or without the risk-free rate. A bar over a variable indicates the in-sample average of the variable. For example,
is the average return of the S&P 500 minus the risk-free rate over the estimation period.
31
One also could use a multifactor model to infer the implied correlations among stocks.
