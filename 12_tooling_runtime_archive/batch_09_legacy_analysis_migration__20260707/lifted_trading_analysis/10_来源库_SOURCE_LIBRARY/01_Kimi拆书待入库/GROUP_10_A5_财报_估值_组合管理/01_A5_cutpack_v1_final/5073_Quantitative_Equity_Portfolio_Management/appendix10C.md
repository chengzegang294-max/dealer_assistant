# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = appendix10C

---

APPENDIX 10C
An Approximate Optimal Portfolio with Market Impact Costs
Estimating market impact costs can be very valuable for a portfolio manager. Unfortunately, there is a nonlinear element to the market impact of trades. The larger your portfolio, the larger the market impact of a trade. As a result, standard portfolio optimization techniques cannot be used because, as the optimal weight of each stock changes, so does the cost of trading. In addition to the optimization dilemma, the portfolio manager also needs a good description of how the size of a trade and market impact are related. This market impact data can either be obtained from a professional organization that has made detailed estimates of transactions costs or from a parametric model of transactions costs. For example, you might specify transactions costs from trading as
where
C
it
is the percentage commission cost from the trade,
s
it
is the bid–ask spread of stock
i
at time
t, p
it
is the price of stock
i
at time
t
, and
c
it
is the percentage market impact costs for stock
i
at time
t
based on a market impact model. These transactions costs,
tc
it
, are in price percentage points (i.e., a value of 0.20 would indicate that this particular trade would lead to costs of 0.20%).
Market impact models will vary but might take a form similar to this:
where
n
it
represents the number of shares of security
i
that need to be traded,
V
it
is the average daily trading volume of the stock (shares traded, not dollars traded), and
a, φ
, and
are parameters that need to be estimated.
1
As mentioned previously, market impact transactions cost models are difficult to use in a standard optimization framework.
2
In this appendix we are going to introduce an approximation technique to allow for portfolio optimizations when the user has a detailed model of market impact costs as described above. The first step is to apply an approximation method to approximate a variety of transactions cost models.
3
The second step is to formulate the optimization problem so as to solve for market impact.
10C.1 APPROXIMATION OF TRANSACTIONS COSTS
The first step is to approximate the transactions cost model, which is usually based on the number of shares traded of a particular stock, and other parameters. The larger the trade of a stock, the larger the market impact. Thus, in order to make the market impact model usable in a standard optimization framework, we need to start with a given portfolio size, say $100 million. We then vary the weights of each stock from 0% of the portfolio to a maximum allowable percentage based on the portfolio manager’s needs. We can choose increments of 1% or smaller and for each weighting we compute the model’s estimated market impact costs. Once these values of market impact (or total transactions costs) are calculated, a series of weights for each stock along with the market impact for each particular stock weight will be known for each period (e.g., monthly).
4
For example, for stock
i
, we might have a series of weights
w
it
= [0.0 0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.10] along with the corresponding market impact costs
c
it
= [
c
0.00
it
…
c
0.10
it
]. From this we compute the total transactions cost vector for each stock, which is given by
Eq. (10C.1)
, and multiply this by
w
it
, to obtain a vector
, which is the weight of stock
i
for every weight level multiplied by the actual transactions costs
tc
it
, given a portfolio of value $
V
t
.
The second step is to estimate for each stock a regression of the following form:
where
is a vector of transactions costs from the transactions cost model multiplied by each stock’s vector of incremental weights, and
a
it
and
b
it
are parameters estimated from the linear regression.
5
This approximation model works extremely well for many transactions cost models.
6
As an example, the actual transactions costs and approximate transactions costs for AT&T for December 2013 were 0.000232% and 0.000257% for a $5 million trade (i.e., 1% position of a $500 million portfolio).
7
This approximation is key to allowing for market impact in the optimizations since we now have a clear link between weight choice and transactions costs impact. In the next section, we show how to use this approximation in a portfolio optimization problem.
10C.2 LONG-ONLY PORTFOLIO
In order to incorporate our approximate transactions costs into the portfolio optimization problem, we must modify the quadratic optimization program slightly. First, we must use a quadratic optimization routine that can accept quadratic constraints, in addition to linear constraints, as discussed in
Appendix 9B.3
.
8
Second, we must modify the traditional portfolio optimization setup to work with transactions costs.
The mathematical expression of the quadratic optimization with quadratic constraints is given as
where
x
is the vector of unknowns in the problem,
Q
is a symmetric positive semi-definite matrix,
c
is a vector of coefficients,
A
is a matrix of coefficients for the equality and inequality constraints,
b
is a vector of constraint values,
l
is a column vector, r is a scalar,
Q*
is a symmetric matrix,
lb
is a lower-bound vector, and
ub
is an upper-bound vector.
The main difference in this optimization problem is the quadratic constraint in
Eq. (10C.5)
. In the traditional mean-variance
optimization problem, we substitute the following variables:
x
=
w
, the stock weights,
Q
= 2
Σ
, the variance-covariance matrix of stock returns,
c
=
0
,
l
=
0
, r = 0,
Q
*
=
0
,
A
is chosen typically to have a row of 1s and a row of expected returns, and the lower and upper bounds are set as desired.
In order to create an optimal portfolio that minimizes the risk of the portfolio and achieves a desired after-transactions cost return, which includes market impact costs, we must set up additional matrices. For this general discussion, we will not create all of the other constraints; we will just assume that the
A
and
b
matrices have been set up for the particular optimization of the portfolio manager. We will assume that the optimization has only
N
choice parameters, that is, that
x
= [
w
1
w
2
… w
N
]. Thus,
Q
= 2
Σ
. We will need to specify,
l
,
Q
*
, and r as follows:
and
, and r = −
µ
P
, where
is a vector of the expected returns of each stock minus the constant estimate in the transactions cost regression (
);
μ
is the expected return of each stock;
µ
P
is the desired target of after-transactions cost expected return for the portfolio to match; and
is the coefficient estimate from the transactions cost regression for stock
i
.
9
10C.3 MARKET-NEUTRAL PORTFOLIO
The market-neutral problem is slightly more complicated. We need to create phantom weights and binary weights. Once again, we will assume the user has set up their desired constraints for the regular weights (
w
), phantom weights (both
w
+
and
w
−
), and the binary weights (both
v
+
and
v
−
). We will also have to increase the size of the
Q
matrix to accommodate the other variables as
where
Σ
is the variance-covariance matrix of stock returns [e.g., see
Eq. (9A.13)
]. We also need to specify,
l
,
Q
*
, and r as follows:
where
where
μ
is the expected return of each stock;
is the coefficient on
w
i
in the regression for stock
i
;
is the coefficient estimate on
from the transactions cost regression for stock
i
;
c
=
0
,
µ
P
is the desired target of after-transactions cost expected return for the portfolio to match; and r = −
µ
P
.
10
10C.4 MARKET IMPACT DURING REBALANCING
In the previous two sections we showed how to use the market impact approximation on a long-only and a market-neutral optimization when building the portfolio from scratch. It may also be of use to model market impact when rebalancing a portfolio. The approach is very similar to the concepts discussed in
Appendix 10B
. As before, we will assume the user has set up their desired constraints for the regular weights (
w
), phantom weights (both
w
+
and
w
−
), prior or current portfolio weights (
w
b
), and the binary weights (both
v
+
and
v
−
) as described in
Appendix 10B
. Thus, we will need to specify,
l
,
Q
*
, and r as before. We will also have to modify
Q
(i.e., expand the variance-covariance matrix).
For the market-neutral portfolio described in
Appendix 10C.3
, we add a prior set of portfolio weights as discussed in
Appendix 10B
. Thus, the only modification we need to make to
Q
,
Q
*
, and
l
is to add a column of six
0
N
×
N
matrices between the third and fourth columns of
Q
and
Q
*
in
Eqs. (10C.14)
and
(10C.15)
, and add
0
1×
N
between the third and fourth columns of
l
. We also need to add the constraints that come with prior weights, as described in
Appendix 10B
. These modifications will account for the new prior portfolio weights, and the optimization setup is complete.
For the long-only portfolio, which needs to be set up as in
Appendix 10B
, we need to remove the second rows of
A
eq
and
b
eq
that target an after-transactions cost return and instead alter
Q
,
Q
*
, and
l
very similarly to the way we did them for the market-neutral portfolio that accounts for market impact during rebalancing.
These changes will allow for optimizations that consider market impact during rebalancing.
10C.5 A NUMERICAL EXAMPLE
We will continue the previous numerical example in
Appendix 10B
. Thus, we will seek a portfolio with an after-tax average return of 8%, with no short sales allowed, and the weights of the portfolio must sum to 1. In this case we will construct transactions costs for every stock based on the actual spread costs (i.e., bid–ask spread) and market impact costs based on a transaction model used in portfolio management. Although not shown here, we first acquired the relevant data to compute the market impact cost for all of our six stocks in a given period in our sample. We then computed the spread costs for this same period. We then computed the market impact costs for various weights for each of our stocks assuming a portfolio size of $500 million and estimated the linear regression to obtain the
and
for every stock. The regression estimates for the stocks were
and
. Thus, for stock 1, a 10% position in this stock would represent a position value of $50 million (0.10 · 500). Suppose this stock was trading at $101.2, that would mean that buying 10% of this stock in the portfolio would require purchasing 494,071 shares of the stock. This stock is a quite liquid stock and trades about 12,410,000 shares per day, on average. Thus, this trade would represent only 4% of the average daily volume. The transaction cost for this stock is 0.07784%.
That is, to trade $50 million all at once would result in a cost of $38,917. The approximation of transaction cost equals 0.07818%
.
11
Thus, our constraints are given as
The solution to this optimization is
In order to understand these results, remember that based on our estimations, stocks 1 and 2 are the most liquid (lowest transactions costs), stocks 3 and 4 are the next most liquid, and stocks 5 and 6 are relatively illiquid. Compared to the prior portfolio weights for stock 5 and 6 of 13% and 28%, the optimization barely altered the weight of stock 6 and sold only 5.2% of stock 5 as opposed to an optimization that ignored market impact costs—costs that are increasingly larger for less liquid stocks. We did the same optimization without considering market impact costs, and the optimal solution was
w′
= [0.293 0.017 0.067 0.287 0.000 0.336].
QUESTIONS
10.1.
Describe the events that might trigger a rebalancing of a portfolio.
10.2.
“If the portfolio manager needs to sell a fraction of the portfolio to meet the cash outflow demand and if there is no change in any parameters of the model, then the portfolio manager does not have any reason to change the portfolio weights.” Is this statement correct?
10.3.
Consider a portfolio consisting of 100 stocks with weights given by
w
1
, …,
w
100
.
(a)    If the one-hundredth stock drops out of the portfolio and if the portfolio manager intends to keep the relative weights unchanged for the remaining 99 stocks, what would be the new weights of the remaining stocks?
(b)    If the portfolio manager needs to add one more stock to the portfolio and makes its weight to be
w
101
, what would be the new weights of the original 100 stocks?
10.4.
Suppose that we estimated an economic factor model using monthly data.
(a)    From the estimates of the model, it is possible to predict the annual stock returns by multiplying the predicted return by 12. What is the implicit assumption that allows us to make this inference?
(b)    Explain why it is preferable that the model periodicity be identical to the rebalancing frequency.
10.5.
Consider an economic factor model
r
it
=
α
i
+
β
i
f
t
+
ϵ
it
Using the observations from
t
= 1 to
t
=
T
, we obtained
and
. Using one more observation, i.e., from
t
= 1 to
t
=
T
+ 1, we obtained
and
. We would like to test whether the parameters changed.
(a)    Can we say that
. and
are independent?
(b)    What is the covariance between
. and
?
(c)    Find the formula for the
t
-statistic when the null hypothesis is that
β
did not change.
10.6.
Evaluate the dividend reinvestment plan offered by certain companies in the context of transactions costs.
10.7.
What is the bid–ask spread? Why is it difficult to observe the bid–ask spread in reality?
10.8.
On the New York Stock Exchange, designated market makers (DMMs) offer their own bid and ask quotes. Explain whether DMMs would increase or decrease their bid–ask spreads in each of the following situations:
(a)    Transaction volume is decreasing.
(b)    More and more limit orders arrive.
(c)    The company is about to announce earnings.
10.9.
Explain the various components of transactions costs, including implicit costs as well as explicit costs.
10.10.
Explain why transactions costs may be higher for small stocks than for large stocks.
10.11.
One simple way to control transactions costs is to determine what percentage of the
average daily trading volume
(ADTV) is acceptable as a weight for any stock in the portfolio. Let’s denote the vector of allowable ranges for all stocks as
w
ADVT
. Write down a problem for finding an optimal portfolio considering these critical weights.
10.12.
To set up an optimal portfolio problem considering transactions costs, we need to adjust the expected return of stocks and calculate the transactions-cost-adjusted expected return. Suppose that a $1 transaction creates 5 cents in transactions costs.
(a)    If stock
A
’s monthly expected return is 1%, what would be the monthly transactions-cost-adjusted expected return?
(b)    If stock
A
’s annual expected return is 15%, what would be the annual transactions-cost-adjusted expected return?
(c)    Explain why we would subtract the same percentage from the expected return to account for the transactions costs regardless of whether the return is monthly or annual.
10.13.
Let
denote the weight of stock
i
in the existing portfolio and
denote the weight of stock
i
in the new portfolio to be created. Let
c
i
denote the transactions cost of stock
i
.
(a)    If
μ
i
is the expected return of stock
i
, what is the trans-actions-cost-adjusted expected return of stock
i
?
(b)    What is the marginal effect of
on the transactions-cost-adjusted expected return? Explain why this marginal effect can be positive.
10.14.
If you hold a stock whose transactions cost is high, it is likely that your
future
transactions costs will be high because you will have to sell the stock eventually. This fact implies that accounting for the
current
transactions costs only is not enough. How should the optimal portfolio problem be modified to account for the future transactions costs?
10.15.
Explain the advantage of futures and ETFs in controlling transactions costs.
1
One such model is the structural model estimated from U.S. equity data by Almgren, Thum, Haptmann, and Li (2005)
, where
is the daily volatility of the returns of stock
i
at the beginning of month
t
;
N
it
is the total amount of shares outstanding in the security;
V
it
(a.k.a. ADTV) is the average daily trading volume of the stock (shares traded, not dollars traded);
T
is the time interval in which the trade takes place in number of days (in the example that follows, we use
T
= 1); and
n
it
represents the number of shares of security
i
that the portfolio is trading. Another model is the market impact model of Northfield. The model is of the form
c
it
=
B
it
|
n
it
| +
C
it
|
n
it
|
0.5
, where
B
it
and
C
it
are parameters estimated by Northfield,
n
it
is the number of shares to be purchased for security
i
in month
t
, and
c
it
is expressed in terms of percentage price movement. To give an example of how the first cost model works, let’s look at the data from two stocks in December 2013: AT&T (ticker symbol: T), a very liquid stock, and AGL Resources (ticker symbol: GAS), a less liquid stock. AT&T for this particular period had a market capitalization of $183 billion, a stock price of $35.16, and a 10-day average daily trading volume of 18,930,000 shares. The spread was 1 cent, or a 0.0284% spread. The trading cost in percentage terms for a 1% position in a $500 million portfolio was 0.0232%. That is, a $5 million trade of AT&T representing 142,000 shares would cost the trader $1,160. This does not represent commissions; it is simply the market impact and spread costs. AGL Resources for this particular period had a market capitalization of $5.6 billion, a stock price of $47.23, and a 10-day average daily trading volume of 490,000 shares. The spread was 2 cents, or a 0.0423% spread. The trading cost in percentage terms for a 1% position in a $500 million portfolio was 0.1621%. That is, a $5 million trade of AGL Resources representing 105,865 shares would cost the trader $8,105.
2
Furthermore, in the case of our example, transactions cost model 1 was not usable as of 2018 even in the leading software provider platforms for portfolio optimization, such as Axioma, Northfield, and BARRA.
3
This technique was proposed by Chincarini (2017).
4
This is done by computing the dollar amount of a trade for a given weight and portfolio size. Thus, for a 1% position with a portfolio size of $100 million, the trade size would be $1 million. Then, dividing by the price of the stock in that period, we obtain the number of shares required to be traded in that stock. This is used in the transactions cost model to obtain the market impact costs in percentage terms. Most transactions cost models require some sort of number of shares to be traded to estimate the transactions costs.
5
There is a different
a
it
and
b
it
for every net asset level since the transactions costs of each stock vary with assets under management.
can also be thought of as net transactions cost as it represents the percentage transactions cost of each stock multiplied by the stock’s weight,
w
it
, reflecting the net transactions cost impact of each stock at each weight to the entire portfolio.
6
The Weierstrass approximation theorem states that every continuous function defined on a closed interval [
a, b
] can be uniformly approximated as closely as desired by a polynomial function. In the case of many common transactions cost models, a quadratic function is sufficient for a very good approximation. The
R
2
for stocks is typically very close to 1.
7
The regression estimates for this particular stock in this particular month were
= 0.0206,
= 0.5096, and
R
2
= 0.9999.
8
For example, CPLEX’s CPLEXQCP.
9
Under certain circumstances, a portfolio manager may wish to create a portfolio that maximizes after-transactions cost returns while achieving a certain target variance. The market impact optimization for a long-only portfolio can be modified to achieve this. In this particular case, we assume that the portfolio manager has chosen his other constraints for
A
and
b
and modifies the remaining matrices to achieve his goal as follows:
where
Σ
is the variance-covariance matrix of stock returns;
, and r =
σ
P
, where
is a vector of the expected returns of each stock minus the constant estimate in the transactions cost regression;
μ
is the expected return of each stock;
σ
P
is the target volatility for the portfolio to match; and
is the coefficient estimate from the transactions cost regression for stock
i
.
10
Under certain circumstances, a portfolio manager may wish to create a portfolio that maximizes after-transactions cost returns while achieving a certain target variance. The market impact optimization for a market-neutral portfolio can be modified to achieve this. In this particular case we assume that the portfolio manager has chosen his other constraints for
A
and
b
and modifies the remaining matrices to achieve his goal as follows:
where
Σ
is the variance-covariance matrix of stock returns,
Σ
2
is defined in
Eq. (10C.12)
,
, and r = −
σ
P
, where
is a (1 × 5
N
) vector of the expected returns of each stock, the constant estimates in the transactions cost regression, and zeros,
μ
is the expected return vector,
σ
P
is the after-transactions cost risk for the portfolio to match, and
is the vector of coefficients on
w
i
in the regression for stock
i
. The main adjustment is that we switch the matrices
Q
and
Q
*
.
11
We must divide by 0.10 since the formula is for
.
