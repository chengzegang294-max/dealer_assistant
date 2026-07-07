# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = chapter12

---

CHAPTER 12
Leverage
Give me a lever long enough and a fulcrum on which to place it, and I shall move the world
.
—Archimedes
12.1 INTRODUCTION
Given a benchmark, the portfolio return can be broken down into two parts: the part related to the benchmark and the part not related to the benchmark. The first part is measured by the benchmark
β
multiplied by the benchmark return, and the second part is measured by
α
B
plus a random component.
1
That is,
Part of the portfolio’s return is beyond the manager’s control. To some extent the portfolio goes the way the benchmark goes (represented by
βr
B
), and occasionally, it does the proverbial “random walk” (represented by
ϵ
). Yet the portfolio’s success or failure is also up to the manager. He or she has the power to boost the
β
of the overall portfolio. Better yet, he or she has the power to boost the
α
B
. We call this power
α mojo
. Leverage is a potent source of
α
mojo and also can be used to boost the
β
of the overall portfolio.
Leverage is perhaps the ultimate source of
α
mojo. In physics, a lever multiplies the force that is applied to it; in investing, leverage
multiplies the force of the portfolio. With leverage in the form of borrowed capital, a portfolio manager can invest double, triple, or even more of the amount of available equity. If he or she has $10 million and can find a lender to match that amount, he or she will have a leveraged portfolio of $20 million, and every dollar that the leveraged portfolio gains will be twice as much as the unleveraged portfolio would have garnered. Leverage applied in the correct way also can generate major
α
mojo and amplify the benchmark return. Leverage easily alters the risk-return profile of any portfolio. If the portfolio is managed well but its risk-return ratio does not satisfy the investor’s appetite for risk, leverage will pump up both the expected return and the risk level. If the risk is too high, leverage through shorting can decrease the overall return and risk of the portfolio. Investors who like to time the market also can leverage the portfolio to enhance the impact of market-timing trades.
2
The sort of power that leverage confers can be dangerous, though. A massive leveraged portfolio can earn the unleveraged portfolio’s profits three times over, but it also will get hit three times as hard by any losses.
3
Borrowed capital increases the portfolio’s exposure to market swings. It opens up the portfolio manager to margin-call risk, which threatens the portfolio’s liquidity by raising the possibility of having to meet daily margin requirements in adverse market conditions. It exacerbates market-timing mistakes. And if it isn’t handled carefully, leverage can turn into an evil mojo, inflicting severe damage on the portfolio manager’s
α
. A number of hedge funds have gone bankrupt when the portfolio was heavily leveraged and the
α
went negative. Long-Term Capital Management (LTCM) may be the most notorious case, but there have been others, such as the Niederhoffer Investments Fund.
For those who dare to use it, leverage comes in different forms. The manager can borrow additional funds to invest more than the equity capital. He or she can leverage the portfolio through the margin account, since most equities require only 50% initial margin. He or she can use financial instruments and derivatives,
such as REPOs, futures, forwards, equity swaps, and option contracts, which require smaller margin requirements than equities and allow for even higher leverage of the portfolio for a given amount of equity capital. Finally, a portfolio manager can achieve leverage by shorting securities. In this chapter we discuss how to leverage skillfully. We explain practical methods for increasing the leverage of a portfolio primarily through the use of index futures and single-stock futures. We cover several portfolio situations, including that of an index portfolio manager and that of an active portfolio manager attempting to leverage an equity portfolio with a positive
α
. We also discuss issues related to rebalancing a levered portfolio and protecting against unlimited losses.
12.2 CASH AND INDEX FUTURES
The easiest way to leverage an equity portfolio is to use futures contracts on equity indices such as the Standard & Poor’s (S&P) 500 futures, the NASDAQ 100 futures, the Russell 2000 futures, and the S&P 400 futures.
4
Table 12.2
shows the relative monthly trading volume of these and other types of futures contracts, which gives a
sense of their relative degree of liquidity. The S&P 500 futures and the NASDAQ 100 futures are the most liquid futures contracts available.
TABLE 12.1
The Advantages and Disadvantages of Leverage in Quantitative Equity Portfolio Management (QEPM)
TABLE 12.2
Commonly Used Domestic Equity Futures Contracts
In this section we discuss leveraging with equity index futures. The discussion applies mainly to managers whose benchmarks are common equity indices with actively traded futures contracts. We first discuss the magnitude of possible leverage and then examine the practical mechanics.
12.2.1 Theoretical Limits of Leverage
The amount of leverage to add to a portfolio varies with the goals of the manager. Leverage is conventionally measured as the total absolute value of all investment positions divided by the equity capital. Thus, if a manager were long $100 M of futures and short another $100 M of index futures, the conventional measure of leverage would be 2. In this chapter, we use an alternative definition of leverage which could also be thought of as net dollar exposure. That is, in our definition, the manager in the preceding example would have a leverage or exposure of 0. In this chapter, we use leverage mainly to refer to futures positions that increase the net exposure of the underlying portfolio position. In these cases, our formula for leverage coincides with the conventional formula for leverage. When futures are shorted with an underlying long position, our definition of leverage is no longer the conventional definition of leverage. Thus when considering long positions combined with short positions, our definition of leverage is more commonly known as the net dollar exposure. We will use the symbol
l
to illustrate the amount of leverage with respect to the underlying equity capital of the portfolio. Leverage at time
t
will be given by the expression
, where
is the total notional value of the futures positions, and
V
t
is the total equity capital. Thus
l
= 1 represents an exposure equal to 100% of the invested capital and hence may be described as “no leverage” (though we write it as the leverage of one), while
l
= 2 represents a 200% exposure to the equity capital.
5
In the simple case of cash and index futures, leverage affects the portfolio manager’s return primarily by increasing its exposure to the benchmark, its benchmark
β
. To achieve a certain benchmark
β
for the portfolio, one needs to compute the appropriate number
of futures contracts to purchase. The portfolio manager is limited by the extent of the margin requirements of the underlying contract.
Table 12.2
gives a summary of the percentage requirements of some major futures contracts as of December 31, 2020.
Let us use
m
f
to denote the margin percentage requirement for every dollar of futures positions acquired. Theoretically, the highest leverage that could be obtained is
The
β
of the portfolio is simply the
β
of the futures contract multiplied by the leverage ratio.
6
Thus the highest
β
that can be achieved is
where
β
f
is the
β
of the futures contract.
7
Suppose that the benchmark is the S&P 500. If the margin requirement on the S&P 500 futures is 5%, then the maximum leverage that can be achieved is 20 (= 1/
m
f
). This is also equal to the maximum
β
that can be achieved because the S&P 500 futures have a
β
f
= 1 when the benchmark is the S&P 500. At that rather high exposure to the S&P 500, if the S&P 500 had a −4% return, the portfolio would lose approximately −80% (= −4
β
max
= −4
l
max
).
12.2.2 Leverage Mechanics
Although very high levels of leverage theoretically can be achieved in an equity portfolio, rarely do portfolio managers maintain a leverage ratio higher than 2 or 3.
8
There are many reasons for this. Higher amounts of leverage put the portfolio at greater risk of vanishing entirely with a significant adverse market movement. For mutual funds and ETFs, the Securities and Exchange Commission (SEC) has to approve the leverage amount in the prospectus, and it may be very uncomfortable with leverage ratios above 2 or 3. For these practical reasons, we will focus on leverage ratios within a moderate range, but the formulas apply to any sort of leverage up to the theoretical maximum.
In order to construct a portfolio of a given
β
with cash and futures, we can use a formula that describes the
β
of the overall portfolio:
where
β
P
is the
β
of the overall portfolio,
β
i
represents the
β
of instrument
i
, and
w
i
represents the weight of instrument
i
in the portfolio. The weights are calculated relative to equity capital
V
so that the sum of the weights of noncash positions is
l
. The preceding equation just states the relationship that the
β
of the overall portfolio is a weighted average of component portfolio
β
’s. The
β
of cash is equal to 0 and drops out of the equation. Since we are using just cash and one futures instrument, we are left with only one term, the product of the weight of the futures contracts and the
β
of the futures. We denote the
β
of the futures as
β
f
.
In order to find the number of contracts that we need to purchase to achieve a given target
β
, denoted by
β
*, we must satisfy the following equation:
where
N
f
is the number of futures contracts purchased,
q
is the futures contract multiplier (e.g.,
q
= 250 for the S&P 500 futures contract), and
S
t
is the value of the index underlying the futures contract at time
t
(e.g., the S&P 500 value).
9
By rearranging this equation, we obtain the standard formula to determine how many futures contracts should be purchased to achieve a given
β
*:
Suppose that the benchmark is the S&P 500 and that the portfolio manager is purchasing S&P 500 futures. To achieve a portfolio of
β
* = 2, given an S&P 500 trading at 1,000, a multiplier for the large S&P 500 contracts of 250, and a sum of cash equal to $100 million, the appropriate number of futures contracts to purchase would be 800. (The
β
of the S&P 500 futures with respect to the S&P 500 is 1.)
When the portfolio manager purchases
N
f
contracts of the futures, it “costs” him or her
qN
f
F
t
dollars, where
F
t
is the price of a futures contract. Then the portfolio manager needs to keep (
qN
f
F
t
)
m
f
dollars in a margin balance and hold the rest of the equity capital in cash earning interest. The general formula for the amount of cash held is
V
t
− (
qN
f
F
t
)
m
f
.
In our example, the margin amount is $10,075,282 (the product of
q
= 250,
N
f
= 800,
F
t
= 1,007.53,
m
f
= 0.05), and the cash portion of the portfolio is $89,924,718 (= $100,000,000 − $10,075,282).
12.2.3 Expected Return and Risk
When the leverage ratio is 1, the return of the futures contracts
r
f
can be expressed as
α
f
+
β
f
r
B
+
ϵ
f
, where
r
B
is the benchmark
return. Given the leverage ratio of
l
, the expected return and risk of the total portfolio become
where
is the residual risk of the futures contract,
μ
B
is the mean return of the benchmark, and
is the variance of the benchmark return. This clearly shows that although leverage can increase the expected return of the portfolio, it also increases proportionately the risk of the portfolio. In the case of leveraging by purchasing futures contracts on the benchmark itself,
β
f
= 1 and
α
f
= 0 (or close to it), and we can ignore the
ϵ
f
because it will be very small. In this particular case, if we assume that the portfolio and futures returns already have subtracted the risk-free rate, the Sharpe ratio (
SR
) of the overall portfolio is equal to
In this particular case, the Sharpe ratio is independent of the degree of leverage, and the
β
of the total portfolio equals the leverage ratio.
10
Most portfolio managers also earn interest on the margined amount minus a small “haircut”. On the margined sum, one can assume that the manager will receive something like 98% of the short-term interest rate for cash. Throughout this chapter we will use
i
to denote the interest rate on the cash position and
i
′ to denote the interest rate on the margin. We expect that
i
>
i
′ owing to the haircut.
In all our calculations for the expected return of the portfolio, we shall ignore the cash returns of the position for simplicity. However, cash returns are not trivial, especially when the portfolio manager has a substantial amount of cash in his or her overall portfolio.
11
Figure 12.1
show how leverage changes the payoff profile of the portfolio. The horizontal axis represents the value of the index, whereas the vertical axis represents profit and loss of the portfolio. If the index were to go to zero, the portfolio would lose the entire value,
V
. Without leverage, the index value and the payoff move one for one along the 45-degree line. With leverage, the payoff becomes steeper versus the underlying index. This diagram depicts the payoff when the leverage is equal to 2. With leverage equal to 2, if the index drops by 50%, the portfolio would lose more than double its assets, or 2
V
.
FIGURE 12.1
Portfolio payoffs with and without leverage.
12.3 STOCKS, CASH, AND INDEX FUTURES
The preceding section dealt with leverage in the case of an index manager. Leverage works somewhat differently for the portfolio manager who does not follow an index and instead selects stocks that he or she believes will outperform the benchmark. This manager will calculate leverage and the number of futures contracts in a similar way, but the underlying portfolio will be a portfolio of stocks with weights that already have been chosen according to the optimization method.
12
In this section we discuss leverage for the portfolio manager who owns a portfolio of stocks that he or she picked. This kind of portfolio most likely will have a
β
not equal to 1. We will call the
β
of this portfolio
β
s
.
12.3.1 Theoretical Limits to Leverage
The portfolio manager may wish to hold cash in addition to stocks. Let’s use the term
ξ
to refer to the percentage of the equity capital that the portfolio manager holds in cash. Thus 1 −
ξ
represents the amount of the portfolio’s equity invested in stocks. The maximum
l
and
β
the manager can achieve is
where
m
s
is the initial margin required on stocks (which is also used in determining the collateral value of stocks), and
m
f
is the required futures margin.
13
Thus, with
m
f
= 0.05 and
m
s
= 0.50 if the manager wants to hold 50% of the equity in cash (
ξ
= 0.50), the maximum achievable leverage ratio is 15.5. The
β
max
, for the case of the S&P 500 assuming that
β
f
=
β
s
= 1, is 15.5.
12.3.2 Leverage Mechanics
The portfolio manager may decide to use index futures to alter the overall beta of his or her total portfolio. To achieve the target
β
* of the overall portfolio, the manager would have to satisfy
By rearranging this equation, we can obtain the number of contracts that the portfolio manager will have to purchase or sell to achieve the desired
β
*:
The portfolio manager can achieve any target
β
* provided that
β
* ≤
β
max
. The portfolio manager need not hold any cash for most
β
ranges because the stock portfolio can be used as margin.
14
Returning to our example from the preceding section, the manager now needs to purchase 600 contracts in order to achieve
β
* = 2 with 50% of the equity in cash and a
β
s
= 1. This results in a portfolio that has (
qN
f
F
t
), or $151,129,500, invested in future contracts when the price of a futures contract
F
t
is $1,007.53. The
purchase of the contracts requires margin collateral of (
qN
f
F
t
)
m
f
, or $7,556,462.
15
12.3.3 Expected Returns and Risk
Given the benchmark return
r
B
, the return of the stock portfolio can be expressed as
Similarly, the return of the futures contracts can be written as
Noting that the weight of the stock portfolio is (1 −
ξ
) and the weight of the futures contracts is
l
+ (
ξ
− 1), the return of the overall portfolio is
16
If the underlying futures index is also the benchmark of the portfolio, then we may assume that
α
f
= 0 and that
β
f
= 1. We also will ignore
ϵ
f
because it is very small. Under these assumptions, the expected return and variance of the overall portfolio are
17
where
μ
B
and
σ
B
denote the expected return and the standard deviation of the benchmark, and
ω
s
denotes the standard deviation of
ϵ
s
. It is clear that leverage increases the market risk of the portfolio and reduces the relative contribution of stock picking. As leverage moves from
l
= 1 (no leverage) to
l
= 2 (leverage two times equity), the expected return of the total portfolio increases by
E
(
r
B
), effectively reducing the value that the portfolio manager
adds by stock picking.
18
Depending on the goals of the quantitative manager, this may or may not be a good thing.
Let’s assume for a moment that we already have subtracted the risk-free rate from all the return figures; the Sharpe ratio (
SR
) is defined as the ratio of the expected return to the standard deviation. Thus the squared Sharpe ratio would be
Rearranging the expression in terms of
l
, we get
This expression suggests that as the value of
l
increases, the Sharpe ratio of the overall portfolio approaches the Sharpe ratio of the benchmark.
19
If the Sharpe ratio of the unleveraged portfolio were higher than the Sharpe ratio of the benchmark, then the leverage would reduce the Sharpe ratio eventually.
12.4 STOCKS, CASH, AND SINGLE-STOCK FUTURES
One of the drawbacks to using index futures to leverage a portfolio is that the relative contribution of the
α
is diminished in the returns of the overall portfolio. We saw in the preceding example that the contribution of stock picking can decrease by as much as 50%. Depending on the goals of QEPM, this may not be a concern, but there is a better way to leverage—through the use of single-stock futures. Leverage
created with single-stock futures results in a
leveraged α
rather than just a leveraged portfolio. In other words, it generates
α
mojo.
Unfortunately, as of December 2020, single-stock futures do not exist in the United States; however, they do exist in other countries, including on Euronext, the European stock exchange.
20
Part of the reason that the U.S. stock futures exchange closed was a lack of investor interest, which subsequently created a set of practical problems for investors wanting to use single-stock futures. First of all, there are typically only a limited number of single-stock futures available for trading.
21
Thus, a manager may not find futures for all the stocks in his or her portfolio.
Second, single-stock futures that do exist have less trading liquidity than index futures.
22
Table 12.3
lists some of the major single-stock futures and their volumes on August 7, 2020, shortly before the exchange closed. The table also includes the percentage of a $100 million portfolio that the daily volume represents. Even the third most-traded security has a volume that represents only
2.69% of a $100 million portfolio. For reasonable holdings of around 1% or 2% in a stock, the portfolio manager would have difficulties using single-stock futures contracts to create a leveraged position. This problem becomes more pronounced as one moves down the list of most-traded securities.
23
TABLE 12.3
Highest-Volume Single-Stock Futures Contracts
12.4.1 Theoretical Limits of Leverage
The theoretical limits to leveraging with single-stock futures are very similar to the limits using index futures. There are three essential differences between the two cases, however. The first is that individual stock futures have initial margin requirements that are higher than index futures.
24
The second difference is that singlestock futures allow the manager to increase the maximum
β
by specifically leveraging higher-
β
stocks or decrease it by specifically leveraging lower-
β
stocks. Leveraging single stocks according to their
β
’s is also a sensible way to leverage one’s
α
if one already has chosen the optimal stock weights. A third concern that is unique to leveraging with single-stock futures is that if the futures are not actively traded, then it will be possible to achieve only partial leverage. For the time being, we will assume that the futures are traded actively enough for the portfolio to achieve maximum leverage.
For leveraging a single security, the formulas for the maximum leverage and maximum
β
for single-stock futures are identical to
Eqs. (12.10)
and
(12.11)
, but with the single-stock futures margin requirement replacing the index futures margin requirement. For these leverage formulas to be the same for the entire portfolio when leveraging single-stock futures, all stocks must be leveraged in relative proportion to their weights in the portfolio.
12.4.2 Leverage Mechanics
There are numerous ways to weight single-stock futures in order to achieve the desired
β
level. In this subsection we consider three specific scenarios that a portfolio manager might encounter, each requiring a different weighting scheme.
In one scenario, all single-stock futures contracts are sufficiently liquid to use for leverage. In this case, to achieve his or her target
β
* for the overall portfolio, the manager must purchase the following amount of futures contracts
25
:
In this equation,
q
s
is the contract multiplier for single-stock futures, which is equal to 100,
p
i,t
is the price of stock
i, β
s
is the
β
of the stock portfolio with respect to the benchmark, and
w
i
is the weight of stock
i
in the equity portfolio. The preceding formula indicates that the portfolio manager may purchase single-stock futures for each stock in proportion to the weight of the stock in the equity portfolio.
The second scenario is that only a subset
N
1
of the
N
stocks in the portfolio is available for single-stock futures trading. The manager therefore uses only the stocks with futures to achieve the desired
β
. To achieve his or her target
β
* for the overall portfolio, he or she must purchase the following amount of futures contracts:
where
w
~
i
is the relative weight of the subset of stocks whose futures contracts are bought from or sold to each other (that is,
w
~
i
=
w
i
/
σ
N
1
j
=1
w
j
),
β
~
s
is the weighted average
β
of the subset of stocks whose futures contracts are bought and sold (that is,
β
~
s
=
σ
N
1
j
=1
w
~
i
β
j
), and all other variables are as defined previously.
In the third scenario, there are futures for some of the stocks in the portfolio, and the manager decides to combine single-stock futures with index futures to achieve the desired leverage. He or she purchases the following amounts of single-stock futures contracts and index futures, respectively:
An example might help to further illustrate these three scenarios. Suppose that the benchmark is the S&P 500 and that we have a simple five-stock portfolio consisting of the Mosaic Company (MOS), the Gap (GPS), Cabot Oil & Gas (COG), CME Group (CME), and Walmart (WMT).
Table 12.4
contains the portfolio and the weights of each stock in the portfolio. Using the preceding formulas, we can compute the number of futures contracts required to
achieve our desired
β
*. As in previous examples, let’s assume that our desired
β
* = 2 and that there is $100 million in equity capital. The actual portfolio
β
of the five stocks in this example is 0.83, and the
β
i
for each of the stock’s futures contract is listed in the table (we assume that it is the same as the underlying stock’s
β
). The prices of each stock are also listed in the table. For this example, we do not round the futures contracts to the nearest whole number. Of course, in reality, you would have to do this.
TABLE 12.4
Example of Single-Stock Leverage in a Simple Portfolio
Let’s walk through the example for each of the three scenarios just outlined. Under the first scenario, in which we can use all the stocks’ futures contracts to create leverage, we purchase a total futures value of $141,067,225.94 to achieve our desired
β
* = 2. Since the underlying portfolio has a
β
that is lower than 1 with respect to the benchmark, we need more than an equal amount in dollars to achieve our desired leverage. The number of contracts of each single-stock futures is listed in the table.
Under the second scenario, we assume that some of the singlestock futures—say, CME and WMT—are not liquid enough to trade. Thus we can use only the other three securities’ futures to achieve our desired leverage. In this case we purchase a total value of $110,996,742.57 of futures. This consists of 18,449, 22,524, and 23,103 contracts of MOS, GPS, and COG, respectively. Although in this scenario we have again achieved our desired
β
* = 2, we have leveraged the portfolio disproportionately. The resulting portfolio
α
is tilted toward the first three stocks.
Under the third scenario, we continue to use the first three single-stock futures, but we also use the index futures of the S&P 500 to achieve the desired
β
*. In this case we purchase a total value of $78,919,353 of the single-stock futures and $33,822,580 of the index futures (40 contracts). This also achieves our desired goal, but we have diluted the overall
α
of the portfolio by using index futures.
12.4.3 Expected Returns, Risk, and
α
Mojo
In the first scenario, the total portfolio is composed of the stock portfolio with the weight of 1 −
ξ
and the portfolio of single-stock futures with the weight of
l
−
ξ
+ 1. Recall that given the benchmark return
r
B
, the return of the stock portfolio can be expressed as
The return of the single-stock futures portfolio is essentially identical to the return of the stock portfolio. For simplicity, we assume
26
Calculation of the expected return and the variance of the total portfolio is straightforward in this case. Given the weight of the stock portfolio and the single-stock futures portfolio, the total portfolio return is
The expected return and the variance of the total portfolio are
where
μ
B
and
σ
B
denote the expected return and the standard deviation of the benchmark, and
ω
s
denotes the standard deviation of
ϵ
s
. We can easily calculate the Sharpe ratio (
SR
) of the total portfolio as well. Assuming that the risk-free rate has been subtracted already, the Sharpe ratio is simply the ratio of
E
(
r
P
) to
:
Thus the Sharpe ratio of the total portfolio is identical to the Sharpe ratio of the stock portfolio, regardless of the leverage. That is, the leverage does not change the Sharpe ratio in the first scenario.
In the second scenario, the total portfolio is again composed of the stock portfolio and the single-stock futures portfolio. The weights of these portfolios are identical to the first scenario. The difference is the composition of the single-stock futures portfolio. The single-stock futures portfolio is
N
1
stock futures that are liquid enough. The weights of these futures are given by
.
It will be useful to think of the stock portfolio as composed of two subportfolios: the portfolio of stocks with liquid futures and the portfolio of stocks without liquid futures. Let us call the first portfolio
s
1 and the second
s
2. Then
s
1 is the portfolio of
N
1
stocks with the
weights
defined earlier.
s
2 is the portfolio of the remaining stocks with the weights
. Defining
, we may express the return of the stock portfolio as
Assuming that the return of the single-stock futures is identical to the return of the underlying stocks, the return of the single-stock futures portfolio is identical to the return of portfolio
s
1.
27
Thus we may express the return of the single-stock futures portfolio as
Now, calculation of the expected return and the variance of the total portfolio is straightforward. Given the weight of the stock portfolio and the single-stock futures portfolio, the total portfolio return is
The expected return and the variance of the total portfolio are
where
ω
s
12
is the covariance between
ϵ
s
1
and
ϵ
s
2
.
Assuming that the risk-free rate already has been subtracted, the Sharpe ratio is simply the ratio of
E
(
r
P
) to
, and the squared Sharpe ratio is the ratio of
E
(
r
P
)
2
to
V
(
r
P
). Expressing the
squared Sharpe ratio as a function of the leverage
l
, one can find the relationship:
as the leverage becomes large.
28
That is, as the leverage gets larger, the risk-return relationship of the total portfolio becomes very similar to that of portfolio
s
1, the portfolio of stocks with liquid futures.
In the third scenario, the total portfolio is composed of the stock portfolio with weight 1 −
ξ
, the index future with weight (1 −
ψ
)(
l
− 1 +
ξ
), and the single-stock futures portfolio with weight
ψ
(
l
− 1 +
ξ
). The single-stock futures portfolio is the same as the one in the second scenario, that is, the portfolio of
N
1 stock futures that are liquid enough, with weights
. We will assume that the futures index return is identical to the benchmark return
29
(i.e.,
r
f
=
r
B
). The returns for the stock portfolio and for the single-stock futures portfolio are identical to those of the second scenario, as described in
Eqs. (12.31)
and
(12.32)
.
The return of the total portfolio can be calculated using the weights of the three subportfolios:
The expected return and the variance of the total portfolio are
where
ω
s
12
is the covariance between
ϵ
s
1
and
ϵ
s
2
as defined before.
Assuming that the risk-free rate already has been subtracted, the squared Sharpe ratio is the ratio of
E
(
r
P
)
2
to
V
(
r
P
). Expressing the squared Sharpe ratio as a function of the leverage
l
, one can find the following relationship:
as the leverage increases. Note that the right-hand side of this equation can be interpreted as the Sharpe ratio of a portfolio made of
s
1 (the portfolio of stocks for which liquid futures are available) and the benchmark, with the respective weights of
ψ
and 1 −
ψ
. That is, the Sharpe ratio of the total portfolio approaches the Sharpe ratio of
ψr
s
1
+ (1 −
ψ
)
r
B
as the leverage increases. This is not surprising. As the leverage increases, the portfolio is dominated by the stocks with liquid futures available and the benchmark.
From these formulas, we find that the portfolio’s
α
gets the biggest boost from leverage that uses all single-stock futures (scenario 1). When futures are available for all the portfolio’s stocks and all the futures have enough trading liquidity, the best approach is to leverage only with single-stock futures. It is the ultimate form of
α
mojo. Leveraging with a subset of futures provides the next-best
α
boost, but it may be suboptimal.
12.5 STOCKS, CASH, INDIVIDUAL STOCKS, AND SINGLE-STOCK AND BASKET SWAPS
A portfolio manager who produces positive
α
may wish to leverage his or her portfolio for a variety of reasons. As we have seen, one of the drawbacks to using index futures for leverage is that it saps the relative
α
contribution. Although single-stock futures would resolve this problem, they may not have enough breadth or liquidity to serve as a realistic solution. In this section we discuss two more related alternatives to leveraging. The first alternative is to buy individual stocks on margin; the second is to create a series of individual stock swap contracts with a broker-dealer.
12.5.1 Margining Individual Stocks
Buying stocks on margin requires an initial margin of
m
s
, which according to Regulation T is currently 50%.
30
A manager technically could purchase his or her entire basket of securities on margin, effectively creating a leveraged position as high as
l
= 2. Thus, margining securities allows for any amount of leverage between
l
= 1 and
l
= 2. The benefit of this approach is that the leverage does not diminish the relative
α
contribution—in fact, margining securities leverages the
α
of the portfolio manager. The drawback of this form of leverage is that it is more costly than leveraging with index futures. The broker-dealer charges the broker call rate as interest on the margined loans, a rate that is typically higher than the futures carry rate (i.e., the implied repo rate).
31
Thus, for an index manager who wants to leverage the portfolio, index futures are clearly the better choice. However, a manager who creates
α
by picking stocks should weigh the extra interest costs of the margin against the strength of his or her
α
.
12.5.2 Single-Stock and Basket Swaps
In common parlance, a
swap
is an exchange of one thing for another. In financial markets, a swap is an agreement between two parties to exchange payments with each other. The most common swaps are interest-rate and currency swaps. With interest-rate swaps, it is usually the case that one party pays fixed interest and the other party pays floating interest. With currency swaps, one party makes payment in one currency, and the other party makes payment in another.
32
Equity swaps are usually set up so that one party pays the return of an equity index, whereas the other party pays fixed or floating interest on the notional principal. Equity swaps are a con
venient way for portfolio managers to increase or decrease their exposure to the equity index without actually buying or selling equities. For example, a typical equity swap might have a broker-dealer pay fund
X
the total return on the S&P 500 in exchange for fund
X
paying the broker-dealer some reference interest rate (say, the 6-month LIBOR rate plus a spread).
33
The swap can be customized many different ways.
Equity swaps can be structured for equity indices or for individual equity securities.
34
The portfolio manager can construct a customized swap with the broker-dealer for a basket of securities (
Fig. 12.2
.) This basket or portfolio of securities in the swap is the same as the basket of securities that the portfolio manager believes will outperform the market. The broker-dealer will pay the portfolio manager the return of the basket of securities during the swap period, whereas the manager will pay the broker-dealer some interest rate
i
s
typically specified as LIBOR +
x
. (Alternatively, it might be SOFR +
x
.) The broker-dealer also will charge the portfolio manager some additional fees for setting up the trades because he or she must hedge his or her position. The broker-dealer typically will hedge the position by buying the actual equity basket of securities and taking on a little risk or by buying a futures contract in proportion to the equity basket and taking on slightly more risk. Collateral for such a trade can be arranged through the custodian of the portfolio manager or directly through the broker-dealer.
FIGURE 12.2
Example of flows from an equity basket swap.
The swap periods should match the portfolio’s rebalancing frequency. If a portfolio manager rebalances his or her portfolio monthly, the swap should be reset monthly. With a monthly swap,
the broker-dealer will pay the portfolio manager the return of the basket at the end of the month, and the portfolio manager will pay the interest cost
i
s
. The portfolio manager then will reconstruct his or her optimal portfolio, send a new basket list to the broker-dealer, and construct a new swap for the following month. In this arrangement, the portfolio manager can invest directly in the equities and construct a swap for leverage, or he or she just can hold cash and leverage the entire position with individual stock or basket swaps.
Equity swaps have several advantages over other means of leveraging a portfolio. With swaps on a basket of securities, the portfolio manager can alter his or her
α
directly by choosing a basket of his or her actual optimal portfolio of securities. This is another kind of
α
mojo that index futures do not provide. Also, leveraging with equity swaps is usually cheaper than margining stocks, and it is an alternative for securities that do not have liquid single-stock futures contracts.
12.6 STOCKS, CASH, AND OPTIONS
A manager who has built a portfolio may wish to leverage the portfolio yet another way. Rather than using index futures to increase the market exposure of the entire portfolio, the manager may wish to leverage the portfolio with index options. The reason to do this is twofold. First of all, options have the potential for a nonlinear payoff. They can leverage returns on the upside without leveraging them on the downside. The second reason is that options offer a greater magnitude of leverage than do index futures. This kind of flexibility comes at a cost, though, because options are pricey.
Figure 12.3
shows how the payoff is altered with a call option on an underlying portfolio. The payoff of the overall portfolio is leveraged two times for upward movements in the index but continues to be unlevered for downward movements.
FIGURE 12.3
Portfolio payoffs with and without leverage using call options.
The number of call option contracts required on a given index to achieve a given level of
β
* for the entire portfolio given a current
β
s
for the stock portion of the portfolio will be given by
where
N
O
represents the number of call option contracts to purchase,
q
O
represents the option contract multiplier,
β
* equals the desired level of exposure,
β
s
is the
β
of the stock portfolio, Δ
O
is the delta of the call option,
β
I
is the
β
of the underlying index with respect to the benchmark, and
β
O
= Δ
O
β
I
is just the delta approximation for the
β
of the option contract.
35
For example, suppose that we use the same numbers as in the preceding example. Thus the S&P 500 is trading at 1,000, the portfolio manager would like to hold 50% cash, and the desired
β
* = 2. Normally, a portfolio manager simply will look up the prices of
traded call options and either use a standard Black-Scholes Δ or compute his or her own. Suppose that the price of an at-the-money call option (i.e.,
K
= 1,000) was
c
= 43.58. Suppose that the Δ of this call equaled 0.55.
36
Using our formula, we find that we should have
Thus the portfolio manager should purchase 1,819 calls on the S&P 500. This will provide the desired leverage of 2.
Leveraging through options offers the major advantage of magnifying only the upside. The chief danger of leverage, as explained at the outset of this chapter, is that it creates the possibility of a very hard fall when the portfolio runs into negative returns. With options leverage, though, the portfolio loses only what it would lose anyway. Perhaps this sounds too good to be true. Indeed, the cost of this kind of insurance is steep. The options in this example have a three-month duration. They would cost a total of 100 · 1,819 · 43.58 = $7,927,202. Leverage with downside protection costs $8 million dollars for a $100 million portfolio. This is clearly an expensive method of leveraging, feasible only in specific cases in which the risk of the portfolio calls for downside protection.
12.7 REBALANCING
The portfolio manager has to rebalance the portfolio regularly to maintain the desired leverage position. The frequency of the rebalancing depends on how closely and how long he or she wants to track the
β
* level. If he or she is leveraging only over the short term, he or she may just close the position at the end of his or her short-term time horizon without rebalancing. Portfolio managers offering the leveraged portfolio to clients through a mutual fund, however, may wish to rebalance daily.
37
Other portfolio managers may believe that leverage will offer higher long-run returns and might choose to rebalance monthly. In this section we describe methods for rebalancing at intervals between
t
and
t
+
k
, where
k
can be any period the portfolio manager chooses from
k
= 1 (1 day) to
k
= 20 (1 month, in business days) or longer.
12.7.1 Cash and Futures
For the simplest case of using cash and futures, we know that the
β
P
of the portfolio at time
t
will be
where subscript
t
indicates the time period
t
of each variable. At
t
+
k
, some of the variables will have changed. In particular, the total portfolio value
V
t
+
k
and the value of the index underlying the futures
S
t
+
k
will have changed.
On day
t
+
k
, the portfolio manager will have to compute the desired number of futures contracts required to maintain his or her desired exposure. To satisfy
the number of future contracts required is
The portfolio manager needs to purchase
N
f,t
+
k
−
N
f,t
contracts, which can be expressed as
This equation says that whether the portfolio manager will have to purchase or sell futures contracts (i.e., whether
N
f,t
+
k
N
f,t
is positive or negative) depends on the total return of the portfolio (
V
t
+
k
−
V
t
)/
V
t
and the return of the underlying futures index (
S
t
+
k
−
S
t
)/
S
t
. The value of the total portfolio at time
t
+
k
is given as
where
F
t
+
k
is the price of the futures contract at time
t
+
k, F
t
is the price of the futures contract at time
t
, and
I
t,t
+
k
V
t
represents the interest earned on the margin cash and the other cash of the portfolio at rates
i
′ and
i
, respectively.
38
Thus the return on the total portfolio is given as
The first part of the right-hand side (
N
f,t
qS
t
/
V
t
) is simply the leverage ratio. Assuming no basis risk, we know that [(
F
t
+
k
−
F
t
)/
S
t
] = [(
S
t
+
k
−
S
t
)/
S
t
], and we can make this substitution into our equation.
39
Thus
Now we may rewrite
Eq. (12.46)
as follows
40
:
From
Eq. (12.50)
we can make the following general statement: For a leveraged position (
l
> 1) and a positive return on the index [(
S
t
+
k
−
S
t
)/
S
t
> 0], the portfolio manager must purchase more futures contracts to maintain
β
* or the desired leverage. On the other hand, the portfolio manager will have to sell futures contracts if the index return is sufficiently negative. Since we have a leveraged position, any time the target
β
* is greater than the
β
of the futures contract, we may state the following: If the target
β
* is greater than the
β
of the futures contract, a positive return on the index will lower
β
over time, and the portfolio manager will have to purchase more futures contracts. A negative index return will increase
β
over time, and the portfolio manager will have to sell futures contracts.
Table 12.5
illustrates the various general rules.
TABLE 12.5
Rebalancing Actions to Achieve Desired
β
*
Suppose that there is a portfolio manager whose benchmark is the S&P 500 and who would like to use S&P 500 futures to leverage his or her portfolio. The following conditions exist:
β
f
= 1 for the S&P 500 futures contracts; the multiplier for the contracts is
q
= 250; the beta the manager would like to achieve is
β
* = 2; the value of the equity capital is $100 million; the S&P 500 and the futures contract are trading at 1,000 and 1,007.53, respectively, on day
t
; and the continuously compounded annual interest rates on margin and cash are
i
′ = 0.02 and
i
= 0.03, respectively. To achieve the desired
β
of the total portfolio on day
t
, the manager must purchase exactly
N
f,t
=
β
*
V
t
/
β
f
qS
t
= 2 · 100,000,000/(1 · 250 · 1,000) = 800 contracts. This will create a portfolio with a
β
P
= 2 and a leverage of 2 as well.
Suppose that one day has passed; it is now day
t
+ 1. The S&P 500 and futures values have increased by 5% in one day, so the
β
exposure has changed. The manager wants to readjust it back to 2. Using our formula, we know that the portfolio manager would have to purchase a net amount of futures contracts. This value is given by
Now, in reality, the portfolio manager will have to buy either 38 or 39 contracts, unless he or she uses S&P 500 E-minis to fine-tune the purchase. It is better to round to the nearest integer, so he or she probably will purchase 39 contracts.
12.7.2 Stocks, Cash, and Futures
A very similar change in the
β
of the overall portfolio will occur with the portfolio of stocks, cash, and futures.
41
At
t
+
k
, the futures prices and portfolio values will have changed. In this case, the portfolio manager actually may change the composition of the underlying portfolio; thus
β
s
may change from time
t
to
t
+
k
. The net change in futures contracts becomes
where
β
s,t
and
β
s,t
+
k
are the stock portfolio
β
at times
t
and
t
+
k
, respectively. This is more complicated to analyze. However, if we assume that the stock portfolio
β
is the same or similar between time
t
and time
t
+
k
and that the percentage held in cash is the same, then the net purchases of futures contracts simplifies to
In this case, the conditions that determine whether there are net purchases or net sales are exactly the same as they were in the preceding subsection with only cash and futures.
12.8 LIQUIDITY BUFFERING
Leveraging a portfolio increases the risk of the portfolio. In fact, except in the case of index options that amplify only gains, leveraging itself can create unrecoverable losses—ones that run in excess of the equity in the portfolio. In order to maintain the portfolio’s liquidity, a manager must purchase some form of portfolio insurance. Although there are various ways to achieve this downside protection, we shall focus on how to use
out-of-the-money put options
to prevent the levered portfolio’s losses from exceeding the amount of equity in the portfolio. This method is simple to implement.
First, we need to compute the index loss that would exactly use up the equity value of the portfolio. Once we know this value, we can purchase the appropriate put options in terms of strike price and quantity. Liquidity buffering is applicable to all the leveraging methods discussed in this chapter, but we will focus on applying it to the cash and futures leverage case.
When we create leverage with cash and futures, we know that in a period of time between
t
and
t
+
k
, the value of the portfolio’s equity equals
where
, and all other variables have been defined previously. The goal is to find the strike price of the put options at which all the portfolio’s equity would be consumed. This is the point at which closing the futures position would wipe out the portfolio’s equity. By purchasing put options at this strike price, any further deterioration in the returns of the index and futures would be completely offset by the put options. There would be no further loss in portfolio value, making the leveraged portfolio feasible.
Assuming for simplicity that there is no basis risk (i.e., that we can substitute
r
t,t
+
k
for
, since they are equal), we must find the index return at which all the account equity would be dissolved.
42
This would be the value that equates the loss on the futures position with the current account equity multiplied by the interest factor, that is,
which implies
Let us return to the example we used in the preceding subsection. Suppose that the portfolio manager’s target
β
* = 2,
β
f
= 1, the index value on day
t
is 1,000, and the futures’value on day
t
is 1,007.53. We also will assume for simplicity that interest rates are 0 or that
I
t,t
+
k
≈ 1. The return that would consume the account equity over the
k
-period horizon would be −0.5, or a negative return of 50%.
We have derived this return on day
t
, so we need to find the actual strike price of the put options to purchase. In particular, if the index is trading at
S
t
, then we will want to purchase options with a strike price
. Thus, in our particular example, we would purchase options with a strike price of 500 (or the closest value to that).
The final step is determining how many options contracts to purchase. The simplest method is to use a dollar hedge adjusted for
β
. Thus we compute the number of options contracts to purchase, given the
β
of the underlying index. Thus
where
β
I
is the
β
of the underlying index with respect to the benchmark,
q
O
is the contract multiplier, and
N
O
is the number of option contracts to purchase.
43
Thus, in our previous example with
β
* = 2,
β
I
= 1,
S
t
= 1,000, and
F
t
= 1,007.53,
q
O
for the S&P 500 being equal to 100, the number of options contracts to purchase is 2,000.
An illustration of the overall payoff to the portfolio when out-of-the-money options are used to limit the losses of the portfolio to the equity capital is shown in
Fig. 12.4
. The resulting portfolio looks similar to an in-the-money call option purchased at strike
price
K
and purchased so as to have a twofold exposure to the index in this particular case.
FIGURE 12.4
Portfolio payoffs with and without leverage and liquidity buffering.
We have closed the matter for day
t
. We have created a leveraged portfolio and purchased out-of-the-money put options to protect the liquidity of the account. We should note that these options are extremely out of the money, and index options are not typically available extremely out of the money. It is rare, even on a major index, to find any active trading in options even 20% out of the money. When it does happen, the bid–ask spreads are very wide.
Therefore, practically speaking, creating this type of leverage requires the portfolio manager to form some kind of over-the-counter (OTC) trade with one of the major broker-dealers. The portfolio manager can have the structured desk of a broker-dealer
create these, or the broker-dealer can create them with
flex options
. Flex options (flexible options) are customized equity or index options contracts available on a number of exchanges, including the Chicago Board Options Exchange (CBOE). The flexible elements of the options include the strike price, contracts terms, exercise styles, and expiration dates. Flex options eliminate counterparty risk because they are guaranteed by the Options Clearing Corporation, and they offer more liquidity than a typical OTC contract because they trade on a secondary market. They can be traded in size, expanding or even canceling entire positions.
These options might cost slightly more than the Black-Scholes or standard option-pricing model would predict, but being extremely out of the money, they still would be very cheap.
44
Continuing with the preceding example, we need to purchase 2,000 put option contracts at a strike price of 500. Using the Black-Scholes formula with an interest rate of 3%, a volatility of the S&P 500 of 20%, and a time to maturity of three months, the Black-Scholes price for one option is $1.16 · 10
−11
. The cost of 2,000 contracts is thus $2.32 · 10
−6
. As a percentage of the equity capital, this is 2.32 · 10
−14
%. Clearly, the cost of this insurance, at least theoretically, is insignificant. In reality, the broker-dealer might charge as much as 5 cents per options contract.
To absolutely protect the equity value of the portfolio, one would need to rebalance these options daily. Some mutual funds require daily rebalancing. From a practical perspective, though, these out-of-the-money options contracts could be set up for a three-month duration and not rebalanced until they expire. Rebalancing would take place every three months for the entire portfolio. The risk of losing the entire equity value of the portfolio is minute, especially considering the fact that all exchanges implement trading halts during severe declines in equity.
45
Halts in trading give the portfolio manager time to reposition his or her portfolio if his or her downside potential is not perfectly hedged.
We have just illustrated liquidity buffering in the case of cash and futures. Liquidity buffering works just as well for a portfolio of stocks, cash, and futures. In that case, as long as the portfolio beta is well estimated and the portfolio well diversified, the man
ager can be comfortable that using index options as buffers will prevent catastrophe.
12.9 LEVERAGED SHORT
So far we have discussed the idea of levering a long-only portfolio. What if the portfolio manager has a negative view of the market as a whole? There is no reason that the manager cannot apply these leveraging concepts to short positions as well, whether he or she is an index manager or a stock picker. There are just some minor differences in technique for leveraging a short portfolio.
When an index manager shorts the market, he or she can bypass trading individual stocks altogether, keep his or her equity capital in cash to serve as margin, and short index futures contracts. Shorting is a little more complicated for a portfolio manager who picks stocks to outperform the market. He or she must selectively short low-
α
stocks. We discuss some of the issues related to shorting individual stocks in the next chapter on market-neutral portfolios. For now, we can say that the stock-picking portfolio manager can short stocks a number of ways: by shorting the stocks combined with shorting index futures, by shorting the stocks combined with single-stock or basket swap contracts (in which, as opposed to the long-position swaps, the portfolio manager pays the stock returns), or by shorting the stocks and/or shorting singlestock futures. The concepts involved are very similar to those that govern the long side; they just operate in reverse.
Consider the case of the index portfolio manager who wishes to short the entire index. We already showed how to find, for the long portfolio, the number of contracts to buy to reach a desired overall portfolio
β
. With shorting, the only difference is that rather than
buying
the futures, the manager will
short
them. The equations for long-only portfolios apply to short-only portfolios, the only difference being that the number of contracts will be negative (reflecting the fact that the
β
* is negative).
Given an S&P 500 trading at 1,000, a multiplier for the large S&P 500 contracts of 250, a sum of cash equal to $100 million, and a
β
* = −2, the appropriate number of futures contracts to sell would be 800. (Remember that
β
f
= 1 when the benchmark is the S&P 500.) The portfolio manager should sell the 800 futures contracts at a cost of (
qN
f
F
t
)
m
f
in margin balance. The remainder is held in cash, earning the interest rate.
As for rebalancing the position, the same concepts apply that apply to long-only portfolios. The triggers for rebalancing simply change. A market rally, for instance, would be cause to short futures contracts. A market decline would call for the purchase of futures contracts.
As for liquidity buffering, the portfolio manager also should follow the guidelines of liquidity buffering for long-only portfolios, except that now he or she should buy out-of-the-money call options rather than out-of-the-money put options.
12.10 CONCLUSION
Leverage is powerful. It introduces plenty of risk into the portfolio and has caused the collapse of entire funds. Yet it is the ultimate source of
α
mojo, and it can boost the portfolio’s overall return. In this chapter we explained leveraging for index managers and stock pickers for long-only portfolios and ones that are short on the market. We looked at leveraging with equity index futures, single-stock futures, equity swaps, and options. We explained methods of fine-tuning the amount of leverage in a portfolio so as to control the amount of associated risk. These methods included calculating the appropriate number of futures contracts to achieve any desired
β
or leverage level, rebalancing the portfolio back to the desired leverage ratio, and creating buffers to ensure that the portfolio does not lose more than its equity capital. We have seen
α
mojo at work in the leveraged portfolio. In the next chapter we find it again in the market-neutral portfolio.
1
See
Chapter 2
for further explanation of
α
B
and other variations of
α
.
2
See
Table 12.1
for a list of the advantages and disadvantages of leverage.
3
Some forms of leverage, such as a long-short portfolio, actually can reduce the market risk of the portfolio. Thoughout this chapter, when we speak of leverage, we are implictly referring to an increase in exposure or amplification of the underlying position. Some people call this
net leverage
, which is different than
gross leverage
, which considers the absolute sum of all positions divided by equity capital. We discuss long-short types of portfolios in
Chapter 13
.
4
Futures capital gains and losses are treated differently from other investments for individual investors. In particular, all futures gains and losses are treated as 60% long-term gains and 40% short-term gains regardless of the time of purchase and sale. This can amount to quite a bit for short-term trades. For example, a short-term trade with futures would result in a tax burden of 26.8% with futures compared with a tax burden of 37% with stocks for the top marginal tax rate individual using the individual tax rates of 2020.
5
Note that we are not including the cash position in the numerator when we calculate the leverage ratio as described above, which is standard, since cash is not really considered a risky investment.
6
Throughout this chapter, when we refer to
β
, we are referring to the
β
of the respective instrument versus the benchmark. For portfolio managers who are more accustomed to using
β
with respect to the market (i.e., the S&P 500), one simply need interpret all our
β
’s as the
β
versus the S&P 500. If one does this, in all cases the overall
β
of the portfolio will be with respect to the S&P 500, irrespective of the benchmark. Of course, if the benchmark is the S&P 500, the resulting
β
also will mean a similar thing. The key is that all the measured
β
’s are, with respect to one underlying instrument, either a benchmark or a market index.
7
Since
, the maximum leverage is achieved when all the equity capital is just sufficient to cover the margin requirements, that is, when
. Substituting this into the equation results in the maximum leverage ratio. The
β
of the portfolio is given by
β
P
=
wβ
f
, where
w
is the weight on the futures position (i.e., the futures position over the equity capital). Since we want the maximum
β
, we will create the maximum leverage on that particular futures contract of 1/
m
f
, which by substitution leads to the
β
max
.
8
Rydex pioneered the idea of levered mutual funds and ETFs, which was then copied by other institutions. The early days of creating mutual funds of leverage equal to 2 were challenging. At the time, the CFTC wanted to limit the size of futures positions held by mutual funds and did not allow a mutual fund to hold more than 5% of its NAV in initial margin on futures positions. This made a leverage of 2 or higher untenable with futures contracts. In order to get around this margin restriction, these mutual funds sometimes used options and other loopholes to leverage the portfolio to a level of 2 and higher. The CFTC eventually dismantled most of its margin regulations, and leveraging is less complicated today.
9
For those unfamiliar with trading futures contracts, these terms might look odd. Every futures contract represents the value of an underlying portfolio. Thus, when buying one futures contract, it is contract to buy 1 ·
q
·
S
t
of the underlying index portfolio at a future date. Thus, if one buys
N
f
contracts, one is agreeing to buy
N
f
·
q
·
S
t
worth of a portfolio with equal composition to the underlying index at a future date.
10
In the case of cash and futures only,
. Thus, to achieve a desired leverage ratio
l
*, the portfolio manager solves
l
* = (
N
f,t
qS
t
)/
V
t
for the number of contracts to purchase. Thus,
N
f,t
= (
l
*
V
t
)/
qS
t
. This is equivalent to the
β
* formula when
β
f
= 1. The leverage ratio in this chapter uses the translation of
, which is known as
equal-position matching
. Some investment professionals prefer to define the leverage ratio in terms of
dollar matching
, where the spot price of the underlying contract would be replaced with the actual price of the futures contract.
11
For those interested, all the expected-return calculations in this chapter can be modified to include the amount held in cash by adding the term
ξ
·
r
cash
, where
ξ
is the proportion of equity held in cash. In the case of cash and index futures,
ξ
= 1; it changes in other sections of this chapter. Using notation employed later in this chapter and continuous compounding, the additional cash term can be expressed as
ξ
(
I
t,t
+
k
−1), where
.
If there is no haircut on margin or if margin is covered by other means, let
i
′ =
i
or let
m
= 0.
12
This section also applies to the case of a portfolio manager who owns an exchange-traded fund (ETF) as the main portfolio. ETFs are not preferable for index leverage because they cost more than futures. The size of the trade may be too large for the ETF to handle because ETFs are generally less liquid than futures, and ETFs do not trade after market close (futures contracts do, on GLOBEX). Investors in ETFs essentially pay two intermediaries, the broker and the specialist on the exchange, who will most likely hedge the position with futures. ETFs are clearly less efficient, and only certain circumstances call for them. For example, if the index manager is a sector portfolio manager, his or her best bet is to use sector ETFs combined with futures to get some leverage because there are no liquid sector futures contracts. For the best combination of liquid futures to leverage with, see Chincarini (2004).
13
Since the portfolio manager can use the cash and the equity portfolio as margin for the futures positions, both need to be considered. However, the equity portfolio is worth only
m
s
, or 50% of cash as collateral. Thus, given that a portion
ξ
of the equity is held in cash, the amount of cash equivalents available for margining equals
V
t
[
ξ
+ (1 −
ξ
)
m
s
]. This should be equal to
for maximum margin. Rearranging this equation for
V
t
and plugging it into the equation for leverage results in the equation for maximum leverage when holding a cash-and-equity portfolio. The broker-dealer may require an additional haircut on the equity as margin. Typically, a portfolio management company can have a triparty agreement with its custodian and its broker-dealer such that the custodian sets up a subaccount with securities to be posted for margin for the broker-dealer.
14
In fact, for
ξ
= 0,
β
max
= 11 when
m
s
= 0.5,
m
f
= 0.05, and
β
s
= 1 as in our example.
15
In the case of futures, cash, and an underlying stock portfolio, leverage is defined as
. One can rearrange this equation in order to find the number of futures contracts required for a given target leverage
l
*. It is
N
f,t
= (
V
t
/
qS
t
) [
l
* + (
ξ
− 1)]. For futures indices with
β
f
= 1 (e.g., when the benchmark is the S&P 500 and the portfolio manager is using S&P 500 futures), the number of futures contracts required to achieve a certain
β
* and
l
* is the same.
16
We did not include the cash return in the expected-return calculation; see footnote 10.
17
The expected return of the portfolio and futures is given by
E
(
r
s
) =
α
s
+
β
s
E
(
r
B
) and
E
(
r
f
) =
α
f
+
β
f
E
(
r
B
).
18
For example, if
E
(
r
B
) = 0.13,
α
s
= 0.02, and
ξ
= 0, moving from a leverage ratio of 1 to a leverage ratio of 2 reduces the contribution of
α
s
as a percentage of the total portfolio return from 13% to 7%.
19
Applying l’Hospital’s rule,
20
Single-stock futures trading existed from November 2002 to September 2020 in the United States through the exchange OneChicago. OneChicago, LLC, was a joint venture created by the CME, CBOE, and CBOT for the primary purpose of trading single-stock futures (former website:
www.onechicago.com
). Contract size was 100 shares of the underlying security. Regular trading hours were 8:30 a.m. to 3:00 p.m. Central time. The initial and maintenance margin requirements for single-stock futures were 20% of the cash value of the contract. This was higher than the margin requirement for index futures but still better than buying stocks outright. Also, there was no need to borrow the stock for shorting, nor was there an “uptick” rule.
21
On January 31, 2005, only 122 individual stock futures were available for trading, although growth in the early years was promising. By April 2006, the number available had grown to 200 securities. Shortly before the exchange closed, on August 7, 2020, there were 1,600 listed securities available for trading, but this also included non-stock securities, such as ETFs. On Euronext, about 350 securities are available as of 2021.
22
On August 7, 2020, the total volume of all single-security futures was 11,699 contracts. Furthermore, only 84 contracts had a positive volume on that particular day. The open interest was 149,953.
23
One method for a portfolio manager to deal with the low trading volume is to place a series of limit orders on individual stock futures and have them executed.
24
Before OneChicago closed, the single-stock futures requirement was 20%. ICE Futures Europe has a margin requirement of 5%–10%, and the Euronext exchange has other margin requirements.
25
See
Appendix 12B
for the derivation of these equations.
26
This assumption is true as long as we ignore basis risk.
27
Note that the weights of futures in the futures portfolio are identical to the weights of stocks in portfolio
s
1.
28
Use L’Hospital’s rule to show this.
29
We are assuming that the underlying security of the futures contract is the benchmark and that there is no basis risk.
30
Regulation T is the rule established by the Federal Reserve Board that limits the amount that an investor can borrow to establish a new position in a security.
31
The cost of carry for a futures contract is the implied rate in the
fair-value equation, F
t
=
S
t
e
r
(
T
−
t
)
.
32
For a more detailed discussion of swaps, the reader is referred to Hull (2005), Cox and Rubenstein (1985), Wilmott et al. (1993), and McDonald (2003).
33
LIBOR is the London Inter-Bank Offer Rate, the short-term interest rate at which many international banks borrow from each other. Due to the highly publicized LIBOR scandal that broke in 2012, it might be more common to see the new overnight benchmark called the Secured Overnight Financing Rate (SOFR) being used.
34
Many broker-dealers, including Goldman Sachs, Citibank, and Credit Suisse, structure such equity products. Jefferies, Thomas Weisel Partners, and Raymond James are better for mid-cap or small-cap securities.
35
Index option contracts are 100 times the actual index. Thus
q
O
= 100. All the major index options are European-style options, except the S&P 100, which is an American-style option. For more details, please consult the Chicago Board Options Exchange (
www.cboe.com
) and/or a derivatives textbook.
36
In reality, it will be very unlikely to find a call option that is perfectly at the money (i.e., strike price equal to index value); thus a portfolio manager will have to find the option with the closest moneyness.
37
Since we wrote the first edition of this book, many mutual fund and ETF companies offering daily leverage were sued due to a discrepancy between what investors may have expected and the actual returns of the levered portfolios. For more info, see Cheng and Madhaven (2009), Avellaneda and Zhang (2010), Shum and Kang (2012), Tang amd Zu (2013), and Bruno et al. (2014).
38
The actual formula for
. This is simply 1 plus the continuously compounded interest from both the cash position and the margin position, where margin interest
i
′ is typically lower than cash interest
i
.
39
Basis risk is the risk that the basis will change over time. The
basis
is defined as the futures rate of the index minus the spot rate of the index. That is,
B
t
=
F
t
−
S
t
. If the futures are held to expiration, the futures price will converge to the spot price, and there is no basis risk. However, at any time prior to futures expiration, the basis can change, and this introduces basis risk because the futures movement and spot movement do not offset each other. This can be an issue for hedgers or investors who use leverage. Basis risk can also affect the effectiveness of rolling over a hedge. In reality, the basis moves even if just by a little bit owing to contraction of the time until maturity, but this is very insignificant. When the basis risk is 0, it implies that
.
40
Since we are dealing with only cash and futures, the leverage ratio reduces to just
l
.
41
The analysis in this subsection follows also for a portfolio manager who invests in ETFs, cash, and futures.
42
With no basis risk,
F
t
+
k
−
F
t
=
S
t
+
k
−
S
t
; thus (
S
t
+
k
−
S
t
)/
S
t
= (
F
t
+
k
−
F
t
)/
S
t
. The former is the return on the underlying equity index, which we call
r
t,t
+
k
, and is what we are interested in because the options depend on the value of the underlying index, not the futures. Some people might wish to define the return on the futures contracts as (
F
t
+
k
−
F
t
)/
F
t
, but it really does not matter for this analysis. We are merely transforming the equation into the item we are interested in.
43
In the daily risk management of option contracts, the
β
of the option contract is actually not the same as the underlying index. That is,
, where
β
O
=
β
I
|Δ|, and Δ is the option’s Δ. In order to determine the number of options to purchase, we use
β
I
, since our purpose for creating this option is not for daily risk management but rather to protect against the catastrophic scenario of a huge negative return. In that scenario, the Δ of the option will converge to −1 very quickly; thus, for the purposes of liquidity protection, we assume that it is −1 from the onset.
44
The theoretical Black-Scholes price of these options is infinitesimal, but the broker-dealer typically charges more because, at “fair value,” he or she earns next to nothing for taking on a risk.
45
The New York Stock Exchange (NYSE) halts trading for 15 minutes if the S&P 500 declines by more than 7% on a given day, for another 15 minutes if it declines by 13%, and for the entire day if it drops by 20% or more. For more information, see
www.nyse.com
.
