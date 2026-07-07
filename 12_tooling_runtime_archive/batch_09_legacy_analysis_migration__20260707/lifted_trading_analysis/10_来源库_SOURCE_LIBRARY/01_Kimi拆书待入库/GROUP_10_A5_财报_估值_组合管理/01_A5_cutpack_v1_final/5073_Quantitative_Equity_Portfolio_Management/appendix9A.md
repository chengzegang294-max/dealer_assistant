# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = appendix9A

---

APPENDIX 9A
Quadratic Programming
For most of the portfolio optimization problems that a portfolio manager will encounter, a general quadratic optimization routine will enable him or her to construct the portfolio given his or her objectives.
1
Most commercial softwares packages employ some form of the concepts we will describe below. For portfolio managers who build their own risk models and optimizers, the standard packages have versions of the quadratic programming techniques we will discuss below.
2
The general quadratic programming problem can be expressed as
where
x
is the vector of unknowns in the problem,
Q
is a symmetric positive semidefinite matrix supplying the coefficients on the
quadratic terms of the optimization problem,
c
is a vector of coefficients related to the linear objective function,
A
is a matrix of coefficients for the equality and inequality constraints, and
b
is a vector of constraint values.
3
The general quadratic optimization problem works for both quadratic and linear optimization problems. For linear optimization problems, one can make
Q
=
0
, and then the problem becomes a linear programming problem. For quadratic optimizations, one uses the appropriate
Q
. In layperson’s terms, the preceding quadratic programming problem says the following: Minimize the function
by choosing the values of
x
that make it minimized. In addition, make sure that the chosen values of
x
satisfy some other
constraints
, some of which might be equality constraints and some of which might be inequality constraints (i.e.,
s.t
.
Ax
≤
b
, where
s.t
. stands for “subject to”). The objective function and the constraints can be almost anything. In the general optimization problem, these are just mathematical concepts. It is only when we apply these tools to actual real-world problems that they make more sense. We will do this in the next section of this appendix.
Let’s consider two special cases of the general quadratic optimization program. In one case, we specify only equality constraints. In the other case, we will allow for inequality as well as equality constraints. The reason we separate these into two categories is that with equality constraints, we actually can solve for the optimal weights with a
closed-form solution
.
4
9A.1 QUADRATIC PROGRAMMING WITH EQUALITY CONSTRAINTS
With only equality constraints, the quadratic optimization can be solved in closed form. The problem becomes
If matrix
A
is of full rank and matrix
Q
is positive definite, then a unique solution exists for
x
.
5
By a unique solution, we mean that there is one set of values for
x
that creates the minimum value of our objective function. Using the Lagrange method, we can find the first-order optimality conditions to solve the minimization problem.
6
The Lagrangian is
By taking the partial derivatives with respect to
x
and
λ
, we obtain the Lagrange necessary (or first-order) conditions for a solution:
The solution for the optimal
x
can be found by algebraically manipulating these equations. From the first equation, we have
Substitution of this into the second equation will give us
As a final step, we substitute this value of
λ
back into the original expression for
x
so that we have a closed-form solution for
x
. The value of
x
that minimizes the earlier general minimization problem with equality constraints is
where
I
is the identity matrix.
7
9A.1.1 A Numerical Example
Typically, in a portfolio risk-minimization problem, a portfolio manager would like to choose the weights of his or her stocks so as to minimize the variance of the portfolio for a given expected return level. The portfolio manager typically will have an equality constraint that the weights of the portfolio sum to 1. We can translate this easily into the quadratic optimization problem. The risk of a portfolio of stocks with weights
w
is given by
where
Σ
is the variance-covariance matrix of the stock returns, and
w
is the vector of stock weights. We also would like to express the mean return for any given selection of weights. The mean return of the portfolio will be
μ
P
=
w′
μ
, where
w
represents the stock weights and
μ
is a vector of mean returns for each of the stocks. We also would like to constrain the weights of the portfolio to sum to 1. This can be represented as
w
′
ι
= 1, where
ι
is just a vector of 1s.
We can see how easily this fits into our quadratic optimization framework. Simply replace
Q
with
Σ
, replace
x
with
w
, and let
c
=
0
. We must be careful how we modify the matrix
A
and the vector
b
. In particular, we want
Now we can substitute these values into our standard quadratic optimization problem with equality constraints, and the solution is readily available from
Eq. (9A.8)
. Since
c
=
0
, the solution will be
Let’s create a simple six stock portfolio to illustrate the application in more detail. Suppose we have six stocks with annualized mean returns of
μ
1
= 14.4,
μ
2
= 10.19,
μ
3
= 9.87,
μ
4
= 7.52,
μ
5
= 20.05, and
μ
6
= 2.66.
8
We also assume that we have an estimate of the annualized variance–covariance matrix of these stock returns. In our example, the matrix is:
where σ
ii
is the variance of stock
i
, and σ
ij
is the covariance of stock
i
with stock
j
. We can see that this matrix is symmetric. The variances and covariances are written in percentage terms. Thus, for stock 1, the annualized variance is 452.33, which is equivalent to a variance of 452% per year (or standard deviation of 21.26% per year). Finally, we must construct the matrix
A
and vector
b
; they are given by
where we have explicitly chosen the value of
μ
P
that we want to reflect an 8% annualized return. Thus, we can now use our formula to find the optimal weights of the six stocks that will achieve the lowest risk for obtaining an expected mean return of 8% per annum. The solution is
Thus, the optimal solution for a portfolio with capital of $1 is to buy $0.305 of stock 1, buy $0.057 of stock 2, buy $0.204 of stock 3, buy $0.274 of stock 4, short sell −$0.085 of stock 5, and buy $0.245 of stock 6.
9
The short position in stock 5 might not be feasible for many portfolio managers for a variety of reasons. Thus, the portfolio manager might like to add inequality constraints—for instance, that the weight of security 2 should be greater than 0.10, or 10%. In addition, the portfolio manager may wish to have the weights of all the securities be greater than 0. In our preceding optimization, we did not apply these restrictions. We will continue with our present example in the following application adding these restrictions.
9A.2 QUADRATIC PROGRAMMING WITH INEQUALITY CONSTRAINTS
The quadratic optimization problem with inequality constraints cannot be solved with a closed-form solution. The solution is
obtained through numerical solution methods. Numerical solutions have become much more reliable and feasible owing to the increased power of computers and some advances in linear and quadratic programming. The most typical method that is used is the
active-set method
or
projection method
. Other methods are used as well, including the
interior-point method
.
10
Since most portfolio managers and quantitative researchers will have access to robust optimizers, we will not go into detail on the mathematics of each numerical method.
11
9A.2.1 A Numerical Example
We will continue the previous numerical example, adding some inequality constraints. We will use the active-set method to solve the problem. The three inequality constraints that we will add are that the weights of each individual stock cannot be less than 0, except for stock 2, which will not be allowed to have a weight of less than 0.10. Thus
w
≥ 0 and
w
2
≥ 0.10. These inequality constraints can be added easily to our matrix
A
.
12
In fact, the new optimization problem with the first two rows of
A
representing equality constraints and the last seven rows representing inequality constraints is
13
where
Notice that to express the constraint that
w
2
≥ 0.10, we stated that
w
1
+
w
3
+
w
4
+
w
5
+
w
6
≤ 0.90. Sometimes, depending on the types of programs we use, the most obvious constraints need a bit of reengineering. The solution using a standard optimization routine is
14
1
For those who wish to have more insight into the mathematics of optimization, we recommend two books, Luenberger (1989) and Gill et al. (1981).
2
For instance, RATS (Regression Analysis of Time Series), produced by Estima Corporation, has a procedure known as LQPROG that performs both linear and quadratic optimizations quite easily. MATLAB, produced by MathWorks Inc., has an optimization toolbox that includes the function QUADPROG, which can handle standard quadratic optimization problems. For a more complete suite of optimization tools that can also be used with other software programs, we recommend IBM’s CPLEX software. For quadratic optimizations, this software has functions CPLEXQP, CPLEXMIQP, CPLEXQCP, and CPLEXMIQCP that are useful for advanced optimizations. The open-source programming language R has a function SOLVE.QP that can handle standard quadratic optimizations.
3
The matrix
Q
in most portfolio problems actually will be positive definite. The symmetry of the matrix is very important. This refers to a matrix for which entry
a
i,k
=
a
k,i
for all
i
and
k
. In layperson’s terms, the matrix on either side of the diagonal terms looks like a mirror reflection of the other side.
4
In mathematics, the term
closed-form solution
refers to an expression for a given function or quantity that can be expressed in terms of known and well-understood quantities. These solutions are preferable because, given a set of variables, you can plug them into an equation and know the optimal solution immediately.
5
A symmetric matrix is called
positive definite
if
x′Qx
> 0 for all
x
≠ 0. A matrix has
full rank
if it has rank equal to the number of rows or columns, whichever is less. If a nonzero
x
for which
Ax
=
0
exists, then
A
is not of full rank. It also means that the columns of
A
are linearly dependent. That is, at least one row of
A
can be expressed as a simple linear transformation of another. This will lead to nonunique solutions. The reader should consult a book on linear algebra for more details, for example, Anton (1991) or Greene (2002).
6
The Lagrange method is a method of solving these types of constrained optimization problems. It is a clever method of reducing a constrained optimization problem to an unconstrained optimization problem by introducing
Lagrange multipliers
. It is named after Joseph Louis Lagrange, an Italian-born French mathematician and physicist who was a professor at the University of Turin in 1755. He later succeeded Euler as director of mathematics at the Berlin Academy of Science. He made many contributions to mathematics, including probability theory, number theory, the theory of equations, and the foundations of group theory.
7
The identity matrix is a diagonal matrix in which every diagonal term is equal to 1, and all other elements in the matrix are equal to 0.
8
In practice, these can be expected future returns, historical mean returns, or returns from one’s factor models. The mean returns are expressed in percentage terms; thus, 14.4 represents an annual return of 14.4%.
9
One can compute the transpose of the matrices (i.e.,
A
′) and the inverse of the matrices (i.e.,
Σ
−1
) using a software program or manually.
10
The state-of-the-art quadratic programming algorithms with inequality constraints are two kinds of approaches called the
active-set method
and the
interior-point method
. Both kinds of approaches solve a series of subproblems where there are only equality constraints. The two approaches differ only in how they arrange the order of the subproblems to be solved. In the active-set method, we proceed along the boundary of the feasible set defined by the constraints. In the interior-point method, we proceed within the feasible set.
11
For a book on the details of the different types of numerical optimization procedures, see Nocedal and Wright (1999). Some software optimizers use a combination of techniques, such as RATS’ LQPROG, which uses the active-set method with the conjugate gradient method. MATLAB’s QUADPROG uses the interior-point algorithm. IBM’s CPLEX suite uses a variety of techniques. See also Sharpe (1987) for an interesting algorithm for portfolio optimization improvement.
12
Many software applications that have optimizers allow the user to specify upper- and lower-bound weights rather than having to include them in a constraint matrix.
13
Many quadratic programming optimizers allow the user to specify the equality
A
eq
and inequality matrices
A
ineq
as two different matrices rather than one (
A
).
14
Using MATLAB, this optimization took 0.0068 second to reach a solution.
