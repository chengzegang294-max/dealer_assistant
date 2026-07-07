# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = appendix13A

---

APPENDIX 13A
Market-Neutral Portfolio Construction Techniques
As discussed in
Appendix 9B
, phantom weights and binary variables can be used to construct a market-neutral portfolio optimization that allows for more general portfolios, including leverage constraints, number of long and short positions, and other possibilities. In this appendix, we will review the ideas in
Appendix 9B
and illustrate an example of constraining leverage.
In order to constrain the total leverage of the portfolio, we will want the sum of the long weights plus the sum of the short weights to equal some amount, say
l
p
. For example, if we want a portfolio with a leverage of 2, we would specify that
l
p
= 2. If we want a portfolio of leverage 4, we would specify that
l
p
= 4, and so on. Some investors might want to constrain leverage further, such that the long and short leverages are different. In this case, the user might specify that the sum of the long weights equals
l
l
(long exposure) and the sum of the short weights equal
l
s
(short exposure). For example, if a user wanted to create a 130–30 portfolio, then
l
l
= 1.30 and
l
s
= 0.30. When using phantom weights and binary variables, these constraints are quite easy to add to the market-neutral optimization.
We start by expanding the
x
vector to include five types of variables. They include the
N
actual portfolio weights,
w
i
; the phantom positive weights
, which represent the
N
“long” positions of the portfolio; the phantom negative weights,
, which represent the
N
“short” positions of the portfolio; and the binary variables
and
for each stock in the portfolio. We then introduce the following constraints in order to ensure that the phantom weights are orthogonal to each other and are also related to the actual weights (
w
i
) of the portfolio:
and
Since
v
+
i
and
v
−
i
are binary variables, the inequality constraint in
Eq. (13A.4)
forces only one of them to be 1 and the other 0. This constraint combined with the constraints in
Eq. (13A.2)
and (13A.3) forces the phantom weights to also be orthogonal to each other. For generality, we used the parameters
κ
l
, γ
l
, κ
h
, and
γ
h
, but in most
market-neutral applications, it will be sufficient to set these equal to 0 and 1. When constructing the optimization, it is important to specify that
v
+
i
and
v
−
i
are binary variables.
1
The minimization problem is similar to our standard one:
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
lb
is a lower-bound vector, and
ub
is an upper-bound vector.
2
We will show the equality matrix constraints and inequality matrix constraints separately, but you can also combine them into one
A
matrix if desired. The equality matrix,
A
eq
, will be an (
N
+ 4) by (5
N
) matrix and the
b
eq
vector will be (
N
+ 4) by (1).
The inequality matrix,
A
ineq
, would be set up as follows:
where
μ
1
×
N
is the row vector of the mean returns for each of the
N
stocks,
μ
P
is the desired annualized portfolio return,
ι
1×
N
is a row of six 1s (that is, the first six entries of matrix
A
’s row 1 are 1s),
0
1×
N
is a row of
N
entries of zero,
I
N
×
N
is the identity matrix (that is, an
N
-by-
N
matrix with 1s on the diagonal and 0s everywhere else), and so on and so forth. In order to aid the reader, we indicate the dimension of every matrix as a subscript.
As stated earlier, you can either put upper- and lower-bound constraints in the inequality, or
A
ineq
matrix, or specify them directly as upper- and lower-bound vectors in many optimization packages. In this example, we chose to specify them directly; thus we constrain weights, phantom weights, and binary weights to be between 0 and 1.
3
Thus,
The
x
solution variables are
We can solve this problem with a mixed integer quadratic programming (MIQP) optimizer.
4
If an MIQP optimizer is not available, but a mixed integer linear programming (MILP) optimizer is, then use an algorithm similar to the one discussed in
Appendix 10B
to find the solution.
13A.1 A NUMERICAL EXAMPLE
We will continue the numerical example in
Appendix 9A
. However, we will change the target return. Typically, with market-neutral portfolios, a lower return target should be sought, since the net position of the portfolio is zero. For this example, we chose a target return of 2% and the leverage of the long and short portfolios equal to 1 (i.e., a total leverage of 2, where
l
l
=
l
s
= 1).
The quadratic programming problem can be expressed as
where
where
μ
1×6
= [14.40 10.19 9.87 7.52 20.05 2.66],
ι
1×6
is a row of six 1s (that is, the first six entries of matrix
A
’s row 1 are 1s),
0
1×6
is a row of 6 entries of 0,
I
6×6
is the identity matrix (that is, a 6-by-6 matrix with 1s on the diagonal and 0s everywhere else), and so on and so forth, and
. In order to aid the reader, we indicate the dimension of every matrix as a subscript, including for the large
A
and
b
matrices.
The economic meaning of these constraints is the following. The first five rows of this
A
matrix are the equality constraints that the sum of weights equals 0, that the average return of the portfolio equals 2%, that
, that the sum of the long weights equals 1 (
), and that the sum of the short weights equals 1 (
). For the binary weights, a zero is placed in the matrix since they are not relevant for these constraints. The sixth row in the matrix (which is really the 11th row through the 16th row) constrains the binary variables to be orthogonal—that is, only one of them can be positive—which consequently constrains the phantom weights to be orthogonal (i.e., we don’t buy and sell the same security). To establish this, we need the last four rows of constraints (which are really rows 17 to 40).
The solution using an optimization routine with continuous and binary variables is
5
:
You will notice that the sum of the portfolio weights equals 0 (i.e., a dollar-neutral portfolio) and that stocks 1, 5, and 6 are sold short and stocks 2, 3, and 4 are held long. If you check the results for
w
+
i
and
w
−
i
, you will note that they have the same value as the actual solution (i.e., there is no buying or selling of the same stock). The mean return of this portfolio is 2% with a standard deviation of 14.62%.
QUESTIONS
13.1.
Who is said to have formed the first market-neutral portfolio? In what year was it formed?
13.2.
True or false: Market-neutral portfolios provide a useful addition to an investor’s portfolio because they have a low correlation with other asset classes.
13.3.
Is there a combination of the risk-free asset and the S&P 500 that also would achieve a low correlation with the market (i.e., the S&P 500)? What about a low
β
?
13.4.
(a)    What is dollar neutrality?
(b)    Suppose that we take a simple two-stock portfolio. The portfolio manager shorts $1 million of T with a
β
= 0.70 and goes long $1 million of MGM with a
β
= 2.42. Is the portfolio market neutral?
13.5.
(a)    What is beta neutrality?
(b)    What is the minimum level of neutrality that a marketneutral portfolio should have?
13.6.
Suppose that a portfolio manager would like to construct a market-neutral portfolio from the four stocks below. He already has identified TGT and BA as stocks for the short portfolio and WYNN and POOL as stocks for the long portfolio. Also suppose that the sum of the weights in the long portfolio must equal 1.
(a)    Suppose that he wishes to build a dollar-neutral portfolio. What are the weights of the other securities?
(b)    Suppose that he wishes to build a dollar-neutral and beta-neutral portfolio. What are the weights of the other stocks in the portfolio?
13.7.
Suppose that a portfolio manager wants to construct a market-neutral portfolio from the four stocks below. She already has identified FIS and KO as stocks for the short portfolio and MMM and ABC as stocks for the long portfolio. She has found the factor exposures of the stocks to two factors that
she believes drive stock returns. Also, suppose that the sum of the weights in the long and short portfolios must equal 1.
(a)    Suppose that she wishes to build a dollar-neutral portfolio. What should be the weights of the securities in the portfolio?
(b)    Suppose that she wishes to build a portfolio that is dollar neutral and beta neutral to all factors. What should be the weights of the stocks in the portfolio? (
Note
: Round to two decimal places.)
13.8.
Suppose that we construct a simple market-neutral portfolio. For each value of
ρ
below (
ρ
being the correlation between the residual returns of the long portfolio and the short portfolio), what is the ratio of the information ratio of the market-neutral portfolio to that of the long-only portfolio? (
Note
: Assume that the market-neutral portfolio is fully leveraged.)
(a)
ρ
= 0
(b)
ρ
= 0.5
(c)
ρ
= 1
13.9.
Suppose that a portfolio manager shorts 1,000 shares at a price of $50 of stock
ZZZ
. The initial margin is 50%, and the maintenance margin is 25%. He deposits enough to satisfy the initial margin. At what price will the portfolio manager receive a margin call? (
Note
: Assume unrealistically that the portfolio manager does not have other collateral to satisfy the margin account credit balance.)
13.10.
Shortly after it became public that Martha Stewart was being investigated for insider trading, the stock of her company (MSO) dropped from $19.40 in May 2002 to $7.00 by September 2002. A portfolio manager believed that the stock price would not continue to decrease. Thus she wanted to buy the maximum number of shares possible using her margin account.
(a)    Given that initial margin is 50%, how many shares could she buy if she deposited $125,000 into her brokerage account?
(b)    If the maintenance margin of her account is 25%, what price can the stock reach before she will receive a margin call?
13.11.
True or false: To create a market-neutral portfolio, a portfolio manager needs to use cash as collateral on the shorts.
13.12.
In a typical market-neutral portfolio, what are the four sources of return when a liquidity buffer is required?
13.13.
Suppose that a performance analyst has access to the returns of a market-neutral portfolio. He knows the returns were 2.4% for the month of April 2020. He also knows that the interest rate on both the collateral and liquidity buffer is 5% per annum (that is,
i
=
i
’ = 0.05). The liquidity buffer is 6% (that is,
m
lb
= 0.06). The total value of the portfolio is $100 million. Assume that he is fully leveraged up to a liquidity buffer.
(a)    What must have been the return difference between the long and short portfolios?
(b)    Does the market-neutral manager know how to separate “good” stocks from “bad” stocks?
13.14.
Name four advantages of a market-neutral portfolio over a long-only portfolio.
13.15.
Name four disadvantages of a market-neutral portfolio over a long-only portfolio.
13.16.
Why is rebalancing necessary when managing a market-neutral portfolio?
13.17.
Briefly describe each of the following portfolio techniques and their relation to the market-neutral strategy.
(a)    Long-short
(b)    Equitization
(c)    Portable
α
(d)    Pair trading
13.18.
A quantitative portfolio manager is very good at managing against the Russell 2000. In fact, she is expected to achieve an
α
B
of 0.5% per month. Unfortunately, her benchmark is the S&P 500. She thus shorts the required amount of Russell 2000 futures and purchases an equivalent amount of S&P 500 futures contracts. Suppose that the S&P 500 is expected to have a return of 6% in the next month.
(a)    What would be the expected return of her new portfolio?
(b)    Would the realized return be similar? Explain.
13.19.
In 1999, many stocks were believed to be overvalued by quantitative portfolio managers. One of those stocks was Amazon (AMZN). This stock was particularly overvalued relative to other companies in the same line of business, such as Barnes & Noble (BKS). Suppose that a portfolio manager wanted to construct a pair trade consisting of AMZN and BKS. Use the table below to answer the questions. [
Note
: The
β
and
σ
for each stock were measured using monthly historical data from May 1997 to April 1999. The
σ
is presented in annualized percentage terms. Assume that the long and short weights (before shorting) sum to 1.]
(a)    How would you weight each stock if you wanted a dollar-neutral pair trade?
(b)    How would you weight each stock if you wanted a beta-neutral pair trade?
(c)    How would you weight each stock if you wanted a volatility-neutral pair trade?
(d)    Which of the three methods above would you actually use, and why?
(e)    Below are the results from the three types of pair trades from April 1999 to December 2001. Did the pair trade work for all three types of constructions? Which one worked the best? [
Note
: The standard deviations (SD) are annualized.]
(f)    Does risk make sense in this setting? Does
β
?
13.20.
If a portfolio manager constructs a portfolio consisting of 50 pair trades, has he created a market-neutral portfolio? Explain.
13.21.
A good friend of yours is a portfolio manager at a leading bank and is very good at creating a positive
α
B
versus the NASDAQ 100. Unfortunately, her benchmark is the S&P 500, which she is not very good at beating. Thus year after year she has received bad bonuses. What would you advise her to do?
1
It is essential that the software package allows for quadratic optimization with binary variables and continuous variables. The CPLEX suite has these and can be used through the CPLEX library in MATLAB. For users who do not have this option, we provide an algorithm in
Appendix 10B
that can be adapted for a market-neutral portfolio optimization.
2
As we discussed in
Appendix 9A
, one can also place these upper- and lower-bound constraints directly in the
A
matrix.
3
Some of these weight boundaries were implicitly already constrained by prior constraints.
4
For example, IBM’s CPLEX optimization software has a MIQP function called CPLEXMIQP.
5
Using the CPLEX function CPLEXMIQP, available through the CPLEX library in MATLAB, this optimization took 0.0484 seconds to reach a solution.
