# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = appendix10B

---

APPENDIX 10B
An Exact Solution to the Optimal Portfolio Problem
Although more complicated, there is a way to construct the portfolio optimization problem so as to consider transactions costs without having to use an approximate method. The minimization problem is similar to our standard one, such that,
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
1
As explained in
Chapter 9
, in the traditional mean-variance optimization problem, we substitute the following variables:
x
=
w
, the stock weights;
Q
= 2
Σ
, the variance-covariance matrix of stock returns;
c
=
0
;
A
is chosen typically to have a row of ones and a row of expected returns, and the other constraints. In many software packages, the
A
matrix is split into two matrices, one for equality constraints and one for inequality constraints.
In order to solve for the optimal weights of the portfolio given a current portfolio and transactions costs, we start by expanding
the
x
vector to include six types of variables. In addition to the prospective weights of the portfolio (
), we create phantom positive weights,
, which represent the (
N
× 1) “long” positions of the portfolio; then we create the phantom negative weights,
w
−
i
, which represent the “short” positions of the portfolio;
, which represent the current weights of the portfolio, and the binary weights
and
. That is, the
x
variable will consist of six types of variables in the following way:
That is, rather than just
N
weights for
N
stocks, we have 6
N
weights that have specific importance in the optimization. Of course, in the end, the variables of the ultimate importance are the first
N
weights: the optimal stock weights.
Since we now have 6
N
weights, the
Q
matrix must also be modified to be (6
N
× 6
N
) by adding zeros all around the variance-covariance matrix so that,
We constrain the prospective weights of the optimized portfolio,
, to be related to these phantom weights and the prior portfolio weights as follows:
This essentially makes the phantom weights equal to the incremental buy or sell for each stock in the portfolio from the prior portfolio weights. We also need to constrain the phantom weights,
and
, to be positive and orthogonal to each other (i.e., only one of them is positive for any given security in the portfolio). This is needed so that we do not unnecessarily buy and sell the same stock. Thus, we introduce the binary variables
and
for each stock in the portfolio. We introduce the following constraints in order to ensure that the phantom weights are orthogonal:
Since
and
are binary variables, the inequality constraint in
Eq. (10B.8)
forces only one of them to be 1 and the other 0. This combined with the constraints in
Eqs. (10B.6)
and
(10B.7)
force the phantom weights to also be orthogonal to each other. For generality, we used the parameters
κ
l
, γ
l
, κ
h
, and
γ
h
, but later in this
section we will assign them values of 0 and 1 to simplify this particular optimization.
2
We then create a vector of transactions costs,
c
, as before. Now that the general setup is in place, we show how to arrange the matrices (equality and inequality constraints) to complete the optimization. We will show the equality matrix constraints and inequality matrix constraints separately, but you can also combine them into one
A
matrix if desired. The equality matrix,
A
eq
, should be a (2
N
+ 2) by (6
N
) matrix, and the corresponding
b
eq
vector will be (2
N
+ 2) by (1).
The inequality matrix,
A
ineq
, should be a (5
N
) by (6
N
) matrix and the corresponding
b
ineq
vector will be (5
N
) by (1).
where
μ
1×
N
is the row vector of the mean returns for each of the
N
stocks;
µ
P
is the desired after-tax portfolio return;
ι
1×
N
is a row of six 1s (that is, the first six entries of matrix
A
’s row 1 are 1s);
0
1×
N
is a row of
N
entries of 0;
I
N
×
N
is the identity matrix (that is, an
N
by
N
matrix with 1s on the diagonal and 0s everywhere else); and so on and so forth. In order to aid the reader, we indicate the dimension of every matrix as a subscript.
The transactions costs are incorporated into the optimization via the second row of the equality matrix, which constrains the optimization so that
μ
′w
−
c′w
+
−
c′w
−
=
µ
P
. Since the phantom weights must be positive and orthogonal, this creates the appropriate after-tax average return.
As stated earlier, you can either put upper- and lower-bound constraints in the inequality, or
A
ineq
, matrix or specify them directly as upper- and lower-bound vectors in many optimization packages. In this example, we chose to specify them directly; thus we constrain weights and phantom weights to be between 0 and 1, as well as the prior portfolio and the binary weights.
3
Thus
We can solve this problem with a mixed integer quadratic optimization (MIQO).
4
If you do not have access to a MIQO optimizer, but have access to a mixed integer linear programming optimizer, then you can use an algorithm to find the solution.
5
10B.1 A NUMERICAL EXAMPLE
We will continue the numerical example in
Appendix 9A
. Thus we will seek to construct a portfolio with an after-tax average return of 8%, with no short sales allowed, and the weights of the portfolio must sum to 1. To make things simple, we will assume all stocks cost 1% to trade, except stock 1, which costs 20% to trade. That is, if one trades $100 of stock 1, one will incur a cost of $20, while a $100 trade of any other stock will result in a cost of $1. This will be represented by a
c
vector. Of course, this solution would work with any cost vector. We also use the following prior weights of the portfolio:
w
b
= [0.23 0.1 0.12 0.14 0.13 0.28]. We will construct an optimization that minimizes variance subject to a target after-tax return of 8% while considering the prior portfolio weights,
.
Since our focus is on transactions costs and not particular upper and lower limits to the phantom weights, we can set the parameters
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
= 1 so that we allow the weights to fluctuate between 0 and 1, but force them to be orthogonal to each other. The constraint matrices will be
6
where
μ
1×6
= [14.40 10.19 9.87 7.52 20.05 2.66];
c
1×6
= [20 1 1 1 1 1];
ι
1×6
is a row of six 1s (that is, the first six entries of matrix
A
’s row 1 are 1s);
0
1×6
is a row of six entries of 0;
I
6×6
is the identity matrix (that is, a 6-by-6 matrix with 1s on the diagonal and 0s everywhere else); and so on and so forth. In order to aid the reader, we indicate the dimension of every matrix as a subscript, including for the large
A
and
b
matrices.
The economic meaning of these constraints is the following: the first two rows of this
A
matrix are the equality constraints that the sum of weights equals 1 and that the target after-tax average return is 8%.
The third row through the eighth row of the equality matrix establishes the links between the actual portfolio weights that are chosen, the phantom weights, and the prior portfolio weights. Rows 9 through 14 constrain the prior portfolio weights to equal
w
b
. Rows 15 through 20 constrain the binary variables to be orthogonal; that is, only one of them can be positive, which consequently constrains the phantom weights to be orthogonal (i.e., we don’t buy
and sell the same security). In order to do this, we employ the constraints from rows 21 to 44. As discussed earlier, we accomplish this by setting
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
= 1.
The solution using an optimization routine with continuous and binary variables is:
7
Notice that the solution does not adjust the weight of stock 1 at all. This is quite understandable given the high transactions cost that we imposed on stock 1. In the absence of transactions costs, the optimal portfolio weights would have been [0.287 0.016 0.065 0.283 0 0.348].
1
As we discussed in
Appendix 9A
, you can also place these upper- and lower-bound constraints directly in the
A
matrix.
2
It is essential that the software package allows for quadratic optimization with binary variables and continuous variables and that the user specifies which variables are binary variables. If the software only allows for integers, then upper and lower bounds of 0 and 1 on the integers will achieve similar results. The CPLEX suite has these and can be used as a library with MATLAB. For users who do not have the option to specify binary variables in a quadratic optimization, we provide an algorithm later in this appendix to solve for this problem with a linear programming integer optimizer.
3
Some of these weight boundaries were implicitly already constrained by prior constraints.
4
For example, IBM’s CPLEX optimization system has a MIQO function called CPLEXMIQP. These are also referred to as mixed integer quadratic programs (MIQPs).
5
For example, MATLAB does not have an MIQP but does have an MILP called INTLINPROG. In order to use an MILP in place of an MIQP, certain adjustments to the matrices must be made and an iterative procedure followed, which converges to the MIQP solution [Kelley (1960)]. Rather than describe all the details for this particular optimization, we will discuss the general concepts and the principal changes required to do a similar transactions cost optimization using the iterative MILP to replicate an MIQP. The steps are as follows. Step 1: Introduce a slack variable called
z
to represent the quadratic term. The idea is that instead of minimizing
λ
x′Qx
, you minimize
λz s.t
.
x′Qx
−
z ≤
0 and
z ≥
0. Then as you iteratively solve the MILP approximations, include new linear constraints, each of which approximates the nonlinear constraint locally near the current point. This is repeated until a satisfactory solution emerges. Practically, the inequality matrix
A
ineq
is altered to include a second column representing
z
(which can be thought of an extra choice parameter, like the
N
+ 1 weight in a standard
N
-asset problem), with a lower bound of 0 and an upper bound of infinity. Also, you should specify that the
v
i
are integers and place upper and lower bounds on them of 0 and 1. Step 2: Transform the nonlinear quadratic objective function, which minimizes risk and maximizes return with a tradeoff of
λ
, into a linear optimization problem with non-linear (e.g., quadratic) constraints. That is, convert the optimization problem
into this one:
where
r
is a vector of variables to maximize. For example, in the case of transactions costs, it would represent the mean returns of the stocks as well as the negative of the transactions costs for the phantom weights (i.e., it would consist of the second row of
A
eq
and that row would be removed from
A
eq
). Since many linear programming softwares are set to minimize
f′x
, the
f
for this particular optimization would look something like
Use a Taylor series expansion of the constraint around
x
0
, ignoring squared terms and higher, such that
Then add the following constraint to the constraint matrix for the next iteration:
Using this approximation, in every iteration of the MILP problem you add a new constraint to the inequality constraint matrix of the form above. In particular, add a row to
A
ineq
with the values of 2
x
′
k
Q
based on the prior optimized value of asset weights
x
k
,
a
−1 for the
z
term, and then 0s for the other decision variables in the optimization problem (e.g., phantom weights, binary variables, etc). You would also add a value to the
b
vector equal to
x
′
k
Qx
k
.
On every iteration, instead of using the actual value of
x
k
from the most recent optimization, one could also use a linear combination of the previous solution and the new solution. That is, use
instead of
x
k
when adding the constraint. Continue the process with the new constraints and using the MILP. On every iteration, compare the value of
z
to the value of the quadratic at the solution point (i.e.,
z
−
x
′
k
Qx
k
). If that is within the tolerance level, stop the process and you have the optimal value of your stock weights. For example, you could choose to stop when
z
<
x
′
k
Qx
k
(1 −
ϵ
), where
ϵ
= 0.0005.
6
The
Q
matrix containing the variance-covariance matrix must also be expanded to account for the additional five variables with 0s on the diagonals. See
Eq. (10B.4)
.
7
Using the CPLEX function CPLEXMIQP, available through the CPLEX library in MATLAB, this optimization took 0.0170 seconds to reach a solution.
