# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = chapter10

---

CHAPTER 10
Rebalancing and Transactions Costs
Changes aren’t permanent, but change is
.
—Neil Peart
10.1 INTRODUCTION
In April 2020, Invesco reported a rebalancing error with its Invesco Equally-Weighted S&P 500 Fund. Invesco simply forgot to rebalance the fund on April 24, 2020, which cost Invesco a total of $105 million over 5 days.
1
Even when funds rebalance correctly, transactions costs can severely deteriorate their returns. In 2019, the small-cap growth managers who traded most often had annual trading costs of more than 2.5%, while those who traded more cautiously had trading costs below 1%. This difference in costs and ultimately net returns could be the difference between investment success and failure. While the mistake in rebalancing by Invesco and the story of small-cap growth funds magnifies the rebalancing problem considerably, the lesson applies to all funds: managers cannot afford to ignore the intricacies of rebalancing and transactions costs.
Almost all portfolios need to be adjusted during their lifetimes, so incurring periodic transactions costs is inevitable—it is simply a question of how often and how much. The portfolio manager’s
decision regarding an adjustment to the portfolio is called the
rebalancing decision
. Three types of events potentially could trigger rebalancing decisions: cash inflows, cash outflows, and changes in the underlying parameters of the stock-return model. Cash inflows and outflows require adjustments to the portfolio’s positions, and the simplest way to adjust the portfolio in such cases is to buy or sell stocks using the current portfolio weights. (There are better ways to adjust the portfolio in the face of cash flows, but we will come back to that later.) Changes in the underlying parameters do not automatically require adjustments in the portfolio. The portfolio manager needs to decide whether a parameter change is big enough to warrant incurring transactions costs. Suppose that the transaction cost of making some adjustment to the portfolio is 5 basis points (i.e., 0.05% of the total portfolio value).
2
If, by making the adjustment, the portfolio manager can increase the expected return of the portfolio by only 3 basis points, then he or she has not recovered 2 basis points of transactions costs.
When the portfolio manager does decide to rebalance the portfolio, the transactions cost will affect the composition of the optimal portfolio. We ignored transactions costs in previous chapters partly because we wanted to focus on the main ideas of modeling and portfolio construction and partly because transactions costs do not greatly affect the initial creation of the portfolio. However, after the portfolio is in place and changes must be made midstream, transactions costs take on greater significance.
Transactions costs affect the returns on stocks within the portfolio. Take stock
A
, which has an exceptionally high transaction cost of 1% owing to thin trading but a relatively high expected return of 12%. Also consider stock
B
, which has a relatively low transaction cost of 10 basis points and an expected return of 10%. Not including transactions costs, the difference in the expected return between stocks
A
and
B
is 2%. However, including transactions costs, $100 invested in stock
A
will return $10.88, whereas $100 invested in stock
B
will return $9.89.
3
Thus, after transactions
costs, the difference in the expected return between the two securities is less than 1%. This certainly has an impact on the composition of the optimal portfolio.
We begin this chapter with a discussion of the rebalancing decision. Then we discuss how the optimal portfolio changes when we consider transactions costs. In the last section of the chapter we explain ways to control transactions costs.
10.2 THE REBALANCING DECISION
The rebalancing decision involves two questions: when to rebalance the portfolio and how to go about it. From an econometric point of view, the answer to the first question is clear. The factor model we used to pick stocks implies a certain rebalancing period. If we estimated the model on monthly returns, then our optimal portfolio is optimal only for one month. If we estimated the model on quarterly returns, then our optimal portfolio is optimal for one quarter. We must rebalance whenever the optimal portfolio expires, which is the model’s periodicity. We discuss model periodicity in the first part of this section. The more challenging rebalancing question is how to change
α
or other parameters in the model in order to update the portfolio. We will discuss that aspect of rebalancing in the second part of this section.
10.2.1 Rebalancing and Model Periodicity
Financial economists have discovered that models of stock returns do not predict daily returns well. Models approximate patterns that emerge from returns over time, whereas daily returns are heavily influenced by specific news and events that a model often does not take into account. In the extreme case of hourly returns, a model’s predictive powers will approach zero. Some financial economists have had moderate success in applying their models to weekly returns. On the whole, though, weekly returns are still too influenced by specific events. For this reason, the majority of financial research is conducted on monthly returns. On the flip side, the danger of trying to apply the model to longer periods is that the parameters may change during the period. For example, to estimate the
β
of annual returns, one would need a sample spanning at least 20 years. It is unlikely that the
β
of a firm would stay constant for 20 years. The same problem arises for quarterly returns. Monthly
returns are an acceptable middle-of-the-road solution to the tradeoff between predictive power and the risk of unstable parameters.
Whether monthly rebalancing is really the best route depends on market conditions. Markets may be very stable for a month so that nothing fundamental changes. Or markets may fluctuate rapidly, forcing more frequent rebalancing. External restrictions on the portfolio manager, such as large cash inflows and outflows, also alter the rebalancing frequency.
Our suggestion is to “update” the estimation of the models at least once a month if the model uses monthly returns. Updating the estimation does not necessarily lead to rebalancing. The portfolio manager simply should make sure that his or her information is up to date, and from there, he or she can decide whether to rebalance.
10.2.2 Change in
α
and Other Parameters
Changes in the parameters of a stock-return model can trigger rebalancing. Recall from the previous discussion of the factor model that the stock return can be expressed as
If we used an economic factor model to predict stock returns, then we should be on the lookout for changes in
α
and the factor exposures (
β
i
1
, …,
β
iK
). If the model is the fundamental factor model, then we should be concerned about
α
and the factor premiums (
f
1
, …,
f
K
).
Parameters can change at any time. Corporate actions and major changes in the business environment all affect the parameters of a model. If firm
A
merges with firm
B
, for instance, the
α
and other parameters of firm
A
are bound to change. If the government imposes a new restriction on the activity of firm
A
, its
α
and other parameters most likely will change. Even a CEO’s retirement can affect a stock’s parameters. Then there are changes that do not become public knowledge. If the portfolio manager bases
α
on private information,
α
could react to new private information.
Quantitative portfolio managers always should think in terms of the model. If a manager reads a piece of negative news about a stock, it warrants a little time considering whether the news lowers the value of
α
or another parameter.
When the manager suspects that a parameter has changed, it is time to reestimate the model. Updating the values of the parameters
updates the expected return and risk of each stock, and it changes the optimal portfolio. After finding the new optimal portfolio, the manager can decide whether to rebalance the portfolio by comparing the benefit of rebalancing to the transactions costs.
10.3 UNDERSTANDING TRANSACTIONS COSTS
By
transactions costs
, we generally mean the commissions that brokerages charge to execute orders. The commissions vary among brokers and also depend on the trades themselves. The same broker may charge different commissions for trading the same stock depending on the number of shares of the trade or the value of the transaction.
There are also two kinds of hidden transactions costs that portfolio managers should be aware of. These are the
bid–ask spread
and the
price impact
. The bid–ask spread equals the difference between the price at which one can buy the stock (the ask price) and the price at which one can sell the stock (the bid price). The bid–ask spread may reflect the operation cost and profit of a market maker or designated market maker. The lower the liquidity of a stock, the bigger is its bid–ask spread.
Figuring out the bid–ask spread can be tricky.
4
The bid–ask spread is not fixed over time, and, at any given moment, we may be able to observe either the bid price or the ask price. If you compare the ask price from one moment to the bid price from another moment, it is unclear whether the difference between these two numbers reflects the change in the equilibrium price or the bid–ask spread.
5
Price impact is the effect that large orders have on the observed stock price. A large order will move the stock price, causing the portfolio manager to pay more when buying, or earn less when selling, than the price per share quoted before trading. Price impact increases as the transaction size becomes large relative to the market size or daily trading volume of the stock. For a large order, the entire order may not be executed at the quoted price, so the average transaction price for the trade may be quite different from the quoted price before trading. This difference is one measure of the costs of price impact.
According to one estimate, the average broker commission is about 4 basis points of the transaction value, while the price impact is about 21 basis points. If one includes the price effect of delayed trades, the transaction cost exceeds 0.4% of the transaction value. As mentioned earlier, trading small-cap stocks costs more than trading large-cap stocks. The average commissions for large-cap stocks and small-cap stocks are 2.4 and 5.9 basis points, respectively. The average price impact is about 21 basis points for large cap and 19.9 basis points for small cap. Including the price effect of delayed trades, the total transaction cost is around 44.6 basis points for small-cap stocks.
6
In general, it is impossible to anticipate the exact cost of the transaction in advance of its execution. This is especially true of the price impact and the bid–ask spread. One can develop a model and make an educated guess, but that is still far from knowing the exact number.
7
10.4 MODELING TRANSACTIONS COSTS
Given the complicated and unpredictable nature of transactions costs, it is conventional to model them as a fixed proportion of the total value of the transaction. That is, we choose a constant, perhaps 5 or 10 basis points, to approximate the transaction cost per dollar transaction. Let us call this constant
c
. If the transaction value is $10, then the transaction cost is $10
c
.
The total transaction value (
TV
) is easy to determine. Let
V
t
denote the dollar value of the current portfolio. Let
denote the weights of stocks in the current portfolio and
denote the weights of stocks in the prospective portfolio. (Superscript
b
refers to “before,” and superscript
a
refers to “after.”) That is,
is the weight of stock
i
in the current portfolio, and
is the weight of stock
i
in the prospective portfolio. Then
is the current holding of stock
i
in dollar terms, and
is the prospective holding of stock
i
in dollar terms. If
is greater than
, it suggests buying stock
i
. If
is smaller than
, it suggests selling stock
i
. In both cases, the difference,
–
, shows how much to buy or sell, in dollar terms. Therefore, the transaction value is simply the sum of this difference across all stocks:
The transaction cost (
TC
) is a constant fraction of the transaction value; thus
Eventually, we want to include the transactions cost formula in our optimization problem. For that purpose, it is useful to write down
TC
as a linear function, that is,
where
Once formulated in this way, we can express the transaction cost as a vector product of the weight vector and the transactions cost vector. Let us denote the vector of the current weights as
w
b
and the vector of the prospective weights as
w
a
. That is,
, and
. Also, we define the vector of transactions costs as
c
. That is,
c
= {
c
1
, …,
c
N
}. Then
Note that the exact value of
c
depends on the values of
w
a
and
w
b
. Thus
c
is not a constant; rather it is a function of
w
a
and
w
b
in the mathematical sense [see
Eq. (10.5)
].
We can generalize our discussion of transactions costs and allow for different stocks to have different transactions costs. Considering the bid–ask spread and, especially, the price impact, one may want to model the transactions cost as proportional to the liquidity of each stock. For example, one might calculate the average trading volume of each stock and assume that the trading cost is inversely proportional to the trading volume. Elements
of
c
then would have both different signs and different absolute values.
8
10.5 PORTFOLIO CONSTRUCTION WITH TRANSACTIONS COSTS
No matter what conditions or costs arise, the principle of portfolio selection always remains the same. Given whatever constraints we may face, we always want the portfolio with the best combination of expected return and risk. (In the case of managing against a benchmark, we always want the best combination of expected excess return and tracking error.) Transactions costs introduce a new variable into the process of determining the optimal portfolio (or the optimal tracking portfolio), but they do not alter the selection principle itself.
10.5.1 The Optimal Portfolio with Transactions Costs
We may formulate the problem of optimizing the portfolio in the face of transactions costs as a problem of minimizing risk given a certain expected return. In the context of our discussion of rebalancing, however, we prefer to use an alternative but equivalent formulation. Specifically, we formulate the optimization problem as one of maximizing the risk-adjusted return on the portfolio, where the risk-adjusted return is defined as the expected return in excess of the variance.
We start by recalculating the expected return of the portfolio, taking into account the transactions costs. If the expected return of the portfolio is
μ
P
and
V
t
dollars are invested in it, the value of the portfolio at the end of the holding period equals
V
t
(1 +
μ
P
).
However, the portfolio manager needs to spend (
V
t
w
a
−
V
t
w
b
)′
c
in transactions costs, and the ending value of the portfolio must take this into account. That is, we need to subtract (
V
t
w
a
−
V
t
w
b
)′
c
(1 +
μ
P
) from the ending portfolio value. Similarly, we need to subtract the transactions costs from the expected return. That is,
The effective expected return has three components. The first component is the gross expected return of the portfolio. The second component, to be subtracted from the gross expected return, is the transactions cost expressed as a fraction of the portfolio value.
9
The last component is the time value of the transactions cost. Since the transactions cost is paid up front rather than at the end of the period, the portfolio manager loses twice, once by paying the cost and once again by not being able to invest and create profit. The second and the third components of the expected return reflect these losses.
For realistic values of the transactions cost and the expected return, the time value of the transactions cost is very small. For example, if the transactions cost is about 0.1% of the transaction value and the expected return is 1%, then the time value of transactions cost is only 0.001% of the transaction value. Therefore, in the discussion that follows, we ignore the time-value term.
10
To obtain the expression for the risk-adjusted return, let us introduce additional notation. Let
μ
= {
μ
1
, …,
μ
N
} be the vector of the expected stock returns. That is,
μ
i
is the expected return of stock
i
. Let
Σ
be the variance-covariance matrix of stock returns. That is,
where
denotes the variance of the return of stock
i
, and
σ
ij
denotes the covariance between the return of stock
i
and the return of stock
j
. Thus
μ
P
=
w
a
′
μ
is the expected return of the prospective portfolio, and
is the variance of the prospective portfolio return. Let us define the
risk-aversion parameter
as
A
. Given
A
, we define the risk-adjusted return as
. Thus
A
= 2 means that the portfolio manager would not mind if the variance goes up by 1% as long as the expected return goes up by 2%.
Using the preceding notation and considering the transactions costs, the risk-adjusted return becomes
The optimal portfolio can be found by maximizing
Eq. (10.9)
subject to
and any other relevant constraints.
While
Eq. (10.9)
looks like a typical quadratic equation, in fact, it is highly nonlinear. The transactions cost vector
c
depends on the weight vector
w
a
[see
Eq. (10.5)
]. Thus this problem cannot be solved by a conventional quadratic optimization technique. In
Appendix 10A
we present a simple technique that will produce an approximate solution.
10.5.2 The Tracking Portfolio with Transactions Costs
If the portfolio manager is more concerned about tracking error than overall risk, then he or she should maximize the effective tracking-error-adjusted return rather than the effective risk-adjusted return.
Recall that the tracking error (
TE
) of the portfolio is defined as the standard deviation of the difference between the portfolio return
r
P
and the benchmark return
r
B
:
where
As explained in
Chapter 9
, the last term does not depend on the weight vector, so only the first two terms will be used in the optimization problem.
The
tracking-error-aversion parameter A
measures the manager’s aversion to squared tracking error in the portfolio. The effective tracking-error-adjusted return becomes
To find the optimal tracking-error portfolio, we maximize the effective tracking-error-adjusted return with certain constraints. For the purpose of solving this optimization problem, we can ignore the terms that do not include
w
a
or
c
. Thus we solve
subject to the constraint that the sum of weights should be 1 and any other constraints. This problem cannot be solved by a conventional quadratic optimization technique because
c
is a function of
w
. In
Appendix 10A
we present a simple technique that will produce an approximate solution and in
Appendix 10B
we present a more complicated optimization framework that produces an exact solution.
10.6 DEALING WITH CASH FLOWS
As we mentioned in the introduction to this chapter, a manager sometimes has to rebalance the portfolio, or at least make additional investments outside the regular rebalancing schedule. Cash inflows and outflows require this sort of extra rebalancing. In this section we discuss some common methods that the portfolio manager can use to reduce transactions costs in the presence of cash flows. The first method involves investing cash temporarily in index futures or exchange-traded funds (ETFs) until there is a better time (such as the next scheduled rebalancing period) to return it to the portfolio. The second method involves purchasing specific, perhaps more liquid, stocks so as to achieve target portfolio weights through fewer transactions.
10.6.1 Reducing Transactions Costs Using Futures and ETFs
For portfolio managers who have daily cash inflows and out-flows, adjusting the portfolio at each cash movement is just not
practical.
11
For the typical fund, daily flows are small relative to the fund’s assets, and new contributions frequently offset fund redemptions. For such a fund, net inflows can be invested temporarily in cash or money market instruments without adversely affecting the portfolio return. Conversely, the fund’s cash buffer can handle small redemptions, avoiding the need to liquidate any stocks. However, for funds with large daily net flows, maintaining a large cash reserve will negatively affect the portfolio return, especially in an environment of low interest rates. If outflows are large, the manager cannot rely on the cash buffer to meet redemptions and may be forced to liquidate part of the portfolio. This, of course, can be particularly problematic if there is low liquidity or if spreads are wide in some of the stocks.
In such cases, the manager might be better off adjusting his or her exposure in one of two ways, either by equitizing cash with index futures or by purchasing an ETF that invests in the same sector as the fund or a sector very correlated with the fund. ETFs became a more feasible solution for many funds when the Securities and Exchange Commission (SEC) lifted some restrictions on ETF ownership in mutual fund portfolios. Even with the wide availability of sector-specific ETFs, however, a manager still might prefer to use futures because futures have three distinct advantages over ETFs: futures are more liquid in normal trading hours, they can be traded after hours on GLOBEX, and they have an added tax benefit in that gains are treated as partly long term and partly short term. On the other hand, if the horizon for using futures is longer than a few days, then the portfolio manager might have to deal with the challenges of rolling over futures contracts.
10.6.2 Rebalancing toward Optimal Target Weights
Whether in a period of cash flows or at the point of conducting regular rebalancing, a portfolio manager can make the necessary trades in such a way that the portfolio maintains an optimal mix of stock weights. Imagine a portfolio that is rebalanced monthly and experiences cash flows at the end of the month. When it comes
time for the monthly rebalancing, the manager can either trade so that he or she maintains the original optimal portfolio weights or so that he or she achieves the new optimal weights determined by updating/reestimating the model. At the end of the month, the manager faces cash flows but can trade in such a way as to redirect the portfolio toward either the original or new optimal target weights. In the following subsections we discuss the algorithm that enables the manager to conduct optimal trades first in the case of regular rebalancing and then in the case of cash flows. In the analysis, we do not include trading costs per se. Rather, we show that by reducing the amount of trading, we can reduce tax costs as well as direct trading costs.
Standard Rebalancing
Standard rebalancing assumes that the portfolio manager has a target set of stock weights to which he or she wants to rebalance the portfolio. If the portfolio tracks a benchmark, then the target weights are those of the benchmark. Unless a new optimal portfolio with new stock weights has been constructed since the last rebalancing date, standard rebalancing involves selling the “winners” and buying the “losers” of the period since the last rebalancing date. You may be wondering why anyone would want to buy the losers. The reason is that the portfolio manager is concerned about the weights of stocks within the portfolio, not about their individual returns during a given period. Stocks that have performed relatively well will have gained weight in the portfolio so that they now exceed their targets; stocks that have done less well will have lost weight so that they now fall short of their targets. Rebalancing means restoring the weights back to their target levels.
Some notation may be useful. Let’s call
the weight of stock
i
in the portfolio before rebalancing,
the target weight of each stock
i, p
i
the price per share of stock
i
,
the number of shares owned in stock
i
of the portfolio, and
the number of shares implicitly held in the optimal portfolio. The weights of the target portfolio and the current portfolio at any time
t
+ 1 are given by
At any point in time, one can calculate the difference between the target weights and the current portfolio weights and use this difference to rebalance the portfolio. The number of shares of each stock that must be bought or sold at time
t
+ 1 is given by
where
V
t
+1
is the value of the portfolio at time
t
+ 1 before rebalancing, and
C
t
+1
is any monetary contribution to (or withdrawal from) the portfolio at time
t
+ 1. The excess shares
x
i,t
+1
are negative if one needs to sell shares of the stock and positive if one needs to buy more of the stock. One should bear in mind that these formulas do not take into account the bid–ask spreads or the price impact, both of which slightly distort the rebalancing procedure and create costs to the portfolio.
An Example
This example of standard rebalancing involves a portfolio of seven stocks (
A
through
G
).
Table 10.1
considers the portfolio at times
t
and
t
+ 1. At time
t
, the portfolio is valued at $100,000; by time
t
+ 1, it has increased to $107,986.68. At time
t
, the portfolio contains the optimal target stock weights, but as stock prices change between times
t
and
t
+ 1, the portfolio drifts out of alignment with
the targets. The table shows the difference between the weights at times
t
(optimal target weights) and
t
+ 1 (misaligned weights). The “Shares to buy/sell” row of the table gives the results of the formulas that we presented earlier for calculating the number of stock shares to sell or buy in order to return to the optimal scenario.
TABLE 10.1
Standard Rebalancing
Using Cash Flows to Rebalance without Selling
Often it is less costly to let a portfolio drift toward the optimal target portfolio rather than make trades that try to match it exactly. There are tax costs associated with rebalancing owing to the selling of securities with capital gains. There is also a transactions cost with each purchase or sale of a security. Thus the manager can choose to not sell any securities but only buy more shares of the securities whose weights have fallen below target. While it does not rebalance the portfolio immediately, this method gives the portfolio a push in the right direction. It is easy to give the portfolio a push by using any cash inflows to add, proportionally to the optimal target weights, to all the portfolio’s existing positions. A slightly harder push, investing the cash inflows according to an algorithm, will send the portfolio a bit faster toward the optimal weights.
The easiest method is to divide the cash inflows among all the portfolio’s securities in amounts proportional to the target weights. Thus, if one has $
C
t
+1
in cash to inject into the portfolio at time
t
+ 1, then one will purchase
x
i,t
+1
of each security:
The new weights that result from this process will fall in between the weights before adjustment and the optimal target weights. Their proximity to the target weights will depend on how large
C
t
+1
is relative to
V
t
+1
.
An Example
We return to the example of stocks
A
through
G
. Now, instead of doing the standard rebalancing, let us rebalance by distributing the cash flow
C
across the entire portfolio in proportion to the target weights.
The cash injection
C
t
+1
= $2,000. One can see from
Table 10.2
that the weights
slowly
converge to the target weights.
TABLE 10.2
Rebalancing by Purchasing at Target Weights
Another method for helping the portfolio gravitate toward the benchmark weights more quickly is to invest the new cash only in stocks that are below their corresponding target weights. All the stocks in the portfolio are divided into two groups, one in which stocks exceed their target weights (i.e.,
) and another in which stocks fall short of target weights (i.e.,
). It is important to calculate these weights
after
the cash has entered the portfolio. We thus use the symbol
to represent the weights of the portfolio considering the current value of the portfolio and the cash inflow. The weight of each stock with the cash inflow is
All these portfolio weights should be compared with their corresponding target weights (
w
a
i,t
+1
). We must figure out how much of the cash should be allocated to each of the stocks that are below target weight. Suppose that for the first
n
u
stocks (
i
= 1, …,
n
u
), the weights are below the target weights. Let us call the cash allocated to stock
i, c
i,t
+1
. We can determine this amount for each stock:
After the
c
i,t
+1
have been calculated,
12
we need to calculate the sum of them:
. We then take the difference between the sum and
C
t
+1
. The difference, which represents the amount of slack funds, equals
. This number always will be less than or equal to zero. It will equal zero when there are enough funds (enough cash) to perfectly rebalance the portfolio. It will be less than zero when there are too few funds (too little cash) to restore deficient stocks to their required weights. In that case, the amount of cash distributed to each stock will have to be scaled down proportionally. Whether the amount of slack funds is zero or negative, the number of shares
x
i,t
+1
that need to be purchased of each stock is
13
The benefit of this type of “buy” system for rebalancing is that it should make the portfolio converge toward the optimal target weights at a faster rate than if we simply invested in the stocks in proportion to the target weights.
A manager might want to know exactly how much cash he or she would need to rebalance the portfolio using this system of purchasing deficient stocks. There are two steps to figuring this out. The first step is to calculate the ratio of the weight of each stock before rebalancing and
before
new money has been added (
) to the target weight (
) of each stock minus one. That is,
The second step is to find the maximum of those values and multiply it by the total value of the portfolio
V
t
+1
at time
t
+ 1. That is,
One can easily verify that this number is the minimum amount of cash inflow required to perfectly rebalance the portfolio without selling.
An Example
This example considers the same portfolio as the one in the two preceding examples. In this case, however, the rebalancing method attempts to achieve the desired weights more quickly. The seventh row of
Table 10.3
shows the weights of the stocks in the portfolio after new cash arrives. These values are the result of
Eq. (10.19)
. The next row provides the number of shares to purchase of each stock in order to rebalance as much as possible according to
Eq. (10.21)
. Finally, for this example, the second-to-last row of the table computes the new weights of the portfolio given the cash injection. One can see how this method pushes the portfolio toward convergence with the target weights much more quickly than the preceding buy-
only method.
14
In this example, $4,697.43 would have been needed to perfectly rebalance without selling.
TABLE 10.3
Rebalancing by Purchasing Only Deficient Stocks
The process of rebalancing without selling should be used whenever there are net cash inflows into the portfolio. A corresponding symmetric algorithm can be used when there are net withdrawals, in which case the rebalancing would involve only selling (and no buying). The selling, too, can be done optimally while reducing transactions costs and tax costs.
10.7 CONCLUSION
Much of portfolio management theory talks about optimizing portfolios without considering transactions costs. Unfortunately, some of the best portfolio management strategies involve trading stocks that are either illiquid or have high trading costs. Thinking about transactions costs ahead of time therefore can save a portfolio a great deal of money.
15
For a quantitative portfolio manager who closely tracks a benchmark, even a small drag on performance owing to transactions costs can cause significant underperformance of the benchmark. Thus we have discussed methods of factoring transactions costs into the optimization techniques for tracking portfolios. These methods help a manager to steer clear of stocks that seem to have high
α
’s before trading but in fact have low or even negative
α
’s once trading costs are considered.
In this chapter we also discussed some rather rudimentary ways to reduce transactions costs when there are frequent cash flows into or out of the portfolio. These methods, though simple to implement, work quite well at reducing the number of transactions involved in rebalancing owing to cash flows. They also allow the manager to spread trades out over time so as to avoid a sudden, immense price impact on the portfolio.
Portfolio managers can save a great deal of money by being aware of explicit transactions costs. They can save yet more by anticipating the “hidden” costs of capital gains and dividend taxes. We cover the critical issue of tax management in the next chapter.
1
Due to volatility in the markets caused by the coronavirus, the S&P Dow Jones index committee made a decision to postpone their rebalancing date to April 24, 2020. Invesco simply forgot to rebalance on April 24, 2020, and did so on April 29, 2020. See Riquier (2020).
2
It is more common to discuss transactions costs with respect to the amount traded. However, when comparing transactions costs to the expected returns of the portfolio, it is better to convert this amount into a number that can compare the cost as a fraction of the entire portfolio value.
3
The transactions costs reduce the $100 invested in stock
A
to $99, which will earn 12%, or $11.88. So stock
A
will reach a total value of $110.88. Transactions costs for stock
B
reduce the $100 to $99.9, which will earn 10%, or $9.99. Stock
B
therefore will reach a total value of $109.89.
4
See Roll (1984), Glosten (1987), and Glosten and Harris (1988).
5
It is somewhat helpful that NASDAQ Level II and III allow many users to see the national best bid and offer prices for given volumes at any given point in time.
6
The data were obtained from Abel Noser and reflect one-way transactions costs in 2020. See
Table 16.12
in
Chapter 16
.
7
Many commercial software providers attempt to supply price impact models to help portfolio managers and traders estimate these costs.
8
If the transactions costs are not a constant fraction of transaction value, then c
i
defined in this section becomes a nonlinear function of transaction value. If, for example, the portfolio manager gets charged a flat fee for trades, then c
i
is inversely proportional to the transaction value. When c
i
is nonlinear, the portfolio optimization problem becomes nonlinear as well. Some commercial software packages have nonlinear programming routines to deal with this, but the reliability of these routines varies. Market impact also can alter the relationship between the trade size and transactions costs. There is a recursive effect because the optimal trade size depends on the transactions costs, which, in turn, depend on the trade size. In
Appendix 10B
, we describe a method for an exact solution to the optimization problem that resolves most of these problems. In
Appendix 10C
, we describe a technique that allows the portfolio optimization to deal with a variety of market impact cost models.
9
Note that there is no adjustment for how long the portfolio is going to be held. We are assuming that the expected return is expressed for the investment horizon. That is, if the portfolio manager plans to rebalance the portfolio six months later, then
μ
P
represents the return for six months. As long as the expected return is expressed for the investment horizon, there is no need to adjust the transactions cost
c
. Some portfolio managers “amortize” the transactions cost to reflect the holding period, but a simpler, equivalent way is to restate
μ
P
.
10
If we do not ignore the time-value term, then the optimization problem in the next section becomes rather complicated; the effective expected return becomes quadratic, rather than linear, in weights. Fortunately, the time-value term is small in most cases.
11
This section is a brief summary of Chincarini (2004).
12
The formula for
c
i,t
+1
as presented is equivalent to
, where the portfolio weights are computed including the cash injection
C
t
+1
.
13
When slack funds equal zero,
14
In this particular example, one can compute the savings in transactions costs and taxes from using the algorithm. Although very small in percentage terms, the algorithm results in about half the costs of standard rebalancing.
15
In fact, a Yale University professor approached one of the coauthors about launching a fund based on the professor’s “phenomenal” portfolio strategy. Once the professor and the coauthor considered transactions costs, however, they realized that it actually underperformed the major indices.
