# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = appendix9B

---

APPENDIX 9B
Advanced Techniques for Quadratic Optimization
Most portfolio optimization problems are covered by the basic techniques discussed in this chapter. However, there are many situations in which the portfolio optimization requires an expansion of the basic optimization setup. For example, a portfolio manager may wish to add transactions costs (discussed in the appendix to
Chapter 10
) or create a market-neutral portfolio with leverage constraints (discussed in the appendix to
Chapter 13
). There are other situations in which a portfolio manager wishes to have a limitation on the number of stocks in the portfolio, or in which the number of stocks in the portfolio is between some minimum and maximum, or, alternatively, in which the weights of any security are either zero or between a minimum and maximum weight. These and many other conceivable preferences in the optimization will require an expanded optimization framework. In other situations the portfolio optimization problem might require quadratic constraints, which are not part of the typical optimization framework. In this appendix we will discuss the basic building blocks for expanding the optimization framework to deal with these advanced optimization situations.
9B.1 PHANTOM WEIGHTS
In the portfolio optimization problems discussed in
Chapter 9
, we typically had only
N
unknowns, which were the portfolio weights. In some nonstandard portfolio problems, it is useful to create what
we term “phantom weights.” The idea of phantom weights is to create additional weights, in addition to the actual weights of the portfolio, for which the optimizer will also find optimal values. These can be used for a variety of purposes. Perhaps the simplest example is to create a set of buy and sell weights. Suppose the optimization problem has
N
stocks. In addition to the portfolio weights
w
1
to
w
N
, we create an additional 2
N
weights
, and
The new optimization is now more complicated because we have 3
N
weights to choose. These phantom weights offer many benefits in a portfolio optimization. Oftentimes, the phantom weights have a specific relationship to the underlying weights, such as
.
9B.2 BINARY WEIGHTS
In addition to creating phantom weights for the portfolio optimization, it may also be useful to create binary variables as optimization weights. These binary weights are very similar to the concept of phantom weights. They are additional weights for the optimizer to select, but the weights are constrained to be binary (i.e., have a value of 0 or 1).
One very practical use of the binary variables is to force the phantom weights to be orthogonal. That is, if the actual weights and phantom weights have the following relationship,
, we could have a situation where
w
i
> 0 and both
and
. This is a wasteful solution because we have a long position and a short position on the same stock. We can use binary variables to prevent this occurring.
Suppose one creates the following binary variables,
and
for each one of the
N
stocks. One can then add a constraint of the following form:
If we set
κ
l
=
γ
l
= 0 and
κ
h
=
γ
h
= 1 so that we allow the weights to fluctuate between 0 and 1, and add the constraint that
, we will force the phantom weights to be orthogonal. That is, for every stock
i
, if
, then
and vice versa.
Of course, this useful portfolio setup is not without costs. The additional phantom and binary weights and associated
constraints make the optimization problem more difficult and complicated to solve.
9B.3 QUADRATIC CONSTRAINTS
Conventional quadratic optimizers typically allow for linear equality and inequality constraints. In some instances, it will be useful to specify quadratic constraints, in addition to a quadratic objective function.
1
The portfolio optimization structure is very similar to the standard one; however, the user typically can also specify constraints of the following form:
l′x
+
x′Q
*
x
≤ r.
9B.4 PRACTICAL EXAMPLES
9B.4.1 Market Neutrality with Leverage Constraints
If we add the following constraints that
,
, and that
w
+
≥ 0 and
w
−
≥ 0, the resulting optimization will create a market-neutral portfolio that is dollar neutral (i.e., the sum of weights of the long stocks equals the sum of weights of the shorted stocks) and such that the leverage of the market-neutral portfolio is limited to 2 (i.e., the portfolio is 100% long and 100% short of the assets under management). If the market-neutral manager wanted more excessive leverage, this could easily be changed by the constraints on the sum of the phantom long and short weights (i.e.,
where
l
l
is the long exposure and
l
s
is the short exposure). For example, a 130–30 long–short portfolio could be constructed by making
l
l
= 1.3 and
l
s
= 0.3. More on the exact portfolio setup will be discussed in
Appendix 13A
.
9B.4.2 Transactions Costs
Fixed Costs
If we want to rebalance a portfolio and we have to select new target weights while acknowledging our current portfolio weights, the use of phantom weights and binary variables will enable us to find an exact solution to the portfolio optimization problem while
considering transactions costs. In particular, we can add the following constraints
where
represents the current weights of the portfolio, and
represents the after-rebalancing weights of the portfolio. We can set the same relationship on the binary variables such that
κ
l
=
γ
l
= 0 and
κ
h
=
γ
h
= 1 so that we allow the weights to fluctuate between 0 and 1 and add the constraint that
, which will force the phantom weights to be orthogonal. Stocks whose weight is reduced vis-à-vis the prior portfolio will have negative net weights, but their phantom weights
will be positive—thus the transactions cost vector can be multiplied by their value. Similarly, the stocks for which the portfolio increases the weight will be positive
, and these can also be multiplied by the transactions cost vector. The optimized final weights of the portfolio will be
w
i
. Thus, in the case of transactions costs, the phantom weights simply serve as a mechanism to denote the change to the current weights, storing the positive changes in the positive phantom weights and the negative changes in the negative phantom weights. Since both positive and negative phantom weights are positive, our transactions cost vector can remain positive, and the transactions cost rebalance problem is resolved. More on the exact portfolio setup will be discussed in
Appendix 10A
.
Market Impact Costs
These techniques along with quadratic optimization with quadratic constraints can be used to construct portfolios while accounting for market impact costs from a variety of market impact cost models.
2
More on the exact details will be discussed in
Appendix 10C
.
9B.4.3 Elimination of Small-Weight Stocks
Sometimes a portfolio manager will wish to reduce the number of securities. That is, the portfolio manager might have a desire to construct an optimized portfolio that forces the weights of individual stocks to be above a minimum or below a maximum weight. The traditional portfolio optimization allows this very easily. One simply adds an inequality constraint that the optimal weights are above and below a given weight, which can differ by stock or be the same for all stocks. The problem with the traditional
method is that there might be many circumstances with no solution to the optimization because it forces all stocks to be within a given range—which may be far from optimal and will not resolve the initial problem of eliminating many stocks with trivial weights. However, the use of binary variables can create the optimization that forces the optimizer to only find weights between the minimum and maximum or forces the weight of that particular stock to zero. This will result in more successful optimizations and will be more in line with the portfolio manager’s thought process. For simplicity, we will focus only on the situation where the portfolio manager would like all stock weights to be between a lower bound (
κ
l
) and an upper bound (
κ
h
). This constraint can be implemented on just the long portion of the portfolio or the long and short portions of the portfolio. Here we consider only the long portion of the portfolio. Using the inequality relationship of the binary variables and phantom weights,
and
, once we specify our values for
κ
l
, γ
l
, κ
h
, and
γ
h
, we have effectively accomplished our goal. If the portfolio is just a long portfolio, phantom weights are not needed and the one set of binary variables should be constructed with respect to the actual weights,
w
i
. Since the binary variables are either 0 or 1, the weights of the portfolio will be chosen to be within the minimum and maximum weights or to equal 0.
A Numerical Example
We will continue the numerical example in
Appendix 9A
. Thus we will seek a portfolio with an average annualized return of 8%, with no short sales allowed, and the weights of the portfolio must sum to 1. We will then add the constraint that a stock can only have a weight greater than 0.03 (i.e., 3%) or less than 0.30 (i.e., 30%) or else it must have a value of 0.
The quadratic programming problem can be expressed as
3
where
The first two rows of this
A
matrix are the equality constraints that the sum of weights equals 1 and that the target mean is 8%. For the binary weights, a 0 is placed in the matrix since binary weights are not relevant for these constraints. The rest of the rows represent inequality constraints to restrict the weights of every stock between 0.03 and 0.30, or a weight of 0. That is, we chose the values of
κ
l
and
κ
h
such that
. Since
is a binary choice variable, if this variable equals 1, then the weight of stock
i
will be forced to lie in the range of 0.03 and 0.30; however, if it’s more optimal to make its weight 0, then
= 0 and
w
i
will also be equal to 0.
With many constraints and more stocks, these matrices can become very large. As a result, we will sometimes represent these
matrices as a series of matrices. For example, it is convenient to write matrix
A
in
Eq. (9B.4)
as
where
μ
1×6
= [14.40 10.19 9.87 7.52 20.05 2.66],
ι
1×6
is a row of six ones (that is, the first six entries of matrix
A
’s row 1 are 1s),
0
1×6
is a row of 6 entries of 0,
I
6×6
is the identity matrix (that is, a 6 × 6 matrix with 1s on the diagonal and 0s everywhere else), and so on and so forth.
The solution using an optimization routine with continuous and binary variables is
4
9B.4.4 Restricting the Number of Stocks
Sometimes portfolio managers will wish to restrict the number of stocks in their portfolio. There could be a variety of reasons for this
preference. For example, if it’s a regularly rebalanced quantitative model, it might be beneficial from a logistical point of view to manage the portfolio with fewer stocks. Whatever the reason, the portfolio optimization can be done such that the portfolio managers can limit the number of stocks within a range of
n
l
and
n
h
, where
n
l
is the smallest number of stocks they want in their portfolio and
n
h
is the largest number of stocks they want in their portfolio. In this particular example, phantom weights are not needed, unless the managers are doing this for a long–short portfolio. However, if the portfolio managers are simply restricting the number of stocks, they need only use the binary variables. For a long-only portfolio, the managers should create one set of
N
binary variables,
. For a long–short portfolio, the managers should create two sets of binary variables,
and
, allowing them to specify the range of stocks in both the long and short portfolios, respectively. For both situations, the portfolio managers should add two inequality constraints. The first is that
(i.e., that the number of stocks in the long portfolio is less than
η
h
) and
(i.e., that the number of stocks in the long portfolio is greater than
η
l
). In reality, most optimization frameworks will require a transformation of the second inequality into
. Of course, with a long–short portfolio, the portfolio manager would add similar constraints on the short portfolio with the corresponding binary variables.
A Numerical Example
We will continue the previous numerical example. Thus we will seek a portfolio with an average annualized return of 8%, with no short sales allowed, and the weights of the portfolio summing to 1. We will allow the weights to have any value between 0 and 1; however, we will not allow the portfolio to have more than three stocks (even though there are six stocks available to purchase).
The quadratic programming problem can be expressed as
5
where
The first two rows of this
A
matrix are the equality constraints that the sum of weights equals 1 and that the target mean is 8%. For the binary weights, a 0 is placed in the matrix since binary weights are not relevant for these constraints. The rest of the rows represent inequality constraints to restrict the weight of every stock to between 0 and 1. The last two rows represent inequality constraints on the binary variables—in particular, that the sum of the binary variables be between 0 and 3. This is equivalent to constraining the number of stocks to be less than or equal to three.
The solution using an optimization routine with continuous and binary variables is
6
QUESTIONS
9.1.
The solution to the mean-variance optimization problem with no constraints can be expressed as
where
X
=
ι
′
Σ
−1
μ
Y
=
μ
′
Σ
−1
μ
Z
=
ι
′
Σ
−1
ι
Show that this can be derived from the general solution to the quadratic optimization solution with equality constraints, that is,
x
= −
Q
−1
[
I
−
A
′ (
AQ
−1
A
′)
−1
AQ
−1
]
c
+
Q
−1
A
′ (
AQ
−1
A
′)
−1
b
.
9.2.
Explain the circumstances under which shorts sales are not feasible.
9.3.
Explain why true diversification may be achieved even when the conventional diversification constraints are violated.
9.4.
Some computer software packages require every constraint to the minimization to be in inequality form. Rewrite the following constraints in the inequality form:
w′
μ
=
μ
P
,
w
′
ι
= 1
9.5.
Consider the following variance-minimization problem:
(a)   Show that this problem is equivalent to minimization of the standard deviation.
(b)   In general, we may consider the minimization of a function of the variance; that is,
What is the property of function
f
(·) that makes the preceding minimization equivalent to the variance minimization?
9.6.
Consider the variance minimization
and the expected return maximization
(a)   If the two problems produce the same solution
w
, what are the portfolio variance and portfolio expected return?
(b)   Can we say that the set of solutions to the variance minimization is identical to the set of solutions to the expected-return maximization as we vary the values of
μ
P
and
?
9.7.
Consider the following minimization problem:
The Lagrangian function is defined as
=
w′Σw
+
γ
(
μ
P
−
w′
μ
) +
γ
′(1 −
w
′
ι
)
The first-order condition of this minimization problem is identical to the first-order condition for minimizing the Lagrangian with respect to
w
,
γ
, and
γ
′. What are the roles of
γ
and
γ
′ in the first-order condition?
9.8.
The portfolio optimization may be expressed as
(a)   Show that given
μ
P
, there exists
γ
such that the solution
w
* to this problem satisfies
w
*′
μ
=
μ
P
.
(b)   Explain why
γ
may be interpreted as a measure of risk tolerance of the portfolio manager.
9.9.
The quality of stratified sampling critically depends on the number of strata and the number of observations drawn from each stratum. Suppose that the portfolio manager wants to select 100 stocks out of a universe of 10,000 stocks. One alternative is to make 5 strata and select 20 stocks from each stratum. The second alternative is to make 10 strata and select 10 stocks from each stratum. Under which conditions would the portfolio manager prefer the first alternative to the second?
9.10.
What is factor tilting? Explain when factor tilting is desirable and how to accomplish it.
9.11.
Show that minimizing tracking error is equivalent to minimizing the mean squared error defined as
MSE(
r
P
−
r
B
) =
V
(
r
P
−
r
B
) + [
E
(
r
P
−
r
B
)]
2
9.12.
Tracking error can be defined alternatively by looking at the downside deviation only. That is, instead of calculating the
standard deviation of
r
P
−
r
B
, we could calculate the standard deviation of min(
r
P
−
r
B
, 0). Would this alternative definition change the optimal portfolio?
9.13.
It is easy to combine the standard risk minimization with tracking-error minimization. Write down the minimization problem of the portfolio manager who wants to minimize the sum of the portfolio risk and the tracking error.
9.14.
Suppose that we constructed a portfolio through factor exposure targeting. Then the return of this portfolio can be expressed as follows:
where
β
B
is the factor exposure of the benchmark.
(a)    Express the tracking error of this portfolio in terms of
w
P
,
w
B
, and
Σ
ϵ
(the variance-covariance matrix of the stock-return errors).
(b)    Is the size of the tracking error bounded?
9.15.
Describe the situation in which the ghost benchmark tracking technique may be used.
9.16.
This question concerns phantom weights and binary weights.
(a)    What are phantom weights?
(b)    What are binary weights?
(c)    Why are these weights important in advanced portfolio optimizations? In particular, what problems can they help solve?
1
For example, IBM’s CPLEX optimization system has a function called CPLEXQCP for standard optimization with quadratic constraints and CPLEXMIQCP for mixed-integer quadratic optimizations with quadratic constraints.
2
See Chincarini (2017).
3
The
Q
matrix containing the variance–covariance matrix must also be expanded to account for the additional
x
variables by placing zeros throughout the larger matrix. That is, in this case with the
N
actual weights and
N
binary variables,
.
4
Using the CPLEX function CPLEXMIQP, available through the CPLEX library in MATLAB, this optimization took 0.0141 second to reach a solution. This technique is better than placing limits on the minimum and maximum value of stocks, which is an easier optimization to set up. The reason is that rather than eliminating small, unnecessary stocks (as in this case, stock 5), the optimizer will be forced to keep them at the minimum weight, which will lead to a higher risk for a given return. For the portfolio constructed here, the standard deviation was 13.51% per year, while the other type of optimization had a standard deviation of 14.77% with the following weights:
w
1
= 0.149,
w
2
= 0.058,
w
3
= 0.163,
w
4
= 0.3,
w
5
= 0.03, and
w
6
= 0.3.
5
The
Q
matrix containing the variance–covariance matrix must also be expanded to account for the additional
x
variables by placing zeros throughout the larger matrix. That is, in this case with the
N
actual weights and
N
binary variables,
.
6
Using MATLAB and CPLEX’s CPLEXMIQP function, this optimization took 0.0178 seconds to reach a solution. There are weights for only three stocks, as desired by the portfolio manager.
