# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = appendix15C

---

APPENDIX 15C
Short Returns
When a portfolio manager, either in an actual portfolio or a model portfolio, has short positions, the performance analyst will have to compute the return to the short positions (which we will call “short returns”) before computing the overall performance of the portfolio. Although this is not a complicated task, it requires some thought for the beginner.
The performance analyst may calculate the
approximate
short returns as the minus of the returns for the corresponding long position. Suppose, for example, that the portfolio has a short position in stock
A
from period
t
to
t
+
k
. Let
r
t,t
+
1
,
…, r
t
+
k
−
1,t
+
k
be the daily returns of stock
A
. The approximate short returns would then be given by
.
One indication that these short returns are only approximate is the fact that, with these short returns, you cannot use geometric linking as is done with long positions. That is,
To calculate the exact short returns, you need to carefully account for the changes in the portfolio value. If we short $1 of stock
A
at the end of day 0 and the day 1 return of stock A is
r
0,1
, then the portfolio value at the end of day 1 becomes 1 −
r
0,1
. If the day 2 return of stock
A
is
r
1,2
, then the portfolio value at the end of day 2 becomes 1 − [(1 +
r
0,1
)(1 +
r
1,2
) − 1] since the cumulative loss 571is (1 +
r
0,1
)(1 +
r
1,2
) − 1.
1
Thus, the short return for day 2 is not −
r
1,2
, but {1 − [(1 +
r
0,1
)(1 +
r
1,2
) − 1]} /(1 −
r
0,1
) − 1. Applying this logic, the day
i
short return is given by
, where
.
You can easily verify that geometric linking works with the exact short returns. That is,
The difference between the approximate short return
and the exact short return
is likely to be small when
k
is small. However, when
k
becomes large, the use of
may lead to significant underestimation of return volatility as well as the absolute value of returns.
15C.1 A NUMERICAL EXAMPLE
We take a small short portfolio of four stocks, stocks
A
to
D
. Each stock starts at a price of $100 and the portfolio manager shorts each stock with a quarter of his portfolio wealth.
2
Table 15C.1
shows the changes in prices from period
t
to period
t
+ 6, along with the period returns of each stock and the weights in each stock based on a long-only portfolio. These weights are used to construct the period portfolio returns (
), and the short portfolio returns are just given as minus the long portfolio returns. The long portfolio cumulative return over the six periods is 20.10% with a volatility of 2.95% per period. The negative of this would also be the cumulative return for the short portfolio. Thus, the short portfolio’s cumulative return over the period is −20.10%. For illustration purposes, we also compounded the short returns, and you can see that they erroneously compound to −17.59%.
Table 15C.1
uses the approximate method for computing short returns.
TABLE 15C.1
Performance Measurement with a Short Portfolio Using the Approximate Method
In
Table 15C.2
we present the calculations for the exact short portfolio returns. Notice that now the typical equations can be used for computing the short portfolio returns in every period, and the cumulative returns can be computed as normal. Also, the period
short returns are now different than the negative of the long-period returns. Despite this, the short-return portfolio over the period
t
to
t
+
k
is equal to the negative of the long-return portfolio over the period. You will also notice the slightly higher volatility over this period when the short returns are computed exactly, rather than approximately.
TABLE 15C.2
Performance Measurement with a Short Portfolio Using Exact Method
1
If the loss is negative, it’s actually a gain for the short position.
2
We do not explicitly consider collateral issues and transactions costs and keep position leverage at 1.
