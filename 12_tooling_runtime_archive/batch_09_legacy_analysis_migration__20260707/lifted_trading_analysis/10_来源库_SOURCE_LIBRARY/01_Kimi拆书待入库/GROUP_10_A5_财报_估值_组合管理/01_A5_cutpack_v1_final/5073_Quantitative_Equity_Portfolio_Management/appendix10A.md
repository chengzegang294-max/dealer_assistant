# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = appendix10A

---

APPENDIX 10A
Approximate Solution to the Optimal Portfolio Problem
Problems specified by
Eqs. (10.9)
and
(10.14)
are not quadratic in
w
a
and are difficult to solve with conventional quadratic optimizers. The mathematics to solve this more complicated problem are described in
Appendix 10B
. The current appendix presents a simple approximate solution that works very well for most situations.
Nonlinearity in
Eqs. (10.9)
and
(10.14)
arises because we do not know, before solving the problem, which stock to sell and which stock to buy. If we knew, the problem would be quadratic as usual. Thus, to avoid nonlinearity, we need to determine which stocks to buy and which stocks to sell before solving the problems in
Eqs. (10.9)
and
(10.14)
.
We suggest the following shortcut. First, we can solve the problem ignoring the transactions costs. That is, solve
subject to
and any other relevant constraints. Call the solution to this problem
. Then define the transactions cost vector
c
= {
c
1
, …,
c
N
} using these weights:
That is, we determine which stocks to buy and which stocks to sell based on the optimization without considering transactions costs. Once we have determined which stocks to buy and which stocks to sell, we can impose this as a constraint to the optimization problem in
Eqs. (10.9)
and
(10.14)
. In the case of
Eq. (10.9)
, the problem to be solved becomes
subject to
and any other relevant constraints. Now
c
is a fixed constraint and does not depend on the value of
w
a
(as long as the additional constraints we imposed are satisfied), and we can solve this problem using a conventional quadratic optimizer.
